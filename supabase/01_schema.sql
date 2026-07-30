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
