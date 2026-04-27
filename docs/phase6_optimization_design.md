# Phase 6 Optimization Design

## Scope

Phase 6 Part 01 added a study-grade source-mask optimization (SMO) MVP. Phase 6
Part 02 extended that loop with PMWO/OPC candidate families and row-wise 2-D EPE
maps. Phase 6 Part 03 adds a numeric-gradient ILT refinement path and
full-layout contour EPE. Phase 6 Part 04 adds assist-feature OPC candidates and
pixel-level ILT refinement. The implementation closes the simulator loop by
evaluating:

- mask candidates,
- Phase 2 source shapes,
- OPC bias candidates,
- pupil and wavefront candidates,
- dose candidates,
- Phase 5 stochastic LWR budget penalties,
- finite-difference bias-gradient updates,
- local binary mask-pixel updates.

The optimizer is deterministic grid search. This is intentionally simpler than
industrial SMO, PMWO, OPC, or ILT, but it gives the project a complete
target-to-candidate optimization loop with measurable loss components.

## Objective

The MVP objective is:

```text
loss = w_cd * CD_error
     + w_epe * EPE_error
     + w_lwr * LWR_fraction
     + w_dose * dose_error
```

Definitions:

- `CD_error = abs(printed_cd - target_cd) / target_cd`
- `EPE_error = mean_abs_edge_error / target_cd`
- `LWR_fraction = phase5_lwr_budget / target_cd`
- `dose_error = (dose - 1)^2`

The LWR term calls `lwr_decomposition_budget()` from `src/resist_stochastic.py`,
so Phase 6 directly reuses the Phase 5 stochastic resist model.

## Source Variable Connection

Each candidate evaluation runs:

```text
mask candidate -> Kirchhoff field
source shape -> partial_coherent_aerial_image()
dose -> threshold_resist()
printed line -> CD/EPE/LWR objective
```

This connects the Phase 2 source-shape API to the Phase 6 objective. The current
MVP supports point and sampled source shapes such as annular, dipole, quadrupole,
or freeform JSON-loaded sources.

## PMWO / OPC Extension

Phase 6 Part 02 adds `src/pmwo.py`:

- `opc_bias_mask_candidates()` converts mask-bias values into binary line-space
  mask candidates.
- `wavefront_zernike_candidates()` sweeps one Zernike coefficient in waves.
- `pupil_obscuration_candidates()` sweeps central-obscuration ratio.
- `edge_placement_error_map_2d()` returns row-wise target-vs-print EPE maps.
- `pmwo_grid_search()` evaluates mask, source, pupil/wavefront, and dose
  combinations with the same weighted objective.

The PMWO loss uses the same CD/LWR/dose terms as Part 01, but replaces the
center-line EPE term with the mean absolute value from the 2-D EPE map.

## ILT / Numeric-Gradient Extension

Phase 6 Part 03 adds `src/ilt.py`:

- `full_layout_contour_epe()` compares target and printed contour transitions
  along both image axes.
- `evaluate_ilt_bias_candidate()` evaluates one scalar OPC/ILT mask-bias point
  with the full-layout contour EPE term.
- `finite_difference_bias_gradient()` estimates `d(loss)/d(mask_bias)` with a
  bounded finite difference.
- `ilt_bias_gradient_refinement()` walks a poor mask-bias point toward lower
  contour loss using deterministic finite-difference descent.

This is not a production ILT engine. It is the first numeric-gradient hook that
keeps the optimization path inspectable while proving that the simulator can
refine a mask parameter using the same forward model and objective stack.

## Assist-Feature OPC / Pixel ILT Extension

Phase 6 Part 04 adds `src/opc.py`:

- `assist_feature_mask_candidates()` builds symmetric sub-resolution assist-bar
  candidates for line-space layouts.
- `assist_feature_line_space_pattern()` creates one deterministic assist-feature
  mask pattern.
- `evaluate_opc_mask_candidate()` evaluates arbitrary binary OPC masks with the
  same full-layout contour objective.
- `pixel_level_ilt_refinement()` applies local target-vs-print mismatch updates
  to binary mask pixels and accepts only loss-reducing candidates.

The pixel-level refinement is intentionally conservative: it does not introduce
autograd or grayscale mask manufacturing rules. It proves that the simulator can
move from scalar bias refinement to local mask-shape edits while preserving the
same source, pupil, resist, contour-EPE, and loss stack.

## Implemented APIs

- `SMOObjectiveWeights`
- `MaskCandidate`
- `SMOCandidateMetrics`
- `SMOCandidateEvaluation`
- `SMOResult`
- `weighted_smo_loss()`
- `line_space_mask_candidates()`
- `evaluate_smo_candidate()`
- `fast_smo_grid_search()`
- `opc_bias_mask_candidates()`
- `wavefront_zernike_candidates()`
- `pupil_obscuration_candidates()`
- `edge_placement_error_map_2d()`
- `pmwo_grid_search()`
- `full_layout_contour_epe()`
- `evaluate_ilt_bias_candidate()`
- `finite_difference_bias_gradient()`
- `ilt_bias_gradient_refinement()`
- `assist_feature_mask_candidates()`
- `assist_feature_line_space_pattern()`
- `evaluate_opc_mask_candidate()`
- `pixel_level_ilt_refinement()`

## Simplifications

| ID | Simplification | Reason |
|---|---|---|
| P6-L1 | Deterministic grid search instead of gradient descent | Keeps the first SMO loop inspectable and stable. |
| P6-L2 | Line-space mask helper for the MVP demo | Enough to verify target-to-mask optimization before contact-array and ILT work. |
| P6-L3 | Threshold resist print check inside the objective | Reuses the existing end-to-end MVP path without adding a new resist abstraction. |
| P6-L4 | Scalar CD/LWR plus row-wise 2-D EPE objective | Enough to expose PMWO/OPC trends before polygon-level contour extraction. |
| P6-L5 | OPC represented as line-space mask bias | Keeps candidate generation deterministic while preserving the mask-bias control axis. |
| P6-L6 | Pupil/wavefront candidates are discrete sweeps | Replaces autograd PMWO with inspectable grid search for the study-grade gate. |
| P6-L7 | ILT gradient is finite-difference over one mask-bias parameter | Provides a stable numeric-gradient hook before continuous pixel-level ILT. |
| P6-L8 | Full-layout contour EPE uses row/column binary transitions | Captures x/y contour drift without requiring polygon contour tracing yet. |
| P6-L9 | Assist features are symmetric line-space absorber bars | Captures an OPC control axis without general curvilinear mask synthesis. |
| P6-L10 | Pixel-level ILT uses binary target-vs-print mismatch updates | Enables local mask edits before grayscale/autograd/pixel-manufacturing constraints. |

## Verification

The Phase 6 test suite checks:

- line-space mask candidate generation,
- improvement from a poor initial mask/source candidate,
- direct Phase 5 LWR budget connection,
- LWR weight influence on candidate ranking,
- OPC bias candidate generation,
- pupil and Zernike wavefront candidate generation,
- 2-D EPE zero-map and candidate ranking,
- full-layout x/y contour EPE extraction,
- finite-difference gradient sign and descent improvement,
- assist-feature mask generation,
- arbitrary OPC mask contour evaluation,
- pixel-level ILT loss reduction from a biased mask,
- input validation before optimization.

Current implementation files:

- `src/smo.py`
- `tests/phase6_smo.py`
- `src/pmwo.py`
- `tests/phase6_pmwo.py`
- `src/ilt.py`
- `tests/phase6_ilt.py`
- `src/opc.py`
- `tests/phase6_opc.py`
- `notebooks/5_SMO_PMWO.ipynb`
- `docs/phase6_optimization_design.md`
