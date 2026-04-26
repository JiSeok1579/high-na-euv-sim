# SHARP — The SEMATECH high-NA actinic reticle review project: EUV mask-imaging microscope

- **링크 / DOI**:
  - DOI: [10.1117/12.2026496](https://doi.org/10.1117/12.2026496)
  - SPIE: https://www.spiedigitallibrary.org/conference-proceedings-of-spie/8880/88800T/The-SEMATECH-high-NA-actinic-reticle-review-project-SHARP-EUV/10.1117/12.2026496.full
  - 저자 preprint (Free): https://goldberg.lbl.gov/papers/Goldberg_SPIE88800_(2013).pdf
- **연도**: 2013
- **저자 / 기관**: Kenneth A. Goldberg, Iacopo Mochi, Markus P. Benk, Antoine Wojdyla, Sungmin Huh 외 (LBNL CXRO + SEMATECH)
- **학회**: Proc. SPIE 8880, Photomask Technology 2013, paper 88800T
- **분야**: Mask metrology / Actinic mask imaging
- **우선순위**: B (보조)
- **PDF 상태**: 저자 preprint 공개 — goldberg.lbl.gov에서 직접 다운로드 가능

---

## 핵심 문제
실제 EUV 스캐너에 마스크를 넣기 전, 13.5 nm actinic 조건에서 EUV reticle을 검사·이미징할 수 있는 synchrotron 기반 마이크로스코프 구축.

## 사용한 모델
- LBNL ALS synchrotron 광원
- Fourier-synthesis multi-mirror illuminator (스캐너 illumination 모사)
- Fresnel zoneplate objective (4x, 6x 등 가변 NA)
- AIT (Actinic Inspection Tool, 2007–2013)의 후속 장비

## 핵심 수식 / 모델 정보
- Köhler illumination at 13.5 nm with programmable σ
- partial coherence 변경을 통해 dipole/quadrupole/annular 모사
- effective wafer-side NA 0.0825 ~ 0.42 까지 지원

## 우리 프로젝트에 쓸 수 있는 부분
- **Phase 4 (Mask 3D)** validation 시 actinic ground truth 데이터 출처로 인용
- mask shadowing, BF shift, NILS 측정값을 시뮬레이터 출력과 비교할 때 reference
- partial coherence illumination 구현 시 실제 장비가 어떻게 σ를 만드는지 참고

## 구현 난이도
N/A (장비 논문, 직접 구현 대상 아님)

## 비고
- 우리는 장비를 만들지 않으므로 직접 구현 대상은 아니지만, **mask 3D effect 검증 데이터의 출처**로 사용
- SHARP 데이터셋이 공개되어 있는지 확인 필요
