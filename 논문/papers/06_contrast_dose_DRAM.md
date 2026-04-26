# Contrast improvement and dose reduction for High-NA EUV DRAM

- **링크 / DOI**:
  - SPIE (Paywalled): https://spie.org/advanced-lithography/presentation/Contrast-improvement-and-dose-reduction-for-High-NA-EUV-DRAM/13979-3
  - DOI: N/A (paper 13979-3, DOI 미공개)
- **연도**: 2025
- **저자 / 기관**:
  - Samsung: Hyung Jong Bae, Yeongchan Cho, Kangjae Lee, Yeeun Han, Moosong Lee, Woojin Jung, Seongbo Shim
  - ASML US: Yunbo Liu, Lang Zhang, Gerui Liu, Paul Derks, Stephen Hsu
  - ASML Netherlands: Eelco van Setten, Toine van den Boogaard, Jungtae Lee, Aysegul Cumurcu Gysen
- **학회**: SPIE Advanced Lithography + Patterning 2025, conference 13979
- **분야**: SMO + OPC/ILT (DRAM 적용)
- **우선순위**: A (필수)
- **PDF 상태**: Paywalled (SPIE Digital Library)

---

## 핵심 문제
0.55 NA EUV(EXE:5000)에서 DRAM 핵심 layer의 image contrast 향상과 dose 절감을 동시에 달성.

## 사용한 모델 / 방법
- **PMWO (Pupil-Mask-Wavefront Co-Optimization)** 기법
- pupil(source shape), mask pattern, wavefront(aberration)을 동시에 최적화
- DRAM 2D layout 대상 (line/space 단순 패턴이 아님)

## 핵심 결과
- contrast 향상 → dose 절감 가능
- LCDU (Local CD Uniformity) 개선
- EPE 개선
- DRAM 관련 2D 레이아웃에서 정량적 benefit 확인

## 우리 프로젝트에 쓸 수 있는 부분
- **Phase 6 (OPC/ILT/SMO)** — pupil + mask + wavefront 3변수 동시 최적화의 산업 사례
- 단순 binary mask가 아닌 2D layout에서의 SMO 평가 메트릭 (LCDU, EPE) 정의 출처
- objective function 구성 가이드: contrast vs dose vs LCDU의 가중치 설정

## 구현 난이도
High (3변수 joint optimization, anamorphic mask)

## 비고
- Paper 10 (PMWO for LWR/overlay)과 같은 PMWO 기법 시리즈
- DRAM 적용 사례가 명시되어 있어 실제 product layer 매핑이 가능
