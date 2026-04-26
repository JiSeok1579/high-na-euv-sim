# Characterization and Mitigation of 3D Mask Effects in EUV Lithography

- **링크 / DOI**:
  - DOI: [10.1515/aot-2017-0019](https://doi.org/10.1515/aot-2017-0019)
  - 저널 페이지: https://www.degruyterbrill.com/document/doi/10.1515/aot-2017-0019/html
  - LBL Symposium 슬라이드: https://euvlsymposium.lbl.gov/pdf/2016/Oral/Wed_S2-1.pdf
- **연도**: 2017
- **저자 / 기관**: Andreas Erdmann, Dongbo Xu, Peter Evanschitzky (Fraunhofer IISB), Vicky Philipsen, Vu Luong, Eric Hendrickx (imec)
- **저널**: Advanced Optical Technologies 6 (3-4): 187–201 (De Gruyter)
- **분야**: Mask 3D
- **우선순위**: A (필수)
- **PDF 상태**: De Gruyter (구독 필요할 수 있음) + LBL 슬라이드 무료

---

## 핵심 문제
EUV reflective mask의 **3D 효과** 전반을 정량 분석하고 **완화 방법** 정리.

## 사용한 모델
- rigorous EM simulation (Fraunhofer IISB의 Dr.LiTHO 등)
- mask absorber/multilayer/시스템의 3D 모델

## 다루는 M3D 현상들
1. **asymmetric shadowing** — chief ray angle이 0이 아니라 발생
2. **orientation-dependent CD bias** — H/V 패턴 차이
3. **telecentricity error** — pitch별 best focus 위치 변동
4. **contrast loss** — destructive interference
5. **pitch/size-dependent best-focus shift** — absorber 위상에 의한 wavefront 왜곡
6. **secondary images** — absorber top reflection으로 인한 ghost image

## 완화 전략
- **thinner absorber** — shadowing 감소
- **etched / phase shift absorber** — destructive interference 활용
- **attenuated PSM** — phase + amplitude 동시 제어
- **illumination/source design** — pupil 모양 최적화

## 우리 프로젝트에 쓸 수 있는 부분
- **Phase 4 (Mask 3D)** — 우리가 구현해야 할 M3D 효과의 **체크리스트**
- 각 효과별 정량 메트릭 (CD bias, BF shift, NILS) 정의 출처
- Kirchhoff vs rigorous mask model의 차이 영역 식별

## 구현 난이도
High (rigorous EM이면 매우 어려움; thin-mask + boundary correction이면 medium)

## 비고
- **이 프로젝트의 Mask 3D 모듈 설계 시 가장 먼저 읽을 review**
- paper 7 (high-k mask), paper 17 (best focus shift mitigation)와 함께 보면 mask engineering 전반이 보임
