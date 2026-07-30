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
