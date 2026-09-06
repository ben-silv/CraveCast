-- ═══════════════════════════════════════════════════════════════════════
--  CraveCast — accounts and cloud sync
--
--  Run this once in your Supabase project: SQL Editor → New query → paste
--  → Run. It creates one table, locks it down so each account can only
--  ever touch its own row, and exposes three functions the page calls.
--
--  Nothing here is specific to your project. There are no secrets in this
--  file, and none of it needs to be edited.
-- ═══════════════════════════════════════════════════════════════════════

-- ── one row per account, holding that account's whole CraveCast state ──
create table if not exists public.cravecast_state (
  user_id    uuid primary key references auth.users (id) on delete cascade,
  state      jsonb       not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

-- ── row level security: the database itself enforces the isolation, so a
--    stolen or tampered client can still only reach its own row ──────────
alter table public.cravecast_state enable row level security;

drop policy if exists cravecast_state_select on public.cravecast_state;
drop policy if exists cravecast_state_insert on public.cravecast_state;
drop policy if exists cravecast_state_update on public.cravecast_state;
drop policy if exists cravecast_state_delete on public.cravecast_state;

create policy cravecast_state_select on public.cravecast_state
  for select using ((select auth.uid()) = user_id);

create policy cravecast_state_insert on public.cravecast_state
  for insert with check ((select auth.uid()) = user_id);

create policy cravecast_state_update on public.cravecast_state
  for update using ((select auth.uid()) = user_id)
             with check ((select auth.uid()) = user_id);

create policy cravecast_state_delete on public.cravecast_state
  for delete using ((select auth.uid()) = user_id);

-- ── save: upsert this account's state, server-side, in one round trip ──
--    security invoker, so the policies above still apply.
create or replace function public.cc_save(p_state jsonb)
returns timestamptz
language plpgsql
security invoker
set search_path = public
as $$
declare
  u  uuid        := (select auth.uid());
  ts timestamptz := now();
begin
  if u is null then
    raise exception 'not signed in';
  end if;
  insert into public.cravecast_state (user_id, state, updated_at)
    values (u, p_state, ts)
  on conflict (user_id) do update
    set state = excluded.state, updated_at = excluded.updated_at;
  return ts;
end;
$$;

-- ── load: this account's state, or null when it has never saved ────────
create or replace function public.cc_load()
returns jsonb
language sql
security invoker
set search_path = public
as $$
  select state from public.cravecast_state where user_id = (select auth.uid());
$$;

-- ── delete account: wipes the data, then the login itself ──────────────
--    security definer is required to reach auth.users; auth.uid() is what
--    keeps it to the caller's own account and nobody else's.
create or replace function public.cc_delete_account()
returns void
language plpgsql
security definer
set search_path = ''
as $$
declare
  u uuid := (select auth.uid());
begin
  if u is null then
    raise exception 'not signed in';
  end if;
  delete from public.cravecast_state where user_id = u;
  delete from auth.users where id = u;
end;
$$;

-- ── only signed-in callers may run these ───────────────────────────────
revoke execute on function public.cc_save(jsonb)      from public, anon;
revoke execute on function public.cc_load()           from public, anon;
revoke execute on function public.cc_delete_account() from public, anon;

grant execute on function public.cc_save(jsonb)      to authenticated;
grant execute on function public.cc_load()           to authenticated;
grant execute on function public.cc_delete_account() to authenticated;
