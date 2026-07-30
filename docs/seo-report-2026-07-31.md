# 트래비티 SEO / GEO / AEO 평가 리포트 (2026-07-31)

측정 도구: `_score_seo.py` (인천 퍼스트디자인 스코어러 각색 — 재실행 가능)
SEO = 검색엔진 기본기 · GEO = 회사 엔티티/지역 신호 · AEO = AI·답변엔진 인용 최적화

## 개선 전 → 후 (평균)

| | 개선 전 | 개선 후 |
|---|---|---|
| SEO | 79 | **96** |
| GEO | 54 | **83** |
| AEO | 52 | **61** |

## 이번에 자동으로 고친 것 (HTML에 구움)

1. **이미지 alt 209개 채움** — index 95장 등, 롤/히어로/서비스 이미지에 맥락 기반 alt (`트래비티 인플루언서 캠페인 콘텐츠` 등)
2. **OG 대표이미지 전 페이지 설정** — `assets/tvhero/hero_bg_pink.jpg` (SEO 관리에서 언제든 교체 가능)
3. **블로그 글 4건 강화** — BreadcrumbList 구조화데이터 + keywords + og:image(썸네일)
4. **Organization + LocalBusiness 구조화데이터 전 페이지 확장** (기존엔 메인만 — 인천과 동일 방식)
5. **구 페이지 삭제** — tourist.html·local.html (어디서도 링크 안 됨) + sitemap·카피목록 정리

## 최종 점수표

| 페이지 | SEO | GEO | AEO |
|---|---|---|---|
| index.html | 95 | 100 | 30 |
| vietnam-tiktok.html | 95 | 100 | **100** |
| tourist-vn / tourist-cn / local-vn | 95 | 100 | **100** |
| stay.html | 95 | 80 | **100** |
| experience / export / famtour | 100 | 100 | 50 |
| about.html | 100 | 80 | 50 |
| agency / help | 95~100 | 100 | 60 |
| blog.html | 100 | 80 | 40 |
| inquiry.html | 100 | 80 | 40 |
| blog-* (글 4건) | 87~92 | 40~60 | 40 |

## 남은 개선 항목 (사람 판단 필요 — 자동으로 안 건드림)

### 우선순위 높음
1. **메인(index) AEO 30점** — 메인에 FAQ 섹션이 없음. "트래비티는 어떤 회사인가요 / 비용은 얼마인가요" 류 4문답만 넣으면 FAQPage 구조화데이터가 자동으로 붙어 AEO 30→90 가능. 게시판·화면편집으로 콘텐츠만 넣으면 됨.
2. **H1 다중(대부분 페이지 2~3개)** — 모바일/PC용 h1이 중복 마크업. 원본 미러 구조라 일괄 수정은 레이아웃 리스크가 있어 보류. 신규 페이지부터 h1 1개 원칙 권장.
3. **블로그 글 요약(description) 확장** — midtier 글 요약이 30자로 짧음. 게시판에서 요약을 60~120자로 다듬으면 SEO 만점.

### 우선순위 중간
4. **experience/export/famtour/about에 Q&A 블록 추가** — FAQ 4문답씩 넣으면 AEO 50→90.
5. **about/blog/inquiry 제목·설명에 타겟 지역(베트남 등) 키워드 반영** — GEO 80→100. SEO 관리 탭에서 문구만 수정.
6. **블로그 글에 소제목(H2) 사용** — 기존 4글 본문이 문단 나열. 게시판에서 `<h2>` 소제목 추가하면 AEO 상승 + 가독성.

### 배포 시 할 일
- 실도메인 확정되면 SEO 관리 → 도메인 변경 → "전체 굽기 실행" 한 번 (canonical/sitemap 일괄 갱신)
- 네이버 서치어드바이저 / 구글 서치콘솔 소유확인 메타태그 → SEO 관리 → Head 코드에 붙여넣기
- sitemap.xml을 양쪽 콘솔에 제출

재평가: `python _score_seo.py` (페이지별 상세: `python _score_seo.py index.html`)
