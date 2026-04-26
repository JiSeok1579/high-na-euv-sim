"""Depth-resolved resist dose model for Phase 5 Level 2."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable

import numpy as np

from .aerial import WaferGrid, aerial_image
from .mask import MaskGrid
from .pupil import PupilSpec


@dataclass(frozen=True)
class DepthSliceSummary:
    """Per-depth dose and exposure summary."""

    depth_m: float
    defocus_m: float
    attenuation: float
    mean_dose: float
    exposed_fraction: float


@dataclass(frozen=True)
class DepthResolvedResist:
    """Depth-resolved aerial, dose, and exposure stack."""

    aerial_stack: np.ndarray
    dose_stack: np.ndarray
    exposed_stack: np.ndarray
    depth_values_m: tuple[float, ...]
    defocus_values_m: tuple[float, ...]
    attenuation_factors: tuple[float, ...]
    wafer: WaferGrid
    dose: float
    threshold: float
    absorption_coefficient_m_inv: float
    slice_summaries: tuple[DepthSliceSummary, ...]


def depth_defocus_values(
    depth_values_m: Iterable[float],
    *,
    top_defocus_m: float = 0.0,
) -> tuple[float, ...]:
    """Map resist depths to signed defocus values.

    Depth increases downward into the resist. With the top surface at focus,
    deeper slices are below best focus, so their defocus is negative.
    """
    depths = _validate_depth_values(depth_values_m)
    if not np.isfinite(top_defocus_m):
        raise ValueError("top_defocus_m must be finite")
    return tuple(float(top_defocus_m - depth_m) for depth_m in depths)


def depth_attenuation_factors(
    depth_values_m: Iterable[float],
    absorption_coefficient_m_inv: float,
) -> tuple[float, ...]:
    """Return Beer-Lambert dose attenuation factors from top to bottom."""
    depths = _validate_depth_values(depth_values_m)
    if (
        not np.isfinite(absorption_coefficient_m_inv)
        or absorption_coefficient_m_inv < 0.0
    ):
        raise ValueError(
            "absorption_coefficient_m_inv must be a non-negative finite value"
        )

    top_depth = depths[0]
    return tuple(
        float(np.exp(-absorption_coefficient_m_inv * (depth_m - top_depth)))
        for depth_m in depths
    )


def depth_resolved_dose_stack(
    aerial_stack: np.ndarray,
    depth_values_m: Iterable[float],
    *,
    dose: float = 1.0,
    absorption_coefficient_m_inv: float = 2.0e6,
) -> np.ndarray:
    """Apply dose and depth attenuation to a 2-D image or 3-D aerial stack."""
    depths = _validate_depth_values(depth_values_m)
    if not np.isfinite(dose) or dose <= 0.0:
        raise ValueError("dose must be a positive finite value")

    aerial = np.asarray(aerial_stack, dtype=np.float64)
    if aerial.ndim == 2:
        aerial = np.broadcast_to(aerial, (len(depths), *aerial.shape)).copy()
    elif aerial.ndim != 3:
        raise ValueError("aerial_stack must be a 2-D image or 3-D depth stack")
    if aerial.shape[0] != len(depths):
        raise ValueError("aerial_stack depth axis must match depth_values_m length")
    if not np.all(np.isfinite(aerial)):
        raise ValueError("aerial_stack must contain finite values")
    if np.any(aerial < 0.0):
        raise ValueError("aerial_stack intensity must be non-negative")

    attenuation = np.array(
        depth_attenuation_factors(depths, absorption_coefficient_m_inv),
        dtype=np.float64,
    )
    return (dose * aerial * attenuation[:, np.newaxis, np.newaxis]).astype(np.float64)


def depth_resolved_threshold_resist(
    aerial_stack: np.ndarray,
    depth_values_m: Iterable[float],
    *,
    dose: float = 1.0,
    threshold: float = 0.3,
    absorption_coefficient_m_inv: float = 2.0e6,
) -> tuple[np.ndarray, np.ndarray]:
    """Return depth dose and exposure stacks from aerial intensity."""
    if not np.isfinite(threshold) or threshold <= 0.0:
        raise ValueError("threshold must be a positive finite value")
    dose_stack = depth_resolved_dose_stack(
        aerial_stack,
        depth_values_m,
        dose=dose,
        absorption_coefficient_m_inv=absorption_coefficient_m_inv,
    )
    return dose_stack, dose_stack > threshold


def top_bottom_dose_asymmetry(dose_stack: np.ndarray) -> float:
    """Return `(top_mean - bottom_mean) / top_mean` for a depth dose stack."""
    stack = np.asarray(dose_stack, dtype=np.float64)
    if stack.ndim != 3 or stack.shape[0] < 2:
        raise ValueError("dose_stack must be a 3-D stack with at least two slices")
    if not np.all(np.isfinite(stack)):
        raise ValueError("dose_stack must contain finite values")
    top_mean = float(np.mean(stack[0]))
    bottom_mean = float(np.mean(stack[-1]))
    if top_mean <= 0.0:
        raise ValueError("top slice mean dose must be positive")
    return float((top_mean - bottom_mean) / top_mean)


def focus_depth_resolved_resist(
    mask_field: np.ndarray,
    mask_grid: MaskGrid,
    depth_values_m: Iterable[float],
    pupil_spec: PupilSpec | None = None,
    *,
    top_defocus_m: float = 0.0,
    dose: float = 1.0,
    threshold: float = 0.3,
    absorption_coefficient_m_inv: float = 2.0e6,
    anamorphic: bool = True,
) -> DepthResolvedResist:
    """Evaluate aerial, dose, and exposure at depth-coupled focus slices."""
    if pupil_spec is None:
        pupil_spec = PupilSpec(grid_size=max(mask_grid.nx, mask_grid.ny))

    depths = _validate_depth_values(depth_values_m)
    defocus_values = depth_defocus_values(depths, top_defocus_m=top_defocus_m)

    aerial_slices: list[np.ndarray] = []
    wafer_grid: WaferGrid | None = None
    for defocus_m in defocus_values:
        intensity, wafer = aerial_image(
            mask_field,
            mask_grid,
            pupil_spec=replace(pupil_spec, defocus_m=defocus_m),
            anamorphic=anamorphic,
        )
        aerial_slices.append(intensity)
        if wafer_grid is None:
            wafer_grid = wafer

    if wafer_grid is None:
        raise RuntimeError("depth-resolved resist produced no focus slices")

    aerial_stack = np.stack(aerial_slices).astype(np.float64)
    dose_stack, exposed_stack = depth_resolved_threshold_resist(
        aerial_stack,
        depths,
        dose=dose,
        threshold=threshold,
        absorption_coefficient_m_inv=absorption_coefficient_m_inv,
    )
    attenuation = depth_attenuation_factors(depths, absorption_coefficient_m_inv)
    summaries = tuple(
        DepthSliceSummary(
            depth_m=depth_m,
            defocus_m=defocus_m,
            attenuation=attenuation_factor,
            mean_dose=float(np.mean(dose_stack[index])),
            exposed_fraction=float(np.mean(exposed_stack[index])),
        )
        for index, (depth_m, defocus_m, attenuation_factor) in enumerate(
            zip(depths, defocus_values, attenuation, strict=True)
        )
    )

    return DepthResolvedResist(
        aerial_stack=aerial_stack,
        dose_stack=dose_stack,
        exposed_stack=exposed_stack,
        depth_values_m=depths,
        defocus_values_m=defocus_values,
        attenuation_factors=attenuation,
        wafer=wafer_grid,
        dose=dose,
        threshold=threshold,
        absorption_coefficient_m_inv=absorption_coefficient_m_inv,
        slice_summaries=summaries,
    )


def _validate_depth_values(depth_values_m: Iterable[float]) -> tuple[float, ...]:
    depths = tuple(float(value) for value in depth_values_m)
    if not depths:
        raise ValueError("depth_values_m must contain at least one value")
    if not all(np.isfinite(value) for value in depths):
        raise ValueError("depth_values_m must contain finite values")
    if any(value < 0.0 for value in depths):
        raise ValueError("depth_values_m must be non-negative")
    if any(next_value < value for value, next_value in zip(depths, depths[1:])):
        raise ValueError("depth_values_m must be sorted from top to bottom")
    return depths
