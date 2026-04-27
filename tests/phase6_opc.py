"""Phase 6 Part 04 tests for assist-feature OPC and pixel-level ILT."""

from __future__ import annotations

import numpy as np
import pytest

from src import constants as C
from src.illuminator import annular_source
from src.mask import MaskGrid, line_space_pattern
from src.opc import (
    assist_feature_mask_candidates,
    evaluate_opc_mask_candidate,
    pixel_level_ilt_refinement,
)
from src.pupil import PupilSpec
from src.smo import MaskCandidate, SMOObjectiveWeights


def _opc_fixture():
    grid = MaskGrid(nx=256, ny=64, pixel_size=2e-9)
    pitch_m = 40e-9
    target_mask = line_space_pattern(grid, pitch_m=pitch_m, duty_cycle=0.5)
    target_printed = target_mask == 0.0
    pupil = PupilSpec(grid_size=256, na=C.NA_HIGH, obscuration_ratio=0.0)
    source = annular_source(0.2, 0.7, num_radial=1, num_azimuthal=4, name="annular")
    weights = SMOObjectiveWeights(cd=2.0, epe=1.0, lwr=0.0)
    return grid, pitch_m, target_mask, target_printed, pupil, source, weights


def test_assist_feature_mask_candidates_add_symmetric_bars():
    """Assist-feature candidates add deterministic absorber bars in clear space."""
    grid, pitch_m, target_mask, _, _, _, _ = _opc_fixture()

    candidates = assist_feature_mask_candidates(grid, pitch_m, [4e-9], [4e-9])

    assert [candidate.name for candidate in candidates] == ["assist_w4.0nm_o4.0nm"]
    assert candidates[0].pattern.shape == grid.shape()
    assert set(np.unique(candidates[0].pattern)) <= {0.0, 1.0}
    assert float(np.mean(candidates[0].pattern)) > float(np.mean(target_mask))


def test_assist_feature_candidates_cover_width_offset_grid():
    """Assist-feature generation exposes a small OPC design-space grid."""
    grid, pitch_m, _, _, _, _, _ = _opc_fixture()

    candidates = assist_feature_mask_candidates(grid, pitch_m, [2e-9, 4e-9], [2e-9, 4e-9])

    assert len(candidates) == 4
    assert candidates[0].name == "assist_w2.0nm_o2.0nm"
    assert candidates[-1].name == "assist_w4.0nm_o4.0nm"


def test_opc_mask_candidate_evaluates_full_contour_metrics():
    """Part 04 OPC candidates reuse the Phase 6 full-layout contour objective."""
    grid, pitch_m, _, target_printed, pupil, source, weights = _opc_fixture()
    candidate = assist_feature_mask_candidates(grid, pitch_m, [4e-9], [4e-9])[0]

    evaluation = evaluate_opc_mask_candidate(
        target_printed,
        grid,
        candidate,
        source,
        pupil_spec=pupil,
        weights=weights,
    )

    assert evaluation.contour_epe.rows_evaluated == grid.ny
    assert evaluation.contour_epe.columns_evaluated == grid.nx
    assert evaluation.metrics.mean_epe_m == pytest.approx(
        evaluation.contour_epe.mean_abs_epe_m
    )
    assert evaluation.metrics.loss >= 0.0


def test_pixel_level_ilt_refinement_reduces_biased_mask_loss():
    """Pixel-level refinement moves a poor local mask toward the target layout."""
    grid, pitch_m, _, target_printed, pupil, source, weights = _opc_fixture()
    biased_mask = MaskCandidate(
        name="biased_duty_0.20",
        pattern=line_space_pattern(grid, pitch_m=pitch_m, duty_cycle=0.2),
    )

    result = pixel_level_ilt_refinement(
        target_printed,
        grid,
        biased_mask,
        source,
        pupil_spec=pupil,
        weights=weights,
        max_steps=2,
    )

    assert result.converged
    assert result.best.metrics.loss < result.initial.metrics.loss
    assert result.best.contour_epe.mean_abs_epe_m < (
        result.initial.contour_epe.mean_abs_epe_m
    )
    assert result.history[0].changed_pixels > 0
    assert result.improvement_fraction > 0.9


def test_opc_rejects_invalid_inputs():
    """Bad Part 04 geometry and refinement inputs fail early."""
    grid, pitch_m, _, target_printed, _, source, _ = _opc_fixture()
    candidate = MaskCandidate(
        name="target",
        pattern=line_space_pattern(grid, pitch_m=pitch_m, duty_cycle=0.5),
    )

    with pytest.raises(ValueError, match="fit inside"):
        assist_feature_mask_candidates(grid, pitch_m, [12e-9], [4e-9])
    with pytest.raises(ValueError, match="update_fraction"):
        pixel_level_ilt_refinement(
            target_printed,
            grid,
            candidate,
            source,
            update_fraction=0.0,
        )
    with pytest.raises(ValueError, match="target_printed shape"):
        pixel_level_ilt_refinement(
            target_printed[:, :-1],
            grid,
            candidate,
            source,
        )
