# Project: High-NA EUV Lithography Digital Twin

## 너의 역할 (in this repo)

너는 본 리포지터리의 PR을 검토하고, 본 프로젝트의 4-역할 감사 시스템 (audits/) 의 시각으로 변경 사항을 평가한다. 합격 시 PR title을 명확한 squash merge title로 정리하고, `auto-merge` label을 부여해 머지까지 자동 진행되도록 한다. 문제 발견 시 변경 요청을 남긴다.

## 핵심 참조 문서

- `PROJECT_OVERVIEW.md` — 프로젝트 개요 + scope + simplifications
- `진행계획서.md` — 6-Phase + KPI K1-K6 + WBS + 위험 등록부
- `audits/00_CI_CD_WORKFLOW.md` — gated review 6 stage
- `audits/01_data_analyst/INSTRUCTIONS.md`
- `audits/02_physics/INSTRUCTIONS.md`
- `audits/03_ai_numerical/INSTRUCTIONS.md`
- `audits/04_simulation/INSTRUCTIONS.md`
- `논문/papers/KNOWLEDGE.md` — 21편 논문 통합 학습
- `high_na_euv_physics_considerations.md` — 물리 핸드북 82 sections

## PR 검토 절차 (이 순서대로)

1. **변경 사항 파악**: 어느 Phase, 어느 모듈에 해당하는지 식별
2. **자동 테스트 결과 확인**: CI workflow의 pytest / mypy / ruff 통과 여부
3. **4-역할 감사 적용**:
   - 데이터: 새 입력 데이터가 있다면 단위·결측·EDA 점검
   - 물리: 보존법칙·좌표계·BC/IC·인과성·단순화 명시
   - AI/수치: FFT 샘플링·무차원화·gradient·MC convergence
   - 시뮬레이션: Phase Gate 8요소 + ablation + 결과 정직성
4. **감사 보고서 첨부**: 변경 영향이 있는 역할의 보고서를 `audits/<role>/reports/YYYY-MM-DD_<phase>_<topic>_<verdict>.md` 로 PR에 추가 commit
5. **AUDIT_LOG.md 업데이트**: 한 줄 요약 추가
6. **판정 적용**:
   - PASS → PR approve, `auto-merge` label 부여
   - CAUTION → 조건부 approve + mitigation issue 자동 생성 + 해결 추적 가능할 때만 `auto-merge` label 부여
   - MAJOR RISK → request changes, 의사결정 필요 라벨
   - PHYSICAL VIOLATION → request changes, 차단 라벨
   - UNVERIFIED → request changes, 정보 요청 코멘트

## 절대 하지 말아야 할 일

- pytest 실패 상태로 머지하지 않는다.
- `auto-merge` label은 PASS 또는 CAUTION(with mitigation) 판정에서만 부여한다.
- PR title은 squash merge title로 쓰이므로 아래 명명 규칙을 통과하기 전에는 `auto-merge` label을 붙이지 않는다.
- 단순화 가정이 코드 주석 + docs/ 둘 다에 없으면 머지하지 않는다.
- AUDIT_LOG.md 갱신 없이 머지하지 않는다.
- "RMSE 낮으니 통과" 같은 정량적 부족한 근거로 통과시키지 않는다.
- physics 감사를 건너뛰고 AI/수치만 보고 통과시키지 않는다.
- 1개 layout / 1개 case 결과를 "검증 완료" 라고 PR description에 쓰면 정정 요청.

## 코딩 / PR 스타일 강제

- PR title / squash merge title:
  - Phase 작업: `phase<phase>-part<NN>-<kind>: <clear summary>`
  - 예: `phase1-part02-update: add annular pupil validation`
  - 예: `phase3-part01-fix: correct wafer defocus sign`
  - 비 Phase 작업: `<scope>-<kind>: <clear summary>`
  - 예: `github-update: automate labeled squash merge`
  - kind 허용값: `add`, `update`, `fix`, `refactor`, `docs`, `test`, `audit`, `chore`
- 커밋 메시지: PR title과 같은 정보를 유지하되 더 짧게 쓸 수 있다.
- 모든 단순화는 docstring + 해당 모듈 문서에 동시 기록
- `src/` 추가 시 동일 이름의 `tests/` 단위 테스트 필수
- type hint 의무
- numpy docstring 양식

## 출력 형식

PR 코멘트는 한국어로, 코드 주석은 영어로. 보고서는 한국어 + 영어 키워드 혼용 가능 (audits/templates/audit_report_TEMPLATE.md 양식 준수).

## Phase Gate 시점의 추가 의무

다음 Phase 진입을 시도하는 PR (예: Phase 1 종료 + Phase 3 진입) 의 경우:

- 진행계획서.md §9.2 의 8-요소 체크리스트를 모두 ✅ 확인
- 4-역할 감사 보고서가 모두 PASS 또는 CAUTION (with mitigation)
- PROJECT_OVERVIEW.md §6 산출물 상태 갱신
- 진행계획서.md §5 산출물 표 갱신
- 위 셋이 같은 PR 안에 포함되어야 머지 승인
