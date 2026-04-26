# High-NA In-Line Projector for EUV Lithography

- **링크 / DOI**:
  - arXiv: [2508.00433](https://arxiv.org/abs/2508.00433)
  - PDF (Open Access): https://arxiv.org/pdf/2508.00433
- **연도**: 2025
- **저자 / 기관**: Tsumoru Shintake (OIST, Okinawa Institute of Science and Technology)
- **종류**: arXiv preprint (Photomask Japan 시리즈에서도 발표)
- **분야**: High-NA overview / 광학 시스템 설계
- **우선순위**: B (보조 — 대안 광학 아키텍처)
- **PDF 상태**: Open Access (arXiv)

---

## 핵심 문제
ASML/Zeiss의 anamorphic 6-mirror 시스템 외에, **oblique-incidence가 없는 in-line(coaxial) 4-mirror 광학**이 가능한가?

## 사용한 모델
- 4-mirror in-line(coaxial) projection optics
- two-stage concave–convex pair → double-Gauss 같은 aberration cancellation
- central obscuration 사용 (in-line이라 불가피)

## 핵심 수식 / 결과
- NA 0.5 (4-mirror 기본 구성), NA 0.7 (hyper-NA 옵션)
- 26 mm circular field 가능
- residual radial distortion 때문에 실제 운용은 18×18 mm 스테퍼 형식

## 우리 프로젝트에 쓸 수 있는 부분
- **Phase 1 (Aerial image)** + **Phase 4 (Mask 3D)** — oblique CRA가 없으면 mask 3D 효과가 어떻게 줄어드는지 비교 시뮬레이션 가능
- central obscuration이 PSF/MTF에 미치는 영향 분석 (paper 15와 연계)
- ASML 6-mirror anamorphic과의 상대 비교 baseline

## 구현 난이도
Medium (4-mirror 광학을 ray tracing + Fourier optics로 구현)

## 비고
- 학계 alternative design — 산업 표준은 여전히 ASML EXE:5000
- 이 논문은 mask 3D 문제의 근본 해결 방향 중 하나를 보여줌 (CRA = 0)
