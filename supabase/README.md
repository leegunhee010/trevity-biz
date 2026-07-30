# 트래비티 — Supabase 연결 가이드

지금 사이트는 브라우저 저장(localStorage) 모드로 돌아갑니다.
아래 순서를 마치고 `assets/js/config.js`에 값 두 개만 채우면 Supabase 모드로 바뀝니다.

## 1. 프로젝트 만들기
1. https://supabase.com 에서 계정을 만들고 New project.
2. Region은 Northeast Asia (Seoul).

## 2. 테이블 만들기
SQL Editor → New query 에 순서대로 붙여넣고 Run:
1. `supabase/01_schema.sql`
2. `supabase/02_seed.sql`
3. `supabase/04_copy.sql` — 텍스트 카피 편집 테이블

## 3. 이미지 저장소
Storage → New bucket → 이름 `trevity-images` → Public bucket 체크. 그다음 SQL Editor에서:
```sql
create policy "img_read"  on storage.objects for select using (bucket_id = 'trevity-images');
create policy "img_write" on storage.objects for insert with check (bucket_id = 'trevity-images' and is_admin());
create policy "img_del"   on storage.objects for delete using (bucket_id = 'trevity-images' and is_admin());
```

## 4. 관리자 계정
1. Authentication → Users → Add user (예: `admin@trevity.com`), **Auto Confirm User** 켜기.
2. 만들어진 사용자의 UID 복사.
3. SQL Editor: `insert into admins (user_id) values ('복사한-UID');`
4. `supabase/03_lockdown.sql` 실행.

## 5. 연결
`assets/js/config.js`:
```js
const TV_SUPABASE_URL  = 'https://xxxxxxxx.supabase.co';
const TV_SUPABASE_ANON = 'eyJhbGciOi...';
```
저장 후 새로고침하면 끝입니다.

## 확인할 것
| 확인 | 방법 | 기대 결과 |
|---|---|---|
| 문의 저장 | `inquiry.html`에서 제출, 로그아웃 상태 | `/admin` 문의함에 뜬다 |
| 블로그 CRUD | 관리자에서 글 작성/수정/삭제 | `blog.html`에 즉시 반영 |
| 이미지 업로드 | 관리자에서 사진 업로드 | Storage에 파일 생기고 사이트에 뜬다 |
