## PR title / squash merge title

형식:
- Phase 작업: `phase<phase>-part<NN>-<kind>: <clear summary>`
- 비 Phase 작업: `<scope>-<kind>: <clear summary>`

예:
- `phase1-part02-update: add annular pupil validation`
- `phase3-part01-fix: correct wafer defocus sign`
- `github-update: automate labeled squash merge`

허용 kind: `add`, `update`, `fix`, `refactor`, `docs`, `test`, `audit`, `chore`

## 변경 요약

(한 단락)

## 영향 받는 Phase / 모듈

- [ ] Phase 1 (Fourier optics)
- [ ] Phase 2 (Partial coherence)
- [ ] Phase 3 (Wafer topography)
- [ ] Phase 4 (Mask 3D)
- [ ] Phase 5 (Resist)
- [ ] Phase 6 (SMO/PMWO)
- [ ] Cross-cutting / 문서 / 감사

## 변경 종류

- [ ] feat: 새 기능
- [ ] fix: 버그 수정
- [ ] docs: 문서만 변경
- [ ] refactor: 리팩터
- [ ] test: 테스트 추가/수정
- [ ] chore: 기타

## 자체 감사 결과 (4-역할)

| Role | Status | Notes |
|------|--------|-------|
| Data Analyst | PASS / CAUTION / N/A | |
| Physics | PASS / CAUTION / N/A | |
| AI / Numerical | PASS / CAUTION / N/A | |
| Simulation | PASS / CAUTION / N/A | |

## 단순화 가정

- 새로 도입한 단순화 (있다면): _______________
- 코드 주석 + docs/ 모두에 기록되었는가: [ ] Yes / [ ] No

## 단위 테스트

- [ ] 새 모듈에 단위 테스트 추가됨
- [ ] `pytest tests/` 로컬에서 모두 통과
- [ ] 기존 테스트 영향 없음

## 관련 논문 / 문서

- 참조 논문: #
- 참조 문서: 

## Phase Gate 시점인가

- [ ] Yes — 진행계획서 §9.2 8-요소 체크리스트도 통과
- [ ] No — 일반 변경

---

@claude 검토 부탁
