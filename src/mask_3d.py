"""Reduced Mask 3D effect stubs for Phase 4.

This module is a qualitative boundary-correction scaffold, not a rigorous
Maxwell or RCWA mask solver. It maps the six paper #12 Mask 3D effects into
stable, testable metrics so downstream Phase 6 SMO work can depend on a clear
interface before a higher-fidelity electromagnetic model is introduced.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Iterable

import numpy as np

from . import constants as C
from .mask import MaskGrid, kirchhoff_mask


@dataclass(frozen=True)
class AbsorberMaterial:
    """EUV absorber optical constants at 13.5 nm."""

    name: str
    n: float
    k: float
    thickness_m: float
    top_reflectivity: float = 0.015


@dataclass(frozen=True)
class Mask3DEffectSummary:
    """Qualitative six-effect Mask 3D summary from paper #12."""

    material: AbsorberMaterial
    pitch_m: float
    chief_ray_angle_deg: float
    orientation: str
    shadowing_loss_fraction: float
    orientation_cd_bias_m: float
    telecentricity_error_mrad: float
    contrast_loss_fraction: float
    best_focus_shift_m: float
    secondary_image_fraction: float
    phase_error_waves: float

    def as_effect_vector(self) -> tuple[float, float, float, float, float, float]:
        """Return the six paper #12 effect metrics in checklist order."""
        return (
            self.shadowing_loss_fraction,
            self.orientation_cd_bias_m,
            self.telecentricity_error_mrad,
            self.contrast_loss_fraction,
            self.best_focus_shift_m,
            self.secondary_image_fraction,
        )


@dataclass(frozen=True)
class BoundaryCorrectionResult:
    """Field-level reduced Mask 3D boundary correction output."""

    baseline_field: np.ndarray
    corrected_field: np.ndarray
    shadow_map: np.ndarray
    phase_map_radians: np.ndarray
    secondary_field: np.ndarray
    summary: Mask3DEffectSummary
    ghost_shift_px: int


TABN_REFERENCE = AbsorberMaterial(
    name="TaBN reference",
    n=0.94,
    k=0.030,
    thickness_m=60.0e-9,
    top_reflectivity=0.018,
)

NI_HIGH_K = AbsorberMaterial(
    name="Ni high-k candidate",
    n=0.98,
    k=0.085,
    thickness_m=42.0e-9,
    top_reflectivity=0.010,
)

RUTA_LOW_N_PSM = AbsorberMaterial(
    name="RuTa low-n attenuated PSM candidate",
    n=0.92,
    k=0.055,
    thickness_m=45.0e-9,
    top_reflectivity=0.012,
)


def default_absorber_materials() -> tuple[AbsorberMaterial, ...]:
    """Return the Phase 4 starter absorber library."""
    return (TABN_REFERENCE, NI_HIGH_K, RUTA_LOW_N_PSM)


def load_absorber_materials_json(path: str | Path) -> tuple[AbsorberMaterial, ...]:
    """Load absorber materials from a JSON material library.

    Rows may specify either `thickness_m` or `thickness_nm`. The loader is
    intentionally small so measured n,k rows can replace the starter qualitative
    values without changing the Phase 4 code interface.
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = data.get("materials")
    if not isinstance(rows, list) or not rows:
        raise ValueError("materials JSON must contain a non-empty materials list")

    materials: list[AbsorberMaterial] = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each material row must be a JSON object")
        if "thickness_m" in row:
            thickness_m = float(row["thickness_m"])
        elif "thickness_nm" in row:
            thickness_m = float(row["thickness_nm"]) * 1.0e-9
        else:
            raise ValueError("material row must include thickness_m or thickness_nm")

        material = AbsorberMaterial(
            name=str(row.get("name", "")),
            n=float(row["n"]),
            k=float(row["k"]),
            thickness_m=thickness_m,
            top_reflectivity=float(row.get("top_reflectivity", 0.015)),
        )
        _validate_material(material)
        materials.append(material)
    return tuple(materials)


def mask3d_six_effects(
    pitch_m: float,
    *,
    material: AbsorberMaterial = TABN_REFERENCE,
    chief_ray_angle_deg: float = 6.0,
    orientation: str = "vertical",
    absorber_fraction: float = 0.5,
) -> Mask3DEffectSummary:
    """Return a reduced six-effect Mask 3D checklist for one pitch/material.

    The model intentionally scales every 3D correction by chief-ray angle. A
    zero-CRA in-line projector therefore collapses to the thin-mask baseline,
    matching the paper #12 mitigation logic used by the Phase 4 gate.
    """
    _validate_material(material)
    _validate_positive(pitch_m, "pitch_m")
    if not np.isfinite(chief_ray_angle_deg):
        raise ValueError("chief_ray_angle_deg must be finite")
    if orientation not in {"vertical", "horizontal"}:
        raise ValueError("orientation must be 'vertical' or 'horizontal'")
    if not np.isfinite(absorber_fraction) or not 0.0 < absorber_fraction < 1.0:
        raise ValueError("absorber_fraction must be in (0, 1)")

    angle_scale = abs(math.sin(math.radians(chief_ray_angle_deg)))
    height_ratio = material.thickness_m / pitch_m
    phase_strength = abs(1.0 - material.n)
    attenuation_leak = 1.0 / (1.0 + 20.0 * material.k)
    m3d_strength = phase_strength + 0.10 * attenuation_leak
    pitch_scale = math.sqrt(32.0e-9 / pitch_m)

    shadowing = min(
        0.80,
        angle_scale * height_ratio * absorber_fraction * (0.7 + attenuation_leak),
    )
    orientation_sign = 1.0 if orientation == "vertical" else -1.0
    orientation_bias = orientation_sign * 0.12 * shadowing * pitch_m
    telecentricity = 1.0e3 * angle_scale * m3d_strength * pitch_scale
    contrast_loss = min(0.80, 0.45 * angle_scale * height_ratio * m3d_strength)
    best_focus_shift = 120.0e-9 * angle_scale * height_ratio * m3d_strength * pitch_scale
    secondary = min(
        0.50,
        0.5 * angle_scale * height_ratio * material.top_reflectivity,
    )
    phase_error_waves = angle_scale * phase_strength * material.thickness_m / C.LAMBDA_EUV

    return Mask3DEffectSummary(
        material=material,
        pitch_m=float(pitch_m),
        chief_ray_angle_deg=float(chief_ray_angle_deg),
        orientation=orientation,
        shadowing_loss_fraction=float(shadowing),
        orientation_cd_bias_m=float(orientation_bias),
        telecentricity_error_mrad=float(telecentricity),
        contrast_loss_fraction=float(contrast_loss),
        best_focus_shift_m=float(best_focus_shift),
        secondary_image_fraction=float(secondary),
        phase_error_waves=float(phase_error_waves),
    )


def boundary_corrected_mask(
    pattern: np.ndarray,
    grid: MaskGrid,
    pitch_m: float,
    *,
    material: AbsorberMaterial = TABN_REFERENCE,
    chief_ray_angle_deg: float = 6.0,
    orientation: str = "vertical",
    absorber_fraction: float | None = None,
    ghost_shift_px: int = 1,
) -> BoundaryCorrectionResult:
    """Apply reduced field-level Mask 3D boundary correction to a binary mask.

    The baseline is the Phase 1 Kirchhoff field. Corrections are localized to
    clear pixels adjacent to absorber boundaries: shadowing attenuates the
    incident-side boundary, absorber phase perturbs the edge field, and the
    secondary-image term adds a shifted weak ghost field. This is still a
    qualitative scaffold, but it returns the same complex field type expected by
    `aerial_image`.
    """
    baseline = kirchhoff_mask(pattern)
    absorber = _as_absorber_mask(pattern, expected_shape=grid.shape())
    if absorber_fraction is None:
        absorber_fraction = float(np.mean(absorber))
    if not 0.0 < absorber_fraction < 1.0:
        raise ValueError("absorber_fraction must be in (0, 1)")
    if ghost_shift_px < 0:
        raise ValueError("ghost_shift_px must be non-negative")

    summary = mask3d_six_effects(
        pitch_m,
        material=material,
        chief_ray_angle_deg=chief_ray_angle_deg,
        orientation=orientation,
        absorber_fraction=absorber_fraction,
    )

    clear = ~absorber
    axis = 1 if orientation == "vertical" else 0
    incidence_shift = 1 if chief_ray_angle_deg >= 0.0 else -1
    incident_absorber = _shift_bool(absorber, incidence_shift, axis=axis)
    boundary_clear = clear & _edge_neighbor_mask(absorber)
    shadow_region = clear & incident_absorber

    shadow_map = np.zeros(grid.shape(), dtype=np.float64)
    shadow_map[shadow_region] = summary.shadowing_loss_fraction

    signed_phase = math.copysign(
        2.0 * math.pi * summary.phase_error_waves,
        chief_ray_angle_deg if chief_ray_angle_deg != 0.0 else 1.0,
    )
    phase_map = np.zeros(grid.shape(), dtype=np.float64)
    phase_map[boundary_clear] = signed_phase

    amplitude = np.abs(baseline)
    amplitude *= 1.0 - shadow_map
    amplitude[boundary_clear] *= 1.0 - 0.5 * summary.contrast_loss_fraction
    corrected = amplitude * np.exp(1j * phase_map)

    if ghost_shift_px == 0 or summary.secondary_image_fraction == 0.0:
        secondary = np.zeros_like(baseline)
    else:
        secondary = (
            summary.secondary_image_fraction
            * _shift_complex(
                baseline,
                incidence_shift * ghost_shift_px,
                axis=axis,
            )
            * np.exp(1j * signed_phase)
        )
    corrected = (corrected + secondary).astype(np.complex128)

    return BoundaryCorrectionResult(
        baseline_field=baseline,
        corrected_field=corrected,
        shadow_map=shadow_map,
        phase_map_radians=phase_map,
        secondary_field=secondary.astype(np.complex128),
        summary=summary,
        ghost_shift_px=int(ghost_shift_px),
    )


def compare_absorber_materials(
    pitch_m: float,
    materials: Iterable[AbsorberMaterial] | None = None,
    *,
    chief_ray_angle_deg: float = 6.0,
    orientation: str = "vertical",
) -> tuple[Mask3DEffectSummary, ...]:
    """Evaluate the same reduced Mask 3D checklist across absorber materials."""
    library = default_absorber_materials() if materials is None else tuple(materials)
    if not library:
        raise ValueError("materials must contain at least one AbsorberMaterial")
    return tuple(
        mask3d_six_effects(
            pitch_m,
            material=material,
            chief_ray_angle_deg=chief_ray_angle_deg,
            orientation=orientation,
        )
        for material in library
    )


def _validate_material(material: AbsorberMaterial) -> None:
    if not material.name:
        raise ValueError("material.name must be non-empty")
    _validate_positive(material.n, "material.n")
    if not np.isfinite(material.k) or material.k < 0.0:
        raise ValueError("material.k must be non-negative and finite")
    _validate_positive(material.thickness_m, "material.thickness_m")
    if (
        not np.isfinite(material.top_reflectivity)
        or not 0.0 <= material.top_reflectivity < 1.0
    ):
        raise ValueError("material.top_reflectivity must be in [0, 1)")


def _validate_positive(value: float, name: str) -> None:
    if not np.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be a positive finite value")


def _as_absorber_mask(pattern: np.ndarray, expected_shape: tuple[int, int]) -> np.ndarray:
    arr = np.asarray(pattern)
    if arr.shape != expected_shape:
        raise ValueError("pattern shape must match MaskGrid.shape()")
    if not np.all((arr == 0) | (arr == 1)):
        raise ValueError("pattern must contain only 0 or 1")
    mask = arr.astype(bool)
    if np.all(mask) or not np.any(mask):
        raise ValueError("pattern must contain both absorber and clear regions")
    return mask


def _edge_neighbor_mask(absorber: np.ndarray) -> np.ndarray:
    neighbors = np.zeros_like(absorber, dtype=bool)
    for axis in (0, 1):
        neighbors |= _shift_bool(absorber, 1, axis=axis)
        neighbors |= _shift_bool(absorber, -1, axis=axis)
    return neighbors


def _shift_bool(values: np.ndarray, shift: int, *, axis: int) -> np.ndarray:
    return _shift_array(values, shift, axis=axis, fill_value=False).astype(bool)


def _shift_complex(values: np.ndarray, shift: int, *, axis: int) -> np.ndarray:
    return _shift_array(values, shift, axis=axis, fill_value=0.0 + 0.0j).astype(
        np.complex128
    )


def _shift_array(
    values: np.ndarray,
    shift: int,
    *,
    axis: int,
    fill_value: object,
) -> np.ndarray:
    if shift == 0:
        return values.copy()
    result = np.full(values.shape, fill_value, dtype=values.dtype)
    source = [slice(None)] * values.ndim
    destination = [slice(None)] * values.ndim
    if shift > 0:
        source[axis] = slice(0, -shift)
        destination[axis] = slice(shift, None)
    else:
        source[axis] = slice(-shift, None)
        destination[axis] = slice(0, shift)
    result[tuple(destination)] = values[tuple(source)]
    return result
