"""Phase 6 Part 03 tests for ILT contour EPE and gradient refinement."""

from __future__ import annotations

import numpy as np
import pytest

from src import constants as C
from src.illuminator import annular_source
from src.ilt import (
    finite_difference_bias_gradient,
    full_layout_contour_epe,
    ilt_bias_gradient_refinement,
)
from src.mask import MaskGrid, line_space_pattern
from src.pupil import PupilSpec
from src.smo import SMOObjectiveWeights


def _ilt_fixture():
    grid = MaskGrid(nx=256, ny=64, pixel_size=2e-9)
    pitch_m = 40e-9
    target_pattern = line_space_pattern(grid, pitch_m=pitch_m, duty_cycle=0.5)
    target_printed = target_pattern == 0.0
    pupil = PupilSpec(grid_size=256, na=C.NA_HIGH, obscuration_ratio=0.0)
    source = annular_source(0.2, 0.7, num_radial=1, num_azimuthal=4, name="annular")
    weights = SMOObjectiveWeights(cd=2.0, epe=1.0, lwr=0.0)
    return grid, pitch_m, target_printed, pupil, source, weights


def test_full_layout_contour_epe_is_zero_for_identical_rectangles():
    """Full-layout EPE compares both row and column contour crossings."""
    target = np.zeros((32, 32), dtype=bool)
    target[8:24, 10:22] = True

    contour = full_layout_contour_epe(target, target.copy(), 1e-9)

    assert contour.rows_evaluated == 32
    assert contour.columns_evaluated == 32
    assert contour.x_edges_per_row == 2
    assert contour.y_edges_per_column == 2
    assert contour.mean_abs_epe_m == pytest.approx(0.0)
    assert contour.max_abs_epe_m == pytest.approx(0.0)
    assert contour.edge_count_mismatch_fraction == pytest.approx(0.0)


def test_full_layout_contour_epe_detects_xy_shift():
    """A two-axis contour shift creates nonzero x and y EPE components."""
    target = np.zeros((32, 32), dtype=bool)
    printed = np.zeros_like(target)
    target[8:24, 10:22] = True
    printed[9:25, 11:23] = True

    contour = full_layout_contour_epe(target, printed, 1e-9, penalty_m=8e-9)

    assert contour.x_edge_error_m.shape == (32, 2)
    assert contour.y_edge_error_m.shape == (32, 2)
    assert contour.mean_abs_epe_m > 0.0
    assert contour.max_abs_epe_m >= 1e-9
    assert contour.edge_count_mismatch_fraction > 0.0


def test_finite_difference_bias_gradient_points_toward_unbiased_mask():
    """Finite-difference gradient sign points back toward the target bias."""
    grid, pitch_m, target_printed, pupil, source, weights = _ilt_fixture()

    negative_gradient = finite_difference_bias_gradient(
        target_printed,
        grid,
        pitch_m,
        -6e-9,
        source,
        delta_m=2e-9,
        pupil_spec=pupil,
        weights=weights,
        lower_bias_m=-12e-9,
        upper_bias_m=12e-9,
    )
    positive_gradient = finite_difference_bias_gradient(
        target_printed,
        grid,
        pitch_m,
        6e-9,
        source,
        delta_m=2e-9,
        pupil_spec=pupil,
        weights=weights,
        lower_bias_m=-12e-9,
        upper_bias_m=12e-9,
    )

    assert negative_gradient < 0.0
    assert positive_gradient > 0.0


def test_ilt_bias_gradient_refinement_reduces_full_contour_loss():
    """Part 03 ILT refinement walks a poor mask bias toward the best contour loss."""
    grid, pitch_m, target_printed, pupil, source, weights = _ilt_fixture()

    result = ilt_bias_gradient_refinement(
        target_printed,
        grid,
        pitch_m,
        source,
        initial_bias_m=-6e-9,
        gradient_delta_m=2e-9,
        update_step_m=2e-9,
        max_steps=5,
        pupil_spec=pupil,
        weights=weights,
        lower_bias_m=-12e-9,
        upper_bias_m=12e-9,
    )

    assert result.converged
    assert result.best.metrics.loss < result.initial.metrics.loss
    assert result.best.contour_epe.mean_abs_epe_m < (
        result.initial.contour_epe.mean_abs_epe_m
    )
    assert abs(result.best.bias_m) <= 2e-9
    assert len(result.history) >= 2


def test_ilt_rejects_invalid_inputs():
    """Invalid Part 03 inputs fail before running repeated image simulations."""
    grid, pitch_m, target_printed, pupil, source, weights = _ilt_fixture()
    blank = np.zeros_like(target_printed)

    with pytest.raises(ValueError, match="target contour edge"):
        full_layout_contour_epe(blank, blank.copy(), grid.pixel_size)
    with pytest.raises(ValueError, match="delta_m"):
        finite_difference_bias_gradient(
            target_printed,
            grid,
            pitch_m,
            0.0,
            source,
            delta_m=0.0,
            pupil_spec=pupil,
            weights=weights,
        )
    with pytest.raises(ValueError, match="max_steps"):
        ilt_bias_gradient_refinement(
            target_printed,
            grid,
            pitch_m,
            source,
            initial_bias_m=0.0,
            gradient_delta_m=1e-9,
            update_step_m=1e-9,
            max_steps=-1,
            pupil_spec=pupil,
            weights=weights,
        )
