# Performance of optics with central obscuration

- **링크 / DOI**:
  - PDF (Free): https://www.beckoptronic.com/uploads/cms/productsdownload/14/beck-tn-performance-of-optics-with-central-obscuration-v2-file.pdf
  - DOI: N/A (industry technical note)
- **연도**: 미상 (~2018–2020 기준)
- **저자 / 기관**: Beck Optronic Solutions (기술팀 익명)
- **종류**: Industry Technical Note
- **분야**: Fourier optics (PSF/MTF)
- **우선순위**: B (보조)
- **PDF 상태**: Free — Beck Optronic 사이트에서 직접 다운로드

---

## 핵심 문제
중앙 차폐(central obscuration)가 광학 시스템의 **PSF**와 **MTF**에 미치는 영향 정량 평가.

## 핵심 내용
- 중앙 차폐로 인한 에너지 재분배:
  - **central peak**의 폭은 거의 변하지 않음
  - **first sidelobe** 강도 증가
  - **MTF 중간 주파수 영역**에서 attenuation
  - **diffraction-limited cutoff frequency**는 보존
- **obscuration ratio** ε = D_inner/D_outer 에 따른 각 효과 정량화

## 핵심 수식
일반적인 annular aperture의 OTF:
```
OTF(ν) = [OTF_full(ν, D_outer) − ε² · OTF_full(ν, D_inner)] / (1 − ε²)
```

PSF는 두 Airy disk의 차로 표현 가능 (annular aperture).

## 우리 프로젝트에 쓸 수 있는 부분
- **Phase 1 (Aerial image)** — ASML EXE:5000의 central obscuration을 pupil function에 정확히 반영
- Airy/PSF/MTF 시뮬레이션의 sanity check (baseline 비교)
- paper 19 (anamorphic optics)에서 언급되는 obscuration의 정량 영향 이해

## 구현 난이도
Low (Fourier optics 기본 구현 가능)

## 비고
- 산업 technote라 peer-review는 아니지만 수식과 그래프가 매우 명확
- 우리 시뮬레이터의 첫 단계 검증에 좋은 reference
