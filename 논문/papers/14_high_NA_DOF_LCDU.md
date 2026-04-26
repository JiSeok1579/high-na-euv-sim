# High-NA EUV imaging in action: tackling the depth-of-focus challenge for superior resolution and LCDU

- **링크 / DOI**:
  - DOI: [10.1117/12.3073923](https://doi.org/10.1117/12.3073923)
  - SPIE (Paywalled): https://www.spiedigitallibrary.org/conference-proceedings-of-spie/13686/136860Z/High-NA-EUV-imaging-in-action--tackling-the-depth/10.1117/12.3073923.full
- **연도**: 2025
- **저자 / 기관**: Eelco van Setten 외 (ASML Netherlands)
- **학회**: Proc. SPIE 13686, paper 136860Z
- **분야**: High-NA overview (DOF / LCDU)
- **우선순위**: A (필수)
- **PDF 상태**: Paywalled (SPIE)

---

## 핵심 문제
NA 0.55에서 **DOF가 NA² 으로 줄어드는 문제**를 어떻게 극복하면서 LCDU를 향상시킬 것인가.

## 사용한 시스템 / 모델
- ASML EXE 0.55 NA platform
- anamorphic demagnification + central obscuration
- 29 nm pitch hex hole/pillar test patterns

## 핵심 결과
- 0.33 NA 대비 **LCDU 18–42% 향상**
- DOF reduction 대응:
  - **PMWO** (Pupil-Mask-Wavefront Co-Optimization)
  - **micro focus-drilling**

## 우리 프로젝트에 쓸 수 있는 부분
- **Phase 3 (Wafer topography / DOF)** — DOF k2·λ/NA² 식의 정량적 검증 데이터
- **Phase 6 (OPC/ILT/SMO)** — PMWO + micro focus-drilling을 우리 최적화 모듈에 어떻게 통합할지
- LCDU metric을 hex hole/pillar 패턴에 적용하는 standard test

## 구현 난이도
N/A (결과 보고)

## 비고
- paper 5, 11 (ASML 라인)과 paper 10 (PMWO LWR)의 종합편 성격
- DOF 챌린지가 우리 시뮬레이터의 핵심 검증 시나리오
