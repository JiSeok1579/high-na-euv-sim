# INST-001 — Study 목적 명문화 + 엄격성 완화 + 3D 시각화 확인

```
지시서 ID:    INST-001
발신:         Claude (외부 감사자, REVIEWER_DIRECTIVE v2.1)
수신:         코드 작성자 (Codex)
작성일:       2026-04-27
근거:         사용자 명시 지시 — "study로 한다는것은 실제랑 아예똑같은
              엄격한 구조를 유지할필요가없다는 이야기. 완화할것은 완화하여
              일단 구현하는게 목적"
관련 감사:    EXT-AUD-005 §4.1 P0 (MT-015) + 사용자 추가 명시
우선순위:     P0 — 다음 PR 안에 처리
```

---

## 0. 본 지시서의 핵심 메시지 (한 단락)

본 프로젝트는 산업 배포·논문 제출용이 아니라 **스터디 프로젝트**다. 데이터·논문 출처가 일관되지 않아 산업 정량 검증은 어차피 불가능하므로, **엄격함을 추구하다가 구현이 막히는 패턴**을 의도적으로 피해야 한다. **"일단 구현 → 3D로 결과 확인 → 미세조정으로 거동 학습"** 이 1차 목표이고, 정밀화·정량 검증은 학습 후 자연 도출되는 보너스다. 본 지시서는 이 인식을 코드·문서·감사 기준에 명문화한다.

---

## 1. 사용자 의도 풀이 (3가지)

### 의도 1 — Study purpose 명문화
- 현재 어디에도 "study purpose" 명시 없음 (`grep` 결과 0건)
- 이대로 두면 외부 감사가 산업 grade 기준으로 계속 P0/P1 발행 → coder fatigue
- **해결**: README, PROJECT_OVERVIEW, 진행계획서에 명시 추가

### 의도 2 — 엄격성 완화
- "실제랑 똑같은 엄격한 구조 유지 X" — 산업 환경의 정확한 1:1 재현이 목표가 아님
- 현재 외부 감사 시스템이 산업 grade 검증 기준으로 작동 중 → 완화 필요
- **해결**: 어떤 항목을 완화할 수 있고 어떤 항목은 유지해야 하는지 명시

### 의도 3 — 일단 구현 → 학습
- "일단 구현하는게 목적" + "처음에 구현하고자했던 대로 진행"
- 진행계획서 §1.2 의 "재현 / 탐색 / 학습 / 공유" 4목적에서 **"학습"** 이 1차
- **해결**: 4목적의 우선순위 명시 (학습 > 공유 > 탐색 > 재현)

---

## 2. 현재 폴더 점검 결과

### 2.1 ✅ 잘 진행 중인 것

| 항목 | 상태 |
|------|------|
| Phase 1 (Fourier optics MVP) | ✅ 완료 |
| Phase 3 (DOF + k₂ fitting) | ✅ KPI K3 100% |
| Phase 4 Part 04 (Mask 3D 일부) | ✅ 진행 중 |
| Phase 5 (4-level resist) | ✅ 완료 (KPI K1 진정 100%, K6 70%) |
| 64/64 tests PASS | ✅ |
| Rebrand (Digital Twin → Simulator) | ✅ 95% (12개 파일 전부 완료) |

### 2.2 ★ 3D 시각화 진행 상태 — **YES, 진행 중**

```
notebooks/
├── 3d_focus_stack.ipynb        (3.2KB, 4 cells, 2 with 3D plot)  ← Apr 27 신규
├── 3d_pupil_wavefront.ipynb    (1.9KB, 3 cells, 2 with 3D plot)  ← Apr 27 신규
├── 3d_resist_depth.ipynb       (2.6KB, 4 cells, 2 with 3D plot)  ← Apr 27 신규
└── (기존 2D) 0_first_aerial_image, 4a_threshold_resist, 4b_resist_levels, 3_M3D_effects
```

- ★ **Tier 1 (matplotlib 3D) 이미 도입됨** — EXT-AUD-005 권고 반영
- 각 노트북이 작은 MVP 단위 (2-4 cells)로 시작 — 좋은 패턴
- 다음 단계: 셀 확장 (parameter sweep, 인터랙티브 슬라이더)

### 2.3 ⚠️ 미완 / 갭

| 항목 | 갭 |
|------|-----|
| **워크스페이스 폴더명** | `~/Desktop/High-NA EUV Lithography Digital Twin/` ← rename 필요 |
| **"Study purpose" 명시** | grep 결과 0건 ★ |
| **엄격성 완화 정책** | 어디에도 명문화되지 않음 |
| **외부 감사 기준** | 산업 grade 적용 중 → study grade 로 재조정 필요 |

---

## 3. Task 목록 (코드 작성자 이행)

### Task 1 (P0) — `README.md` 첫 부분에 Study Purpose 섹션 추가

**위치**: `README.md` 의 1줄 description 다음, "Quick Start" 앞.

**삽입할 내용**:

```markdown
## Study Purpose / 스터디 목적

This is a **study-purpose simulator**, not a paper, report, or industry
deployment tool. Goals:

1. **Build** a working simulation of 0.55 NA EUV lithography
2. **Visualize** results in 3D (focus stack, pupil wavefront, resist depth)
3. **Understand qualitatively**:
   - the structural pipeline (source → mask → optics → wafer → resist)
   - what a "good result" looks like at each stage
   - which input parameters can be fine-tuned and how the output responds

**This is NOT**:
- Paper or report writing
- Real-equipment 1:1 replication or reverse engineering
- Industry-grade quantitative validation
  (data and paper sources are inconsistent → strict validation is out of scope)

본 프로젝트는 **스터디 목적의 시뮬레이터**입니다. 데이터·논문 출처가
일관되지 않으므로 정량적 산업 검증은 범위 밖이며, 다음을 정성적으로 학습:

1. 시뮬레이션을 만들어서 작동시키기 (Build)
2. 결과를 3D로 시각화하여 구조·흐름 보기 (Visualize)
3. 어떤 결과가 "좋은 것"인지 정성 파악 + 어떤 입력을 미세조정하면
   출력이 어떻게 바뀌는지 학습 (Understand & Fine-tune)

**엄격한 산업 정량 검증은 추구하지 않습니다.** 일단 구현 → 결과 확인
→ 미세조정 → 활용 학습이 핵심.
```

**작업량**: 10분

---

### Task 2 (P0) — `PROJECT_OVERVIEW.md §1.2` 갱신 (4 목적 우선순위 명시)

**현재 §1.2 "이 프로젝트가 추구하는 것"** 이 3개 bullet 으로만 있음. 다음으로 교체:

```markdown
### 이 프로젝트가 추구하는 것 — 4 목적의 우선순위

본 프로젝트는 **스터디 목적**입니다. 4가지 활동의 우선순위는:

1. **학습 (Understand)** ★ 1차 — 각 Phase의 의미·흐름·"좋은 결과 기준"
   을 정성적으로 파악
2. **시각화 (Visualize)** ★ 1차 — 3D notebook으로 결과를 입체적으로 확인
3. **탐색 (Explore)** — NA, σ, dose, focus 등 입력 변수 sweep으로
   거동 관찰
4. **공유 (Share)** — 21편 논문의 핵심 거동을 코드로 명시화 (정성 일치)

**5번째 목적이 아닌 것**: 산업 grade 정량 검증, 실제 장비 1:1 재현.
데이터·논문 출처가 제각각이라 환경 통일 자체가 불가능하므로 추구 X.

### 운영 원칙: 일단 구현 우선

엄격한 검증으로 진척이 막히면 의도적으로 단순화. 4중 기록 미달, mypy
strict 미적용, depth absorption paper 정량 비교 부재 등은 **study-grade
에서는 P3 이하 backlog**로 둔다 (P0/P1 발행하지 않음).
```

**작업량**: 15분

---

### Task 3 (P0) — `진행계획서.md §1.2 목적` 갱신 + §0.3 KPI 합격선 완화

**§1.2 목적**: 위 PROJECT_OVERVIEW와 동일한 우선순위 표 적용.

**§0.3 KPI 표 갱신** — 현재 정량 합격선을 정성 합격선으로 완화:

| 지표 | 기존 합격선 | **신규 합격선 (study-grade)** |
|------|-------------|-------------------------------|
| K1 End-to-end | Phase 1+3+5 MVP 통과 | ✓ 유지 (이미 합격) |
| K2 회절 정성 | paper 11 정성 패턴 | ✓ 유지 (이미 합격) |
| K3 DOF 정량 | 오차 ≤ 30% | **정성 합격: k₂ 식 형태 일치 + 단조성** (정량 30%는 stretch goal) |
| K4 M3D 6 효과 | 6/6 정성 통과 | ✓ 유지 (study-grade 와 일치) |
| K5 SMO 수렴 | 1 layout 수렴 | ✓ 유지 |
| K6 Stochastic LWR | paper 1 dose-CD 정성 재현 | ✓ 유지 (이미 70% 도달) |

**§13 v1.5 entry 추가**:
```
| v1.5 | 2026-04-27 | Study purpose 명문화 + KPI 합격선 완화 + workspace rename | Codex |
```

**작업량**: 20분

---

### Task 4 (P0) — 워크스페이스 폴더 rename (수동)

```bash
# 사용자 직접 실행:
cd ~/Desktop
mv "High-NA EUV Lithography Digital Twin" "High-NA EUV Lithography Simulator"

# git 작업 폴더 다시 열기:
cd "High-NA EUV Lithography Simulator"
git status   # 정상 작동 확인
```

**주의**:
- macOS Spotlight 인덱스 자동 재생성됨
- Cowork 모드는 새 폴더 path를 다시 선택해야 함
- 기존 git remote 그대로 작동 (URL 변경 없음 — repo 이름은 이미 `high-na-euv-sim`)

**작업량**: 5분

---

### Task 5 (P1) — 3D 시각화 셀 확장 (이미 도입된 3개 노트북)

**현재 상태**:
- `3d_focus_stack.ipynb`: 4 cells (1 MD + 3 code, 2 with 3D)
- `3d_pupil_wavefront.ipynb`: 3 cells (1 MD + 2 code, 2 with 3D)
- `3d_resist_depth.ipynb`: 4 cells (1 MD + 3 code, 2 with 3D)

**확장 권고 (각 노트북에 추가)**:

#### 3d_focus_stack.ipynb 추가 셀
```python
# Sweep cell — defocus를 -100 ~ +100 nm 로 sweep, 3D volume
defocus_values = np.linspace(-100e-9, 100e-9, 21)
# focus_stack_contrast() 호출 + 3D plot
# x축 = x [nm], y축 = defocus [nm], z축 = contrast
```

#### 3d_pupil_wavefront.ipynb 추가 셀
```python
# Zernike coefficient 변경 시 wavefront 변화 시각화
# (n, m) = (2, 0) defocus, (2, 2) astigmatism, (3, 1) coma 등
# subplot(2, 3) 으로 6 aberration 비교
```

#### 3d_resist_depth.ipynb 추가 셀
```python
# Different absorption coefficients → 3D dose volume 비교
# 좋은 result vs 나쁜 result 시각적 대비
```

**작업량**: 1-2시간 (3 노트북 × 30분)

**효과**: 사용자가 "어떤 결과가 좋은지", "미세조정이 어떻게 작동하는지" 시각적으로 학습 가능 — 본 프로젝트 study purpose 의 핵심 산출물.

---

### Task 6 (P1) — `docs/study_grade_relaxation.md` 신규 작성

신규 문서로 "어떤 엄격성을 완화하고 어떤 것은 유지하는지" 명시.

```markdown
# Study-Grade Relaxation Policy

## 1. 완화 (Relaxed — study-grade에서는 P3 이하)
- 단순화 4중 기록률 88% (drift) — 정상, 100% 추구 X
- mypy strict 미적용 — 정상
- CONTRIBUTING.md 부재 — 정상 (외부 contributor 가정 X)
- Depth absorption paper #20 정량 비교 부재 — 정상
- Industry-grade quantitative GroundTruth 부재 — 정상
- KPI K3 정량 30% 합격선 미달 — 정상 (정성 합격으로 충분)
- `_validate_*` 코드 중복 — 정상 (성능 영향 없음)

## 2. 유지 (Maintained — study에서도 P0/P1)
- ★ Test pass rate 100% — 깨진 코드는 학습 도구가 못 됨
- ★ 부호 컨벤션 (D5) — 한 번 깨지면 모든 결과 무효
- ★ Phase Gate 8 요소 (entry/exit) — 학습 트래킹의 기본
- ★ AUDIT_LOG 정직성 — 학습 진척의 trace
- ★ KPI K1, K2 합격 (정성) — 동작 보장
- ★ 단위 일관성 (m, nm, rad) — 학습자가 헷갈리면 잘못 학습
- ★ Reproducibility (seed) — 같은 입력 → 같은 결과

## 3. 의사결정 원칙
- 엄격함이 학습을 방해하면 → 완화
- 엄격함이 학습을 보호하면 → 유지
- 애매하면 → 일단 구현, 학습 결과 보고 사후 결정
```

**작업량**: 30분

---

### Task 7 (P1) — `.github/CLAUDE.md` 의 외부 감사 기준 study-grade 로 재조정

**갱신 내용**:

```markdown
## Audit Grade — Study Purpose Acknowledgment

본 프로젝트는 **스터디 목적**이다 (REVIEWER_DIRECTIVE.md, README §Study Purpose).
외부 감사 진행 시:

### Study-grade 에서 P0 으로 발행 가능한 항목 (제한)
- Test pass rate < 100% (코드 깨짐)
- 부호 컨벤션 (D5) 위반
- 단위 혼용 (m vs nm 등)
- AUDIT_LOG 부정직 (closure 미반영)
- 메타 sync drift (CLAUDE.md ↔ REVIEWER_DIRECTIVE)

### Study-grade 에서 P0 으로 발행하지 않는 항목 (완화)
- 단순화 4중 기록 미달 (88% → 80% 까지 OK)
- mypy strict 미적용
- Industry-grade 정량 검증 부재
- Paper #20/#21 정량 비교 부재
- CONTRIBUTING.md 부재
- 코드 중복 (`_validate_*` 등)

이 완화 적용 후에도 study purpose에 핵심적인 학습 가치는 유지.
```

**작업량**: 20분

---

### Task 8 (P2 옵션) — 외부 감사 보고서들의 P0/P1 재분류 (소급)

본 정책 발효 후, EXT-AUD-001~005 의 P0/P1 권고 중 **study-grade 에서는 P3 이하** 인 것들을 명시적으로 표기 (재할당). 미래 감사에서는 본 정책 적용.

**예시**: EXT-AUD-005 의 MT-019, MT-020, MT-021 모두 P2 → P3 또는 backlog로 재분류 가능.

**작업량**: 30분 (옵션, 즉시 안 해도 OK)

---

## 4. 권장 PR 흐름

### PR 1 (즉시) — `chore-update: declare study purpose and relax audit grade`

포함 내용:
- Task 1: README Study Purpose 섹션
- Task 2: PROJECT_OVERVIEW §1.2 갱신
- Task 3: 진행계획서 §1.2 + §0.3 + §13
- Task 4: workspace rename (사용자 manual 후 git 정상 확인)
- Task 6: `docs/study_grade_relaxation.md` 신규
- Task 7: `.github/CLAUDE.md` study-grade 추가

PR title 후보: `chore-update: declare study purpose and relax audit grade`

작업량 합계: ~1.5시간

### PR 2 (PR 1 머지 후) — `viz-add: expand 3d notebooks for parameter sweeps`

포함 내용:
- Task 5: 3개 3D 노트북 셀 확장

작업량: 1-2시간

---

## 5. 외부 감사 영향 — Study-grade 재조정 후 예상

### 위험 지수 변화 (예상)

| 등급 | 현재 | Study-grade 적용 후 |
|------|------|---------------------|
| P0 | 1 (CLAUDE.md sync — 본 PR에 포함) | 0 |
| P1 | 3 | 1-2 (Task 5 만 P1, 나머지 P3) |
| P2 | 9 | 3-4 |
| P3 | 5 | 11-12 (재분류) |
| **가중 합계** | **23.5** | **~9** (-62%) |

### 다음 외부 감사 (EXT-AUD-006) 의 톤 변화
- 현재 (산업 grade): "P0 1건 + P1 3건 + ..."
- 미래 (study grade): "Study purpose 충실. KPI 학습 진척 양호. P0/P1 없음."

### 코드 작성자 부담 감소
- "deferred 누적" 패턴 사라짐 (mypy strict, CONTRIBUTING 등이 P3로 자연 정리)
- 학습 진척 자체에 집중 가능

---

## 6. 본 지시서 자체의 용도

본 INST-001 은:
- ✅ MD 파일로 보관 (`docs/INST-001_study_purpose_relaxation.md`)
- ✅ 다음 PR description에 link
- ✅ EXT-AUD-006 의 follow-up 추적 source
- ✅ 향후 비슷한 갈등 ("엄격함 vs 학습 진척") 발생 시 reference

---

## 7. 한 페이지 요약 (cheat sheet)

```
═══════════════════════════════════════════════════════════════
  INST-001 — Study Purpose 명문화 + 엄격성 완화 + 3D 확인
═══════════════════════════════════════════════════════════════

3D 시각화 진행 상태:
  ✅ Tier 1 도입 완료 (matplotlib 3D)
  ✅ 3개 노트북 신규 (focus_stack, pupil_wavefront, resist_depth)
  → Task 5: 셀 확장 (parameter sweep)

코드 작성자 Task (PR 1 즉시):
  Task 1: README Study Purpose 섹션 (10분)
  Task 2: PROJECT_OVERVIEW §1.2 (15분)
  Task 3: 진행계획서 §1.2 + §0.3 + §13 (20분)
  Task 4: workspace rename (사용자 manual, 5분)
  Task 6: docs/study_grade_relaxation.md 신규 (30분)
  Task 7: .github/CLAUDE.md study-grade 추가 (20분)
  → 합계 ~1.5시간

코드 작성자 Task (PR 2 후속):
  Task 5: 3D 노트북 셀 확장 (1-2시간)

원칙 (한 줄):
  엄격함이 학습을 방해 → 완화. 엄격함이 학습을 보호 → 유지.

이미 합격한 KPI:
  K1 (end-to-end), K2 (회절 정성), K3 (50%→study에서 합격),
  K6 (70%, study에서 진척으로 충분)

다음 외부 감사 (EXT-AUD-006) 시점:
  본 PR 처리 후 자동 트리거. Study-grade 적용 첫 사례.
═══════════════════════════════════════════════════════════════
```
