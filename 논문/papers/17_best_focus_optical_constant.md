# Mitigating best focus shift in high-NA EUV lithography via optical constant screening

- **링크 / DOI**:
  - DOI: [10.1117/12.3072152](https://doi.org/10.1117/12.3072152)
  - SPIE (Paywalled): https://www.spiedigitallibrary.org/conference-proceedings-of-spie/13686/136861O/Mitigating-best-focus-shift-in-high-NA-EUV-lithography-via/10.1117/12.3072152.full
- **연도**: 2025
- **저자 / 기관**: Seungho Lee 외 (Samsung / imec 협업 추정 — full list paywalled)
- **학회**: Proc. SPIE 13686, paper 136861O
- **분야**: Mask 3D / Absorber engineering
- **우선순위**: A (필수)
- **PDF 상태**: Paywalled (SPIE)

---

## 핵심 문제
0.55 NA에서 pitch별 **best focus(BF) shift**가 좁아진 DoF budget을 더 갉아먹음 → absorber 재료 선정으로 완화.

## 사용한 모델 / 접근
- absorber 후보의 **n-k optical constant 공간** screening
- single-element / binary / 합금 후보 평가
- TaBN reference vs candidate 재료 비교

## 핵심 결과
- **High-k absorber** 후보: Ni 등 → BF shift 감소
- **Low-n attenuated PSM** 후보: RuTa, PtMo, PtTe → NILS, MEEF, BF metric 모두 개선
- 각 후보의 정량 NILS, MEEF, BF range 표 제시

## 우리 프로젝트에 쓸 수 있는 부분
- **Phase 4 (Mask 3D)** — 다양한 absorber n-k 조합을 시뮬레이션할 때 후보 리스트
- BF through pitch metric 정의 (paper 12, 14와 일관)
- NILS, MEEF 메트릭 계산 reference

## 구현 난이도
High (rigorous mask EM simulation 필요)

## 비고
- paper 7 (Novel high-k mask)과 같은 흐름 — 함께 보면 absorber engineering 전체 그림
- 산업 우선 후보(RuTa, PtMo, PtTe 등)를 우리 시뮬레이터의 default 옵션으로 쓸 수 있음
