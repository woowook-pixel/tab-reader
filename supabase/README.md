# Supabase 설정 (Google 로그인 + 악보 저장)

1. https://supabase.com 에서 프로젝트를 만든다.
2. SQL Editor에서 `supabase/schema.sql` 전체를 실행한다(`songs` 테이블과 본인 곡만 접근하는 RLS 정책이 만들어진다).
3. Google Cloud Console > API 및 서비스 > 사용자 인증 정보에서 OAuth 클라이언트 ID(웹 애플리케이션)를 만든다.
   - 승인된 리디렉션 URI: Supabase의 Authentication > Providers > Google 화면에 보이는 Callback URL
4. Supabase > Authentication > Providers > Google을 켜고 클라이언트 ID와 비밀번호를 넣는다.
5. Supabase > Authentication > URL Configuration
   - Site URL: `https://woowook-pixel.github.io/tab-reader/`
   - Redirect URLs에 같은 주소를 추가한다.
6. Project Settings > API의 **Project URL**과 **anon public key**를 `index.html`의 `SUPABASE_URL`, `SUPABASE_KEY`에 넣는다(anon key는 공개용이며 접근은 RLS가 막는다. service_role key는 절대 넣지 않는다).
