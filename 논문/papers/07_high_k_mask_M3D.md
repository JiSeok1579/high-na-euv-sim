# Novel high-k mask considering M3D effects & focus control

- **링크 / DOI**:
  - PDF (Free Workshop): https://euvlitho.com/2023/P14.pdf
  - DOI: N/A (workshop proceedings)
- **연도**: 2023
- **저자 / 기관**: 한국 DRAM 제조사 마스크 팀 (SK hynix 또는 Samsung로 추정 — 정확한 저자 리스트 확인 필요)
- **학회**: International Workshop on EUV Lithography 2023, paper P14
- **분야**: Mask 3D
- **우선순위**: A (필수)
- **PDF 상태**: Free — euvlitho.com에서 직접 다운로드 가능

---

## 핵심 문제
EUV mask M3D effect로 인한 **pitch별 best focus 변동**과 **telecentricity 손실**을 absorber 재료로 어떻게 완화할 것인가?

## 사용한 모델 / 접근
- absorber 재료의 굴절률 n과 흡수 계수 k 공간 탐색
- **n ≈ 1 (즉, 진공/공기와 거의 같은 위상)** + **고흡수(high-k)** absorber 후보 평가
- Ru, Ta-기반 reference와 비교

## 핵심 결과
- high-k near-n=1 absorber → M3D-induced BF shift 감소
- pitch through best-focus uniformity 개선
- High-NA에서 telecentricity 향상

## 우리 프로젝트에 쓸 수 있는 부분
- **Phase 4 (Mask 3D)** — absorber 재료 변경이 aerial image에 미치는 영향 시뮬레이션
- Kirchhoff mask model을 넘어서는 rigorous EM simulation 필요성 근거
- BF shift through pitch 메트릭 정의 출처

## 구현 난이도
High (rigorous Maxwell/RCWA mask 시뮬레이션 필요)

## 비고
- paper 17 (best focus shift via optical constant screening)과 강하게 연관 — 두 논문 함께 보면 absorber engineering 맥락이 완전해짐
- 실제 product mask로의 적용 가능성도 다룸
