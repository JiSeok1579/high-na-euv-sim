# /논문/papers/ — 폴더 구성 안내

## 폴더 구조

```
논문/
├── 0.55 High-NA EUV참고 논문리스트.txt   (원본 21편 리스트)
├── high_na_euv_paper_search_handoff.md   (탐색 인수인계 지시서)
└── papers/                               (← 본 폴더)
    ├── INDEX.md                          (★ 마스터 인덱스 — 여기서 시작)
    ├── README.md                         (이 파일)
    ├── 01_stochastic_effects_LWR.md
    ├── 02_SHARP_actinic_microscope.md
    ├── ...
    └── 21_statistics_EUV_nanopatterns.md  (총 21편 metadata)
```

## 사용 순서

1. **`INDEX.md`** 부터 읽기 — 21편 전체 개요, 분야별 분류, Phase 매핑, MVP 추천 3편
2. 관심 분야 논문의 개별 `.md` 파일을 펼쳐 메타데이터 + 우리 프로젝트 적용 포인트 확인
3. 각 논문의 PDF는 **외부 도메인 네트워크 차단** 때문에 자동 다운로드되지 못했습니다.
   각 .md 파일의 "링크 / DOI" 섹션에 있는 URL을 브라우저에서 직접 열어 받으세요.
4. Open Access (★ 표시) 11편은 즉시 무료 다운로드 가능 — `INDEX.md §6` 참고

## 개별 .md 파일 양식

각 논문은 다음 구조로 정리됨:
- 링크 / DOI / PDF URL
- 연도 / 저자 / 학회·저널
- 분야 / 우선순위 / PDF 상태
- 핵심 문제
- 사용한 모델 / 알고리즘
- 핵심 수식 / 결과
- **우리 프로젝트에 쓸 수 있는 부분** (Phase 매핑)
- 구현 난이도 (Low / Medium / High)
- 비고

## 다음 행동

- [ ] Open Access 11편 PDF 다운로드 후 `papers/pdfs/` 서브폴더에 보관
- [ ] MVP 3편 (#19, #9, #12) 정독 — 핵심 수식을 각 .md 파일의 "핵심 수식" 섹션에 채우기
- [ ] Paywalled 논문은 기관 라이브러리로 일괄 다운로드
- [ ] #13 매핑 확인 (사용자 검증)
