# Phase 1 — Scalar Fourier Optics MVP: Design Decisions

> 작성일: 2026-04-26  
> 모듈: `src/constants.py`, `src/pupil.py`, `src/mask.py`, `src/aerial.py`  
> 대응 계획서: `진행계획서.md` §4.1  
> 우선 학습 논문: #19 (anamorphic), #15 (annular pupil), #11 (target imaging)

---

## 1. 좌표계 및 기호 컨벤션 (D5 결정사항 구현)

| 평면 | 좌표 | 단위 | 설명 |
|------|------|------|------|
| Mask | (x_m, y_m) | meter | 마스크 평면. `MaskGrid.pixel_size` 정사각 |
| Pupil | (f_x, f_y) | 1/meter | 공간 주파수. `pupil[ny/2, nx/2]`이 DC |
| Wafer | (x_w, y_w) | meter | 웨이퍼 평면. `WaferGrid.pixel_x_m`, `pixel_y_m` 비대칭 |

**Anamorphic 변환** (paper #19 Migura 2015 fig. 3):
```
x_w = x_m / 4   (scan direction, 4× demag)
y_w = y_m / 8   (cross-scan,    8× demag)
```
구현: `wafer_grid_from_mask()`. `anamorphic=False`로 1× 모드 (테스트용) 가능.

**부호/회전 컨벤션**: numpy `meshgrid(..., indexing='xy')` 표준. f_x는 가로 (axis=1), f_y는 세로 (axis=0). FFT는 `np.fft.fft2` + `fftshift`로 DC를 중앙에 배치한 뒤 pupil을 곱한다. 한 번 정한 컨벤션은 변경 금지 (D5).

---

## 2. Pupil function (`src/pupil.py`)

`PupilSpec` dataclass:
- `grid_size`: 정사각 sampling. 짝수만 허용.
- `na`: numerical aperture (default 0.55).
- `obscuration_ratio`: ε ∈ [0, 1) (default 0.20).
- `wavelength`: λ (default 13.5 nm).
- `zernike`: `{(n, m): coeff_in_waves}` mapping. 비어 있으면 평면파.

**Annular shape**: `P = (rho ≤ 1) ∧ (rho ≥ ε)` where `rho = sqrt(f_x² + f_y²) / (NA / λ)`.

**Aberration**: standard Zernike R_n^|m|(rho) radial polynomials × cos/sin(mθ). Contribution accumulates as OPD W(rho, θ) in waves; phase factor `exp(i · 2π · W)`.

**왜 두 종류의 pupil 함수?**  
`build_pupil(spec)` returns a *normalized* (rho ∈ [-1, 1]) pupil for stand-alone visualization. `aerial._build_aerial_pupil(...)` resamples the same physics on the actual FFT frequency grid of the wafer image — this is what gets multiplied with `FFT(M)`. They share `_wavefront()`.

---

## 3. Mask (`src/mask.py`)

**Kirchhoff thin-mask** (`kirchhoff_mask`):
```
field(x, y) = 1 - pattern(x, y)        # absorber=1 -> field=0
```
Complex output for forward compatibility with phase-shift masks (Phase 4+).

**Pattern generators**:
- `line_space_pattern(grid, pitch_m, duty_cycle, orientation)`
- `pinhole_pattern(grid, radius_m=None)`

**중요한 구현 노트 — 정수 픽셀 양자화**: `pitch_m / pixel_size`를 `int(round(...))`로 양자화한다. 이 fix가 없으면 `(coord * pixel) % pitch` 부동소수점 누적 오차가 큰 grid에서 pattern을 **non-periodic**으로 만들고, 그 결과 FFT spectral leakage가 발생해 sub-resolution pitch에서도 잘못된 high-contrast가 나온다 (실제로 디버깅 중 46/64 periods가 어긋나는 현상 확인). 결과적으로 pitch가 grid 총 길이의 정확한 약수일 때만 깨끗한 sub-resolution 거동이 보장된다. 이 제약은 노트북 sweep에 명시했다 (`nx*pixel = 960 nm` divisor list).

**Out-of-scope (Phase 4에서 추가)**:
- 두꺼운 absorber의 위상 (M3D)
- BF shift, telecentricity, shadowing
- CRA-dependent reflection

---

## 4. Aerial image solver (`src/aerial.py`)

**Hopkins coherent step**:
```
spectrum   = fftshift( fft2(mask_field) )
filtered   = spectrum * P(f_x, f_y)
field_w    = ifft2( ifftshift(filtered) )
intensity  = |field_w|²
```

**Sampling guard**: aerial-plane Nyquist 1/(2·dx_w) must support pupil cutoff NA/λ. 위반 시 `ValueError`. 이 가드는 mask grid 해상도가 부족해 pupil이 잘리는 잘못된 시뮬을 차단한다.

**Normalization (중요한 설계 결정)**: 출력 intensity를 max로 나눠서 [0, 1] 범위로 정규화한다. 단, *bright-field reference* 보다 작은 신호 (즉 DC + 모든 1차 ordersrkfr 모두 차단된 상태 = numerical noise level)는 0으로 floor한다. 이 floor가 없으면 sub-resolution pattern + central obscuration 조합에서 noise가 1.0으로 정규화돼 contrast가 1로 잘못 보고된다 (디버깅 중 발견).

```python
bright_field = (sum(|P|) / N_pixels)²       # DC throughput
noise_floor  = max(bright_field, 1) * 1e-12
if peak > noise_floor: I /= peak
else:                  I = zeros
```

**Metrics**:
- `contrast(line)` — Michelson `(Imax - Imin) / (Imax + Imin)`.
- `nils(line, dx, cd)` — `CD · |∂ ln I / ∂x|` at threshold crossing.
- `cd_from_threshold(line, dx, t)` — pixels above threshold × dx.

---

## 5. 단순화 가정 (명시 — P3 운영 원칙)

| # | 단순화 | 영향 | 어디서 풀 것인가 |
|---|--------|------|-----------------|
| S1 | Single on-axis plane wave (fully coherent) | partial coherence 효과 무시 | Phase 2 (illuminator.py) |
| S2 | Kirchhoff thin-mask | M3D 6 효과 모두 무시 | Phase 4 (mask_3d.py) |
| S3 | Monochromatic 13.5 nm | spectral bandwidth, OOB radiation 무시 | source.py 옵션 (Phase 1+) |
| S4 | Constant multilayer reflectivity (R=1) | angle/polarization-dependent reflectivity 무시 | 미래 확장 |
| S5 | Scalar field (no polarization) | s/p 분리 무시 | Phase 4 보강 |
| S6 | Anamorphic은 픽셀 스케일링만, 광학적 회전·왜곡 없음 | 실제 6-mirror cascade의 wavefront error 무시 | Phase 4+ |
| S7 | Defocus = 0 (flat wafer) | DOF 효과 무시 | Phase 3 (wafer_topo.py) |

---

## 6. 검증 (진행계획서 §4.1 Verification 1:1 매핑)

| 검증 항목 | 테스트 | 결과 |
|-----------|--------|------|
| 단일 pinhole + circular pupil → Airy 형상 | `test_pinhole_psf_radial_structure` | PASS — 중심 peak + 측면 대칭 + 첫 sidelobe < 0.2 |
| 40 nm pitch resolved, 16 nm pitch washed | `test_line_space_resolution_vs_pitch` | PASS — c(40) > 0.3, c(16) ≈ 0 |
| Annular vs solid pupil → sidelobe 변화 | `test_annular_pupil_modifies_sidelobes` | PASS — paper #15 정성 일치 |
| Anamorphic 4×/8× 좌표 매핑 | `test_anamorphic_field_mapping` | PASS — 26×33 mm → 6.5×4.125 mm |
| (보너스) CD 측정 헬퍼 sanity | `test_cd_helper_on_square_signal` | PASS |

```
$ pytest tests/phase1_aerial_image.py -v
========== 5 passed in 0.06s ==========
```

---

## 7. 노트북 (`notebooks/0_first_aerial_image.ipynb`)

5개 섹션:
1. Annular pupil 시각화
2. PSF (solid vs annular)
3. Pitch sweep — contrast & NILS vs pitch (cutoff at λ/NA = 24.5 nm)
4. Anamorphic field-size sanity check
5. End-to-end aerial image (32 nm pitch line/space)

---

## 8. KPI 합격 (PROJECT_OVERVIEW §0.3)

- ✅ **K1** End-to-end (광학 파트만): mask → aerial image 통과
- ✅ **K2** 정성적 회절 재현: pitch sweep에서 cutoff 정확히 24.5 nm

K3 (DOF 정량) 는 Phase 3에서, K4–K6는 후속 Phase에서.

---

## 9. Exit gate (다음 Phase 진입 조건)

- ✅ 5 unit tests PASS (`pytest tests/phase1_aerial_image.py`)
- ✅ 노트북 end-to-end 실행 OK
- ✅ 단순화 가정 7개 명시 (§5)
- ✅ 좌표계 컨벤션 fix 완료 (D5)
- → **Phase 3** (Wafer topography & DOF) 진입 가능
- → 또는 **Phase 5 MVP** (threshold resist) 와 병렬 진행 가능 (계획서 §2.2 Phase 진행 모델 참조)

---

## 10. 알려진 제약 / 메모

- `nx*pixel = grid_total_length` 가 sweep pitch들의 정확한 배수여야 깨끗한 결과. Sub-pixel pitch는 양자화로 인한 duty-cycle 오차가 누적될 수 있음.
- Central obscuration 활성화 (ε > 0) + on-axis source 조합은 dark-field 거동을 보임 — DC 차단으로 fully clear mask도 0 intensity. Phase 2 partial coherence 도입 시 source 분포로 보완됨.
- Aberration은 Zernike (n, m) tuple 기반. Noll index 변환 helper는 Phase 4에서 필요할 때 추가.
- FFT-based imaging의 periodic boundary 가정 → 패턴 가장자리에서 wrap-around artifact 가능. 큰 mask 또는 padding으로 회피 (notebook §5에서는 wide grid 사용).
