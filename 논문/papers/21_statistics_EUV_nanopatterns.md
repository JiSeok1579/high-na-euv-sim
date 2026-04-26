# Statistics of EUV exposed nanopatterns: Photons to molecular dissolutions

- **링크 / DOI**:
  - 저널: https://pubs.aip.org/aip/jap/article/137/20/204902/3347586
  - DOI: 10.1063/5.0264... (정확한 DOI는 저널 페이지에서 확인)
- **연도**: 2025
- **저자 / 기관**: Hiroshi Fukuda (Hitachi High-Tech Corporation)
- **저널**: Journal of Applied Physics, Vol. 137, Issue 20, article 204902 (28 May 2025)
- **분야**: Resist / Stochastic
- **우선순위**: A (필수)
- **PDF 상태**: AIP — 일반적으로 paywalled (저자 preprint 미확인)

---

## 핵심 문제
EUV resist exposure를 **photon → secondary electron → acid → deprotection → dissolution** 의 chained stochastic 사건으로 첫 원리에서 모델링.

## 사용한 모델 / 방법
- **First-principle Monte Carlo**
- **Directional network model**:
  - binomial 분포
  - beta-binomial 분포
  - mixed Bernoulli convolution
- 각 단계의 확률 분포가 다음 단계로 전파되는 구조

## 핵심 결과 / 인사이트
- feature 크기가 **molecular interaction range**에 가까워질수록 averaging 효과가 약해짐
- High-NA EUV에서 resolution과 stochastic behavior의 한계 정량화
- photon shot noise만 보면 안 되고 chain 전체 stochastic 누적이 중요

## 핵심 수식 / 모델 정보
- 각 단계 X_i의 분포: P(X_{i+1} | X_i) — Markov chain 형태
- end-to-end stochastic dose response = convolution of stage variances

## 우리 프로젝트에 쓸 수 있는 부분
- **Phase 5 (Resist model)** — full stochastic resist 모델의 가장 최신 학문 reference
- 각 단계별 Monte Carlo 시뮬레이션 구조 reference
- paper 1, 4, 20과 함께 보면 stochastic resist 전체 그림 완성
- LER/LWR/missing contact rate를 분포 합성으로 예측하는 framework

## 구현 난이도
Very High (4단계 chained stochastic Monte Carlo)

## 비고
- 2025년 최신 — High-NA 시대의 stochastic 한계를 가장 정확히 다룸
- 우리 프로젝트 후반부의 advanced resist 모듈 reference
