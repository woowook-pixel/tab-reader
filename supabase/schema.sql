-- 기존 Supabase 프로젝트에 Strum 전용 테이블만 추가합니다. SQL Editor에서 한 번 실행합니다.
-- 모든 이름에 strum_ 접두사를 붙였고, 기존 테이블·정책·함수는 건드리지 않습니다.
-- 여러 번 실행해도 안전합니다(이미 있으면 건너뜀). 로그인 사용자(auth.users)는 다른 앱과 공유합니다.
create table if not exists public.strum_songs (
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  id      text not null,
  title   text not null,
  text    text not null default '',
  images  jsonb not null default '[]'::jsonb,
  tr      int  not null default 0,
  updated bigint not null,
  primary key (user_id, id)
);

alter table public.strum_songs enable row level security;

-- 이 테이블에만 적용되는 정책: 로그인한 사용자는 자기 곡만 읽고 쓰고 지운다.
do $$
begin
  if not exists (
    select 1 from pg_policies
    where schemaname = 'public' and tablename = 'strum_songs' and policyname = 'strum_songs_own'
  ) then
    create policy strum_songs_own on public.strum_songs
      for all to authenticated
      using (user_id = (select auth.uid()))
      with check (user_id = (select auth.uid()));
  end if;
end $$;
