# Design of a high transmission illumination optics for anamorphic EUV lithography optics using deep RL

- **링크 / DOI**:
  - DOI: [10.1364/OE.547606](https://doi.org/10.1364/OE.547606)
  - 저널: https://opg.optica.org/oe/abstract.cfm?uri=oe-33-2-2261
  - PubMed: https://pubmed.ncbi.nlm.nih.gov/39876379/
- **연도**: 2025
- **저자 / 기관**: Tianjiao Li, Yanqiu Li, Y. Chen, L. Liu (Beijing Institute of Technology 추정)
- **저널**: Optics Express, Vol. 33, Issue 2, pp. 2261–2276
- **분야**: Illumination / Source-mask (illuminator design)
- **우선순위**: A (필수)
- **PDF 상태**: Optica Open Access — opg.optica.org에서 직접 다운로드 가능 (대부분 OA 논문)

---

## 핵심 문제
NA 0.55 anamorphic EUV illuminator를 위한:
1. **고투과율(High Transmission) Relay system 설계**
2. Field facet ↔ Pupil facet **double-facet matching** 최적화 (deep RL 사용)

## 사용한 모델 / 알고리즘
1. **Relay system 설계**:
   - matrix optics + conic-fit decentering으로 obscuration 제거
   - one-mirror off-axis relay
2. **Double-facet matching**:
   - **Deep Reinforcement Learning** 기반 assignment
   - field facet의 빛을 pupil facet에 어떻게 mapping할지 최적화

## 핵심 결과
- **illumination efficiency 26.24%** 달성
- 다양한 illumination mode에서 **mask uniformity ~99%**

## 우리 프로젝트에 쓸 수 있는 부분
- **Phase 2 (Partial coherence / source shape)** — illuminator 단의 정확한 source shape 생성 모델
- **Phase 6 (SMO)** — source 변수를 deep RL로 최적화하는 alternative 접근
- annular/dipole/quadrupole illumination을 facet 조합으로 만드는 실제 메커니즘 이해

## 구현 난이도
High (RL을 우리 환경에서 구현하는 것은 큰 일; 단, 결과만 reference로 쓰면 medium)

## 비고
- 학계 RL 적용 사례 — paper 9 (gradient/CS-based SMO)와 비교 가능
- Optics Express는 일반적으로 open access — 풀 PDF 무료
