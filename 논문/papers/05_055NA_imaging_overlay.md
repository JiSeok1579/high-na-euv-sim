# 0.55 NA EUV lithography: Imaging & Overlay

- **링크 / DOI**:
  - PDF (Free Workshop): https://euvlitho.com/2024/S1.pdf
  - DOI: N/A (workshop proceedings)
- **연도**: 2024
- **저자 / 기관**: Jan van Schoot (ASML Fellow) 외 (ASML / Carl Zeiss SMT)
- **학회**: International Workshop on EUV Lithography 2024, invited talk S1
- **분야**: High-NA overview
- **우선순위**: A (필수)
- **PDF 상태**: Free — euvlitho.com에서 직접 다운로드 가능

---

## 핵심 문제
0.55 NA EUV(EXE:5000) 스캐너의 imaging 성능과 overlay 성능을 정량적으로 보고.

## 사용한 모델 / 시스템
- ASML EXE-series 스캐너 (NA 0.55)
- anamorphic 4×/8× demagnification
- half-field 26 × 16.5 mm
- central obscuration optics

## 핵심 수치 / 결과
- 8 nm half-pitch 패턴 시연
- contrast, EPE 향상 정량화
- overlay/focus control 솔루션 (stitching, 고속 스테이지, 개선된 센서)

## 우리 프로젝트에 쓸 수 있는 부분
- **모든 Phase의 reference target** — 우리 시뮬레이터가 출력해야 할 수치(8 nm hp, contrast, EPE 등)의 ground truth
- anamorphic magnification 4×/8× 구현 시 좌표 변환 reference
- half-field stitching 모델링 reference (Phase 3에서 wafer topography와 함께 다룰 가능성)

## 구현 난이도
N/A (review/시스템 보고 논문)

## 비고
- 산업 표준 baseline 논문 — 이 논문의 결과를 우리 시뮬레이터가 정성적으로 재현해야 함
- paper 11 (Moore's Law first imaging)과 같은 ASML 라인업
