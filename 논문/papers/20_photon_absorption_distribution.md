# Understanding the impact of the EUV photon absorption distribution in 0.55 NA EUV

- **링크 / DOI**:
  - DOI: [10.1117/12.3072194](https://doi.org/10.1117/12.3072194)
  - SPIE (Paywalled): https://www.spiedigitallibrary.org/conference-proceedings-of-spie/13686/136860D/Understanding-the-impact-of-the-EUV-photon-absorption-distribution-in/10.1117/12.3072194.short
- **연도**: 2025
- **저자 / 기관**: Danilo De Simone, Vicky Philipsen, Alessandro Vaglio Pret, Anatoly Burov (imec)
- **학회**: Proc. SPIE 13686, paper 136860D
- **분야**: Resist / Stochastic
- **우선순위**: A (필수)
- **PDF 상태**: Paywalled (SPIE)

---

## 핵심 문제
0.55 NA EUV에서 **resist film 두께 방향 EUV photon 흡수 분포**가 lithographic performance에 미치는 영향.

## 사용한 모델 / 방법
- **Rigorous stochastic imaging simulation**
- 대표 0.55 NA test pattern
- resist 두께 방향에 **gradient extinction coefficient** 도입 (top vs bottom 비대칭)

## 핵심 결과 / 정량
- 두께 방향 absorption 비대칭 → top vs bottom dose 불균형
- **stochastic LWR / CDU** 영향 정량화
- focus를 통한 process window 평가 → 0.55 NA의 좁은 DoF에서 더 critical

## 우리 프로젝트에 쓸 수 있는 부분
- **Phase 5 (Resist model)** — 단순 2D aerial image threshold가 아닌 **3D depth-resolved absorption** 필요성 명시적 근거
- **Phase 5 + Phase 1** 결합 — aerial image의 z(depth) 의존성 모델
- LWR/CDU stochastic 메트릭의 0.55 NA 특화 분석

## 구현 난이도
High (3D depth + stochastic Monte Carlo)

## 비고
- paper 1 (stochastic decomposition), paper 13 (resist SWA), paper 21 (statistics nanopatterns)와 강하게 연관
- 0.55 NA 환경의 stochastic 효과를 가장 직접적으로 다루는 imec 논문
