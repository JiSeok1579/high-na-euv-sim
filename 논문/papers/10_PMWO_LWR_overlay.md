# Pupil, mask, wavefront co-optimization for enhanced EUV patterning: reducing LWR and evaluating overlay

- **링크 / DOI**:
  - SPIE (Paywalled): https://spie.org/photomask-technology/presentation/Pupil-mask-wavefront-co-optimization-for-enhanced-EUV-patterning/13686-16
  - DOI: N/A (paper-level DOI 미공개)
- **연도**: 2025
- **저자 / 기관**: Christopher Kaplan 외 (ASML) — full list paywalled
- **학회**: Proc. SPIE 13686, Photomask Technology + EUV Lithography 2025, paper 13686-16
- **분야**: OPC/ILT (Mask 3D 보정 포함)
- **우선순위**: A (필수)
- **PDF 상태**: Paywalled (SPIE)

---

## 핵심 문제
EUV에서 mask 3D phase error로 인한 **contrast fading**을 PMWO(Pupil-Mask-Wavefront Co-Optimization)로 보정 + LWR 감소 + overlay 영향 평가.

## 사용한 모델 / 방법
- **PMWO (Pupil + Mask + Wavefront 동시 최적화)**
- mask 3D phase error를 wavefront 항으로 흡수
- pupil shape 변경에 따른 overlay 변화 정량화

## 핵심 결과
- **LWR 감소** (또는 동일 LWR에서 dose 절감)
- pupil shape 변경의 overlay impact 평가 — 단순 contrast 향상이 다른 메트릭을 깨지 않는지 확인

## 우리 프로젝트에 쓸 수 있는 부분
- **Phase 6 (OPC/ILT/SMO)** — PMWO 목적 함수에 LWR 항을 어떻게 포함할지 reference
- **Phase 4 (Mask 3D)** — mask 3D phase error를 wavefront로 흡수하는 모델링 기법
- pupil-vs-overlay tradeoff 분석 framework

## 구현 난이도
High (3변수 joint optimization + stochastic LWR estimator)

## 비고
- paper 6 (PMWO for DRAM)과 같은 PMWO 시리즈
- 학계 fast SMO (paper 9) → 산업 PMWO로의 흐름 비교
