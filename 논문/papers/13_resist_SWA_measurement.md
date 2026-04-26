# Measurement and adjustment of resist SWA (Sidewall Angle) in EUV lithography

- **링크 / DOI**:
  - 가장 가까운 매칭 SPIE: [10.1117/12.3072665](https://doi.org/10.1117/12.3072665) — "Controlling the resist profile in EUV imaging using source mask optimization"
  - SPIE (Paywalled): https://www.spiedigitallibrary.org/conference-proceedings-of-spie/13686/136860G/Controlling-the-resist-profile-in-EUV-imaging-using-source-mask/10.1117/12.3072665.full
- **연도**: 2025
- **저자 / 기관**: P. Dhagat 외 (ASML) — full list paywalled
- **학회**: Proc. SPIE 13686, Photomask Technology + EUV Lithography 2025, paper 136860G
- **분야**: Resist / Process (sidewall angle)
- **우선순위**: B (보조)
- **PDF 상태**: Paywalled (SPIE)

---

## 핵심 문제
EUV resist의 **높은 EUV 흡수 계수** 때문에 발생하는 **sidewall angle (SWA) 기울기**와 through-resist CD 변동.

## 사용한 모델 / 실험
- 0.33 NA + 0.55 NA 모두에서 SWA-through-focus 실험
- LCDU-through-stack 측정
- micro focus-drilling 기법 — 특히 negative defocus에서 SWA 균질화

## 핵심 결과
- 두꺼운 resist에서는 top vs bottom의 EUV photon flux 차이 큼
- 결과적으로 SWA가 sloped → DOF 손해
- micro focus-drilling으로 SWA를 더 균질하게 만들 수 있음

## 우리 프로젝트에 쓸 수 있는 부분
- **Phase 5 (Resist model)** — single-plane threshold model의 한계, 3D resist absorption volume 필요성
- **Phase 3 (Wafer topography / focus)** — micro focus-drilling을 dose/focus map에 어떻게 반영할지
- aerial image 위에 단순 threshold가 아니라 **depth-resolved absorption profile**을 적용해야 하는 이유

## 구현 난이도
High (3D resist absorption + dissolution 모델)

## 비고
- 원본 리스트 제목 ("Measurement and adjustment of resist SWA in EUV lithography")이 정확히 매칭되지 않아 가장 가까운 SPIE 13686 논문으로 매핑함 — **사용자 확인 필요**
- paper 20 (EUV photon absorption distribution)과 강한 연관
