# Unraveling the relative impact of material and optical stochastic effects on EUV LWR

- **링크 / DOI**:
  - DOI: [10.1038/s41598-025-29021-2](https://doi.org/10.1038/s41598-025-29021-2)
  - PDF (Open Access): https://www.nature.com/articles/s41598-025-29021-2
- **연도**: 2025
- **저자 / 기관**: Ji Young Park, Yongbeom Seo, Dong-Hun Shin 외 (Hanyang University, Seoul)
- **저널**: Scientific Reports (Nature) Vol. 15, Article 43476
- **분야**: Resist / Stochastic
- **우선순위**: A (필수)
- **PDF 상태**: Open Access — 브라우저에서 직접 다운로드 가능 (이 환경에서는 네트워크 제한으로 자동 다운로드 불가)

---

## 핵심 문제
EUV 패터닝(36 nm pitch L/S)에서 LWR의 stochastic 기여를 **광학(optical)**, **물질(material)**, **마스크 LER**로 분리해 정량화.

## 사용한 모델
- 시뮬레이션 기반 stochastic decomposition
- CD–LWR 상관관계의 "smile" 형태 분석

## 핵심 수식 / 인사이트
- 저전류/작은 CD 영역 → optical stochastics 지배
- 고전류/큰 CD 영역 → material stochastics 지배
- 두 효과는 **상호 보완적(partial compensation)**으로 작용 — 단순 합이 아님

## 우리 프로젝트에 쓸 수 있는 부분
- **Phase 5 (Resist model)** stochastic resist 구현 시 최우선 reference
- aerial image 위에 photon shot noise + acid diffusion + secondary electron blur 추가할 때 각 항의 상대 가중치 산정 근거
- LER/LWR metric을 단순 표준편차로 보면 안 되고, dose-dependent decomposition을 해야 한다는 교훈

## 구현 난이도
High (rigorous Monte Carlo + multi-physics stochastic model)

## 비고
- Open Access 논문 — 라이선스 확인 후 인용 가능
- High-NA 이전 0.33 NA 환경의 분석이지만, decomposition 방법론은 0.55 NA에도 그대로 적용
