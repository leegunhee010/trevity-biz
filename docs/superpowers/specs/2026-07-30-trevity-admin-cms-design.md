# 트래비티(creplanet-clone) 관리자 페이지 + Supabase CMS 설계

날짜: 2026-07-30
대상 사이트: `C:\Users\이건희\creplanet-clone` (localhost:5695, 배포: leegunhee010/creplanet-clone 추정)
참고 구현: `C:\Users\이건희\makenov\admin` (사이드바 셸 + local↔supabase 자동전환 패턴)

## 배경

- `inquiry.html`의 `SHEET_ENDPOINT`가 빈 문자열이라 문의가 저장되지 않음
- `blog.html` + `blog-market/midtier/diy/hantown.html` 4개 글이 전부 정적 HTML 하드코딩, 수정하려면 파일을 직접 고쳐야 함
- 포트폴리오 이미지(`assets/roll`, `assets/pfv`)가 6개 페이지에 흩어져 있고, 최근 실제로 6장 중 일부가 존재하지 않는 mp4를 참조해 깨졌던 사례 있음(이번 세션에서 수정)
- 위 세 가지를 makenov에서 검증된 관리자 패턴(사이드바 셸, Quill 에디터, 이미지 업로드 위젯, local↔supabase 자동전환)으로 통합 관리

## 1. 전체 구조

makenov와 동일한 이중 백엔드 패턴을 그대로 가져온다.

- `assets/js/config.js`에 `TV_SUPABASE_URL` / `TV_SUPABASE_ANON`이 비어있으면 `store.js`(localStorage)가 동작
- 값이 채워지면 `store-supabase.js`가 같은 인터페이스(`Store`, `Admin`, `TvImg`)를 덮어씀 — 렌더 코드는 손대지 않음
- **makenov와의 핵심 차이**: 트래비티는 회원(바이어) 시스템이 없다. 관리자 로그인 1개(Supabase Auth)만 존재하고, 공개 방문자는 인증 없이 문의만 INSERT 가능. makenov의 buyer/tier/사업자인증 로직은 전부 불필요.
- 새 Supabase 프로젝트를 별도로 생성(만들기 가이드는 makenov `supabase/README.md`를 트래비티용으로 각색해 제공 — 사용자가 대시보드에서 프로젝트 생성 후 URL/anon key를 `config.js`에 채우는 수동 단계 필요)

## 2. 데이터 모델

### `inquiries`
| 컬럼 | 타입 | 비고 |
|---|---|---|
| id | uuid pk | default gen_random_uuid() |
| created_at | timestamptz | default now() |
| name / company / phone / email | text | |
| message | text | |
| source_page | text | 어느 페이지에서 제출했는지(예: vietnam-tiktok.html) |
| status | text | 'new' \| 'doing' \| 'done', default 'new' |
| memo | text | 관리자 메모 |

RLS: `insert` 익명 허용(`true`). `select/update/delete`는 `is_admin()`만.

### `blog_posts`
| 컬럼 | 타입 | 비고 |
|---|---|---|
| id | uuid pk | |
| slug | text unique | URL용, 예: `market`, `midtier` |
| title | text | |
| category | text | '베트남 시장' \| '인플루언서 부킹' \| '틱톡 마케팅' \| '캠페인 사례' |
| thumbnail_url | text | |
| excerpt | text | 목록 카드용 요약 |
| body_html | text | Quill 출력 |
| read_minutes | int | |
| published | boolean | default true |
| created_at / updated_at | timestamptz | |

기존 4개 글(`blog-market.html` 등)을 시드 데이터로 이관 → **관리자에서 완전 CRUD(수정·삭제 포함)**. 구 URL(`blog-market.html` 등)은 `blog-post.html?slug=market`으로 리다이렉트하는 얇은 스텁으로 교체해 기존 링크 보존.

### `portfolio_items`
| 컬럼 | 타입 | 비고 |
|---|---|---|
| id | uuid pk | |
| media_type | text | 'image' \| 'video' |
| url | text | |
| poster_url | text | 영상일 때 썸네일 |
| alt | text | |
| sort_order | int | |
| active | boolean | default true |

지금 `assets/roll`(index.html 전용)과 `assets/pfv`(local-vn/stay/tourist-vn/tourist-cn/vietnam-tiktok 5개 페이지 공용 히어로)가 별개로 존재. **하나의 테이블로 통합**하되 `placement` 컬럼으로 어느 롤에 쓰일지 구분한다:
- `placement`: 'home-roll'(index.html) | 'hero-wall'(나머지 5개 페이지 공용)

RLS: `select` 공개. `insert/update/delete`는 관리자만.

### `packages`
| 컬럼 | 타입 | 비고 |
|---|---|---|
| id | uuid pk | |
| slug | text unique | starter / growth / dominant |
| name | text | 스타터 / 그로스 / 도미넌트 |
| influencer_count | int | 10 / 20 / 50 |
| price_krw | int | 2000000 / 4000000 / 10000000 |
| description | text | |
| sort_order | int | |

`vietnam-tiktok.html`에만 쓰임(다른 페이지엔 패키지 가격 없음 확인함). RLS: `select` 공개, 쓰기는 관리자만.

### Storage
- 버킷 `trevity-images` (public read, admin write) — 블로그 썸네일·포트폴리오 이미지 업로드용. makenov의 `product-images` 버킷과 동일한 정책 구조.

### `admins`
- makenov와 동일하게 `admins(user_id uuid)` 테이블 + `is_admin()` 함수로 RLS 판별. Supabase Authentication에서 관리자 계정 1개를 수동 생성 후 이 테이블에 등록.

## 3. 공개 페이지 변경

| 파일 | 변경 |
|---|---|
| `inquiry.html` | `SHEET_ENDPOINT` fetch 제거 → `TvStore.submitInquiry(...)`(Supabase insert)로 교체 |
| `blog.html` | 하드코딩된 4개 `<article>` 카드 제거 → 부팅 시 `blog_posts` 조회해 카드 렌더(카테고리 필터는 기존 UI 유지) |
| `blog-post.html` (신규) | `?slug=` 쿼리로 글 1건 조회해 렌더 (makenov `product.html?id=` 패턴과 동일) |
| `blog-market.html` `blog-midtier.html` `blog-diy.html` `blog-hantown.html` | 본문 대신 `blog-post.html?slug=xxx`로 즉시 리다이렉트하는 스텁으로 교체 |
| `index.html` | `.tvpf-rows` 두 줄(현재 20장 정적 img/video)을 부팅 시 `portfolio_items`(placement='home-roll') 조회 후 동일 마크업으로 렌더 |
| `local-vn.html`, `stay.html`, `tourist-vn.html`, `tourist-cn.html`, `vietnam-tiktok.html` | 히어로 영상벽(`assets/pfv` 기반 swiper-slide 마크업)을 `portfolio_items`(placement='hero-wall') 조회 후 렌더. **주의**: 확인 결과 `swiper-slide` 클래스는 실제 Swiper.js 라이브러리 없이 순수 정적 마크업(원본 Next.js 미러 잔재)이었음 — 캐러셀은 CSS만으로 동작하므로 JS는 동일한 DOM만 생성하면 되고 라이브러리 이식 불필요 |
| `vietnam-tiktok.html` | 패키지 3장(스타터/그로스/도미넌트)을 `packages` 조회 후 렌더 |

## 4. 관리자 (`/admin`)

makenov 셸 재사용(사이드바, 로그인 게이트, 카드/테이블/폼 CSS 그대로), 탭만 트래비티에 맞게 교체:

| 탭 | 내용 |
|---|---|
| 대시보드 | 누적 문의·신규/처리중/완료 건수, 최근 문의 5건 |
| 문의함 | 목록(상태 필터: 전체/신규/처리중/완료), 상태변경, 메모, CSV 내보내기 |
| 블로그 | 목록 + 작성/수정(Quill), 카테고리 선택, 발행 토글, 삭제 |
| 카피 | ① 포트폴리오 이미지 목록 — placement별 업로드·순서변경(드래그 또는 순서 입력)·삭제 ② vietnam-tiktok 패키지 3종 가격·인원·설명 수정 |
| 설정 | 관리자 비밀번호/계정, Supabase 연결 상태 표시 |

로그인은 Supabase Auth 게이트(makenov와 동일, `admins` 테이블로 판별).

## 5. 코드 구성 (신규/수정 파일)

**신규**
- `admin/index.html`, `assets/js/admin.js` — makenov 것을 뼈대로 삼되 leads/buyers/products 탭 제거, 문의함/블로그/카피로 축소
- `assets/js/config.js`, `store.js`, `store-supabase.js`, `upload.js` — makenov 것을 트래비티 스키마에 맞게 포팅
- `assets/js/site-data.js` — 공개 페이지용 렌더러(블로그 목록/상세, 포트폴리오 롤, 패키지 카드)
- `blog-post.html`
- `supabase/01_schema.sql`, `02_seed.sql`(기존 문의 4건 없음, 블로그 4건 + 현재 portfolio/package 값 시드), `03_lockdown.sql`, `README.md`

**수정**
- `inquiry.html`, `blog.html`, `index.html`, `local-vn.html`, `stay.html`, `tourist-vn.html`, `tourist-cn.html`, `vietnam-tiktok.html`

**대체(스텁화)**
- `blog-market.html`, `blog-midtier.html`, `blog-diy.html`, `blog-hantown.html`

## 6. 아직 안 하는 것 (스코프 제외)

- 문의 도착 알림(텔레그램/이메일) — makenov도 미구현, 동일하게 후속 과제로 남김
- 포트폴리오 외 다른 페이지(export/famtour 등) 카피 CMS화 — 이번엔 가격이 있는 vietnam-tiktok만
- 국세청 인증 등 makenov 특유의 바이어 인증 로직 — 트래비티엔 해당 없음
