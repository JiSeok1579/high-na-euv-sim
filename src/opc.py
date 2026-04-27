"""Phase 6 Part 04 OPC assist-feature and pixel-level ILT helpers.

The helpers in this module extend the scalar ILT bias refinement from
``src.ilt`` with two study-grade controls:

- deterministic sub-resolution assist-feature candidates for line-space masks,
- a pixel-level binary mask refinement loop driven by target-vs-print mismatch.

This is still not production OPC/ILT. It is a compact, deterministic bridge from
global mask-bias refinement toward local mask-shape updates.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

import numpy as np

from .illuminator import SourceShape
from .ilt import ContourEPEMap, full_layout_contour_epe
from .mask import MaskGrid, line_space_pattern
from .pupil import PupilSpec
from .smo import (
    MaskCandidate,
    SMOCandidateMetrics,
    SMOObjectiveWeights,
    evaluate_smo_candidate,
    weighted_smo_loss,
)


@dataclass(frozen=True)
class OPCLayoutEvaluation:
    """Evaluation for one OPC/ILT mask layout candidate."""

    mask_candidate: MaskCandidate
    source_shape: SourceShape
    dose: float
    metrics: SMOCandidateMetrics
    contour_epe: ContourEPEMap
    aerial: np.ndarray
    printed: np.ndarray


@dataclass(frozen=True)
class PixelILTRefinementStep:
    """One accepted pixel-level refinement step."""

    step_index: int
    evaluation: OPCLayoutEvaluation
    changed_pixels: int
    next_loss: float


@dataclass(frozen=True)
class PixelILTResult:
    """Pixel-level ILT refinement result bundle."""

    initial: OPCLayoutEvaluation
    best: OPCLayoutEvaluation
    history: tuple[PixelILTRefinementStep, ...]
    weights: SMOObjectiveWeights
    improvement_fraction: float

    @property
    def converged(self) -> bool:
        """Return True when the best candidate is no worse than the initial one."""
        return self.best.metrics.loss <= self.initial.metrics.loss


def assist_feature_mask_candidates(
    mask_grid: MaskGrid,
    pitch_m: float,
    assist_widths_m: Iterable[float],
    assist_offsets_m: Iterable[float],
    *,
    target_duty_cycle: float = 0.5,
    orientation: str = "vertical",
) -> tuple[MaskCandidate, ...]:
    """Build line-space masks with symmetric sub-resolution assist bars."""
    widths = tuple(float(width) for width in assist_widths_m)
    offsets = tuple(float(offset) for offset in assist_offsets_m)
    if not widths:
        raise ValueError("assist_widths_m must contain at least one width")
    if not offsets:
        raise ValueError("assist_offsets_m must contain at least one offset")

    candidates: list[MaskCandidate] = []
    for width_m in widths:
        for offset_m in offsets:
            candidates.append(
                MaskCandidate(
                    name=(
                        f"assist_w{width_m * 1e9:.1f}nm_"
                        f"o{offset_m * 1e9:.1f}nm"
                    ),
                    pattern=assist_feature_line_space_pattern(
                        mask_grid,
                        pitch_m,
                        width_m,
                        offset_m,
                        target_duty_cycle=target_duty_cycle,
                        orientation=orientation,
                    ),
                )
            )
    return tuple(candidates)


def assist_feature_line_space_pattern(
    mask_grid: MaskGrid,
    pitch_m: float,
    assist_width_m: float,
    assist_offset_m: float,
    *,
    target_duty_cycle: float = 0.5,
    orientation: str = "vertical",
) -> np.ndarray:
    """Return a line-space mask with two assist bars in each clear space."""
    pitch_px, line_px, width_px, offset_px = _assist_geometry_pixels(
        mask_grid,
        pitch_m,
        assist_width_m,
        assist_offset_m,
        target_duty_cycle=target_duty_cycle,
    )
    pattern = line_space_pattern(
        mask_grid,
        pitch_m=pitch_m,
        duty_cycle=target_duty_cycle,
        orientation=orientation,
    )
    first_start = line_px + offset_px
    first_stop = first_start + width_px
    second_stop = pitch_px - offset_px
    second_start = second_stop - width_px

    if orientation == "vertical":
        coord = np.arange(mask_grid.nx, dtype=np.int64) % pitch_px
        assist = (
            ((first_start <= coord) & (coord < first_stop))
            | ((second_start <= coord) & (coord < second_stop))
        )
        pattern[:, assist] = 1.0
    elif orientation == "horizontal":
        coord = np.arange(mask_grid.ny, dtype=np.int64) % pitch_px
        assist = (
            ((first_start <= coord) & (coord < first_stop))
            | ((second_start <= coord) & (coord < second_stop))
        )
        pattern[assist, :] = 1.0
    else:
        raise ValueError("orientation must be 'vertical' or 'horizontal'")
    return pattern


def evaluate_opc_mask_candidate(
    target_printed: np.ndarray,
    mask_grid: MaskGrid,
    mask_candidate: MaskCandidate,
    source_shape: SourceShape,
    *,
    pupil_spec: PupilSpec | None = None,
    dose: float = 1.0,
    weights: SMOObjectiveWeights | None = None,
    threshold: float = 0.3,
    anamorphic: bool = False,
) -> OPCLayoutEvaluation:
    """Evaluate an OPC mask candidate with full-layout contour EPE."""
    if weights is None:
        weights = SMOObjectiveWeights()
    base = evaluate_smo_candidate(
        target_printed,
        mask_grid,
        mask_candidate,
        source_shape,
        pupil_spec=pupil_spec,
        dose=dose,
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
    return OPCLayoutEvaluation(
        mask_candidate=mask_candidate,
        source_shape=source_shape,
        dose=base.dose,
        metrics=SMOCandidateMetrics(
            target_cd_m=base.metrics.target_cd_m,
            printed_cd_m=base.metrics.printed_cd_m,
            mean_epe_m=contour_epe.mean_abs_epe_m,
            lwr_m=base.metrics.lwr_m,
            cd_error_fraction=base.metrics.cd_error_fraction,
            epe_error_fraction=float(epe_error_fraction),
            lwr_fraction=base.metrics.lwr_fraction,
            dose_error_fraction=base.metrics.dose_error_fraction,
            loss=loss,
        ),
        contour_epe=contour_epe,
        aerial=base.aerial,
        printed=base.printed,
    )


def pixel_level_ilt_refinement(
    target_printed: np.ndarray,
    mask_grid: MaskGrid,
    initial_mask_candidate: MaskCandidate,
    source_shape: SourceShape,
    *,
    pupil_spec: PupilSpec | None = None,
    dose: float = 1.0,
    weights: SMOObjectiveWeights | None = None,
    threshold: float = 0.3,
    max_steps: int = 2,
    update_fraction: float = 1.0,
    anamorphic: bool = False,
) -> PixelILTResult:
    """Refine a binary mask by applying local target-vs-print mismatch updates."""
    target = _as_bool_image(target_printed, "target_printed")
    if target.shape != mask_grid.shape():
        raise ValueError("target_printed shape must match mask_grid")
    if int(max_steps) < 0:
        raise ValueError("max_steps must be non-negative")
    if not np.isfinite(update_fraction) or not 0.0 < update_fraction <= 1.0:
        raise ValueError("update_fraction must be in (0, 1]")
    if weights is None:
        weights = SMOObjectiveWeights()

    current_pattern = np.array(initial_mask_candidate.pattern, dtype=np.float64)
    if current_pattern.shape != mask_grid.shape():
        raise ValueError("initial mask candidate shape must match mask_grid")
    desired_mask = (~target).astype(np.float64)
    best: OPCLayoutEvaluation | None = None
    initial: OPCLayoutEvaluation | None = None
    steps: list[PixelILTRefinementStep] = []

    for step_index in range(int(max_steps) + 1):
        evaluation = evaluate_opc_mask_candidate(
            target,
            mask_grid,
            MaskCandidate(name=f"pixel_ilt_step_{step_index}", pattern=current_pattern),
            source_shape,
            pupil_spec=pupil_spec,
            dose=dose,
            weights=weights,
            threshold=threshold,
            anamorphic=anamorphic,
        )
        if initial is None:
            initial = evaluation
        if best is None or evaluation.metrics.loss < best.metrics.loss:
            best = evaluation
        if step_index == int(max_steps):
            break

        mismatch = target != evaluation.printed
        editable = mismatch & (current_pattern != desired_mask)
        editable_indices = np.flatnonzero(editable.ravel())
        if editable_indices.size == 0:
            break

        selected_indices = _select_update_indices(editable_indices, update_fraction)
        proposal = current_pattern.copy().ravel()
        proposal[selected_indices] = desired_mask.ravel()[selected_indices]
        proposal = proposal.reshape(current_pattern.shape)
        proposed_evaluation = evaluate_opc_mask_candidate(
            target,
            mask_grid,
            MaskCandidate(
                name=f"pixel_ilt_step_{step_index + 1}_proposal",
                pattern=proposal,
            ),
            source_shape,
            pupil_spec=pupil_spec,
            dose=dose,
            weights=weights,
            threshold=threshold,
            anamorphic=anamorphic,
        )
        if proposed_evaluation.metrics.loss > evaluation.metrics.loss:
            steps.append(
                PixelILTRefinementStep(
                    step_index=step_index,
                    evaluation=evaluation,
                    changed_pixels=0,
                    next_loss=evaluation.metrics.loss,
                )
            )
            break

        steps.append(
            PixelILTRefinementStep(
                step_index=step_index,
                evaluation=evaluation,
                changed_pixels=int(selected_indices.size),
                next_loss=proposed_evaluation.metrics.loss,
            )
        )
        current_pattern = proposal
        if proposed_evaluation.metrics.loss < best.metrics.loss:
            best = proposed_evaluation

    if initial is None or best is None:
        raise RuntimeError("pixel-level ILT refinement did not evaluate any candidate")
    denominator = max(abs(initial.metrics.loss), float(np.finfo(np.float64).eps))
    improvement = (initial.metrics.loss - best.metrics.loss) / denominator
    return PixelILTResult(
        initial=initial,
        best=best,
        history=tuple(steps),
        weights=weights,
        improvement_fraction=float(improvement),
    )


def _assist_geometry_pixels(
    mask_grid: MaskGrid,
    pitch_m: float,
    assist_width_m: float,
    assist_offset_m: float,
    *,
    target_duty_cycle: float,
) -> tuple[int, int, int, int]:
    _validate_positive_finite(pitch_m, "pitch_m")
    _validate_positive_finite(assist_width_m, "assist_width_m")
    _validate_nonnegative_finite(assist_offset_m, "assist_offset_m")
    if not 0.0 < target_duty_cycle < 1.0:
        raise ValueError("target_duty_cycle must be in (0, 1)")
    pitch_px = max(2, int(round(pitch_m / mask_grid.pixel_size)))
    line_px = max(1, min(pitch_px - 1, int(round(target_duty_cycle * pitch_px))))
    width_px = max(1, int(round(assist_width_m / mask_grid.pixel_size)))
    offset_px = int(round(assist_offset_m / mask_grid.pixel_size))
    clear_px = pitch_px - line_px
    if 2 * offset_px + 2 * width_px > clear_px:
        raise ValueError("assist features must fit inside the clear space")
    return pitch_px, line_px, width_px, offset_px


def _select_update_indices(indices: np.ndarray, update_fraction: float) -> np.ndarray:
    update_count = max(1, int(np.ceil(indices.size * float(update_fraction))))
    return indices[:update_count]


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


def _validate_nonnegative_finite(value: float, name: str) -> None:
    if not np.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be a non-negative finite value")
