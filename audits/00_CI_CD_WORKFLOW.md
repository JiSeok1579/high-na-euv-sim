# CI/CD 게이트 워크플로

> 코드 변경 → 자동 테스트 → 4-역할 감사 → Phase Gate 승인 → 진행
> 모든 변경은 본 워크플로를 통과해야 main에 머지되거나 다음 Phase로 진행된다.

---

## 1. 워크플로 한눈에 보기

```text
┌─────────────────────────────────────────────────────────────┐
│  STAGE 0: 개발자 브랜치에서 코드 변경                        │
│           git checkout -b feature/phaseX-<topic>             │
└─────────────────────┬───────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 1: 자동 테스트 (Local + CI)                           │
│  - pytest tests/                                            │
│  - mypy src/                                                │
│  - ruff check src/                                          │
│  - coverage ≥ 80%                                           │
│  → FAIL 시 STAGE 0으로 복귀                                  │
└─────────────────────┬───────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 2: 자체 감사 체크리스트 (Self-Audit)                  │
│  개발자가 4개 역할 INSTRUCTIONS.md의 체크리스트로            │
│  스스로 점검 → 결과를 PR description에 첨부                  │
└─────────────────────┬───────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 3: 4-역할 감사 (External Audit)                       │
│                                                             │
│  ┌──────────┐ ┌──────────┐ ┌─────────────┐ ┌────────────┐  │
│  │ 데이터   │ │ 물리     │ │ AI/수치      │ │ 시뮬레이션  │  │
│  │ 분석가    │ │ 학자     │ │ 분석가       │ │ 검증자      │  │
│  └────┬─────┘ └────┬─────┘ └──────┬──────┘ └─────┬──────┘  │
│       │            │              │              │         │
│       └────────────┴──────┬───────┴──────────────┘         │
│                           ▼                                 │
│              각자 audit_report.md 작성                       │
│              audits/<role>/reports/ 에 저장                  │
└─────────────────────┬───────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 4: 판정 집계                                          │
│                                                             │
│  모두 PASS                  → STAGE 5 진행                   │
│  PASS + CAUTION (mitig.)    → STAGE 5 조건부 진행            │
│  MAJOR RISK 1개 이상         → 의사결정 회의                  │
│  PHYSICAL VIOLATION 1개     → 차단, STAGE 0 복귀             │
│  UNVERIFIED 1개 이상        → 정보 확보 후 재감사            │
└─────────────────────┬───────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 5: Phase Gate 체크리스트                              │
│  진행계획서 §9.2의 8개 항목 모두 ✅ 확인                     │
└─────────────────────┬───────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 6: 머지 / 진행                                        │
│  - PR 머지 (git)                                             │
│  - AUDIT_LOG.md 업데이트                                     │
│  - PROJECT_OVERVIEW.md §6 산출물 상태 갱신                   │
│  - 다음 Phase 진입 또는 다음 작업 패키지 진입                │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. STAGE별 상세

### STAGE 0 — 개발 (Development)

**브랜치 명명 규약:**
```
feature/phaseX-<short-topic>     (새 기능)
fix/phaseX-<short-topic>          (버그 수정)
audit/<role>-<phase>              (감사 보고서만 추가)
docs/<topic>                      (문서만 변경)
```

**커밋 메시지:**
```
phase1: implement annular pupil function

- Add src/pupil.py with build_pupil()
- Cover: NA, ε_obscuration, Zernike phase
- Reference: paper #19, #15

Refs: #issue-N
```

---

### STAGE 1 — 자동 테스트

**필수 통과 항목:**

| 도구 | 명령 | 합격선 |
|------|------|--------|
| pytest | `pytest tests/` | 100% pass |
| coverage | `pytest --cov=src --cov-report=term-missing` | ≥ 80% |
| mypy (타입 체크) | `mypy src/` | error 0 |
| ruff (린트) | `ruff check src/ tests/` | error 0 |
| numpy doctest | `pytest --doctest-modules src/` | 100% pass |

**CI 설정 예시 (GitHub Actions, 옵션):**
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -e .[dev]
      - run: pytest tests/ --cov=src
      - run: mypy src/
      - run: ruff check src/ tests/
```

---

### STAGE 2 — 자체 감사

개발자는 자신의 변경 사항에 대해 4개 역할 모두의 체크리스트를 1차 통과해야 한다. 한 사람이 작성하더라도 **시각을 명시적으로 분리**해서 본다.

자체 감사 결과는 PR description의 다음 형식으로 첨부:

```markdown
## Self-Audit Summary

| Role | Status | Notes |
|------|--------|-------|
| Data Analyst | ✅ PASS | N/A (코드만 변경) |
| Physics | ✅ PASS | annular pupil의 부호 규약 확인 |
| AI/Numerical | ⚠️ CAUTION | FFT 샘플링 한계 케이스 미테스트 |
| Simulation | ✅ PASS | Phase 1 entry criteria 만족 |
```

---

### STAGE 3 — 4-역할 감사

**감사자 배정:**
- 단독 개발자: 자신이 4개 시각으로 작성. 단, **시간 간격** 두고 작성 (즉시 자기 코드 보고 같은 자리에서 4개 보고서 쓰면 의미 없음). 권장 1일 이상 간격.
- 팀 진행: 가능한 한 다른 사람이 감사

**감사 작성 절차:**
1. `audits/templates/audit_report_TEMPLATE.md` 복사
2. 해당 역할 폴더의 reports/에 저장 (파일명 규약 `README.md §7`)
3. 해당 역할 `INSTRUCTIONS.md` 의 체크리스트 모두 적용
4. 판정 등급 부여 + 근거 명시
5. `AUDIT_LOG.md` 에 한 줄 요약 추가

**감사에 사용하는 정보:**
- 변경된 코드 (PR diff)
- 관련 단위 테스트
- 관련 노트북 결과
- `physics_considerations.md`, 21편 논문, 진행계획서 등 reference

---

### STAGE 4 — 판정 집계

판정 매트릭스:

| 데이터 | 물리 | AI/수치 | 시뮬 | 결과 |
|--------|------|---------|------|------|
| PASS | PASS | PASS | PASS | ✅ STAGE 5 진행 |
| CAUTION | PASS | PASS | PASS | ⚠️ 조건부 진행 + mitigation task 생성 |
| PASS | CAUTION | CAUTION | PASS | ⚠️ 조건부 진행 + 2개 mitigation task |
| 1개 이상 MAJOR RISK | | | | 🛑 의사결정 회의 |
| 1개 이상 PHYSICAL VIOLATION | | | | ❌ 차단, STAGE 0 복귀 |
| 1개 이상 UNVERIFIED | | | | 🔄 정보 확보 후 재감사 |

**조건부 진행 (CAUTION 처리):**
- CAUTION 판정 시 반드시 mitigation task 생성 (TaskCreate)
- mitigation task는 다음 Phase Gate 전까지 처리
- CAUTION이 누적되면 (3개 이상) 그 자체로 STAGE 4 차단

---

### STAGE 5 — Phase Gate

진행계획서 §9.2의 8개 항목 모두 ✅:

```
[ ] Entry criteria 모두 만족했는가
[ ] Work package 모두 구현되었는가
[ ] Deliverable 모두 산출되었는가
[ ] Verification 단위 테스트 모두 통과했는가
[ ] Exit criteria 모두 만족했는가
[ ] 단순화 가정이 코드 주석 + docs/에 모두 기록되었는가
[ ] PROJECT_OVERVIEW.md가 업데이트되었는가
[ ] 다음 Phase의 Entry criteria가 만족 가능한 상태인가
```

---

### STAGE 6 — 머지 / 진행

**머지 후 의무 작업:**
1. `audits/AUDIT_LOG.md` 업데이트 (감사 결과 한 줄 요약)
2. `PROJECT_OVERVIEW.md §6` 산출물 상태 갱신 (✅로 변경)
3. 진행계획서 `진행계획서.md §13` 변경 이력 추가 (Phase 단위 변경 시)
4. CHANGELOG.md (옵션) 업데이트
5. 다음 Phase 진입 시 `진행계획서.md §4.X`의 Entry criteria 확인

---

## 3. 단독 개발자용 간소화 모드

소규모 변경 (1개 함수 추가, 노트북 수정 등)에는 다음 간소화 적용 가능:

| 변경 규모 | 필요 감사 |
|-----------|----------|
| 노트북 / 문서만 | 시뮬레이션 감사만 (PASS 가정) |
| 1개 함수 / 1개 모듈 | 관련 1–2개 역할만 |
| Phase 내부 모듈 추가 | 관련 2–3개 역할 |
| **Phase Gate 통과 시** | **반드시 4개 역할 모두** |

> Phase Gate 시점에는 간소화 금지. 4개 역할 정식 감사 보고서 모두 필요.

---

## 4. 감사 갈등 해결

여러 역할의 판정이 모순될 때:

```
물리 PASS, AI/수치 MAJOR RISK
→ 물리적으로는 맞지만 수치 구현이 깨지는 경우
→ 우선순위: 수치 분석가 의견 채택 (PHYSICAL VIOLATION 가능성)
→ 회의에서 mitigation 결정

데이터 CAUTION (입력 분포 특이), 시뮬 PASS (결과는 문제 없어 보임)
→ EDA 충분히 했는지 재확인
→ 입력 분포가 OOD인 경우 fallback 정책 필요
→ 우선순위: 데이터 분석가 의견 + 시뮬레이션의 OOD 처리 추가 task
```

---

## 5. 감사 자동화 후보

다음은 자동화 가능한 감사 항목 (pytest 또는 별도 스크립트):

| 항목 | 자동화 가능 |
|------|------------|
| FFT 샘플링 (Nyquist) | ✅ 자동 |
| 단위 일관성 (m/nm/rad 혼용) | ✅ pint 라이브러리 |
| 타입 체크 (mypy) | ✅ 자동 |
| Coverage | ✅ 자동 |
| 부호 규약 (defocus z 방향) | ⚠️ 부분 자동 (assert) |
| 보존법칙 (mirror chain throughput) | ⚠️ 부분 자동 (assert) |
| 좌표계 일관성 | ❌ 수동 |
| 결과 해석의 정성 일관성 | ❌ 수동 |
| ablation 충분성 | ❌ 수동 |

장기적으로 자동화 가능한 항목들은 `tests/audits/` 서브폴더에 별도 자동 테스트로 추가한다.

---

## 6. 응급 핫픽스 (Hotfix) 절차

긴급 수정이 필요한 경우 (예: 시연 직전에 발견된 결정적 버그):

1. `hotfix/` 브랜치에서 작업
2. STAGE 1 (자동 테스트) + STAGE 3 의 **물리 + 시뮬레이션 감사 2개만** 빠르게 진행
3. 머지 후 **48시간 내** 4-역할 정식 감사 사후 작성
4. `AUDIT_LOG.md`에 "[HOTFIX]" 태그로 기록

---

## 7. 변경 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| v1.0 | 2026-04-25 | 초기 작성 |
