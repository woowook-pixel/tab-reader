-- Supabase 대시보드 > SQL Editor에서 한 번 실행합니다.
create table if not exists public.songs (
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  id      text not null,
  title   text not null,
  text    text not null default '',
  images  jsonb not null default '[]'::jsonb,
  tr      int  not null default 0,
  updated bigint not null,
  primary key (user_id, id)
);

alter table public.songs enable row level security;

-- 로그인한 사용자는 자기 곡만 읽고 쓰고 지울 수 있습니다.
drop policy if exists "own songs" on public.songs;
create policy "own songs" on public.songs
  for all to authenticated
  using (user_id = (select auth.uid()))
  with check (user_id = (select auth.uid()));
