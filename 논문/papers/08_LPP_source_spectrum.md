# EUV spectrum of high power LPP source

- **링크 / DOI**:
  - DOI: [10.1117/12.3072173](https://doi.org/10.1117/12.3072173)
  - SPIE (Paywalled): https://www.spiedigitallibrary.org/conference-proceedings-of-spie/13686/1368611/EUV-spectrum-of-high-power-LPP-source/10.1117/12.3072173.full
- **연도**: 2025
- **저자 / 기관**: Hakaru Mizoguchi 외 추정 (Gigaphoton) — full author list 미확인
- **학회**: Proc. SPIE 13686, Photomask Technology + EUV Lithography 2025
- **분야**: Source / LPP
- **우선순위**: B (보조)
- **PDF 상태**: Paywalled (SPIE Digital Library)

---

## 핵심 문제
HVM(고생산성) EUV 리소그래피용 고출력 tin LPP 광원의 **EUV emission spectrum** 특성화.

## 사용한 모델 / 측정
- in-band 13.5 nm power 측정
- conversion efficiency (CE: drive laser energy → EUV in-band)
- out-of-band radiation 측정 (DUV, IR 누설)

## 핵심 수치 / 결과
- in-band 13.5 nm (2% bandwidth) 출력
- out-of-band radiation이 wafer dose와 resist response에 미치는 영향
- scanner dose 안정성 관련 spectrum 안정성

## 우리 프로젝트에 쓸 수 있는 부분
- **Phase 1 시작 전 / source 모델링** — 광원의 spectral content를 모노크로매틱이 아닌 finite bandwidth로 모델링할 때 reference
- out-of-band radiation이 photoresist에 추가 dose를 주는 현상 (Phase 5)
- paper 18 (tin plasma physics)과 함께 보면 광원 모델 완성

## 구현 난이도
Medium (광원 spectrum을 multi-wavelength FFT optics로 처리)

## 비고
- 산업 LPP source 보고 — 학계 광원 물리 (paper 18)와 보완 관계
- out-of-band radiation을 단순 무시하는 시뮬레이터의 한계 인식 자료
