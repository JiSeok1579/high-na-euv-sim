# QUICK REFERENCE — 21편 1줄 카드 (Phase별)

> 각 카드: **#번호 (★OA표시) | 짧은제목 (연도) | 1줄 핵심 | 시뮬레이터 적용**
> 자세한 내용은 각 `XX_*.md` 파일과 `KNOWLEDGE.md` 참고

---

## 광원 (Source / LPP)

- **#18 ★OA** — Tin plasma physics review (Versolato 2019)
  - 핵심: Sn⁸⁺~Sn¹⁴⁺ 4d→4f UTA가 13.5 nm in-band 형성 + ps~μs 스케일 droplet/plasma 동역학
  - 적용: monochromatic point source 단순화의 정당성 + Δλ/λ ≈ 2% bandwidth 옵션 근거

- **#8** — EUV spectrum of high-power LPP source (2025, paywall)
  - 핵심: in-band 13.5 nm + out-of-band (DUV/IR) radiation 측정
  - 적용: 정밀 모드에서 OOB radiation을 별도 dose 항으로 추가

---

## Phase 1 — Projection Optics (Fourier optics)

- **#19** — Anamorphic high-NA EUV optics (Migura 2015, paywall)
  - 핵심: NA > 0.5 + full-field 4×는 mask shadowing 때문에 불가 → **4× scan / 8× cross-scan anamorphic + half-field 26×16.5 mm**
  - 적용: **mask → wafer 좌표 변환 (비대칭 scale)** — Phase 1의 출발점

- **#15 ★free** — Performance of optics with central obscuration (Beck technote)
  - 핵심: obscuration ratio ε에 따라 PSF first sidelobe ↑, MTF 중간대역 ↓, cutoff freq 보존
  - 적용: **annular pupil function** `P = (r ≤ NA) ∧ (r ≥ NA·ε)`

- **#3 ★OA** — In-Line projector for EUV (Shintake 2025, arXiv)
  - 핵심: 4-mirror coaxial + central obscuration → CRA = 0 → M3D 효과 근본 제거 (alternative)
  - 적용: **CRA = 0 옵션을 두면 M3D ablation study가 가능**

---

## Phase 2 — Illuminator (partial coherence / source shape)

- **#16 ★OA** — Deep RL relay & facet matching (Li 2025 Optics Express)
  - 핵심: NA 0.55 anamorphic illuminator를 one-mirror off-axis relay + RL facet 매칭으로 → 26.24% 효율, ~99% uniformity
  - 적용: source shape를 **field facet × pupil facet 조합**으로 모델링 (단순 σ 파라미터는 1차 근사)

- **#5 ★free** — 0.55 NA Imaging & Overlay (van Schoot 2024)
  - 핵심: ASML EXE-series imaging + overlay 산업 baseline (8 nm hp 시연)
  - 적용: σ_in/σ_out, illumination mode 기본값의 ground truth

- **#11 ★free** — Moore's Law: First Imaging (ASML/imec 2024)
  - 핵심: EXE:5000에서 10 nm 라인 / 20 nm pitch 인쇄 성공 + High-NA roadmap
  - 적용: 시뮬레이터의 첫 reference target 패턴 (10 nm line / 20 nm pitch)

---

## Phase 3 — Wafer Topography & DOF

- **#14** — High-NA DOF challenge & LCDU (van Setten 2025, paywall)
  - 핵심: 0.55 NA에서 LCDU 18–42% 향상 (vs 0.33 NA, 29 nm pitch hex) + PMWO + micro focus-drilling으로 좁은 DOF 대응
  - 적용: **DOF = k₂·λ/NA²의 정량 검증 데이터** + focus drilling 모델

---

## Phase 4 — Reflective Mask 3D (M3D)

- **#12** — M3D Characterization & Mitigation (Erdmann 2017, partial)
  - 핵심: M3D **6대 현상** — asymmetric shadowing, H/V CD bias, telecentricity, contrast loss, BF shift, secondary images
  - 적용: **Phase 4 단위 테스트 체크리스트의 baseline**

- **#7 ★free** — Novel high-k mask, M3D & focus (EUVL 2023)
  - 핵심: n ≈ 1, high-k absorber → BF shift 최소화, telecentricity 향상
  - 적용: absorber n, k를 시뮬레이션 입력 파라미터로 노출

- **#17** — Best focus shift via optical constant screening (2025, paywall)
  - 핵심: high-k (Ni 등) + low-n attPSM (RuTa, PtMo, PtTe) 후보 비교, NILS/MEEF/BF range 정량
  - 적용: **NILS, MEEF, BF range를 mask 모듈 출력 메트릭으로 정의**

- **#2** — SHARP actinic microscope (Goldberg 2013, preprint)
  - 핵심: synchrotron 13.5 nm actinic mask 마이크로스코프 (장비)
  - 적용: 직접 구현 X. **rigorous M3D 시뮬레이션 출력의 ground truth 비교 데이터** 출처

---

## Phase 5 — Photoresist (threshold → stochastic)

### Level 1 — Chemical blur

- **#4 ★free** — PSCAR / CAR fundamentals (Tagawa 2017)
  - 핵심: CAR 메커니즘 (acid generation → diffusion → deprotection) + PSCAR가 RLS trade-off + photon shot noise를 동시 완화
  - 적용: **aerial image에 Gaussian blur (σ ≈ 2-4 nm) 적용**으로 chemical blur 1차 모델

### Level 2 — Depth-resolved absorption

- **#20** — EUV photon absorption distribution at 0.55 NA (imec 2025, paywall)
  - 핵심: resist 두께 방향 absorption 비대칭 (gradient extinction) → top vs bottom dose 불균형
  - 적용: aerial image를 **2D `I(x,y)` → 3D `I(x,y,z)`** 로 확장

- **#13** — Resist SWA / SMO for resist profile (Dhagat 2025, paywall) **(매핑 확인 필요)**
  - 핵심: resist의 높은 EUV 흡수 → sloped SWA → DOF 손해. micro focus-drilling으로 SWA 균질화
  - 적용: **focus map을 z slice별로 다르게 두는 옵션 (focus drilling)**

### Level 3 — Full stochastic

- **#1 ★OA** — Material vs optical stochastic LWR (Park 2025 Sci. Reports)
  - 핵심: LWR을 optical / material로 분리 → 두 효과는 **partial compensation** (단순 합 아님). dose-dependent decomposition 필요
  - 적용: **`σ²_LWR = σ²_optical(dose, CD) + σ²_material(dose, CD) + cross`** 분리

- **#21** — Statistics of EUV nanopatterns (Fukuda 2025, paywall)
  - 핵심: 4단계 chained stochastic Monte Carlo (photon → secondary electron → acid → deprotection → dissolution) + binomial / beta-binomial / mixed Bernoulli 합성
  - 적용: **Markov chain Monte Carlo** 구조의 full stochastic resist 모델 reference

---

## Phase 6 — Correction / Optimization (SMO / PMWO / RL)

### 학계 (구현 가이드)

- **#9 ★OA** — Fast SMO for high-NA EUV (Li, Dong 2024 OEA) **★★ 가장 직접 구현 가이드**
  - 핵심: Fast High-NA imaging model (M3D + anamorphic 포함) + gradient-based mask + compressive-sensing source + MRC step
  - 적용: **이 프로젝트의 SMO 모듈 baseline 알고리즘** — 수식과 알고리즘을 OA로 자유 인용 가능

### 산업 (PMWO 시리즈)

- **#10** — PMWO: LWR + overlay (ASML 2025, paywall)
  - 핵심: pupil + mask + wavefront 동시 최적화, contrast fading 보정 → LWR 감소
  - 적용: 목적함수에 LWR 항 포함하는 PMWO framework

- **#6** — PMWO for High-NA DRAM (Samsung+ASML 2025, paywall)
  - 핵심: PMWO를 DRAM 2D layout (line/space 아님)에 적용 → contrast 향상, dose 절감, LCDU 개선
  - 적용: 2D layout에서의 SMO 평가 메트릭 (LCDU, EPE) 정의

### 대안 — Deep RL

- **#16 ★OA** — Deep RL illumination relay (다시 등장, Phase 2와 6의 연결)
  - 핵심: source 변수 최적화에 RL 적용
  - 적용: gradient/CS-based SMO와 비교 가능한 alternative

---

## 분야별 빠른 lookup 표

| 분야 | 핵심 (★OA 우선) |
|------|-----------------|
| **광학 시스템** | #19, #15, #3, #14 |
| **광원** | #18 ★OA, #8 |
| **조명계** | #16 ★OA, #5 ★free |
| **마스크 3D** | #12, #7 ★free, #17, #2 |
| **레지스트** | #4 ★free, #1 ★OA, #20, #13, #21 |
| **SMO/PMWO** | #9 ★OA, #10, #6 |
| **첫 imaging 결과** | #11 ★free, #5 ★free |

---

## 가장 먼저 받아야 할 무료 11편 (★OA / ★free)

체크박스로 다운로드 진행 추적:

- [ ] **#1** Material vs optical stochastic LWR (Nature)
- [ ] **#2** SHARP (LBNL preprint)
- [ ] **#3** In-Line Projector (arXiv)
- [ ] **#4** PSCAR/CAR (EUVL Workshop 2017)
- [ ] **#5** 0.55 NA Imaging & Overlay (EUVL 2024)
- [ ] **#7** High-k mask (EUVL 2023)
- [ ] **#9** Fast SMO (Opto-Electronic Advances)
- [ ] **#11** Moore's Law First Imaging (EUVL 2024)
- [ ] **#12** M3D Characterization (LBL slides)
- [ ] **#15** Central Obscuration (Beck technote)
- [ ] **#16** Deep RL Relay (Optics Express)
- [ ] **#18** Tin plasma review (ARCNL OA)

---

## 첫 1주 학습 권장 순서

1. **#19** Migura 2015 — anamorphic 좌표계 출발점 (paywall, 학교/회사 라이브러리 필요)
2. **#15** central obscuration technote (★free) — annular pupil 정량 이해
3. **#9** Li 2024 OEA (★OA) — fast imaging + SMO 알고리즘 의사코드 추출
4. **#12** Erdmann 2017 review — M3D 6 효과 체크리스트
5. **#11** ASML 첫 imaging 결과 (★free) — 시뮬레이터 target 수치 확정

→ 이 5편만 보면 Phase 1 + Phase 4의 frame이 잡힘
