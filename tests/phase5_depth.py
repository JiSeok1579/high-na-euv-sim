"""Phase 5 Level 2 tests for depth-resolved resist dose."""

from __future__ import annotations

import numpy as np
import pytest

from src import constants as C
from src.dof import focus_drilling_average
from src.mask import MaskGrid, kirchhoff_mask, line_space_pattern
from src.pupil import PupilSpec
from src.resist_depth import (
    depth_attenuation_factors,
    depth_defocus_values,
    depth_resolved_dose_stack,
    depth_resolved_threshold_resist,
    focus_depth_resolved_resist,
    top_bottom_dose_asymmetry,
)


def test_depth_defocus_values_map_deeper_slices_negative():
    """Deeper resist slices sit below the top focus plane."""
    values = depth_defocus_values([0.0, 10e-9, 30e-9], top_defocus_m=5e-9)

    assert values == pytest.approx((5e-9, -5e-9, -25e-9))


def test_depth_attenuation_factors_decay_from_top_to_bottom():
    """Beer-Lambert factors should monotonically decay with depth."""
    factors = depth_attenuation_factors(
        [0.0, 25e-9, 50e-9],
        absorption_coefficient_m_inv=4.0e6,
    )

    assert factors[0] == pytest.approx(1.0)
    assert factors[0] > factors[1] > factors[2]


def test_depth_resolved_dose_stack_has_top_bottom_asymmetry():
    """A uniform aerial image becomes depth-asymmetric after absorption."""
    dose_stack = depth_resolved_dose_stack(
        np.ones((2, 4, 4)),
        [0.0, 80e-9],
        dose=2.0,
        absorption_coefficient_m_inv=5.0e6,
    )

    assert dose_stack.shape == (2, 4, 4)
    assert float(np.mean(dose_stack[0])) == pytest.approx(2.0)
    assert float(np.mean(dose_stack[1])) < float(np.mean(dose_stack[0]))
    assert top_bottom_dose_asymmetry(dose_stack) > 0.0


def test_depth_resolved_threshold_preserves_stack_shape():
    """Thresholding returns dose and boolean exposure stacks together."""
    aerial = np.stack(
        [
            np.full((3, 5), 0.8),
            np.full((3, 5), 0.4),
        ]
    )
    dose_stack, exposed = depth_resolved_threshold_resist(
        aerial,
        [0.0, 40e-9],
        dose=1.0,
        threshold=0.5,
        absorption_coefficient_m_inv=0.0,
    )

    assert dose_stack.shape == exposed.shape == aerial.shape
    assert np.all(exposed[0])
    assert not np.any(exposed[1])


def test_focus_depth_stack_matches_focus_drilling_average_without_absorption():
    """Depth focus slices stay consistent with the Phase 3 focus-drilling API."""
    grid = MaskGrid(nx=256, ny=64, pixel_size=2e-9)
    mask = kirchhoff_mask(line_space_pattern(grid, pitch_m=80e-9))
    pupil_spec = PupilSpec(grid_size=256, na=C.NA_HIGH, obscuration_ratio=0.0)
    depths = [0.0, 20e-9, 40e-9]

    result = focus_depth_resolved_resist(
        mask,
        grid,
        depths,
        pupil_spec=pupil_spec,
        absorption_coefficient_m_inv=0.0,
        threshold=0.2,
        anamorphic=False,
    )
    focus_average, wafer = focus_drilling_average(
        mask,
        grid,
        result.defocus_values_m,
        pupil_spec=pupil_spec,
        anamorphic=False,
    )

    assert result.wafer == wafer
    assert result.aerial_stack.shape == (3, wafer.ny, wafer.nx)
    assert np.allclose(np.mean(result.aerial_stack, axis=0), focus_average)


def test_focus_depth_resolved_resist_reports_top_bottom_summary():
    """Absorbing depth stack reports lower bottom dose and exposure fraction."""
    grid = MaskGrid(nx=256, ny=64, pixel_size=2e-9)
    mask = kirchhoff_mask(line_space_pattern(grid, pitch_m=80e-9))
    result = focus_depth_resolved_resist(
        mask,
        grid,
        [0.0, 40e-9, 80e-9],
        pupil_spec=PupilSpec(grid_size=256, na=C.NA_HIGH, obscuration_ratio=0.0),
        dose=1.0,
        threshold=0.2,
        absorption_coefficient_m_inv=6.0e6,
        anamorphic=False,
    )

    top = result.slice_summaries[0]
    bottom = result.slice_summaries[-1]
    assert result.exposed_stack.dtype == np.bool_
    assert top.depth_m == pytest.approx(0.0)
    assert bottom.defocus_m < top.defocus_m
    assert bottom.mean_dose < top.mean_dose
    assert bottom.attenuation < top.attenuation
