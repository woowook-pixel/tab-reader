# Supabase 설정 (기존 프로젝트에 Strum 추가)

이미 쓰는 Supabase 프로젝트에 **추가만** 합니다. 새 프로젝트를 만들 필요가 없고, 기존 테이블·정책·로그인 설정은 바꾸지 않습니다.

1. SQL Editor에서 `supabase/schema.sql` 전체를 실행한다.
   - `strum_songs` 테이블과 이 테이블 전용 보안 정책(`strum_songs_own`)만 만든다. 이미 있으면 건너뛰므로 다시 실행해도 안전하다.
2. Authentication > Providers > Google이 이미 켜져 있으면 그대로 둔다(같은 OAuth 클라이언트를 공유). 꺼져 있을 때만 켜고 Google Cloud의 OAuth 클라이언트 ID와 비밀번호를 넣는다.
3. Authentication > URL Configuration > **Redirect URLs에 `https://woowook-pixel.github.io/tab-reader/`를 추가**한다. 기존 목록은 지우지 않는다. Site URL은 기존 값을 그대로 둔다.
4. Project Settings > API의 **Project URL**과 **anon public key**를 `index.html`의 `SUPABASE_URL`, `SUPABASE_KEY`에 넣는다(다른 앱이 쓰는 값과 같다. service_role key는 넣지 않는다).

참고
- 같은 주소(`woowook-pixel.github.io`)의 다른 앱과 로그인 세션이 공유될 수 있다. Strum에서 로그아웃해도 다른 앱의 로그인은 끊기지 않게 현재 기기에서만 로그아웃한다(`scope: 'local'`).
- 앱 쪽 저장 키는 모두 `tr.` 접두사를 쓰고, 서버 테이블은 `strum_songs`다.
