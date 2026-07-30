alter table admins enable row level security;
create policy "admins_select_self" on admins for select using (auth.uid() = user_id);
-- no insert/update/delete policy for admins on purpose: only editable via SQL editor / service_role,
-- so no client (even a logged-in one) can ever add themselves as admin.
