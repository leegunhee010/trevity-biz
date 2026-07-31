-- ========== 01_schema.sql ==========
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


-- ========== 02_seed.sql ==========
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


-- ========== 04_copy.sql ==========
-- 사이트 카피 오버라이드 (관리자 텍스트 편집)
-- key = 원문 텍스트의 djb2 해시 (assets/js/copy-data.js의 k 값)
create table site_copy (
  key text primary key,
  value text not null default '',
  updated_at timestamptz not null default now()
);
alter table site_copy enable row level security;
create policy "copy_select_public" on site_copy for select using (true);
create policy "copy_insert_admin" on site_copy for insert with check (is_admin());
create policy "copy_update_admin" on site_copy for update using (is_admin());
create policy "copy_delete_admin" on site_copy for delete using (is_admin());


-- ========== storage: trevity-images 버킷 + 정책 ==========
insert into storage.buckets (id, name, public) values ('trevity-images','trevity-images', true)
on conflict (id) do nothing;
create policy "img_read"  on storage.objects for select using (bucket_id = 'trevity-images');
create policy "img_write" on storage.objects for insert with check (bucket_id = 'trevity-images' and is_admin());
create policy "img_del"   on storage.objects for delete using (bucket_id = 'trevity-images' and is_admin());


-- ========== 03_lockdown.sql ==========
alter table admins enable row level security;
create policy "admins_select_self" on admins for select using (auth.uid() = user_id);
-- no insert/update/delete policy for admins on purpose: only editable via SQL editor / service_role,
-- so no client (even a logged-in one) can ever add themselves as admin.
