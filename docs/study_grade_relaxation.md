# Study-Grade Relaxation Policy

## 1. Purpose

This project is a study-purpose simulator. The goal is to build working
approximations, visualize behavior, and learn how 0.55 NA EUV lithography
parameters affect the pipeline. It is not an industry-grade validation package
and it does not target 1:1 equipment replication.

Strictness is useful only when it protects learning quality. When strictness
blocks implementation without improving study value, it should be relaxed and
tracked as backlog.

## 2. Relaxed Items

The following are study-grade P3/backlog items unless they directly break
learning, reproducibility, or correctness:

- Simplification four-way tracking below 100%, down to roughly 80%.
- Missing mypy strict mode.
- Missing `CONTRIBUTING.md`.
- Missing paper #20 or paper #21 quantitative reproduction.
- Missing industry-grade quantitative ground truth.
- KPI K3 missing the old 30% quantitative tolerance, as long as the k2 law shape
  and monotonic DOF trend are preserved.
- Small `_validate_*` helper duplication that does not affect correctness.
- Missing real RCWA/DDM/measured Mask 3D rows, when loaders and regression hooks
  are explicit that current data is qualitative.

## 3. Maintained Items

The following remain P0/P1 in study-grade mode:

- Test pass rate below 100%.
- Defocus, anamorphic, CRA, or other sign-convention violations.
- Unit inconsistency, especially mixed meters/nanometers/radians without explicit
  conversion.
- Dishonest `AUDIT_LOG.md` or false closure of mitigation tasks.
- Broken reproducibility for seeded stochastic paths.
- Missing Phase gate tracking for work that claims to close a Phase or Part.
- Metadata drift between `REVIEWER_DIRECTIVE.md`, `.github/CLAUDE.md`, and
  current project policy.

## 4. Decision Rule

- If strictness blocks learning progress, relax it.
- If strictness protects correct learning, keep it.
- If uncertain, implement the smallest working version first, inspect the
  behavior, then decide whether refinement is needed.

## 5. Workspace Rename

The GitHub repository is already `JiSeok1579/high-na-euv-sim`, and project docs
use the simulator name. The local folder may still be:

```bash
~/Desktop/High-NA EUV Lithography Digital Twin
```

Renaming the active Codex workspace can break the current desktop session. Do it
manually after a clean merge if desired:

```bash
cd ~/Desktop
mv "High-NA EUV Lithography Digital Twin" "High-NA EUV Lithography Simulator"
cd "High-NA EUV Lithography Simulator"
git status
```

No Git remote change is required.
