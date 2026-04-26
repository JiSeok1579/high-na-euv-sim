# Physics of laser-driven tin plasma sources of EUV radiation for nanolithography

- **링크 / DOI**:
  - DOI: [10.1088/1361-6595/ab3302](https://doi.org/10.1088/1361-6595/ab3302)
  - 저널: https://iopscience.iop.org/article/10.1088/1361-6595/ab3302
  - PDF (Open Access ARCNL): https://ir.arcnl.nl/pub/67/00076OA.pdf
- **연도**: 2019
- **저자 / 기관**: Oscar O. Versolato (ARCNL, Advanced Research Center for Nanolithography, Amsterdam)
- **저널**: Plasma Sources Science and Technology, Vol. 28, No. 8, article 083001 (Topical Review)
- **분야**: Source / LPP (광원 물리)
- **우선순위**: A (필수)
- **PDF 상태**: Open Access (ARCNL 리포지토리)

---

## 핵심 문제
13.5 nm EUV 광원으로 사용되는 **laser-produced tin plasma (LPP)**의 물리를 6 orders of magnitude 시간 스케일에서 review.

## 핵심 내용
다음 시간 스케일에서의 물리:
- **sub-ps / ns** — laser-driven atomic / plasma processes
  - highly charged Sn ion spectroscopy (Sn⁸⁺ ~ Sn¹⁴⁺)
  - 4d → 4f, 4d → 5p transition lines가 모여 13.5 nm "UTA" 형성
  - plasma expansion dynamics
- **microsecond** — fluid dynamics
  - tin droplet deformation by pre-pulse
  - main pulse target shaping

## 핵심 결과
- **Conversion Efficiency (CE)** 최적 조건:
  - droplet pre-pulse + main pulse 시퀀스
  - mass-limited target
- in-band 13.5 nm power → wafer-side dose
- source power, stability, reliability 결정 요인

## 우리 프로젝트에 쓸 수 있는 부분
- **광원 모델링 (Phase 0 / Phase 1 시작 전)** — 광원을 단순 monochromatic point source로 보기 전에 spectral & angular profile 파악
- paper 8 (LPP source spectrum)과 함께 광원 모델 완성
- out-of-band radiation 평가 시 학문적 근거

## 구현 난이도
N/A (review 논문, 직접 구현 대상 아님)

## 비고
- **Topical Review** — 학계의 종합 정리
- ARCNL OA copy 무료 — 라이선스 자유
- 우리 시뮬레이터는 광원 자체를 plasma physics로 모델링하지는 않지만, **spectral content + angular content**의 ground truth로 사용
