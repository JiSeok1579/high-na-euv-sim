# Fundamental aspects of Photosensitized chemically amplified resist (PSCAR) and CAR — Overcoming RLS trade-off and photon shot noise

- **링크 / DOI**:
  - PDF (Free Workshop): https://www.euvlitho.com/2017/P46.pdf
  - DOI: N/A (workshop proceedings)
- **연도**: 2017
- **저자 / 기관**: Seiichi Tagawa, Seiichi Nagahara, Takahiro Kozawa 외 (Osaka University, TEL 외)
- **학회**: International Workshop on EUV Lithography 2017, paper P46
- **분야**: Resist / Stochastic
- **우선순위**: A (필수)
- **PDF 상태**: Free — euvlitho.com에서 직접 다운로드 가능

---

## 핵심 문제
EUV resist에서 항상 발생하는 **RLS trade-off** (Resolution × LER × Sensitivity)와 **photon shot noise**를 어떻게 동시에 극복할 것인가?

## 사용한 모델
- CAR (Chemically Amplified Resist) 기본 메커니즘 review
  - acid 생성 → acid diffusion → polymer deprotection → development
- PSCAR: CAR + photosensitizer precursor + UV flood exposure
  - EUV 노광부에서만 photosensitizer 생성 → UV flood로 추가 acid 발생
  - 결과적으로 sensitivity 향상 + photon shot noise 감소

## 핵심 수식 / 모델 정보
- acid generation rate ∝ EUV photon absorption density
- secondary electron blur ≈ 2–4 nm radius
- PSCAR의 acid amplification factor가 추가 control parameter

## 우리 프로젝트에 쓸 수 있는 부분
- **Phase 5 (Resist model)** — threshold model 다음 단계의 stochastic resist 구현 가이드
- aerial image → acid concentration map → dissolution rate map 의 단계별 변환 모델
- shot noise 영향 정량 평가 시 베이스라인

## 구현 난이도
Medium (CAR threshold + Gaussian blur), High (full stochastic PSCAR)

## 비고
- workshop paper지만 fundamentals review로서 매우 좋음
- paper 1 (stochastic decomposition)과 함께 보면 resist stochastic 모델링의 큰 그림이 잡힘
