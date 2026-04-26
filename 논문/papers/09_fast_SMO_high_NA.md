# A fast SMO method for high-NA EUV lithography imaging model

- **링크 / DOI**:
  - DOI: [10.29026/oea.2024.230235](https://doi.org/10.29026/oea.2024.230235)
  - PDF (Open Access): https://www.oejournal.org/oea/article/doi/10.29026/oea.2024.230235
- **연도**: 2024
- **저자 / 기관**: Ziqi Li, Lisong Dong, Xu Ma, Yayi Wei (Chinese Academy of Sciences / 관련 연구소)
- **저널**: Opto-Electronic Advances, Vol. 7, No. 4, Article 230235
- **분야**: SMO (Source-Mask Optimization)
- **우선순위**: A (필수)
- **PDF 상태**: Open Access (OEA)

---

## 핵심 문제
**High-NA EUV imaging model**(mask 3D + anamorphic 효과 포함)을 빠르게 평가하면서 **SMO**까지 수행하는 방법.

## 사용한 모델 / 알고리즘
1. **Fast High-NA imaging model**:
   - mask 3D effect 근사
   - anamorphic magnification (4× scan / 8× cross-scan) 반영
2. **SMO scheme**:
   - **mask optimization**: gradient-based
   - **source optimization**: compressive sensing 기반
3. **MRC (Mask Rule Check)** step 통합

## 핵심 수식 / 결과
- patterning error 감소 정량 보고
- 고전 SMO 대비 계산 효율 유지
- mask 3D를 무시한 SMO 대비 정확도 향상

## 우리 프로젝트에 쓸 수 있는 부분
- **Phase 6 (OPC/ILT/SMO)** — 우리 시뮬레이터의 SMO 모듈 baseline 알고리즘
- **Phase 4 (Mask 3D)** + Phase 6 통합 — fast 3D mask model을 어떻게 SMO loop 안에 넣는지 구체적 방법
- gradient-based mask + compressive sensing source의 **목적 함수 + gradient 정의** 직접 인용 가능

## 구현 난이도
High (anamorphic 좌표 + mask 3D + dual optimization)

## 비고
- **이 프로젝트에서 가장 직접 구현 가이드가 되는 논문 중 하나**
- Open Access — 코드/수식 자유롭게 참조 가능
- paper 6, 10 (PMWO 시리즈)와 비교하면 학계 vs 산업 SMO 접근의 차이 파악 가능
