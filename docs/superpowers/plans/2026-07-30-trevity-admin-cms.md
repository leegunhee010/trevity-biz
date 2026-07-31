# 트래비티 관리자 페이지 + Supabase CMS Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `/admin` console + Supabase-backed CMS to the creplanet-clone (Trevity) site that manages inquiries, blog posts, portfolio media, and vietnam-tiktok.html package pricing, replacing hardcoded HTML and the broken Google-Sheets inquiry endpoint.

**Architecture:** Port the makenov admin pattern (`C:\Users\이건희\makenov\admin`, `assets/js/{config,store,store-supabase,upload,admin}.js`) into creplanet-clone, trimmed to Trevity's scope (no buyer/member tiers — one admin login only). `config.js` toggles between `store.js` (localStorage) and `store-supabase.js` (real backend) by whether Supabase keys are filled in — render code always reads the same synchronous global arrays (`TV_BLOG_POSTS`, `TV_PORTFOLIO`, `TV_PACKAGES`) regardless of backend.

**Tech Stack:** Vanilla JS (no build step, no framework — matches the rest of the static site), Supabase (Postgres + Auth + Storage), Quill 2.0.3 (CDN) for the blog rich-text editor, Python `http.server` for local preview (already wired at port 5695 in `.claude/launch.json`).

## Global Constraints

- No test framework exists anywhere in this project or its sibling projects (makenov, dfirst-*, hao*) — verification is via `curl`/`grep` against the static HTML/JS output and manual browser checks through the Browser preview tools. Every task's "test" steps follow that convention, not a unit-test framework.
- Site is 100% static HTML/CSS/JS served via `python -m http.server` and deployed to GitHub Pages — no server-side code except Supabase Edge/RLS. Do not introduce a build step.
- Brand primary color is `#fa6781` (coral pink) — confirmed from `blog.html`'s `.tvwhy-label{color:#fa6781}`. Use this (not makenov's mint `#27CAA1`) for all new admin/public UI.
- Trevity has **no buyer/member accounts**. Only a single admin login (Supabase Auth + `admins` table). Do not port makenov's buyer signup/tier/사업자인증 logic — it does not apply.
- `anon` key is meant to be public or in client code; RLS enforces security. Never put a `service_role` key in any file under `creplanet-clone/`.
- Existing bug fixes already applied this session (do not revert): `index.html`'s `.tvpf-rows` no longer references `assets/roll/v5.mp4` etc (uses jpg instead); `blog.html`'s hero subtitle no longer says "베트남 시장과..." — it says "인플루언서 마케팅과 틱톡 캠페인,...".
- Reference source for porting: `C:\Users\이건희\makenov\admin\index.html`, `C:\Users\이건희\makenov\assets\js\{config,store,store-supabase,upload,admin}.js`, `C:\Users\이건희\makenov\supabase\{01_schema.sql,03_lockdown.sql,README.md}`. Read the exact section referenced before porting it — do not guess at makenov's code.

---

## Task 1: Supabase schema, seed data, RLS lockdown, setup guide

**Files:**
- Create: `C:\Users\이건희\creplanet-clone\supabase\01_schema.sql`
- Create: `C:\Users\이건희\creplanet-clone\supabase\02_seed.sql`
- Create: `C:\Users\이건희\creplanet-clone\supabase\03_lockdown.sql`
- Create: `C:\Users\이건희\creplanet-clone\supabase\README.md`

**Interfaces:**
- Produces: tables `inquiries`, `blog_posts`, `portfolio_items`, `packages`, `admins`; function `is_admin()`; storage bucket `trevity-images`. All later tasks (store-supabase.js, admin.js, site-data.js) query these exact table/column names.

- [ ] **Step 1: Write `01_schema.sql`**

```sql
-- 트래비티 관리자 CMS 스키마
create extension if not exists pgcrypto;

-- ---------- admins ----------
create table admins (
  user_id uuid primary key references auth.users(id) on delete cascade
);

create or replace function is_admin() returns boolean as $$
  select exists(select 1 from admins where user_id = auth.uid());
$$ language sql stable security definer;

-- ---------- inquiries ----------
create table inquiries (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  name text not null default '',
  company text not null default '',
  phone text not null default '',
  email text not null default '',
  message text not null default '',
  source_page text not null default '',
  status text not null default 'new' check (status in ('new','doing','done')),
  memo text not null default ''
);
alter table inquiries enable row level security;
create policy "inq_insert_public" on inquiries for insert with check (true);
create policy "inq_all_admin" on inquiries for select using (is_admin());
create policy "inq_update_admin" on inquiries for update using (is_admin());
create policy "inq_delete_admin" on inquiries for delete using (is_admin());

-- ---------- blog_posts ----------
create table blog_posts (
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,
  title text not null default '',
  category text not null default '' check (category in ('베트남 시장','인플루언서 부킹','틱톡 마케팅','캠페인 사례')),
  thumbnail_url text not null default '',
  excerpt text not null default '',
  body_html text not null default '',
  read_minutes int not null default 4,
  published boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
alter table blog_posts enable row level security;
create policy "blog_select_published" on blog_posts for select using (published = true or is_admin());
create policy "blog_write_admin" on blog_posts for insert with check (is_admin());
create policy "blog_update_admin" on blog_posts for update using (is_admin());
create policy "blog_delete_admin" on blog_posts for delete using (is_admin());

-- ---------- portfolio_items ----------
create table portfolio_items (
  id uuid primary key default gen_random_uuid(),
  placement text not null check (placement in ('home-roll','hero-wall')),
  media_type text not null check (media_type in ('image','video')),
  url text not null default '',
  poster_url text not null default '',
  alt text not null default '',
  sort_order int not null default 0,
  active boolean not null default true
);
alter table portfolio_items enable row level security;
create policy "pf_select_active" on portfolio_items for select using (active = true or is_admin());
create policy "pf_write_admin" on portfolio_items for insert with check (is_admin());
create policy "pf_update_admin" on portfolio_items for update using (is_admin());
create policy "pf_delete_admin" on portfolio_items for delete using (is_admin());

-- ---------- packages ----------
create table packages (
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,
  name text not null default '',
  influencer_count int not null default 0,
  price_krw int not null default 0,
  description text not null default '',
  sort_order int not null default 0
);
alter table packages enable row level security;
create policy "pkg_select_public" on packages for select using (true);
create policy "pkg_write_admin" on packages for insert with check (is_admin());
create policy "pkg_update_admin" on packages for update using (is_admin());
create policy "pkg_delete_admin" on packages for delete using (is_admin());
```

- [ ] **Step 2: Write `02_seed.sql`** (migrates the 4 existing hardcoded blog posts, current package prices from `vietnam-tiktok.html` HANDOFF section 3, and a placeholder portfolio row per placement so the site never renders an empty roll)

```sql
insert into blog_posts (slug, title, category, thumbnail_url, excerpt, body_html, read_minutes, published, created_at) values
('market', '동남아 틱톡 사용률 2위, 베트남 시장이 특별한 이유', '베트남 시장',
 './images/blog/thumb-market.png', '동남아에서 틱톡 사용률 2위인 베트남 시장이 왜 특별한지 살펴봅니다.',
 '<p>동남아에서 틱톡 사용률 2위인 베트남 시장이 왜 특별한지 살펴봅니다.</p>', 4, true, '2026-07-21'),
('midtier', '팔로워 10만~50만, 왜 이 구간이 가장 효율적일까요?', '인플루언서 부킹',
 './images/about-tiktok.png', '팔로워 10만~50만 구간 인플루언서가 캠페인에 가장 효율적인 이유입니다.',
 '<p>팔로워 10만~50만 구간 인플루언서가 캠페인에 가장 효율적인 이유입니다.</p>', 4, true, '2026-07-20'),
('diy', 'DIY 인플루언서 섭외, 왜 오히려 더 비쌀까요?', '인플루언서 부킹',
 './images/blog/thumb-diy.png', '직접 섭외가 대행보다 왜 더 비용이 드는지 비교합니다.',
 '<p>직접 섭외가 대행보다 왜 더 비용이 드는지 비교합니다.</p>', 4, true, '2026-07-19'),
('hantown', '베트남 한인타운, 왜 로컬 마케팅의 시작점일까요?', '캠페인 사례',
 './images/blog/thumb-hantown.png', '베트남 한인타운 상권의 로컬 마케팅 사례를 소개합니다.',
 '<p>베트남 한인타운 상권의 로컬 마케팅 사례를 소개합니다.</p>', 4, true, '2026-07-18');

insert into packages (slug, name, influencer_count, price_krw, description, sort_order) values
('starter', '스타터', 10, 2000000, '인플루언서 10명 부킹, 부가세 별도', 1),
('growth', '그로스', 20, 4000000, '인플루언서 20명 부킹, 부가세 별도', 2),
('dominant', '도미넌트', 50, 10000000, '인플루언서 50명 부킹, 부가세 별도', 3);

insert into portfolio_items (placement, media_type, url, poster_url, alt, sort_order, active) values
('home-roll', 'image', './assets/roll/1.jpg', '', '', 1, true),
('hero-wall', 'video', './assets/pfv/s01.mp4', './assets/pfv/s01.jpg', '트래비티 인플루언서 콘텐츠', 1, true);
```

- [ ] **Step 3: Write `03_lockdown.sql`** (blocks a signed-up-but-not-admin user from self-granting admin — mirrors makenov's `03_lockdown.sql` intent, adapted: since Trevity has no public signup at all, the only lockdown needed is making sure `admins` itself can't be written by non-admins)

```sql
alter table admins enable row level security;
create policy "admins_select_self" on admins for select using (auth.uid() = user_id);
-- no insert/update/delete policy for admins on purpose: only editable via SQL editor / service_role,
-- so no client (even a logged-in one) can ever add themselves as admin.
```

- [ ] **Step 4: Write `README.md`** (adapt `makenov/supabase/README.md`, dropping the buyer-signup, NTS/edge-function, and product_terms sections which don't apply to Trevity)

```markdown
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
```

- [ ] **Step 5: Verify SQL has no syntax errors before Supabase exists** (static check only — actual execution happens once the user creates the project, which is a manual step outside this plan)

Run: `grep -c "create table\|create policy\|insert into" "C:\Users\이건희\creplanet-clone\supabase\01_schema.sql" "C:\Users\이건희\creplanet-clone\supabase\02_seed.sql" "C:\Users\이건희\creplanet-clone\supabase\03_lockdown.sql"`
Expected: non-zero counts in each file, no shell errors.

- [ ] **Step 6: Commit**

```bash
cd "C:\Users\이건희\creplanet-clone"
git add supabase/01_schema.sql supabase/02_seed.sql supabase/03_lockdown.sql supabase/README.md
git commit -m "feat(admin): add Supabase schema, seed data, and setup guide for CMS"
```

---

## Task 2: `config.js` + `store.js` (localStorage backend)

**Files:**
- Create: `C:\Users\이건희\creplanet-clone\assets\js\config.js`
- Create: `C:\Users\이건희\creplanet-clone\assets\js\store.js`

**Interfaces:**
- Consumes: nothing (first JS file loaded)
- Produces: `TV_BACKEND` ('local'|'supabase'), `TV_SUPABASE_URL`, `TV_SUPABASE_ANON` globals. `Store.submitInquiry(data)`, `Store.allInquiries()`, `Store.allBlogPosts()`, `Store.blogPost(slug)`, `Store.allPortfolio()`, `Store.allPackages()` — all consumed by `site-data.js` (Task 11) and `admin.js` (Tasks 6-10). `Admin.login(pw)`, `Admin.isIn()`, `Admin.logout()`, `Admin.upsertInquiry/deleteInquiry/setInquiryStatus`, `Admin.upsertBlogPost/deleteBlogPost`, `Admin.upsertPortfolioItem/deletePortfolioItem/movePortfolioItem`, `Admin.upsertPackage` — consumed by `admin.js`.

- [ ] **Step 1: Write `config.js`**

```js
/* ============================================================
   트래비티 관리자 백엔드 설정
   ------------------------------------------------------------
   아래 두 값을 채우면 자동으로 Supabase 모드로 전환됩니다.
   비워두면 브라우저 저장(localStorage) 모드로 동작합니다.
   값 찾는 곳: Supabase 대시보드 → Project Settings → API
   ============================================================ */
const TV_SUPABASE_URL  = '';
const TV_SUPABASE_ANON = '';

const TV_BACKEND = (TV_SUPABASE_URL && TV_SUPABASE_ANON) ? 'supabase' : 'local';
```

- [ ] **Step 2: Write `store.js`**

```js
/* 트래비티 store — localStorage MVP. Supabase 키를 채우면 store-supabase.js가 이 인터페이스를 덮어쓴다. */
function tvId(prefix){ return prefix + '_' + Date.now().toString(36) + Math.floor(Math.random()*1e6).toString(36); }
function tvRead(key, fallback){ try{ return JSON.parse(localStorage.getItem(key) || JSON.stringify(fallback)); }catch(e){ return fallback; } }
function tvWrite(key, val){ localStorage.setItem(key, JSON.stringify(val)); }

const Store = {
  /* ---- 문의: 공개 방문자가 씀 ---- */
  async submitInquiry(data){
    const list = tvRead('tv_inquiries', []);
    list.unshift({
      id: tvId('inq'), created_at: new Date().toISOString(),
      name: data.name||'', company: data.company||'', phone: data.phone||'',
      email: data.email||'', message: data.message||'', source_page: data.source_page||'',
      status: 'new', memo: '',
    });
    tvWrite('tv_inquiries', list);
    return { ok:true };
  },
  async allInquiries(){ return tvRead('tv_inquiries', []); },

  async allBlogPosts(){ return TV_BLOG_POSTS; },
  async blogPost(slug){ return TV_BLOG_POSTS.find(p=>p.slug===slug) || null; },

  async allPortfolio(){ return TV_PORTFOLIO; },
  async allPackages(){ return TV_PACKAGES; },
};

const Admin = {
  DEFAULT_PW: 'trevity2026',
  _hash(s){ let h=5381; for(let i=0;i<s.length;i++) h=((h<<5)+h+s.charCodeAt(i))|0; return String(h); },
  password(){ return localStorage.getItem('tv_admin_pw') || this._hash(this.DEFAULT_PW); },
  login(pw){
    if(this._hash(pw) !== this.password()) return false;
    sessionStorage.setItem('tv_admin_in','1'); return true;
  },
  changePassword(pw){ localStorage.setItem('tv_admin_pw', this._hash(pw)); },
  isIn(){ return sessionStorage.getItem('tv_admin_in')==='1'; },
  logout(){ sessionStorage.removeItem('tv_admin_in'); },

  /* ---- 문의 처리 ---- */
  async setInquiryStatus(id, status){
    const list = tvRead('tv_inquiries', []);
    const i = list.findIndex(x=>x.id===id); if(i>=0) list[i].status = status;
    tvWrite('tv_inquiries', list);
  },
  async setInquiryMemo(id, memo){
    const list = tvRead('tv_inquiries', []);
    const i = list.findIndex(x=>x.id===id); if(i>=0) list[i].memo = memo;
    tvWrite('tv_inquiries', list);
  },
  async deleteInquiry(id){
    tvWrite('tv_inquiries', tvRead('tv_inquiries', []).filter(x=>x.id!==id));
  },

  /* ---- 블로그 CRUD (오버라이드는 TV_BLOG_POSTS 위에 얹는다) ---- */
  saveBlogPosts(list){ tvWrite('tv_blog_override', list); TV_BLOG_POSTS.length = 0; TV_BLOG_POSTS.push(...list); },
  async upsertBlogPost(p){
    const list = [...TV_BLOG_POSTS];
    const i = list.findIndex(x=>x.slug===p.slug);
    if(i>=0) list[i] = {...list[i], ...p, updated_at:new Date().toISOString()};
    else list.unshift({...p, created_at:new Date().toISOString(), updated_at:new Date().toISOString()});
    this.saveBlogPosts(list);
  },
  async deleteBlogPost(slug){ this.saveBlogPosts(TV_BLOG_POSTS.filter(p=>p.slug!==slug)); },

  /* ---- 포트폴리오 CRUD ---- */
  savePortfolio(list){ tvWrite('tv_portfolio_override', list); TV_PORTFOLIO.length = 0; TV_PORTFOLIO.push(...list); },
  async upsertPortfolioItem(item){
    const list = [...TV_PORTFOLIO];
    const i = list.findIndex(x=>x.id===item.id);
    if(i>=0) list[i] = {...list[i], ...item};
    else list.push({...item, id: item.id || tvId('pf'), sort_order: list.length});
    this.savePortfolio(list);
  },
  async deletePortfolioItem(id){ this.savePortfolio(TV_PORTFOLIO.filter(x=>x.id!==id)); },
  async movePortfolioItem(id, dir){
    const list = [...TV_PORTFOLIO];
    const i = list.findIndex(x=>x.id===id);
    const j = i + dir;
    if(i<0 || j<0 || j>=list.length) return;
    [list[i], list[j]] = [list[j], list[i]];
    list.forEach((x,idx)=>x.sort_order = idx);
    this.savePortfolio(list);
  },

  /* ---- 패키지 CRUD (3종 고정 slug, 수정만) ---- */
  savePackages(list){ tvWrite('tv_packages_override', list); TV_PACKAGES.length = 0; TV_PACKAGES.push(...list); },
  async upsertPackage(p){
    const list = [...TV_PACKAGES];
    const i = list.findIndex(x=>x.slug===p.slug);
    if(i>=0) list[i] = {...list[i], ...p}; else list.push(p);
    this.savePackages(list);
  },
};
```

- [ ] **Step 3: Verify no JS syntax errors**

Run: `node --check "C:\Users\이건희\creplanet-clone\assets\js\config.js" && node --check "C:\Users\이건희\creplanet-clone\assets\js\store.js"`
Expected: no output, exit code 0.

- [ ] **Step 4: Commit**

```bash
cd "C:\Users\이건희\creplanet-clone"
git add assets/js/config.js assets/js/store.js
git commit -m "feat(admin): add config toggle and localStorage store backend"
```

---

## Task 3: `upload.js` (image compression + storage, simplified from makenov)

**Files:**
- Create: `C:\Users\이건희\creplanet-clone\assets\js\upload.js`

**Interfaces:**
- Consumes: nothing
- Produces: `TvImg.save(file) -> {ref, dataUrl, w, h, bytes}`, `TvImg.isRef(v)`, `TvImg.resolve(v)`, `TvImg.usage()`, `TvImg.gc()`, `fmtBytes(n)` — consumed by `admin.js` uploader widget (Task 6) and overridden by `store-supabase.js` (Task 4) in Supabase mode.

**Note:** Trevity has no tall-detail-page images (makenov's `sliceTall`/`DETAIL_MAXW`/`isTall` existed only for 848×17000-style product detail pages). Drop that entirely — YAGNI. Blog thumbnails and portfolio photos are normal aspect ratio.

- [ ] **Step 1: Write `upload.js`** (ported from `C:\Users\이건희\makenov\assets\js\upload.js` lines 9-94 and 130-240, with `sliceTall`/`saveDetail`/`isTall`/`DETAIL_*` removed and `MkImg`→`TvImg`, `makenov_img`→`trevity_img`, `mkimg:`→`tvimg:`)

```js
/* ============================================================
   트래비티 이미지 업로드 — 관리자에서 파일을 직접 올린다.
   서버가 없는 로컬 모드: 브라우저에서 리사이즈·압축 후 IndexedDB에 저장,
   데이터에는 'tvimg:<id>' 참조만 넣고 부팅 시 실제 이미지로 치환.
   Supabase 모드에서는 store-supabase.js가 _store()만 갈아끼워 Storage로 올린다.
   ============================================================ */
const TvImg = {
  DB: 'trevity_img', STORE: 'img',
  MAXW: 1600,
  QUALITY: 0.86,
  _db: null,
  _cache: {},

  open(){
    if(this._db) return Promise.resolve(this._db);
    return new Promise((res, rej)=>{
      const rq = indexedDB.open(this.DB, 1);
      rq.onupgradeneeded = e => {
        const db = e.target.result;
        if(!db.objectStoreNames.contains(this.STORE)) db.createObjectStore(this.STORE);
      };
      rq.onsuccess = e => { this._db = e.target.result; res(this._db); };
      rq.onerror   = e => rej(e.target.error);
    });
  },
  async _tx(mode, fn){
    const db = await this.open();
    return new Promise((res, rej)=>{
      const tx = db.transaction(this.STORE, mode);
      const rq = fn(tx.objectStore(this.STORE));
      rq.onsuccess = () => res(rq.result);
      rq.onerror   = () => rej(rq.error);
    });
  },
  put(id, dataUrl){ return this._tx('readwrite', s => s.put(dataUrl, id)); },
  get(id){         return this._tx('readonly',  s => s.get(id)); },
  del(id){         return this._tx('readwrite', s => s.delete(id)); },
  keys(){          return this._tx('readonly',  s => s.getAllKeys()); },
  values(){        return this._tx('readonly',  s => s.getAll()); },

  _load(file){
    return new Promise((res, rej)=>{
      if(!/^image\//.test(file.type)) return rej(new Error('이미지 파일만 올릴 수 있습니다'));
      const fr = new FileReader();
      fr.onerror = () => rej(new Error('파일을 읽지 못했습니다'));
      fr.onload = () => {
        const img = new Image();
        img.onerror = () => rej(new Error('이미지를 열지 못했습니다'));
        img.onload = () => res(img);
        img.src = fr.result;
      };
      fr.readAsDataURL(file);
    });
  },

  async compress(file){
    const img = await this._load(file);
    const keepAlpha = /png|webp|svg/i.test(file.type);
    const scale = Math.min(1, this.MAXW / img.width);
    const w = Math.round(img.width * scale);
    const h = Math.round(img.height * scale);
    const cv = document.createElement('canvas');
    cv.width = w; cv.height = h;
    const cx = cv.getContext('2d');
    cx.imageSmoothingQuality = 'high';
    if(!keepAlpha){ cx.fillStyle = '#fff'; cx.fillRect(0,0,w,h); }
    cx.drawImage(img, 0, 0, w, h);
    const out = keepAlpha ? cv.toDataURL('image/png') : cv.toDataURL('image/jpeg', this.QUALITY);
    return { dataUrl: out, w, h, bytes: Math.round(out.length * 0.75) };
  },

  _newId(){
    return 'i' + Date.now().toString(36) + Math.floor(Math.random()*1e6).toString(36);
  },
  async _store(dataUrl){
    const id = this._newId();
    await this.put(id, dataUrl);
    this._cache[id] = dataUrl;
    return 'tvimg:' + id;
  },
  async save(file){
    const { dataUrl, w, h, bytes } = await this.compress(file);
    const ref = await this._store(dataUrl);
    return { ref, dataUrl, w, h, bytes };
  },

  isRef(v){ return typeof v === 'string' && v.startsWith('tvimg:'); },
  resolve(v){ if(!this.isRef(v)) return v; return this._cache[v.slice(6)] || ''; },

  async loadCache(){
    try{
      const [keys, vals] = await Promise.all([this.keys(), this.values()]);
      keys.forEach((k,i)=>{ this._cache[k] = vals[i]; });
      return true;
    }catch(e){ return false; }
  },

  async usage(){
    let used = 0, count = 0;
    try{ const vals = await this.values(); count = vals.length; vals.forEach(v => used += v.length * 0.75); }catch(e){}
    let quota = 0;
    try{ const est = await navigator.storage.estimate(); quota = est.quota || 0; }catch(e){}
    return { count, used, quota };
  },

  async gc(){
    const used = new Set();
    const walk = obj => {
      if(!obj || typeof obj !== 'object') return;
      Object.values(obj).forEach(v=>{
        if(typeof v === 'string'){ if(this.isRef(v)) used.add(v.slice(6)); }
        else walk(v);
      });
    };
    ['tv_blog_override','tv_portfolio_override'].forEach(k=>{
      try{ walk(JSON.parse(localStorage.getItem(k)||'null')); }catch(e){}
    });
    const keys = await this.keys();
    const dead = keys.filter(k=>!used.has(k));
    for(const k of dead){ await this.del(k); delete this._cache[k]; }
    return dead.length;
  },
};

function fmtBytes(n){
  if(n < 1024) return n + ' B';
  if(n < 1024*1024) return (n/1024).toFixed(0) + ' KB';
  return (n/1024/1024).toFixed(1) + ' MB';
}
```

- [ ] **Step 2: Verify no JS syntax errors**

Run: `node --check "C:\Users\이건희\creplanet-clone\assets\js\upload.js"`
Expected: no output, exit code 0.

- [ ] **Step 3: Commit**

```bash
cd "C:\Users\이건희\creplanet-clone"
git add assets/js/upload.js
git commit -m "feat(admin): add image upload/compression widget backend"
```

---

## Task 4: `store-supabase.js` (Supabase backend override)

**Files:**
- Create: `C:\Users\이건희\creplanet-clone\assets\js\store-supabase.js`

**Interfaces:**
- Consumes: `TV_BACKEND`, `TV_SUPABASE_URL`, `TV_SUPABASE_ANON` (Task 2), `Store`/`Admin`/`TvImg` objects to override (Tasks 2-3), global `supabase` (loaded via CDN script tag in Task 5's `admin/index.html` and in every public page that needs `TvData.boot()`).
- Produces: `TvData` global with `.boot()`, `.admin` (bool), `.session`; overrides `Store.*`/`Admin.*`/`TvImg._store` to hit Supabase when `TV_BACKEND==='supabase'`.

- [ ] **Step 1: Write `store-supabase.js`** (ported from `C:\Users\이건희\makenov\assets\js\store-supabase.js` lines 1-15 and the `_store`/Storage override at lines 383-410, with the buyer/profile/tier/leads logic removed since Trevity has no buyer accounts)

```js
/* ============================================================
   트래비티 — Supabase 백엔드
   config.js 에 URL/키가 채워져 있을 때만 동작하며, store.js(localStorage)의
   Store / Admin / TvImg 를 같은 인터페이스로 덮어씁니다.
   ============================================================ */
if (typeof TV_BACKEND !== 'undefined' && TV_BACKEND === 'supabase') {

const SB = supabase.createClient(TV_SUPABASE_URL, TV_SUPABASE_ANON, {
  auth: { persistSession: true, autoRefreshToken: true },
});
window.SB = SB;

const TvData = {
  session: null,
  admin: false,

  async boot(){
    const { data:{ session } } = await SB.auth.getSession();
    this.session = session;
    if(session){
      const { data:adm } = await SB.from('admins').select('user_id').eq('user_id', session.user.id).maybeSingle();
      this.admin = !!adm;
    }
    await this.loadContent();
  },

  async loadContent(){
    const [bp, pf, pk] = await Promise.all([
      SB.from('blog_posts').select('*').eq('published', true).order('created_at', {ascending:false}),
      SB.from('portfolio_items').select('*').eq('active', true).order('sort_order'),
      SB.from('packages').select('*').order('sort_order'),
    ]);
    if(bp.error) console.error('트래비티 콘텐츠 로드 실패(blog_posts)', bp.error);
    if(pf.error) console.error('트래비티 콘텐츠 로드 실패(portfolio_items)', pf.error);
    if(pk.error) console.error('트래비티 콘텐츠 로드 실패(packages)', pk.error);

    TV_BLOG_POSTS.length = 0;
    (bp.data||[]).forEach(p => TV_BLOG_POSTS.push(p));
    TV_PORTFOLIO.length = 0;
    (pf.data||[]).forEach(p => TV_PORTFOLIO.push(p));
    TV_PACKAGES.length = 0;
    (pk.data||[]).forEach(p => TV_PACKAGES.push(p));
  },
};
window.TvData = TvData;

Object.assign(Store, {
  async submitInquiry(data){
    const { error } = await SB.from('inquiries').insert({
      name: data.name||'', company: data.company||'', phone: data.phone||'',
      email: data.email||'', message: data.message||'', source_page: data.source_page||'',
    });
    if(error) return { ok:false, err: error.message };
    return { ok:true };
  },
  async allInquiries(){
    const { data, error } = await SB.from('inquiries').select('*').order('created_at', {ascending:false});
    if(error){ console.error(error); return []; }
    return data;
  },
  async allBlogPosts(){ return TV_BLOG_POSTS; },
  async blogPost(slug){
    if(TvData.admin){
      const { data } = await SB.from('blog_posts').select('*').eq('slug', slug).maybeSingle();
      return data || null;
    }
    return TV_BLOG_POSTS.find(p=>p.slug===slug) || null;
  },
  async allPortfolio(){ return TV_PORTFOLIO; },
  async allPackages(){ return TV_PACKAGES; },
});

Object.assign(Admin, {
  isIn(){ return !!TvData.session && TvData.admin; },
  async loginEmail(email, pw){
    const { error } = await SB.auth.signInWithPassword({ email, password: pw });
    if(error) return { ok:false, err:error.message };
    await TvData.boot();
    if(!TvData.admin){ await SB.auth.signOut(); return { ok:false, err:'관리자 계정이 아닙니다' }; }
    return { ok:true };
  },
  async logout(){ await SB.auth.signOut(); TvData.session=null; TvData.admin=false; },

  async setInquiryStatus(id, status){ await SB.from('inquiries').update({status}).eq('id', id); },
  async setInquiryMemo(id, memo){ await SB.from('inquiries').update({memo}).eq('id', id); },
  async deleteInquiry(id){ await SB.from('inquiries').delete().eq('id', id); },

  async upsertBlogPost(p){
    const { error } = await SB.from('blog_posts').upsert({
      ...p, updated_at: new Date().toISOString(),
    }, { onConflict: 'slug' });
    if(error) throw new Error(error.message);
  },
  async deleteBlogPost(slug){ await SB.from('blog_posts').delete().eq('slug', slug); },

  async upsertPortfolioItem(item){
    const { error } = await SB.from('portfolio_items').upsert(item);
    if(error) throw new Error(error.message);
  },
  async deletePortfolioItem(id){ await SB.from('portfolio_items').delete().eq('id', id); },
  async movePortfolioItem(id, dir){
    const list = [...TV_PORTFOLIO];
    const i = list.findIndex(x=>x.id===id);
    const j = i + dir;
    if(i<0 || j<0 || j>=list.length) return;
    [list[i], list[j]] = [list[j], list[i]];
    await Promise.all(list.map((x,idx)=> SB.from('portfolio_items').update({sort_order:idx}).eq('id', x.id)));
  },

  async upsertPackage(p){
    const { error } = await SB.from('packages').upsert(p, { onConflict: 'slug' });
    if(error) throw new Error(error.message);
  },
});

const BUCKET = 'trevity-images';
Object.assign(TvImg, {
  async _store(dataUrl){
    const blob = await (await fetch(dataUrl)).blob();
    const ext  = blob.type === 'image/png' ? 'png' : 'jpg';
    const path = `${new Date().getFullYear()}/${Date.now().toString(36)}${Math.floor(Math.random()*1e9).toString(36)}.${ext}`;
    const { error } = await SB.storage.from(BUCKET).upload(path, blob, {
      contentType: blob.type, cacheControl: '31536000', upsert: false,
    });
    if(error) throw new Error('업로드 실패: ' + error.message);
    return SB.storage.from(BUCKET).getPublicUrl(path).data.publicUrl;
  },
  isRef(){ return false; },
  resolve(v){ return v; },
  async loadCache(){ return true; },
  async usage(){ return { count:0, used:0, quota:0 }; },
  async gc(){ return 0; },
});

}
```

- [ ] **Step 2: Verify no JS syntax errors**

Run: `node --check "C:\Users\이건희\creplanet-clone\assets\js\store-supabase.js"`
Expected: no output, exit code 0.

- [ ] **Step 3: Commit**

```bash
cd "C:\Users\이건희\creplanet-clone"
git add assets/js/store-supabase.js
git commit -m "feat(admin): add Supabase backend override for store/admin/image upload"
```

---

## Task 5: `data.js` (global content arrays) + `admin/index.html` shell

**Files:**
- Create: `C:\Users\이건희\creplanet-clone\assets\js\data.js`
- Create: `C:\Users\이건희\creplanet-clone\admin\index.html`

**Interfaces:**
- Consumes: none directly (data.js loads before store.js so `TV_BLOG_POSTS` etc exist when store.js references them — verify script order in Step 3)
- Produces: `TV_BLOG_POSTS`, `TV_PORTFOLIO`, `TV_PACKAGES` (empty arrays, filled by `store.js`'s override read or `store-supabase.js`'s `loadContent()`). `admin/index.html` produces the DOM elements `admin.js` (Task 6+) targets: `#gate`, `#gate-pw`, `#gate-err`, `#app`, `#sb-nav`, `#pg-title`, `#pg-desc`, `#tab-dash`, `#tab-inq`, `#tab-blog`, `#tab-copy`, `#tab-settings`.

- [ ] **Step 1: Write `data.js`**

```js
/* 트래비티 콘텐츠 전역 배열 — store.js/store-supabase.js가 채운다. 렌더 코드는 이 배열만 읽는다. */
const TV_BLOG_POSTS = [];
const TV_PORTFOLIO = [];
const TV_PACKAGES = [];
```

- [ ] **Step 2: Create `admin/index.html`** (ported layout from `C:\Users\이건희\makenov\admin\index.html` — same sidebar-shell CSS structure, but: (a) all CSS vars self-contained instead of importing `../assets/css/style.css` which doesn't exist in this project — creplanet-clone's own styling lives in compiled Tailwind under `_next/`, confirmed via `HANDOFF.md`-equivalent inspection this session; (b) `--mk-primary` mint `#27CAA1` → `--tv-primary` coral `#fa6781` (confirmed site brand color from `blog.html`); (c) nav trimmed to 5 tabs: 대시보드/문의함/블로그/카피/설정)

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TREVITY 관리자</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/quill@2.0.3/dist/quill.snow.css">
<link rel="icon" href="../trevity-logo.png">
<style>
:root{
  --tv-primary:#fa6781; --tv-primary-dark:#e0536c; --tv-primary-soft:#fff0f3;
  --tv-danger:#E03131; --r-pill:999px;
  --font-body:'Pretendard',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;
  --sb-w:236px; --adm-bg:#F6F7F9; --adm-line:#E5E8EB; --adm-ink:#191F28; --adm-sub:#8B95A1;
}
*{box-sizing:border-box}
body{background:var(--adm-bg);color:var(--adm-ink);font-family:var(--font-body);margin:0}
button{font-family:var(--font-body);cursor:pointer;border:none;background:none;color:inherit}

.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:11px 22px;
  border-radius:8px;font-size:14px;font-weight:700;transition:all .12s}
.btn-primary{background:var(--tv-primary);color:#fff}
.btn-primary:hover{background:var(--tv-primary-dark)}
.btn-ghost{background:#fff;color:#4E5968;border:1px solid var(--adm-line)}
.btn-ghost:hover{border-color:var(--adm-ink);color:var(--adm-ink)}
.btn-block{width:100%}
.btn-sm{padding:8px 14px;font-size:13px}

.sb{position:fixed;top:0;left:0;bottom:0;width:var(--sb-w);background:#fff;border-right:1px solid var(--adm-line);
  display:flex;flex-direction:column;z-index:120;transition:transform .22s}
.sb-brand{padding:22px 20px 18px;border-bottom:1px solid var(--adm-line)}
.sb-brand .lg{font-size:21px;font-weight:800;letter-spacing:-.03em;color:var(--adm-ink)}
.sb-brand .lg b{color:var(--tv-primary)}
.sb-brand .role{display:inline-block;margin-top:7px;font-size:11px;font-weight:700;color:var(--tv-primary);
  background:var(--tv-primary-soft);border-radius:var(--r-pill);padding:3px 9px}
.sb-nav{flex:1;overflow-y:auto;padding:12px 12px 20px}
.sb-nav .grp{font-size:11px;font-weight:700;color:var(--adm-sub);letter-spacing:.04em;padding:14px 10px 7px}
.sb-nav button{display:flex;align-items:center;gap:10px;width:100%;text-align:left;padding:11px 12px;
  border-radius:8px;font-size:14px;font-weight:600;color:#4E5968;margin-bottom:2px;transition:background .12s}
.sb-nav button .cnt{margin-left:auto;font-size:11px;font-weight:700;background:var(--adm-bg);
  color:var(--adm-sub);border-radius:var(--r-pill);padding:2px 8px}
.sb-nav button:hover{background:var(--adm-bg)}
.sb-nav button.on{background:var(--tv-primary);color:#fff}
.sb-nav button.on .cnt{background:rgba(255,255,255,.24);color:#fff}
.sb-foot{padding:14px;border-top:1px solid var(--adm-line);display:flex;gap:8px}
.sb-foot a,.sb-foot button{flex:1;text-align:center;font-size:12px;font-weight:600;color:#4E5968;
  border:1px solid var(--adm-line);border-radius:6px;padding:9px 6px}

.mainarea{margin-left:var(--sb-w);min-height:100vh;display:flex;flex-direction:column}
.topbar2{background:#fff;border-bottom:1px solid var(--adm-line);position:sticky;top:0;z-index:90;
  display:flex;align-items:center;gap:14px;padding:0 26px;height:62px}
.topbar2 h1{font-size:19px;font-weight:700;letter-spacing:-.02em}
.topbar2 .desc{font-size:13px;color:var(--adm-sub)}
.topbar2 .sp{flex:1}
.burger{display:none;font-size:20px;color:var(--adm-ink)}
.content{padding:24px 26px 60px;max-width:1180px;width:100%}

.kpi{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:22px}
@media(max-width:900px){.kpi{grid-template-columns:repeat(2,1fr)}}
.kpi-card{background:#fff;border:1px solid var(--adm-line);border-radius:12px;padding:18px 20px}
.kpi-card .lbl{font-size:12px;font-weight:600;color:var(--adm-sub)}
.kpi-card .num{font-size:28px;font-weight:800;letter-spacing:-.03em;margin-top:8px;line-height:1}
.kpi-card .sub{font-size:12px;color:var(--adm-sub);margin-top:7px}

.card{background:#fff;border:1px solid var(--adm-line);border-radius:12px;padding:20px 22px;margin-bottom:16px}
.card-head{display:flex;align-items:center;gap:12px;margin-bottom:16px;flex-wrap:wrap}
.card-head h3{font-size:16px;font-weight:700}
.card-head .sp{flex:1}
.note{font-size:13px;color:var(--adm-sub);margin-bottom:16px;line-height:1.75}

.tbl-wrap{overflow-x:auto;margin:0 -22px;padding:0 22px}
table{width:100%;border-collapse:collapse;font-size:13px;min-width:640px}
th{font-size:12px;font-weight:600;color:var(--adm-sub);text-align:left;padding:10px;
  border-bottom:1px solid var(--adm-line);white-space:nowrap}
td{padding:13px 10px;border-bottom:1px solid var(--adm-line);vertical-align:middle}
td .sub{font-size:12px;color:var(--adm-sub);margin-top:3px}
tbody tr:hover{background:#FAFBFC}
.empty-row td{text-align:center;color:var(--adm-sub);padding:44px;font-size:14px}

.bar{display:flex;align-items:center;gap:9px;margin-bottom:16px;flex-wrap:wrap}
.bar .grow{flex:1}
.srch{border:1px solid var(--adm-line);border-radius:7px;padding:9px 12px;font-size:13px;min-width:200px}
.fgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.fgrid.two{grid-template-columns:repeat(2,1fr)}
@media(max-width:900px){.fgrid,.fgrid.two{grid-template-columns:1fr}}
.fld{margin-bottom:14px}
.fld label{display:block;font-size:13px;font-weight:600;color:#4E5968;margin-bottom:6px}
.fld input,.fld select,.fld textarea{width:100%;border:1px solid var(--adm-line);border-radius:7px;
  padding:10px 12px;font-size:14px;font-family:var(--font-body)}
.fld textarea{resize:vertical;min-height:74px;line-height:1.7}
.sect{border-top:1px solid var(--adm-line);margin-top:22px;padding-top:20px}
.sect h4{font-size:14px;font-weight:700;margin-bottom:14px}

.upl{display:flex;gap:16px;align-items:flex-start;border:1px dashed var(--adm-line);
  border-radius:10px;padding:14px;background:#FAFBFC}
.upl.over{border-color:var(--tv-primary);background:var(--tv-primary-soft)}
.upl-prev{width:176px;height:132px;flex-shrink:0;border-radius:8px;overflow:hidden;background:#fff;
  border:1px solid var(--adm-line);display:flex;align-items:center;justify-content:center}
.upl-prev img{width:100%;height:100%;object-fit:cover;display:block}
.upl-prev .ph{font-size:12px;color:var(--adm-sub)}
.upl-side{flex:1;min-width:0}
.upl-acts{display:flex;gap:8px;margin-bottom:10px;flex-wrap:wrap}
.upl-hint{font-size:12px;color:var(--adm-sub);line-height:1.65;margin:0}
.upl-url{margin-top:12px}
.upl-url summary{font-size:12px;color:var(--adm-sub);cursor:pointer;font-weight:600}

.pill-st{display:inline-block;font-size:11px;font-weight:700;padding:4px 10px;border-radius:var(--r-pill)}
.st-new{background:var(--tv-primary-soft);color:var(--tv-primary-dark)}
.st-doing{background:#FFF4E0;color:#B7791F}
.st-done{background:#EEF1F4;color:#6B7684}
.thumb-sm{width:54px;height:41px;object-fit:cover;border-radius:6px;background:var(--adm-bg)}

.login-wrap{max-width:380px;margin:0 auto;padding:100px 20px}
.login-wrap .lg{font-size:30px;font-weight:800;letter-spacing:-.03em;text-align:center;margin-bottom:6px}
.login-wrap .lg b{color:var(--tv-primary)}
.login-wrap .desc{font-size:14px;color:var(--adm-sub);text-align:center;margin-bottom:26px}

.rte{background:#fff;border:1px solid var(--adm-line);border-radius:0 0 7px 7px}
.rte .ql-editor{min-height:220px;font-size:15px;line-height:1.8;font-family:var(--font-body)}
.ql-toolbar.ql-snow{border:1px solid var(--adm-line);border-radius:7px 7px 0 0;background:#FAFBFC}
.ql-container.ql-snow{border:0}

.hidden{display:none!important}
.toast{position:fixed;left:50%;bottom:28px;transform:translateX(-50%) translateY(20px);opacity:0;
  background:#191F28;color:#fff;padding:12px 20px;border-radius:8px;font-size:13px;z-index:200;
  transition:all .25s;pointer-events:none}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}

.sb-backdrop{position:fixed;inset:0;background:rgba(0,0,0,.4);z-index:110;display:none}
@media(max-width:900px){
  .sb{transform:translateX(-100%);box-shadow:0 0 40px rgba(0,0,0,.14)}
  .sb.open{transform:translateX(0)}
  .sb-backdrop.open{display:block}
  .mainarea{margin-left:0}
  .burger{display:block}
  .content{padding:18px 16px 60px}
  .topbar2{padding:0 16px}
}
</style>
</head>
<body>
<div id="gate" class="login-wrap">
  <div class="lg">TRE<b>VITY</b></div><p class="desc">관리자 콘솔</p>
  <div class="card">
    <div class="fld" id="gate-email-fld" style="display:none"><label>이메일</label><input id="gate-email" type="email"></div>
    <div class="fld"><label>비밀번호</label><input id="gate-pw" type="password" onkeydown="if(event.key==='Enter')doAdminLogin()" autofocus>
      <p class="hint" id="gate-hint" style="font-size:12px;color:var(--adm-sub);margin-top:5px">초기 비밀번호 <code>trevity2026</code> — 설정에서 변경하세요.</p></div>
    <button class="btn btn-primary btn-block" onclick="doAdminLogin()">로그인</button>
    <p id="gate-err" style="color:var(--tv-danger);font-size:13px;margin-top:12px;display:none"></p>
  </div>
</div>
<div id="app" class="hidden">
  <div class="sb-backdrop" id="sb-backdrop" onclick="toggleSb(false)"></div>
  <aside class="sb" id="sb">
    <div class="sb-brand"><div class="lg">TRE<b>VITY</b></div><span class="role">관리자 콘솔</span></div>
    <nav class="sb-nav" id="sb-nav"></nav>
    <div class="sb-foot"><a href="../index.html" target="_blank">사이트 </a><button onclick="Admin.logout();location.reload()">로그아웃</button></div>
  </aside>
  <div class="mainarea">
    <div class="topbar2"><button class="burger" onclick="toggleSb(true)">☰</button>
      <h1 id="pg-title">대시보드</h1><span class="sp"></span><span class="desc" id="pg-desc"></span></div>
    <div class="content">
      <section id="tab-dash"></section>
      <section id="tab-inq" class="hidden"></section>
      <section id="tab-blog" class="hidden"></section>
      <section id="tab-copy" class="hidden"></section>
      <section id="tab-settings" class="hidden"></section>
    </div>
  </div>
</div>
<script src="../assets/js/config.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>
<script src="../assets/js/data.js"></script>
<script src="../assets/js/store.js"></script>
<script src="../assets/js/upload.js"></script>
<script src="../assets/js/store-supabase.js"></script>
<script src="https://cdn.jsdelivr.net/npm/quill@2.0.3/dist/quill.js"></script>
<script src="../assets/js/admin.js"></script>
</body>
</html>
```

- [ ] **Step 3: Verify script load order is correct** (data.js before store.js before store-supabase.js before admin.js — `store.js` reads `TV_BLOG_POSTS` etc at call time not load time so order between data.js/store.js is only a hard requirement for `store-supabase.js`'s `TV_BLOG_POSTS.length = 0` calls, which run after boot(), well after all scripts loaded — but keep this order for clarity and to match Task 2/3/4 declarations)

Run: `grep -o '<script src="[^"]*"' "C:\Users\이건희\creplanet-clone\admin\index.html"`
Expected output in this exact order: `config.js`, `supabase-js@2`, `data.js`, `store.js`, `upload.js`, `store-supabase.js`, `quill.js`, `admin.js`

- [ ] **Step 4: Commit**

```bash
cd "C:\Users\이건희\creplanet-clone"
git add assets/js/data.js admin/index.html
git commit -m "feat(admin): add admin shell HTML and global content data.js"
```

---

## Task 6: `admin.js` core — helpers, login gate, tab shell, upload widget

**Files:**
- Create: `C:\Users\이건희\creplanet-clone\assets\js\admin.js`

**Interfaces:**
- Consumes: `Store`/`Admin`/`TvImg` (Tasks 2-4), `TvData` (Task 4, only present in Supabase mode), DOM ids from Task 5's `admin/index.html`.
- Produces: `esc(s)`, `av(id)`, `toastA(msg)`, `uploader(id,value,opts)` HTML string + its handlers (`uplDrag/uplDrop/uplPick/uplStore/uplClear/uplSetUrl`), `doAdminLogin()`, `boot()`, `showTab(name)`, `toggleSb(open)`, `renderNav()`, `renderAll()`, `admDo(promise, reload)`, `refreshAdm()`, global `ADM` cache object. Tasks 7-10 append their own `render*()` functions to this same file and are called from `renderAll()`.

- [ ] **Step 1: Write the core of `admin.js`** (ported from `C:\Users\이건희\makenov\assets\js\admin.js` lines 1-6 (esc/av/ac), 66-133 (today/toastA/uploader widget — unchanged except `MkImg`→`TvImg`), 178-231 (admDo/refreshAdm/login/boot — simplified: no buyer/lead fetch, and login supports both local-password and Supabase-email+password modes), 233-286 (nav/tabs — trimmed to 5 tabs))

```js
/* ============================================================
   트래비티 관리자 로직
   ============================================================ */
function esc(s){ return String(s??'').replace(/[&<>"']/g, m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m])); }
function av(id){ const el=document.getElementById(id); return el ? el.value.trim() : ''; }
function today(){ const d=new Date(); return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0'); }
function toastA(msg){
  let el=document.querySelector('.toast');
  if(!el){ el=document.createElement('div'); el.className='toast'; document.body.appendChild(el); }
  el.textContent=msg; el.classList.add('show');
  clearTimeout(el._t); el._t=setTimeout(()=>el.classList.remove('show'),2400);
}

/* ---------- 이미지 업로드 위젯 ---------- */
function imgSrc(v){ return TvImg.isRef(v) ? (TvImg.resolve(v) || '') : (v || ''); }
function uploader(id, value, opts){
  opts = opts || {};
  const v = value || '';
  const src = TvImg.isRef(v) ? TvImg.resolve(v) : v;
  return `
  <div class="upl" id="${id}-box" ondragover="uplDrag(event,1)" ondragleave="uplDrag(event,0)" ondrop="uplDrop(event,'${id}')">
    <input type="hidden" id="${id}" value="${esc(v)}">
    <div class="upl-prev" id="${id}-prev">${src?`<img src="${esc(src)}" alt="">`:`<span class="ph">이미지 없음</span>`}</div>
    <div class="upl-side">
      <div class="upl-acts">
        <button type="button" class="btn btn-primary btn-sm" onclick="document.getElementById('${id}-file').click()">파일 선택</button>
        <button type="button" class="btn btn-ghost btn-sm" onclick="uplClear('${id}')">비우기</button>
      </div>
      <input type="file" id="${id}-file" accept="image/*" hidden onchange="uplPick(this,'${id}')">
      <p class="upl-hint" id="${id}-info">${opts.hint||'파일을 끌어다 놓아도 됩니다. 자동으로 1600px·JPEG로 압축됩니다.'}</p>
      <details class="upl-url"><summary>URL로 넣기</summary>
        <input class="srch" style="width:100%;margin-top:8px" placeholder="https://..."
          value="${TvImg.isRef(v)?'':esc(v)}" onchange="uplSetUrl('${id}',this.value)"></details>
    </div>
  </div>`;
}
function uplDrag(e, on){ e.preventDefault(); e.currentTarget.classList.toggle('over', !!on); }
function uplDrop(e, id){
  e.preventDefault(); e.currentTarget.classList.remove('over');
  const f = e.dataTransfer.files && e.dataTransfer.files[0];
  if(f) uplStore(f, id);
}
function uplPick(input, id){ if(input.files[0]) uplStore(input.files[0], id); input.value=''; }
async function uplStore(file, id){
  const info = document.getElementById(id+'-info');
  if(info) info.textContent = '압축하는 중…';
  try{
    const r = await TvImg.save(file);
    document.getElementById(id).value = r.ref;
    document.getElementById(id+'-prev').innerHTML = `<img src="${r.dataUrl||r.ref}" alt="">`;
    if(info) info.textContent = `${r.w}×${r.h} · ${fmtBytes(r.bytes)} 로 저장됨`;
  }catch(err){
    if(info) info.textContent = err.message || '업로드에 실패했습니다';
    toastA(err.message || '업로드 실패');
  }
}
function uplClear(id){
  document.getElementById(id).value = '';
  document.getElementById(id+'-prev').innerHTML = `<span class="ph">이미지 없음</span>`;
  const info = document.getElementById(id+'-info');
  if(info) info.textContent = '파일을 끌어다 놓아도 됩니다.';
}
function uplSetUrl(id, url){
  const u = String(url||'').trim();
  document.getElementById(id).value = u;
  document.getElementById(id+'-prev').innerHTML = u ? `<img src="${esc(u)}" alt="">` : `<span class="ph">이미지 없음</span>`;
}

/* ---------- 운영 데이터 캐시 ---------- */
const ADM = { inqs:[] };
const isSB = () => typeof TvData !== 'undefined' && typeof TV_BACKEND !== 'undefined' && TV_BACKEND === 'supabase';

async function admDo(promise, reload){
  try{
    await promise;
    if(reload === 0){ await refreshAdm(); renderAll(); }
    else location.reload();
  }catch(e){
    console.error(e);
    toastA('저장에 실패했습니다: ' + (e.message||e));
  }
}
async function refreshAdm(){
  ADM.inqs = await Store.allInquiries() || [];
  ADM.inqs.sort((a,b)=>String(b.created_at).localeCompare(String(a.created_at)));
}

/* ---------- 로그인 ---------- */
function doAdminLogin(){
  const err = document.getElementById('gate-err');
  err.style.display = 'none';
  if(isSB()){
    const email = av('gate-email'), pw = av('gate-pw');
    if(!email){ err.textContent='관리자 이메일을 입력하세요'; err.style.display='block'; return; }
    Admin.loginEmail(email, pw).then(r=>{
      if(!r.ok){ err.textContent = r.err; err.style.display='block'; return; }
      boot();
    });
    return;
  }
  const pw = av('gate-pw');
  if(Admin.login(pw)){ boot(); }
  else { err.textContent='비밀번호가 올바르지 않습니다'; err.style.display='block'; }
}
async function boot(){
  document.getElementById('gate').classList.add('hidden');
  document.getElementById('app').classList.remove('hidden');
  try{ await TvImg.loadCache(); }catch(e){}
  try{ await refreshAdm(); }catch(e){ console.error('운영 데이터 로드 실패', e); }
  renderAll();
}

/* ---------- 사이드바 · 탭 ---------- */
const TABS = ['dash','inq','blog','copy','settings'];
const NAV = [
  { id:'dash',     label:'대시보드', title:'대시보드',        desc:'문의·콘텐츠 현황 한눈에 보기' },
  { id:'inq',      label:'문의함',   title:'문의함',          desc:'inquiry.html로 들어온 문의' },
  { id:'blog',     label:'블로그',   title:'블로그 관리',      desc:'글 작성·수정·발행' },
  { id:'copy',     label:'카피',     title:'포트폴리오 · 패키지', desc:'이미지 롤과 vietnam-tiktok 패키지 가격' },
  { id:'settings', label:'설정',     title:'설정',            desc:'관리자 비밀번호와 연결 상태' },
];
let curTab = 'dash';

function renderNav(){
  const newCnt = ADM.inqs.filter(i=>i.status==='new').length;
  const counts = { inq:newCnt||'', blog:TV_BLOG_POSTS.length, copy:'', dash:'', settings:'' };
  document.getElementById('sb-nav').innerHTML = NAV.map(n=>navBtn(n,counts)).join('');
}
function navBtn(n, counts){
  const c = counts[n.id];
  return `<button class="${curTab===n.id?'on':''}" onclick="showTab('${n.id}')"><span>${n.label}</span>
    ${c!=='' && c!==undefined ? `<span class="cnt">${c}</span>` : ''}</button>`;
}
function showTab(name){
  curTab = name;
  TABS.forEach(x=>document.getElementById('tab-'+x).classList.toggle('hidden', x!==name));
  const n = NAV.find(x=>x.id===name) || NAV[0];
  document.getElementById('pg-title').textContent = n.title;
  document.getElementById('pg-desc').textContent = n.desc;
  renderNav();
  toggleSb(false);
  window.scrollTo(0,0);
}
function toggleSb(open){
  document.getElementById('sb').classList.toggle('open', !!open);
  document.getElementById('sb-backdrop').classList.toggle('open', !!open);
}
function renderAll(){
  renderNav(); renderDash(); renderInq(); renderBlog(); renderCopy(); renderSettings();
  showTab(curTab);
}

if(isSB()){
  document.getElementById('gate-email-fld').style.display = 'block';
  document.getElementById('gate-hint').style.display = 'none';
}
```

- [ ] **Step 2: Verify no JS syntax errors**

Run: `node --check "C:\Users\이건희\creplanet-clone\assets\js\admin.js"`
Expected: no output, exit code 0 (this will fail until Tasks 7-10 append `renderDash/renderInq/renderBlog/renderCopy/renderSettings` — those are referenced in `renderAll()` but `node --check` only parses syntax, not references, so this passes even before they exist)

- [ ] **Step 3: Commit**

```bash
cd "C:\Users\이건희\creplanet-clone"
git add assets/js/admin.js
git commit -m "feat(admin): add admin core — login gate, tab shell, upload widget"
```

---

## Task 7: `admin.js` — Dashboard + Inquiries tabs

**Files:**
- Modify: `C:\Users\이건희\creplanet-clone\assets\js\admin.js` (append)

**Interfaces:**
- Consumes: `ADM.inqs`, `TV_BLOG_POSTS`, `TV_PORTFOLIO`, `esc/av/toastA/admDo` (Task 6)
- Produces: `renderDash()`, `renderInq()`, `exportInquiries()` — called from `renderAll()` (already wired in Task 6)

- [ ] **Step 1: Append dashboard + inquiries rendering** (adapted from `makenov/assets/js/admin.js` lines 324-398, dropping buyer/leads sections)

```js
/* ============================================================
   대시보드
   ============================================================ */
function renderDash(){
  const newCnt = ADM.inqs.filter(i=>i.status==='new').length;
  document.getElementById('tab-dash').innerHTML = `
    <div class="kpi">
      <div class="kpi-card"><div class="lbl">누적 문의</div><div class="num">${ADM.inqs.length}</div><div class="sub">미처리 <b>${newCnt}</b>건</div></div>
      <div class="kpi-card"><div class="lbl">블로그 글</div><div class="num">${TV_BLOG_POSTS.length}</div><div class="sub">발행됨</div></div>
      <div class="kpi-card"><div class="lbl">포트폴리오</div><div class="num">${TV_PORTFOLIO.length}</div><div class="sub">등록된 미디어</div></div>
      <div class="kpi-card"><div class="lbl">패키지</div><div class="num">${TV_PACKAGES.length}</div><div class="sub">vietnam-tiktok.html</div></div>
    </div>
    <div class="card"><div class="card-head"><h3>최근 문의</h3><span class="sp"></span><button class="btn btn-ghost btn-sm" onclick="showTab('inq')">전체 보기</button></div>
      <div class="tbl-wrap"><table><thead><tr><th style="width:96px">일시</th><th>회사 · 담당자</th><th>내용</th><th style="width:76px">상태</th></tr></thead><tbody>${
        ADM.inqs.length ? ADM.inqs.slice(0,5).map(i=>`
          <tr><td>${esc(String(i.created_at).slice(0,10))}</td><td><b>${esc(i.company)}</b><div class="sub">${esc(i.name)}</div></td>
          <td style="max-width:320px"><div style="white-space:pre-wrap">${esc(i.message).slice(0,60)}</div></td>
          <td><span class="pill-st st-${i.status}">${INQ_ST[i.status]}</span></td></tr>`).join('')
        : `<tr class="empty-row"><td colspan="4">아직 접수된 문의가 없습니다</td></tr>`
      }</tbody></table></div></div>`;
}

/* ============================================================
   문의함
   ============================================================ */
const INQ_ST = { new:'신규', doing:'처리중', done:'완료' };
let inqFilter = 'all';

function renderInq(){
  const all = ADM.inqs;
  const cnt = k => all.filter(i=>i.status===k).length;
  const list = inqFilter==='all' ? all : all.filter(i=>i.status===inqFilter);

  document.getElementById('tab-inq').innerHTML = `
    <div class="card"><p class="note">inquiry.html에서 방문자가 제출한 문의입니다.</p>
    <div class="bar">
      <button class="btn btn-sm ${inqFilter==='all'?'btn-primary':'btn-ghost'}" onclick="inqFilter='all';renderInq()">전체 ${all.length}</button>
      <button class="btn btn-sm ${inqFilter==='new'?'btn-primary':'btn-ghost'}" onclick="inqFilter='new';renderInq()">신규 ${cnt('new')}</button>
      <button class="btn btn-sm ${inqFilter==='doing'?'btn-primary':'btn-ghost'}" onclick="inqFilter='doing';renderInq()">처리중 ${cnt('doing')}</button>
      <button class="btn btn-sm ${inqFilter==='done'?'btn-primary':'btn-ghost'}" onclick="inqFilter='done';renderInq()">완료 ${cnt('done')}</button>
      <span class="grow"></span><button class="btn btn-ghost btn-sm" onclick="exportInquiries()">CSV 내보내기</button>
    </div>
    <div class="tbl-wrap"><table><thead><tr><th style="width:96px">일시</th><th>회사</th><th>담당자 · 연락처</th><th>내용 · 메모</th><th style="width:150px">상태</th><th style="width:60px"></th></tr></thead><tbody>${
      list.length ? list.map(i=>`
        <tr><td>${esc(String(i.created_at).slice(0,10))}<div class="sub">${esc(String(i.created_at).slice(11,16))}</div></td>
        <td><b>${esc(i.company)}</b><div class="sub">${esc(i.source_page)}</div></td>
        <td>${esc(i.name)}<div class="sub">${esc(i.phone)} · ${esc(i.email)}</div></td>
        <td style="max-width:280px"><div style="white-space:pre-wrap;line-height:1.6">${esc(i.message)}</div>
          <input class="srch" style="margin-top:8px;width:100%" placeholder="메모" value="${esc(i.memo)}"
            onchange="admDo(Admin.setInquiryMemo('${i.id}', this.value), 0)"></td>
        <td><select class="srch" style="width:100%" onchange="admDo(Admin.setInquiryStatus('${i.id}', this.value), 0)">
          <option value="new" ${i.status==='new'?'selected':''}>신규</option>
          <option value="doing" ${i.status==='doing'?'selected':''}>처리중</option>
          <option value="done" ${i.status==='done'?'selected':''}>완료</option></select></td>
        <td><button class="btn btn-ghost btn-sm" onclick="if(confirm('삭제할까요?')){admDo(Admin.deleteInquiry('${i.id}'), 0);}">삭제</button></td></tr>`).join('')
      : `<tr class="empty-row"><td colspan="6">해당하는 문의가 없습니다</td></tr>`
    }</tbody></table></div></div>`;
}
function exportInquiries(){
  const rows = [['일시','회사','담당자','연락처','이메일','내용','유입페이지','상태','메모']];
  ADM.inqs.forEach(i=>rows.push([i.created_at,i.company,i.name,i.phone,i.email,i.message,i.source_page,INQ_ST[i.status],i.memo]));
  const csv = rows.map(r=>r.map(v=>`"${String(v??'').replace(/"/g,'""')}"`).join(',')).join('\n');
  downloadFile('trevity-문의_'+today()+'.csv', '\uFEFF'+csv, 'text/csv');
}
function downloadFile(name, content, mime){
  const blob = new Blob([content], {type:(mime||'text/plain')+';charset=utf-8'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = name;
  document.body.appendChild(a); a.click();
  setTimeout(()=>{ URL.revokeObjectURL(a.href); a.remove(); }, 400);
}
```

- [ ] **Step 2: Verify no JS syntax errors**

Run: `node --check "C:\Users\이건희\creplanet-clone\assets\js\admin.js"`
Expected: no output, exit code 0.

- [ ] **Step 3: Commit**

```bash
cd "C:\Users\이건희\creplanet-clone"
git add assets/js/admin.js
git commit -m "feat(admin): add dashboard and inquiries tab rendering"
```

---

## Task 8: `admin.js` — Blog tab (Quill editor CRUD)

**Files:**
- Modify: `C:\Users\이건희\creplanet-clone\assets\js\admin.js` (append)

**Interfaces:**
- Consumes: `TV_BLOG_POSTS`, `Admin.upsertBlogPost/deleteBlogPost`, `uploader()`, `Quill` (CDN global, loaded in Task 5's `admin/index.html`)
- Produces: `renderBlog()` (called from `renderAll()`), `bEditing` state var

**Note:** Unlike makenov's tri-lingual (ko/vi/en) columns, Trevity blog posts are single-language Korean — one Quill instance per post, not three. This simplifies `initColumnEditors`/`rteGet`/`rteSet`/`tri()` down to a single `RTE_BLOG` instance.

- [ ] **Step 1: Append blog tab rendering** (adapted from `makenov/assets/js/admin.js` lines 43-65 (Quill init, simplified to one language) and 668-699 (list/form/save, simplified to one language + `published` toggle + `category` select))

```js
/* ============================================================
   블로그 CRUD
   ============================================================ */
let bEditing = null;
let RTE_BLOG = null;

function initBlogEditor(html){
  if(typeof Quill === 'undefined') return;
  const el = document.getElementById('rte-b-body');
  if(!el) return;
  RTE_BLOG = new Quill(el, {
    theme: 'snow',
    placeholder: '여기에 본문을 작성하세요…',
    modules: { toolbar: [
      [{ header:[2,3,false] }], ['bold','italic','underline'],
      [{ list:'ordered' }, { list:'bullet' }], ['blockquote','link','image'], ['clean'],
    ] },
  });
  if(html) RTE_BLOG.clipboard.dangerouslyPasteHTML(html);
}
function blogBodyGet(){
  if(!RTE_BLOG) return '';
  const html = RTE_BLOG.root.innerHTML;
  return html.replace(/<[^>]*>/g,'').trim() ? html : '';
}

const BLOG_CATS = ['베트남 시장','인플루언서 부킹','틱톡 마케팅','캠페인 사례'];

function renderBlog(){
  const el = document.getElementById('tab-blog');
  if(bEditing !== null){
    el.innerHTML = blogForm(bEditing);
    const p = bEditing ? TV_BLOG_POSTS.find(x=>x.slug===bEditing) : null;
    initBlogEditor(p ? p.body_html : '');
    return;
  }
  el.innerHTML = `
    <div class="card"><p class="note">blog.html 목록과 blog-post.html?slug=... 상세에 노출됩니다.</p>
    <div class="bar"><span class="grow"></span><button class="btn btn-primary btn-sm" onclick="bEditing='';renderBlog()">+ 새 글 작성</button></div>
    <div class="tbl-wrap"><table><thead><tr><th style="width:76px">썸네일</th><th>제목</th><th>분류</th><th>발행</th><th style="width:120px"></th></tr></thead><tbody>${
      TV_BLOG_POSTS.length ? TV_BLOG_POSTS.map(p=>`
        <tr><td><img class="thumb-sm" src="${esc(imgSrc(p.thumbnail_url))}" alt=""></td>
        <td><b>${esc(p.title)}</b><div class="sub">/${esc(p.slug)}</div></td><td>${esc(p.category)}</td>
        <td>${p.published?'게시중':'비공개'}</td>
        <td><button class="btn btn-ghost btn-sm" onclick="bEditing='${p.slug}';renderBlog()">수정</button>
          <button class="btn btn-ghost btn-sm" onclick="if(confirm('삭제할까요?')){admDo(Admin.deleteBlogPost('${p.slug}'), 0);}">삭제</button></td></tr>`).join('')
      : `<tr class="empty-row"><td colspan="5">글이 없습니다</td></tr>`
    }</tbody></table></div></div>`;
}

function blogForm(slug){
  const p = slug ? TV_BLOG_POSTS.find(x=>x.slug===slug) : null;
  return `
    <div class="card"><div class="bar"><h3 style="margin:0">${p?'글 수정':'새 글 작성'}</h3><span class="grow"></span>
      <button class="btn btn-ghost btn-sm" onclick="bEditing=null;renderBlog()">취소</button>
      <button class="btn btn-primary btn-sm" onclick="saveBlogPost('${slug||''}')">저장</button></div>
    <div class="fgrid two">
      <div class="fld"><label>제목</label><input id="b-title" value="${esc(p?p.title:'')}"></div>
      <div class="fld"><label>URL 슬러그 (영문/숫자/하이픈)</label><input id="b-slug" value="${esc(p?p.slug:'')}" ${p?'readonly':''}></div>
    </div>
    <div class="fgrid two">
      <div class="fld"><label>분류</label><select id="b-cat">${BLOG_CATS.map(c=>`<option ${p&&p.category===c?'selected':''}>${c}</option>`).join('')}</select></div>
      <div class="fld"><label>읽는 시간(분)</label><input id="b-min" type="number" value="${p?p.read_minutes:4}"></div>
    </div>
    <div class="sect"><h4>썸네일</h4>${uploader('b-thumb', p?p.thumbnail_url:'', {hint:'목록 카드와 상세 상단에 쓰입니다. 16:9 권장.'})}</div>
    <div class="fld"><label>요약 (목록 카드에 표시)</label><textarea id="b-excerpt">${esc(p?p.excerpt:'')}</textarea></div>
    <div class="sect"><h4>본문</h4><div class="rte" id="rte-b-body"></div></div>
    <div class="fld" style="margin-top:16px"><label style="display:flex;align-items:center;gap:8px;font-weight:600">
      <input type="checkbox" id="b-pub" ${!p||p.published?'checked':''} style="width:auto"> 발행 (체크 해제 시 blog.html에서 숨김)</label></div>
    <div class="bar" style="margin-top:22px"><span class="grow"></span>
      <button class="btn btn-ghost" onclick="bEditing=null;renderBlog()">취소</button>
      <button class="btn btn-primary" onclick="saveBlogPost('${slug||''}')">저장</button></div></div>`;
}

function saveBlogPost(oldSlug){
  const title = av('b-title'), slug = av('b-slug');
  if(!title){ toastA('제목을 입력하세요'); return; }
  if(!slug || !/^[a-z0-9-]+$/.test(slug)){ toastA('슬러그는 영문 소문자·숫자·하이픈만 가능합니다'); return; }
  toastA('저장하는 중…');
  admDo(Admin.upsertBlogPost({
    slug, title, category: av('b-cat'), thumbnail_url: av('b-thumb'),
    excerpt: av('b-excerpt'), body_html: blogBodyGet(),
    read_minutes: Number(av('b-min'))||4, published: document.getElementById('b-pub').checked,
  }), 0);
  bEditing = null;
}
```

- [ ] **Step 2: Verify no JS syntax errors**

Run: `node --check "C:\Users\이건희\creplanet-clone\assets\js\admin.js"`
Expected: no output, exit code 0.

- [ ] **Step 3: Commit**

```bash
cd "C:\Users\이건희\creplanet-clone"
git add assets/js/admin.js
git commit -m "feat(admin): add blog CRUD tab with Quill editor"
```

---

## Task 9: `admin.js` — Copy tab (portfolio images + packages)

**Files:**
- Modify: `C:\Users\이건희\creplanet-clone\assets\js\admin.js` (append)

**Interfaces:**
- Consumes: `TV_PORTFOLIO`, `TV_PACKAGES`, `Admin.upsertPortfolioItem/deletePortfolioItem/movePortfolioItem/upsertPackage`, `uploader()`
- Produces: `renderCopy()` (called from `renderAll()`)

- [ ] **Step 1: Append copy tab rendering** (new — no direct makenov equivalent since Trevity's portfolio-roll/package-price concept doesn't exist in makenov; loosely modeled on makenov's gallery pattern at lines 137-166 for the move/delete affordance)

```js
/* ============================================================
   카피 — 포트폴리오 이미지 + 패키지 가격
   ============================================================ */
let pfEditing = null; // {placement} while adding new item, or null

function renderCopy(){
  const el = document.getElementById('tab-copy');
  const home = TV_PORTFOLIO.filter(x=>x.placement==='home-roll').sort((a,b)=>a.sort_order-b.sort_order);
  const hero = TV_PORTFOLIO.filter(x=>x.placement==='hero-wall').sort((a,b)=>a.sort_order-b.sort_order);

  el.innerHTML = `
    <div class="card"><div class="card-head"><h3>포트폴리오 — 메인 페이지 롤 (index.html)</h3><span class="sp"></span>
      <button class="btn btn-primary btn-sm" onclick="pfEditing='home-roll';renderCopy()">+ 추가</button></div>
      ${pfEditing==='home-roll' ? pfForm('home-roll') : ''}
      ${pfList(home)}
    </div>
    <div class="card"><div class="card-head"><h3>포트폴리오 — 히어로 영상벽 (local-vn/stay/tourist-vn/tourist-cn/vietnam-tiktok 5개 페이지 공용)</h3><span class="sp"></span>
      <button class="btn btn-primary btn-sm" onclick="pfEditing='hero-wall';renderCopy()">+ 추가</button></div>
      ${pfEditing==='hero-wall' ? pfForm('hero-wall') : ''}
      ${pfList(hero)}
    </div>
    <div class="card"><div class="card-head"><h3>vietnam-tiktok.html 패키지 가격</h3></div>
      ${TV_PACKAGES.slice().sort((a,b)=>a.sort_order-b.sort_order).map(pkgForm).join('')}
    </div>`;
}

function pfList(items){
  if(!items.length) return `<p class="note" style="margin:0">아직 없습니다.</p>`;
  return `<div class="tbl-wrap"><table><thead><tr><th style="width:76px">미리보기</th><th>종류</th><th>주소</th><th style="width:150px"></th></tr></thead><tbody>${
    items.map((it,i)=>`
      <tr><td>${it.media_type==='video'
          ? `<img class="thumb-sm" src="${esc(it.poster_url)}" alt="">`
          : `<img class="thumb-sm" src="${esc(it.url)}" alt="">`}</td>
      <td>${it.media_type==='video'?'영상':'이미지'}</td>
      <td style="max-width:280px;word-break:break-all">${esc(it.url)}</td>
      <td>
        <button class="btn btn-ghost btn-sm" onclick="admDo(Admin.movePortfolioItem('${it.id}',-1),0)" ${i===0?'disabled':''}>↑</button>
        <button class="btn btn-ghost btn-sm" onclick="admDo(Admin.movePortfolioItem('${it.id}',1),0)" ${i===items.length-1?'disabled':''}>↓</button>
        <button class="btn btn-ghost btn-sm" onclick="if(confirm('삭제할까요?')){admDo(Admin.deletePortfolioItem('${it.id}'),0);}">삭제</button>
      </td></tr>`).join('')
  }</tbody></table></div>`;
}

function pfForm(placement){
  return `<div class="sect" style="margin-top:0;padding-top:16px">
    <div class="fgrid two">
      <div class="fld"><label>종류</label><select id="pf-type"><option value="image">이미지</option><option value="video">영상</option></select></div>
      <div class="fld"><label>대체 텍스트(alt)</label><input id="pf-alt" placeholder="트래비티 인플루언서 콘텐츠"></div>
    </div>
    <div class="fld"><label>이미지 파일(이미지일 때) 또는 영상 URL(영상일 때)</label>${uploader('pf-url', '', {hint:'영상이면 아래 URL로 넣기에 mp4 주소를 직접 입력하세요.'})}</div>
    <div class="fld"><label>영상 포스터 이미지(영상일 때만)</label>${uploader('pf-poster', '', {hint:'영상 로딩 전 보여줄 썸네일'})}</div>
    <div class="bar"><span class="grow"></span><button class="btn btn-ghost btn-sm" onclick="pfEditing=null;renderCopy()">취소</button>
      <button class="btn btn-primary btn-sm" onclick="savePortfolioItem('${placement}')">추가</button></div>
  </div>`;
}
function savePortfolioItem(placement){
  const url = av('pf-url');
  if(!url){ toastA('이미지 또는 영상 주소를 넣으세요'); return; }
  admDo(Admin.upsertPortfolioItem({
    placement, media_type: document.getElementById('pf-type').value,
    url, poster_url: av('pf-poster'), alt: av('pf-alt'), active: true,
  }), 0);
  pfEditing = null;
}

function pkgForm(p){
  return `<div class="sect" style="margin-top:0;padding-top:16px;border-top:1px solid var(--adm-line)">
    <h4>${esc(p.name)} (${esc(p.slug)})</h4>
    <div class="fgrid">
      <div class="fld"><label>이름</label><input id="pkg-name-${p.slug}" value="${esc(p.name)}"></div>
      <div class="fld"><label>인플루언서 인원수</label><input id="pkg-cnt-${p.slug}" type="number" value="${p.influencer_count}"></div>
      <div class="fld"><label>가격(원, 부가세 별도)</label><input id="pkg-price-${p.slug}" type="number" value="${p.price_krw}"></div>
    </div>
    <div class="fld"><label>설명</label><input id="pkg-desc-${p.slug}" value="${esc(p.description)}"></div>
    <button class="btn btn-primary btn-sm" onclick="savePackage('${p.slug}')">저장</button>
  </div>`;
}
function savePackage(slug){
  admDo(Admin.upsertPackage({
    slug, name: av('pkg-name-'+slug), influencer_count: Number(av('pkg-cnt-'+slug))||0,
    price_krw: Number(av('pkg-price-'+slug))||0, description: av('pkg-desc-'+slug),
    sort_order: TV_PACKAGES.find(x=>x.slug===slug)?.sort_order ?? 0,
  }), 0);
}
```

- [ ] **Step 2: Verify no JS syntax errors**

Run: `node --check "C:\Users\이건희\creplanet-clone\assets\js\admin.js"`
Expected: no output, exit code 0.

- [ ] **Step 3: Commit**

```bash
cd "C:\Users\이건희\creplanet-clone"
git add assets/js/admin.js
git commit -m "feat(admin): add portfolio and package pricing CMS tab"
```

---

## Task 10: `admin.js` — Settings tab

**Files:**
- Modify: `C:\Users\이건희\creplanet-clone\assets\js\admin.js` (append)

**Interfaces:**
- Consumes: `Admin.changePassword`, `TvImg.usage/gc`, `TV_BACKEND`
- Produces: `renderSettings()` (called from `renderAll()`, already wired in Task 6)

- [ ] **Step 1: Append settings tab** (adapted from `makenov/assets/js/admin.js` lines 704-734, dropping the data.js-export/JSON-backup section since Trevity's Supabase-first path makes that unnecessary — YAGNI)

```js
/* ============================================================
   설정
   ============================================================ */
function renderSettings(){
  document.getElementById('tab-settings').innerHTML = `
    <div class="card"><h3>연결 상태</h3>
      <p class="note">백엔드: <b>${isSB() ? 'Supabase (실서비스)' : '브라우저 저장 (로컬 테스트)'}</b>
      ${isSB() ? '' : '<br>supabase/README.md를 따라 프로젝트를 만들고 assets/js/config.js에 키를 넣으면 실서비스 모드로 전환됩니다.'}</p></div>
    ${isSB() ? '' : `
    <div class="card"><h3>관리자 비밀번호 변경</h3>
      <div class="fgrid two"><div class="fld"><label>새 비밀번호</label><input id="set-pw" type="password"></div>
      <div class="fld"><label>새 비밀번호 확인</label><input id="set-pw2" type="password"></div></div>
      <button class="btn btn-primary btn-sm" onclick="changePw()">변경</button></div>`}
    <div class="card"><h3>업로드 이미지 저장공간</h3>
      <p class="note">${isSB() ? 'Supabase Storage에 저장됩니다.' : '이 브라우저 안에 저장됩니다(IndexedDB). Supabase 연결 시 자동으로 Storage로 전환됩니다.'}</p>
      <div id="img-usage"><p class="note" style="margin:0">불러오는 중…</p></div>
      <div class="bar" style="margin:14px 0 0"><button class="btn btn-ghost btn-sm" onclick="runGc()">사용하지 않는 이미지 정리</button></div></div>`;
  renderStorage();
}
async function renderStorage(){
  const el = document.getElementById('img-usage');
  if(!el) return;
  const u = await TvImg.usage();
  const pct = u.quota ? Math.min(100, (u.used / u.quota) * 100) : 0;
  el.innerHTML = isSB()
    ? `<p class="note" style="margin:0">Supabase Storage 사용량은 대시보드에서 확인하세요.</p>`
    : `<p class="note" style="margin:0">업로드 이미지 <b>${u.count}장</b> · ${fmtBytes(u.used)}${u.quota?` / 여유 ${fmtBytes(u.quota)} (${pct.toFixed(1)}%)`:''}</p>`;
}
async function runGc(){
  const n = await TvImg.gc();
  toastA(n ? `사용하지 않는 이미지 ${n}장을 정리했습니다` : '정리할 이미지가 없습니다');
  renderStorage();
}
function changePw(){
  const a=av('set-pw'), b=av('set-pw2');
  if(a.length<4){ toastA('4자 이상 입력하세요'); return; }
  if(a!==b){ toastA('두 비밀번호가 다릅니다'); return; }
  Admin.changePassword(a); toastA('비밀번호가 변경되었습니다');
  document.getElementById('set-pw').value=''; document.getElementById('set-pw2').value='';
}
```

- [ ] **Step 2: Verify no JS syntax errors, and that every function `renderAll()` calls now exists**

Run: `node --check "C:\Users\이건희\creplanet-clone\assets\js\admin.js" && grep -c "^function renderDash\|^function renderInq\|^function renderBlog\|^function renderCopy\|^function renderSettings" "C:\Users\이건희\creplanet-clone\assets\js\admin.js"`
Expected: no syntax error, count line prints `5`.

- [ ] **Step 3: Commit**

```bash
cd "C:\Users\이건희\creplanet-clone"
git add assets/js/admin.js
git commit -m "feat(admin): add settings tab"
```

---

## Task 11: `site-data.js` — public blog listing renderer

**Files:**
- Create: `C:\Users\이건희\creplanet-clone\assets\js\site-data.js`

**Interfaces:**
- Consumes: `TV_BLOG_POSTS` (Task 2/4), `data-js` load order.
- Produces: `renderBlogList()` — called from `blog.html` (Task 13's wiring) after `TvBoot()` resolves. Also produces `TvBoot()` — a single async bootstrap every public page (blog.html, blog-post.html, index.html, the 5 hero-wall pages, vietnam-tiktok.html) calls once to ensure `TV_BLOG_POSTS`/`TV_PORTFOLIO`/`TV_PACKAGES` are populated before rendering, working in both local and Supabase mode.

- [ ] **Step 1: Write `site-data.js`**

```js
/* 공개 페이지 부트스트랩 — local/Supabase 어느 모드든 TV_BLOG_POSTS 등 전역 배열을 채운 뒤 resolve된다. */
async function TvBoot(){
  if(typeof TvData !== 'undefined'){ await TvData.boot(); return; }
  // 로컬 모드: store.js의 오버라이드를 전역 배열에 얹는다
  const override = (key, seedArr) => {
    try{
      const raw = localStorage.getItem(key);
      if(raw){ const list = JSON.parse(raw); seedArr.length = 0; seedArr.push(...list); }
    }catch(e){}
  };
  override('tv_blog_override', TV_BLOG_POSTS);
  override('tv_portfolio_override', TV_PORTFOLIO);
  override('tv_packages_override', TV_PACKAGES);
  try{ await TvImg.loadCache(); }catch(e){}
}

/* ---------- 블로그 목록 (blog.html) ---------- */
function renderBlogList(){
  const grid = document.querySelector('.tv-grid');
  if(!grid) return;
  const posts = TV_BLOG_POSTS.filter(p=>p.published !== false)
    .sort((a,b)=>String(b.created_at||'').localeCompare(String(a.created_at||'')));

  const catCounts = {};
  posts.forEach(p=>{ catCounts[p.category] = (catCounts[p.category]||0) + 1; });
  document.querySelectorAll('.tv-cats li').forEach(li=>{
    const cat = li.getAttribute('data-cat');
    const span = li.querySelector('span:last-child');
    if(!span) return;
    span.textContent = cat==='all' ? `(${posts.length})` : `(${catCounts[cat]||0})`;
  });

  grid.innerHTML = posts.map(p => `
    <article class="tv-card" data-cat="${esc(p.category)}" data-title="${esc(p.title)}">
      <a href="./blog-post.html?slug=${encodeURIComponent(p.slug)}">
        <div class="tv-thumb"><img src="${esc(p.thumbnail_url)}" alt="${esc(p.title)}" loading="lazy"></div>
        <div class="tv-card-body"><span class="tv-chip">${esc(p.category)}</span><h3>${esc(p.title)}</h3>
        <div class="tv-meta"><time>${esc(String(p.created_at||'').slice(0,10))}</time><span>${p.read_minutes||4}분 분량</span></div></div>
      </a></article>`).join('') || '<p style="padding:40px;color:#8B95A1">아직 글이 없습니다.</p>';
}
function esc(s){ return String(s??'').replace(/[&<>"']/g, m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m])); }

/* ---------- 포트폴리오 롤/히어로 (index.html 및 5개 페이지) ----------
   selector는 "행" 자체를 직접 가리켜야 한다 (컨테이너가 아니라 각 row 엘리먼트).
   index.html처럼 행이 여러 개면 selector가 여러 엘리먼트에 매치되게 넘긴다
   (예: '.tvpf-rows [data-pf-row]'). 히어로 페이지처럼 행이 하나면 그 엘리먼트 자체를
   가리키는 selector를 넘긴다 (예: '[data-pf-hero]'). */
function renderPortfolioRoll(selector, placement){
  const rows = document.querySelectorAll(selector);
  const items = TV_PORTFOLIO.filter(x=>x.placement===placement && x.active!==false).sort((a,b)=>a.sort_order-b.sort_order);
  if(!items.length || !rows.length) return;
  rows.forEach((row, ri) => {
    const slice = ri % 2 === 0 ? items : [...items].reverse();
    const repeated = [...slice, ...slice, ...slice, ...slice];
    row.innerHTML = repeated.map(it => it.media_type === 'video'
      ? `<video src="${esc(it.url)}" muted loop playsinline autoplay preload="metadata" poster="${esc(it.poster_url)}"></video>`
      : `<img src="${esc(it.url)}" alt="${esc(it.alt)}" loading="lazy"/>`
    ).join('');
  });
}

/* ---------- 패키지 카드 (vietnam-tiktok.html) ---------- */
function renderPackages(containerSelector){
  const el = document.querySelector(containerSelector);
  if(!el) return;
  const pkgs = TV_PACKAGES.slice().sort((a,b)=>a.sort_order-b.sort_order);
  const cards = el.querySelectorAll('[data-pkg-slug]');
  cards.forEach(card => {
    const slug = card.getAttribute('data-pkg-slug');
    const p = pkgs.find(x=>x.slug===slug);
    if(!p) return;
    const nameEl = card.querySelector('[data-pkg-name]');
    const cntEl = card.querySelector('[data-pkg-count]');
    const priceEl = card.querySelector('[data-pkg-price]');
    const descEl = card.querySelector('[data-pkg-desc]');
    if(nameEl) nameEl.textContent = p.name;
    if(cntEl) cntEl.textContent = p.influencer_count + '명';
    if(priceEl) priceEl.textContent = p.price_krw.toLocaleString('ko-KR') + '원';
    if(descEl) descEl.textContent = p.description;
  });
}
```

- [ ] **Step 2: Verify no JS syntax errors**

Run: `node --check "C:\Users\이건희\creplanet-clone\assets\js\site-data.js"`
Expected: no output, exit code 0.

- [ ] **Step 3: Commit**

```bash
cd "C:\Users\이건희\creplanet-clone"
git add assets/js/site-data.js
git commit -m "feat(cms): add public-page renderer for blog list, portfolio rolls, packages"
```

---

## Task 12: `blog.html` — wire to dynamic renderer

**Files:**
- Modify: `C:\Users\이건희\creplanet-clone\blog.html`

**Interfaces:**
- Consumes: `TvBoot()`, `renderBlogList()` (Task 11)

- [ ] **Step 1: Remove the 4 hardcoded `<article class="tv-card">` elements from `.tv-grid`**

Find the `<div class="tv-grid">...</div>` block (currently containing 4 static `<article>` cards) and replace its inner content with nothing — `renderBlogList()` will populate it:

```
Old: <div class="tv-grid"><article class="tv-card" data-cat="베트남 시장" ...>...</article>...(4 total)...</div>
New: <div class="tv-grid"></div>
```

- [ ] **Step 2: Add script tags before `</body>` and a boot call**

```html
<script src="./assets/js/config.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>
<script src="./assets/js/data.js"></script>
<script src="./assets/js/store.js"></script>
<script src="./assets/js/upload.js"></script>
<script src="./assets/js/store-supabase.js"></script>
<script src="./assets/js/site-data.js"></script>
<script>TvBoot().then(renderBlogList);</script>
```

- [ ] **Step 3: Verify the grid is empty in source and boot script is present**

Run: `grep -c "tv-card" "C:\Users\이건희\creplanet-clone\blog.html"; grep -c "TvBoot().then(renderBlogList)" "C:\Users\이건희\creplanet-clone\blog.html"`
Expected: first count `0`, second count `1`.

- [ ] **Step 4: Browser check**

Start preview: server already runs at port 5695 (`.claude/launch.json` entry `creplanet-clone`). Open `http://localhost:5695/blog.html`, confirm 4 cards render (from `tv_blog_override` if Task 8 was tested, otherwise the page will be empty until Task 1's seed is loaded via Supabase, or until an admin creates posts in local mode — note this in the task's manual verification, it is expected to be empty at this point since local mode starts with `TV_BLOG_POSTS` empty and no override yet).

- [ ] **Step 5: Commit**

```bash
cd "C:\Users\이건희\creplanet-clone"
git add blog.html
git commit -m "feat(cms): wire blog.html to dynamic blog_posts renderer"
```

---

## Task 13: `blog-post.html` template + redirect stubs for old URLs

**Files:**
- Create: `C:\Users\이건희\creplanet-clone\blog-post.html`
- Modify: `C:\Users\이건희\creplanet-clone\blog-market.html`, `blog-midtier.html`, `blog-diy.html`, `blog-hantown.html` (replace entire contents with redirect stub)

**Interfaces:**
- Consumes: `Store.blogPost(slug)`, `TvBoot()` (Task 11)

- [ ] **Step 1: Create `blog-post.html`** (structure copied from `blog.html`'s `<head>`/header/footer — read `blog.html` first to copy its exact header/nav/footer markup verbatim so styling matches, then insert this body)

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title id="tv-post-title">블로그 | 트래비티</title>
<!-- COPY: same <link> tags as blog.html's <head> (Tailwind CSS, favicon, fonts) -->
</head>
<body class="max-[767px]:min-w-[360px] min-[767px]:min-w-[1440px]">
<!-- COPY: same <header class="tvh">...</header> markup as blog.html, verbatim -->
<div class="tv-bloghero"><h1 id="tv-post-cat">블로그</h1></div>
<div style="max-width:760px;margin:0 auto;padding:40px 20px 100px">
  <article id="tv-post-body">
    <p style="color:#8B95A1">불러오는 중…</p>
  </article>
</div>
<!-- COPY: same <footer> markup as blog.html, verbatim -->
<script src="./assets/js/config.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>
<script src="./assets/js/data.js"></script>
<script src="./assets/js/store.js"></script>
<script src="./assets/js/upload.js"></script>
<script src="./assets/js/store-supabase.js"></script>
<script src="./assets/js/site-data.js"></script>
<script>
TvBoot().then(async () => {
  const slug = new URLSearchParams(location.search).get('slug');
  const post = slug ? await Store.blogPost(slug) : null;
  const body = document.getElementById('tv-post-body');
  if(!post){ body.innerHTML = '<p>글을 찾을 수 없습니다. <a href="./blog.html">블로그 목록으로</a></p>'; return; }
  document.title = post.title + ' | 트래비티';
  document.getElementById('tv-post-title').textContent = post.title + ' | 트래비티';
  document.getElementById('tv-post-cat').textContent = post.category;
  body.innerHTML = `<h1 style="font-size:28px;font-weight:800;margin-bottom:10px">${esc(post.title)}</h1>
    <p style="color:#8B95A1;font-size:13px;margin-bottom:28px">${esc(String(post.created_at||'').slice(0,10))} · ${post.read_minutes||4}분 분량</p>
    <div style="line-height:1.85;font-size:16px">${post.body_html}</div>`;
});
</script>
</body>
</html>
```

- [ ] **Step 2: Replace `blog-market.html` with a redirect stub**

```html
<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8">
<meta http-equiv="refresh" content="0; url=./blog-post.html?slug=market">
<script>location.replace('./blog-post.html?slug=market');</script>
<title>트래비티</title></head><body></body></html>
```

- [ ] **Step 3: Replace `blog-midtier.html`, `blog-diy.html`, `blog-hantown.html` with the same stub pattern**, substituting `slug=midtier`, `slug=diy`, `slug=hantown` respectively (same two redirect mechanisms — `meta refresh` as a no-JS fallback, `location.replace` as the primary path since it doesn't add a history entry).

- [ ] **Step 4: Verify all 4 stubs redirect to the right slug**

Run: `for f in blog-market:market blog-midtier:midtier blog-diy:diy blog-hantown:hantown; do file="C:\Users\이건희\creplanet-clone\${f%%:*}.html"; slug="${f##*:}"; grep -q "slug=$slug" "$file" && echo "$file OK" || echo "$file MISSING slug=$slug"; done`
Expected: all 4 lines print `OK`.

- [ ] **Step 5: Commit**

```bash
cd "C:\Users\이건희\creplanet-clone"
git add blog-post.html blog-market.html blog-midtier.html blog-diy.html blog-hantown.html
git commit -m "feat(cms): add blog-post.html template, redirect old blog URLs to it"
```

---

## Task 14: `inquiry.html` — wire to Supabase/local Store instead of broken Google Sheet

**Files:**
- Modify: `C:\Users\이건희\creplanet-clone\inquiry.html`

**Interfaces:**
- Consumes: `Store.submitInquiry(data)` (Task 2/4)

- [ ] **Step 1: Read the current submit handler** to find the exact `SHEET_ENDPOINT` fetch block

Run: `grep -n "SHEET_ENDPOINT" "C:\Users\이건희\creplanet-clone\inquiry.html"`

- [ ] **Step 2: Replace the fetch-to-Google-Sheet call with `Store.submitInquiry`**

The existing code (per this session's earlier investigation) does:
```js
const SHEET_ENDPOINT = '';
// ...
if(!SHEET_ENDPOINT) { console.warn('SHEET_ENDPOINT 미설정 — 접수 데이터가 저장되지 않습니다.'); }
```
Replace the whole submit-time block that references `SHEET_ENDPOINT` with:
```js
const result = await Store.submitInquiry({
  name: av('inq-name'), company: av('inq-company'), phone: av('inq-phone'),
  email: av('inq-email'), message: av('inq-message'), source_page: 'inquiry.html',
});
if(!result.ok){ alert('문의 접수에 실패했습니다. 다시 시도해 주세요.'); return; }
```
(adjust the field-reading calls — `av('inq-name')` etc — to match whatever the existing form's actual input `id`s are, found in Step 1's surrounding markup; add a local `function av(id){ return (document.getElementById(id)||{}).value?.trim()||''; }` helper if `inquiry.html` doesn't already define one, since it doesn't load `admin.js`)

- [ ] **Step 3: Add script tags before `</body>`**

```html
<script src="./assets/js/config.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>
<script src="./assets/js/data.js"></script>
<script src="./assets/js/store.js"></script>
<script src="./assets/js/upload.js"></script>
<script src="./assets/js/store-supabase.js"></script>
<script src="./assets/js/site-data.js"></script>
<script>TvBoot();</script>
```
`site-data.js` (Task 11) is what defines `TvBoot` — it must be loaded here even though `inquiry.html` doesn't use its blog/portfolio renderers, since `TvBoot()` is also what calls `TvData.boot()` in Supabase mode to establish the client session before `Store.submitInquiry` can insert. In local mode `TvBoot()` is a cheap no-op-ish localStorage read, safe to call unconditionally.

- [ ] **Step 4: Verify `SHEET_ENDPOINT` is gone and `Store.submitInquiry` is wired**

Run: `grep -c "SHEET_ENDPOINT" "C:\Users\이건희\creplanet-clone\inquiry.html"; grep -c "Store.submitInquiry" "C:\Users\이건희\creplanet-clone\inquiry.html"`
Expected: first count `0`, second count `1`.

- [ ] **Step 5: Browser check** — open `http://localhost:5695/inquiry.html`, fill the form, submit, then open browser console and run `JSON.parse(localStorage.getItem('tv_inquiries'))` (local mode) — expect an array with the just-submitted entry.

- [ ] **Step 6: Commit**

```bash
cd "C:\Users\이건희\creplanet-clone"
git add inquiry.html
git commit -m "fix(inquiry): replace broken Google Sheets endpoint with Store.submitInquiry"
```

---

## Task 15: `index.html` — dynamic portfolio roll

**Files:**
- Modify: `C:\Users\이건희\creplanet-clone\index.html`

**Interfaces:**
- Consumes: `TvBoot()`, `renderPortfolioRoll()` (Task 11)

- [ ] **Step 1: Add `data-pf-row` markers to the two `.tvpf-row` divs** so `renderPortfolioRoll` can find them without depending on exact class match (the class already exists per this session's earlier fix; this step only adds the data attribute)

Find: `<div class="tvpf-row " style="animation-duration:58s">` → add `data-pf-row` : `<div class="tvpf-row" data-pf-row style="animation-duration:58s">`
Find: `<div class="tvpf-row rev" style="animation-duration:74s">` → add `data-pf-row` : `<div class="tvpf-row rev" data-pf-row style="animation-duration:74s">`

- [ ] **Step 2: Add script tags + boot call before `</body>`**

```html
<script src="./assets/js/config.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>
<script src="./assets/js/data.js"></script>
<script src="./assets/js/store.js"></script>
<script src="./assets/js/upload.js"></script>
<script src="./assets/js/store-supabase.js"></script>
<script src="./assets/js/site-data.js"></script>
<script>TvBoot().then(() => renderPortfolioRoll('.tvpf-rows [data-pf-row]', 'home-roll'));</script>
```

- [ ] **Step 3: Verify markers and boot call are present**

Run: `grep -c "data-pf-row" "C:\Users\이건희\creplanet-clone\index.html"; grep -c "renderPortfolioRoll" "C:\Users\이건희\creplanet-clone\index.html"`
Expected: first count `2`, second count `1`.

- [ ] **Step 4: Browser check** — since `TV_PORTFOLIO` starts empty in local mode with no override yet, this will render an EMPTY roll until an admin adds portfolio items or Supabase's seed loads. This is expected at this point in the plan; visually confirm no console errors on `http://localhost:5695/index.html` (an empty `.tvpf-rows` is correct, not a bug, until Task 1's seed or an admin entry exists).

- [ ] **Step 5: Commit**

```bash
cd "C:\Users\이건희\creplanet-clone"
git add index.html
git commit -m "feat(cms): wire index.html portfolio roll to dynamic renderer"
```

---

## Task 16: Hero-wall pages — dynamic portfolio (5 files)

**Files:**
- Modify: `C:\Users\이건희\creplanet-clone\local-vn.html`, `stay.html`, `tourist-vn.html`, `tourist-cn.html`, `vietnam-tiktok.html`

**Interfaces:**
- Consumes: `TvBoot()`, `renderPortfolioRoll()` (Task 11)

**Note:** confirmed earlier this session that `swiper-slide` markup on these pages is static (no actual Swiper.js library loaded) — the horizontal motion is pure CSS. `renderPortfolioRoll` only needs to replace the slide contents, not reimplement any carousel behavior.

- [ ] **Step 1: For each of the 5 files, find the swiper container** (the parent element wrapping the repeated `<div class="swiper-slide ...">` elements)

Run per file: `grep -boa 'swiper-wrapper\|class="[^"]*swiper[^"]*"' "C:\Users\이건희\creplanet-clone\local-vn.html" | head -3`
(repeat for the other 4 files — identify the exact wrapper class/selector for each; they should share the same markup pattern since all 5 came from the same source mirror per this session's investigation of `local-vn.html`)

- [ ] **Step 2: Add a `data-pf-hero` attribute directly on the element whose children are the repeated `swiper-slide` items** in each of the 5 files — i.e. the immediate parent of the `<div class="swiper-slide ...">` elements found in Step 1, not an outer wrapper. `renderPortfolioRoll` (Task 11) replaces `innerHTML` of whatever matches the selector, so the selector must resolve to that exact parent.

- [ ] **Step 3: Add script tags + boot call before `</body>`** in each of the 5 files:

```html
<script src="./assets/js/config.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>
<script src="./assets/js/data.js"></script>
<script src="./assets/js/store.js"></script>
<script src="./assets/js/upload.js"></script>
<script src="./assets/js/store-supabase.js"></script>
<script src="./assets/js/site-data.js"></script>
<script>TvBoot().then(() => renderPortfolioRoll('[data-pf-hero]', 'hero-wall'));</script>
```

Since `renderPortfolioRoll('[data-pf-hero]', ...)` now (per Task 11's fix) queries `selector` directly rather than a descendant, this only works correctly because Step 2 put `data-pf-hero` on the item-parent itself, not a wrapper around it.

- [ ] **Step 4: Verify each of the 5 files has the marker and boot call**

Run: `for f in local-vn stay tourist-vn tourist-cn vietnam-tiktok; do file="C:\Users\이건희\creplanet-clone\$f.html"; grep -q "data-pf-hero" "$file" && grep -q "renderPortfolioRoll" "$file" && echo "$f OK" || echo "$f MISSING"; done`
Expected: all 5 lines print `OK`.

- [ ] **Step 5: Browser check** — open each of the 5 pages, confirm no console errors (empty hero wall expected until portfolio items exist, same caveat as Task 15).

- [ ] **Step 6: Commit**

```bash
cd "C:\Users\이건희\creplanet-clone"
git add local-vn.html stay.html tourist-vn.html tourist-cn.html vietnam-tiktok.html
git commit -m "feat(cms): wire 5 hero-wall pages to dynamic portfolio renderer"
```

---

## Task 17: `vietnam-tiktok.html` — dynamic package pricing

**Files:**
- Modify: `C:\Users\이건희\creplanet-clone\vietnam-tiktok.html`

**Interfaces:**
- Consumes: `TvBoot()`, `renderPackages()` (Task 11)

- [ ] **Step 1: Find the 3 package cards** (스타터/그로스/도미넌트 per this session's HANDOFF review) and add `data-pkg-slug`/`data-pkg-name`/`data-pkg-count`/`data-pkg-price`/`data-pkg-desc` attributes to the relevant elements

Run: `grep -n "스타터\|그로스\|도미넌트" "C:\Users\이건희\creplanet-clone\vietnam-tiktok.html" | head -10`
Then locate each card's name/count/price/description elements and add:
- Card wrapper: `data-pkg-slug="starter"` / `"growth"` / `"dominant"`
- Name element: `data-pkg-name`
- Count element: `data-pkg-count`
- Price element: `data-pkg-price`
- Description element: `data-pkg-desc`
- Also add a common wrapper class or id around all 3 cards if none exists, e.g. `id="tv-packages"`, to use as `renderPackages`'s `containerSelector`.

- [ ] **Step 2: Add script tags + boot call before `</body>`**

```html
<script src="./assets/js/config.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>
<script src="./assets/js/data.js"></script>
<script src="./assets/js/store.js"></script>
<script src="./assets/js/upload.js"></script>
<script src="./assets/js/store-supabase.js"></script>
<script src="./assets/js/site-data.js"></script>
<script>TvBoot().then(() => { renderPortfolioRoll('[data-pf-hero]', 'hero-wall'); renderPackages('#tv-packages'); });</script>
```
(this page needs both the hero-wall renderer from Task 16 AND the package renderer — combine both calls here since Task 16 already added the hero-wall script block to this same file; do not duplicate the `<script src>` tags, only add the `renderPackages` call to the existing inline `<script>` block)

- [ ] **Step 3: Verify markers and call are present**

Run: `grep -c "data-pkg-slug" "C:\Users\이건희\creplanet-clone\vietnam-tiktok.html"; grep -c "renderPackages" "C:\Users\이건희\creplanet-clone\vietnam-tiktok.html"`
Expected: first count `3`, second count `1`.

- [ ] **Step 4: Browser check** — open `http://localhost:5695/vietnam-tiktok.html`, confirm no console errors (package text stays as static original markup values until an admin edits packages, since `renderPackages` only overwrites text content when `TV_PACKAGES` has matching slugs — with an empty local store this is a no-op, which is correct: the static original copy remains visible as a fallback).

- [ ] **Step 5: Commit**

```bash
cd "C:\Users\이건희\creplanet-clone"
git add vietnam-tiktok.html
git commit -m "feat(cms): wire vietnam-tiktok.html package cards to dynamic pricing"
```

---

## Task 18: End-to-end local-mode verification

**Files:** none (verification only)

- [ ] **Step 1: Start the server**

Run: `cd "C:\Users\이건희\creplanet-clone" && python -m http.server 5695` (or use the existing `.claude/launch.json` `creplanet-clone` preview)

- [ ] **Step 2: Log into admin with the default local password**

Open `http://localhost:5695/admin/`, enter `trevity2026`, confirm the dashboard renders with 0 inquiries / 0 blog posts / 0 portfolio / 0 packages (packages will show `0` count from `TV_PACKAGES.length` since local mode has no seed — this is expected; Supabase mode picks up Task 1's seed).

- [ ] **Step 3: Create one blog post through the admin UI**, confirm it appears in `blog.html` and is reachable at `blog-post.html?slug=<slug>`.

- [ ] **Step 4: Add one portfolio item (placement: home-roll)**, confirm `index.html`'s roll now shows it.

- [ ] **Step 5: Submit `inquiry.html`'s form**, confirm it appears in the admin's 문의함 tab.

- [ ] **Step 6: No commit for this task** — it is a manual verification checkpoint. If any step fails, return to the relevant earlier task and fix before proceeding.

---

## Deferred (explicitly out of scope, per design doc section 6)

- Inquiry arrival notifications (Telegram/email)
- Copy CMS for pages other than the portfolio rolls and vietnam-tiktok packages (export/famtour/stay/etc body copy stays static HTML)
- Multi-admin roles/permissions beyond the single `admins` table membership check
