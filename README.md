# High-NA EUV Lithography Digital Twin

> 0.55 NA EUV 리소그래피의 광원 → 조명 → 반사형 마스크 → 6-mirror anamorphic projection → wafer → resist 흐름을 Fourier optics + ray tracing + mask 3D + photoresist 모델로 근사하는 연구·교육용 디지털 트윈 시뮬레이터.

## 빠른 시작

```bash
# 환경
python -m pip install numpy scipy matplotlib pytest

# 단위 테스트
pytest tests/ -v

# 첫 노트북
jupyter lab notebooks/0_first_aerial_image.ipynb
```

## 진행 상태

| Phase | 내용 | 상태 |
|-------|------|------|
| 1 | Scalar Fourier optics MVP — pupil + mask + aerial | ✅ 완료 (2026-04-26) |
| 2 | Partial coherence / illuminator | ⏳ 대기 |
| 3 | Wafer topography & DOF | ⏳ 다음 |
| 4 | Mask 3D effects | ⏳ 대기 |
| 5 | Photoresist (threshold → blur → depth → stochastic) | ⏳ 대기 |
| 6 | SMO / PMWO / OPC / ILT | ⏳ 대기 |

## 문서 진입점

- [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) — 단일 진입점, 인벤토리, 로드맵
- [진행계획서.md](진행계획서.md) — 6 Phase + KPI + WBS + 위험 등록부
- [docs/phase1_design.md](docs/phase1_design.md) — Phase 1 설계 결정 + 단순화 명시
- [docs/github_claude_automerge_setup.md](docs/github_claude_automerge_setup.md) — GitHub + Claude Code 자동화 셋업
- [audits/README.md](audits/README.md) — 4-역할 gated review 시스템
- [high_na_euv_physics_considerations.md](high_na_euv_physics_considerations.md) — 82-section 물리 핸드북
- [논문/papers/KNOWLEDGE.md](논문/papers/KNOWLEDGE.md) — 21편 논문 통합 학습

## 라이선스

연구·교육용. 상업적 사용은 별도 협의.
