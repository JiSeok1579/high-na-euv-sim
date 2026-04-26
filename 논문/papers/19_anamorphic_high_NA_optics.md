# Anamorphic high-NA EUV lithography optics

- **링크 / DOI**:
  - DOI: [10.1117/12.2196393](https://doi.org/10.1117/12.2196393)
  - SPIE (Paywalled): https://www.spiedigitallibrary.org/conference-proceedings-of-spie/9661/96610T/Anamorphic-high-NA-EUV-lithography-optics/10.1117/12.2196393.short
- **연도**: 2015
- **저자 / 기관**: Sascha Migura, Bernhard Kneer, Jens T. Neumann, Winfried Kaiser (Carl Zeiss SMT), Jan van Schoot (ASML)
- **학회**: Proc. SPIE 9661, 31st European Mask and Lithography Conference (EMLC 2015), paper 96610T
- **분야**: High-NA overview (광학 시스템 설계)
- **우선순위**: A (필수)
- **PDF 상태**: Paywalled (SPIE)

---

## 핵심 문제
**8 nm half-pitch 이하**를 인쇄하려면 NA > 0.5가 필요 → 그러나 4× 등배 full-field 26×33 mm reticle은 mask shadowing 때문에 불가능 → 어떻게 풀 것인가?

## 제안 솔루션 — Anamorphic Projection Optics
- **4× scan / 8× cross-scan demagnification**
- **half-field 26 × 16.5 mm**
- 기존 6" mask 인프라 재사용 가능
- ASML EXE:5000에 실제 구현됨 (with central obscuration)

## 핵심 수식 / 모델
- demagnification 비대칭 (4x : 8x)으로 mask CRA가 줄어들어 shadowing 완화
- field stitching으로 26 × 33 mm reticle을 두 노광으로 처리
- pupil에 central obscuration이 들어가는 trade-off

## 우리 프로젝트에 쓸 수 있는 부분
- **Phase 1 + Phase 4** — 우리 시뮬레이터의 anamorphic 좌표 변환 구현 핵심 reference
- **mask side coordinate vs wafer side coordinate** 변환 공식
- field stitching 모델링 (필요 시)
- central obscuration이 왜 도입되었는지의 광학 설계 히스토리

## 구현 난이도
Medium (anamorphic 좌표 + central obscuration pupil)

## 비고
- High-NA EUV의 출발점 논문 — **반드시 인용**
- 2015년 논문이지만 현재 EXE:5000의 설계 근간
- paper 5, 11, 14의 산업 결과 논문들의 이론적 근거
