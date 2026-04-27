"""Phase 6 Part 03 ILT-style contour and gradient helpers.

This module keeps the inverse-lithography step study-grade: it uses
deterministic finite differences over an OPC mask-bias parameter instead of a
full differentiable mask engine. The result is still useful for closing the
Phase 6 loop because it exposes a numeric-gradient refinement path and a
full-layout contour EPE metric that looks along both image axes.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .illuminator import SourceShape
from .mask import MaskGrid, line_space_pattern
from .metrics import edge_positions
from .pupil import PupilSpec
from .smo import (
    MaskCandidate,
    SMOCandidateMetrics,
    SMOObjectiveWeights,
    evaluate_smo_candidate,
    weighted_smo_loss,
)


@dataclass(frozen=True)
class ContourEPEMap:
    """Full-layout contour EPE summary in meters."""

    x_edge_error_m: np.ndarray
    y_edge_error_m: np.ndarray
    mean_abs_epe_m: float
    max_abs_epe_m: float
    edge_count_mismatch_fraction: float
    rows_evaluated: int
    columns_evaluated: int
    x_edges_per_row: int
    y_edges_per_column: int


@dataclass(frozen=True)
class ILTBiasEvaluation:
    """Evaluation for one ILT/OPC mask-bias point."""

    bias_m: float
    mask_candidate: MaskCandidate
    source_shape: SourceShape
    dose: float
    metrics: SMOCandidateMetrics
    contour_epe: ContourEPEMap
    aerial: np.ndarray
    printed: np.ndarray


@dataclass(frozen=True)
class ILTRefinementStep:
    """One accepted finite-difference refinement step."""

    step_index: int
    evaluation: ILTBiasEvaluation
    gradient_loss_per_m: float
    update_step_m: float
    next_bias_m: float


@dataclass(frozen=True)
class ILTRefinementResult:
    """Finite-difference ILT refinement result bundle."""

    initial: ILTBiasEvaluation
    best: ILTBiasEvaluation
    history: tuple[ILTRefinementStep, ...]
    weights: SMOObjectiveWeights
    improvement_fraction: float

    @property
    def converged(self) -> bool:
        """Return True when the best point improves or matches the initial loss."""
        return self.best.metrics.loss <= self.initial.metrics.loss


@dataclass(frozen=True)
class _AxisEPEStats:
    edge_error_m: np.ndarray
    mean_abs_epe_m: float
    max_abs_epe_m: float
    mismatch_count: int
    counted_edges: int
    max_target_edges: int


def full_layout_contour_epe(
    target_printed: np.ndarray,
    printed: np.ndarray,
    pixel_size_m: float,
    *,
    penalty_m: float | None = None,
) -> ContourEPEMap:
    """Return contour EPE by comparing row and column transition edges."""
    target = _as_bool_image(target_printed, "target_printed")
    candidate = _as_bool_image(printed, "printed")
    if target.shape != candidate.shape:
        raise ValueError("target_printed and printed must have the same shape")
    _validate_positive_finite(pixel_size_m, "pixel_size_m")
    if penalty_m is not None:
        _validate_positive_finite(penalty_m, "penalty_m")
    fallback_penalty = (
        float(penalty_m)
        if penalty_m is not None
        else float(max(pixel_size_m, max(target.shape) * pixel_size_m / 4.0))
    )

    x_stats = _axis_contour_epe(target, candidate, pixel_size_m, fallback_penalty)
    y_stats = _axis_contour_epe(
        target.T,
        candidate.T,
        pixel_size_m,
        fallback_penalty,
    )
    target_edge_count = np.count_nonzero(~np.isnan(x_stats.edge_error_m))
    target_edge_count += np.count_nonzero(~np.isnan(y_stats.edge_error_m))
    if target_edge_count == 0:
        raise ValueError("target_printed must contain at least one target contour edge")

    total_abs_error = (
        x_stats.mean_abs_epe_m * x_stats.counted_edges
        + y_stats.mean_abs_epe_m * y_stats.counted_edges
    )
    counted_edges = x_stats.counted_edges + y_stats.counted_edges
    mismatch_count = x_stats.mismatch_count + y_stats.mismatch_count

    return ContourEPEMap(
        x_edge_error_m=x_stats.edge_error_m,
        y_edge_error_m=y_stats.edge_error_m,
        mean_abs_epe_m=float(total_abs_error / max(counted_edges, 1)),
        max_abs_epe_m=float(max(x_stats.max_abs_epe_m, y_stats.max_abs_epe_m)),
        edge_count_mismatch_fraction=float(mismatch_count / max(counted_edges, 1)),
        rows_evaluated=int(target.shape[0]),
        columns_evaluated=int(target.shape[1]),
        x_edges_per_row=int(x_stats.max_target_edges),
        y_edges_per_column=int(y_stats.max_target_edges),
    )


def evaluate_ilt_bias_candidate(
    target_printed: np.ndarray,
    mask_grid: MaskGrid,
    pitch_m: float,
    bias_m: float,
    source_shape: SourceShape,
    *,
    pupil_spec: PupilSpec | None = None,
    dose: float = 1.0,
    weights: SMOObjectiveWeights | None = None,
    threshold: float = 0.3,
    target_duty_cycle: float = 0.5,
    orientation: str = "vertical",
    anamorphic: bool = False,
) -> ILTBiasEvaluation:
    """Evaluate one scalar ILT/OPC bias using full-layout contour EPE."""
    if weights is None:
        weights = SMOObjectiveWeights()
    mask_candidate = _bias_mask_candidate(
        mask_grid,
        pitch_m,
        bias_m,
        target_duty_cycle=target_duty_cycle,
        orientation=orientation,
    )
    base = evaluate_smo_candidate(
        target_printed,
        mask_grid,
        mask_candidate,
        source_shape,
        dose=dose,
        pupil_spec=pupil_spec,
        weights=weights,
        threshold=threshold,
        anamorphic=anamorphic,
    )
    contour_epe = full_layout_contour_epe(
        target_printed,
        base.printed,
        base.wafer_grid.pixel_x_m,
        penalty_m=base.metrics.target_cd_m,
    )
    epe_error_fraction = contour_epe.mean_abs_epe_m / base.metrics.target_cd_m
    loss = weighted_smo_loss(
        cd_error_fraction=base.metrics.cd_error_fraction,
        epe_error_fraction=epe_error_fraction,
        lwr_fraction=base.metrics.lwr_fraction,
        dose_error_fraction=base.metrics.dose_error_fraction,
        weights=weights,
    )
    metrics = SMOCandidateMetrics(
        target_cd_m=base.metrics.target_cd_m,
        printed_cd_m=base.metrics.printed_cd_m,
        mean_epe_m=contour_epe.mean_abs_epe_m,
        lwr_m=base.metrics.lwr_m,
        cd_error_fraction=base.metrics.cd_error_fraction,
        epe_error_fraction=float(epe_error_fraction),
        lwr_fraction=base.metrics.lwr_fraction,
        dose_error_fraction=base.metrics.dose_error_fraction,
        loss=loss,
    )
    return ILTBiasEvaluation(
        bias_m=float(bias_m),
        mask_candidate=mask_candidate,
        source_shape=source_shape,
        dose=base.dose,
        metrics=metrics,
        contour_epe=contour_epe,
        aerial=base.aerial,
        printed=base.printed,
    )


def finite_difference_bias_gradient(
    target_printed: np.ndarray,
    mask_grid: MaskGrid,
    pitch_m: float,
    bias_m: float,
    source_shape: SourceShape,
    *,
    delta_m: float,
    pupil_spec: PupilSpec | None = None,
    dose: float = 1.0,
    weights: SMOObjectiveWeights | None = None,
    threshold: float = 0.3,
    target_duty_cycle: float = 0.5,
    orientation: str = "vertical",
    anamorphic: bool = False,
    lower_bias_m: float | None = None,
    upper_bias_m: float | None = None,
) -> float:
    """Estimate d(loss)/d(mask_bias) with a bounded finite difference."""
    _validate_positive_finite(delta_m, "delta_m")
    lower, upper = _resolve_bias_bounds(
        pitch_m,
        target_duty_cycle,
        lower_bias_m=lower_bias_m,
        upper_bias_m=upper_bias_m,
    )
    bias = _clip_bias(bias_m, lower, upper)
    minus_bias = _clip_bias(bias - delta_m, lower, upper)
    plus_bias = _clip_bias(bias + delta_m, lower, upper)
    if plus_bias <= minus_bias:
        raise ValueError("delta_m is too small for the configured bias bounds")

    minus = evaluate_ilt_bias_candidate(
        target_printed,
        mask_grid,
        pitch_m,
        minus_bias,
        source_shape,
        pupil_spec=pupil_spec,
        dose=dose,
        weights=weights,
        threshold=threshold,
        target_duty_cycle=target_duty_cycle,
        orientation=orientation,
        anamorphic=anamorphic,
    )
    plus = evaluate_ilt_bias_candidate(
        target_printed,
        mask_grid,
        pitch_m,
        plus_bias,
        source_shape,
        pupil_spec=pupil_spec,
        dose=dose,
        weights=weights,
        threshold=threshold,
        target_duty_cycle=target_duty_cycle,
        orientation=orientation,
        anamorphic=anamorphic,
    )
    return float((plus.metrics.loss - minus.metrics.loss) / (plus_bias - minus_bias))


def ilt_bias_gradient_refinement(
    target_printed: np.ndarray,
    mask_grid: MaskGrid,
    pitch_m: float,
    source_shape: SourceShape,
    *,
    initial_bias_m: float,
    gradient_delta_m: float,
    update_step_m: float,
    max_steps: int,
    pupil_spec: PupilSpec | None = None,
    dose: float = 1.0,
    weights: SMOObjectiveWeights | None = None,
    threshold: float = 0.3,
    target_duty_cycle: float = 0.5,
    orientation: str = "vertical",
    anamorphic: bool = False,
    lower_bias_m: float | None = None,
    upper_bias_m: float | None = None,
    gradient_tolerance_loss_per_m: float = 0.0,
) -> ILTRefinementResult:
    """Refine a scalar OPC/ILT bias with finite-difference descent."""
    _validate_positive_finite(gradient_delta_m, "gradient_delta_m")
    _validate_positive_finite(update_step_m, "update_step_m")
    if int(max_steps) < 0:
        raise ValueError("max_steps must be non-negative")
    if not np.isfinite(gradient_tolerance_loss_per_m) or gradient_tolerance_loss_per_m < 0.0:
        raise ValueError("gradient_tolerance_loss_per_m must be non-negative")
    if weights is None:
        weights = SMOObjectiveWeights()
    lower, upper = _resolve_bias_bounds(
        pitch_m,
        target_duty_cycle,
        lower_bias_m=lower_bias_m,
        upper_bias_m=upper_bias_m,
    )
    current_bias = _clip_bias(initial_bias_m, lower, upper)
    best: ILTBiasEvaluation | None = None
    steps: list[ILTRefinementStep] = []

    for step_index in range(int(max_steps) + 1):
        evaluation = evaluate_ilt_bias_candidate(
            target_printed,
            mask_grid,
            pitch_m,
            current_bias,
            source_shape,
            pupil_spec=pupil_spec,
            dose=dose,
            weights=weights,
            threshold=threshold,
            target_duty_cycle=target_duty_cycle,
            orientation=orientation,
            anamorphic=anamorphic,
        )
        if best is None or evaluation.metrics.loss < best.metrics.loss:
            best = evaluation
        gradient = finite_difference_bias_gradient(
            target_printed,
            mask_grid,
            pitch_m,
            current_bias,
            source_shape,
            delta_m=gradient_delta_m,
            pupil_spec=pupil_spec,
            dose=dose,
            weights=weights,
            threshold=threshold,
            target_duty_cycle=target_duty_cycle,
            orientation=orientation,
            anamorphic=anamorphic,
            lower_bias_m=lower,
            upper_bias_m=upper,
        )
        if (
            step_index == int(max_steps)
            or abs(gradient) <= gradient_tolerance_loss_per_m
        ):
            steps.append(
                ILTRefinementStep(
                    step_index=step_index,
                    evaluation=evaluation,
                    gradient_loss_per_m=gradient,
                    update_step_m=0.0,
                    next_bias_m=evaluation.bias_m,
                )
            )
            break

        direction = -float(np.sign(gradient))
        accepted_bias = evaluation.bias_m
        accepted_step = 0.0
        trial_step = float(update_step_m)
        for _ in range(12):
            proposed_bias = _clip_bias(evaluation.bias_m + direction * trial_step, lower, upper)
            if abs(proposed_bias - evaluation.bias_m) < np.finfo(np.float64).eps:
                break
            proposed = evaluate_ilt_bias_candidate(
                target_printed,
                mask_grid,
                pitch_m,
                proposed_bias,
                source_shape,
                pupil_spec=pupil_spec,
                dose=dose,
                weights=weights,
                threshold=threshold,
                target_duty_cycle=target_duty_cycle,
                orientation=orientation,
                anamorphic=anamorphic,
            )
            if proposed.metrics.loss <= evaluation.metrics.loss:
                accepted_bias = proposed_bias
                accepted_step = proposed_bias - evaluation.bias_m
                if best is None or proposed.metrics.loss < best.metrics.loss:
                    best = proposed
                break
            trial_step *= 0.5

        steps.append(
            ILTRefinementStep(
                step_index=step_index,
                evaluation=evaluation,
                gradient_loss_per_m=gradient,
                update_step_m=float(accepted_step),
                next_bias_m=float(accepted_bias),
            )
        )
        if accepted_step == 0.0:
            break
        current_bias = accepted_bias

    if best is None or not steps:
        raise RuntimeError("ILT refinement did not evaluate any candidate")
    initial = steps[0].evaluation
    denominator = max(abs(initial.metrics.loss), float(np.finfo(np.float64).eps))
    improvement = (initial.metrics.loss - best.metrics.loss) / denominator
    return ILTRefinementResult(
        initial=initial,
        best=best,
        history=tuple(steps),
        weights=weights,
        improvement_fraction=float(improvement),
    )


def _axis_contour_epe(
    target: np.ndarray,
    candidate: np.ndarray,
    pixel_size_m: float,
    penalty_m: float,
) -> _AxisEPEStats:
    target_edges_by_line = tuple(
        edge_positions(target[line, :], pixel_size_m) for line in range(target.shape[0])
    )
    printed_edges_by_line = tuple(
        edge_positions(candidate[line, :], pixel_size_m)
        for line in range(candidate.shape[0])
    )
    max_edges = max((edges.size for edges in target_edges_by_line), default=0)
    edge_error = np.full((target.shape[0], max_edges), np.nan, dtype=np.float64)
    total_abs_error = 0.0
    counted_edges = 0
    mismatch_count = 0
    max_abs_error = 0.0

    for line_index, (target_edges, printed_edges) in enumerate(
        zip(target_edges_by_line, printed_edges_by_line, strict=True)
    ):
        for edge_index, target_edge in enumerate(target_edges):
            if edge_index < printed_edges.size:
                signed_error = float(printed_edges[edge_index] - target_edge)
            else:
                signed_error = penalty_m
                mismatch_count += 1
            edge_error[line_index, edge_index] = signed_error
            abs_error = abs(signed_error)
            total_abs_error += abs_error
            max_abs_error = max(max_abs_error, abs_error)
            counted_edges += 1
        if printed_edges.size > target_edges.size:
            extra_edges = int(printed_edges.size - target_edges.size)
            mismatch_count += extra_edges
            total_abs_error += extra_edges * penalty_m
            max_abs_error = max(max_abs_error, penalty_m)
            counted_edges += extra_edges

    return _AxisEPEStats(
        edge_error_m=edge_error,
        mean_abs_epe_m=float(total_abs_error / max(counted_edges, 1)),
        max_abs_epe_m=float(max_abs_error),
        mismatch_count=int(mismatch_count),
        counted_edges=int(counted_edges),
        max_target_edges=int(max_edges),
    )


def _bias_mask_candidate(
    mask_grid: MaskGrid,
    pitch_m: float,
    bias_m: float,
    *,
    target_duty_cycle: float,
    orientation: str,
) -> MaskCandidate:
    _validate_positive_finite(pitch_m, "pitch_m")
    if not np.isfinite(bias_m):
        raise ValueError("bias_m must be finite")
    if not 0.0 < target_duty_cycle < 1.0:
        raise ValueError("target_duty_cycle must be in (0, 1)")
    duty_cycle = target_duty_cycle + 2.0 * float(bias_m) / pitch_m
    if not 0.0 < duty_cycle < 1.0:
        raise ValueError("bias_m produces duty cycle outside (0, 1)")
    return MaskCandidate(
        name=f"ilt_bias_{bias_m * 1e9:+.2f}nm",
        pattern=line_space_pattern(
            mask_grid,
            pitch_m=pitch_m,
            duty_cycle=duty_cycle,
            orientation=orientation,
        ),
    )


def _resolve_bias_bounds(
    pitch_m: float,
    target_duty_cycle: float,
    *,
    lower_bias_m: float | None,
    upper_bias_m: float | None,
) -> tuple[float, float]:
    _validate_positive_finite(pitch_m, "pitch_m")
    if not 0.0 < target_duty_cycle < 1.0:
        raise ValueError("target_duty_cycle must be in (0, 1)")
    margin_m = max(pitch_m * 1e-9, float(np.finfo(np.float64).eps))
    lower_default = -0.5 * pitch_m * target_duty_cycle + margin_m
    upper_default = 0.5 * pitch_m * (1.0 - target_duty_cycle) - margin_m
    lower = lower_default if lower_bias_m is None else float(lower_bias_m)
    upper = upper_default if upper_bias_m is None else float(upper_bias_m)
    if not np.isfinite(lower) or not np.isfinite(upper) or lower >= upper:
        raise ValueError("bias bounds must be finite and increasing")
    lower = max(lower, lower_default)
    upper = min(upper, upper_default)
    if lower >= upper:
        raise ValueError("configured bias bounds leave no feasible duty-cycle range")
    return lower, upper


def _clip_bias(bias_m: float, lower_bias_m: float, upper_bias_m: float) -> float:
    if not np.isfinite(bias_m):
        raise ValueError("bias_m must be finite")
    return float(np.clip(float(bias_m), lower_bias_m, upper_bias_m))


def _as_bool_image(image: np.ndarray, name: str) -> np.ndarray:
    arr = np.asarray(image)
    if arr.ndim != 2:
        raise ValueError(f"{name} must be 2-D")
    if arr.size == 0:
        raise ValueError(f"{name} must contain at least one pixel")
    return arr.astype(bool)


def _validate_positive_finite(value: float, name: str) -> None:
    if not np.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be a positive finite value")
