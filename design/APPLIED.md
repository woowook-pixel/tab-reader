# 공통 디자인 적용 현황 (Strum)

- 사용 중인 공통 CSS: v1 (https://personal-design-rho.vercel.app/v1/tokens.css)
- 적용한 CHANGELOG 번호: 002
- 참고: 이 저장소는 예전 복사본 `design/tokens.css`도 계속 불러온다(`index.html`의 `<link>` 두 줄, 복사본이 먼저, 중앙 CSS가 그 다음). 복사본을 지우고 중앙 CSS만 쓰려면 `design/tokens.css` 링크를 지우면 된다.

## 002 상단 헤더 위치·높이 통일

- 모든 화면(악보 목록, 악보 보기, 새 곡)의 상단 바를 `.pf-header > .pf-topbar > (.pf-wordmark, .pf-actions > .pf-action)` 구조로 바꿨다.
- 앱이 직접 주던 화면 위 여백, 안전영역 계산, 상단 바 높이·고정(sticky) 규칙, 워드마크·오른쪽 버튼의 크기·자간·여백을 지우고 공통 클래스에 맡겼다.
- 제목 블록(`.pf-titleblock`)은 헤더 바로 다음에 두고, 앱이 준 제목 위 여백을 지웠다(위 여백은 중앙 CSS의 `.pf-header + .pf-titleblock`이 24px로 준다).
- 화면 좌우 여백(`var(--pf-side)`)은 각 화면 바깥 상자(`#lib`, `#view`, `#edit`)가 갖고, 헤더가 음수 여백으로 화면 끝까지 채운다.
- 악보 보기의 섹션 탭이 헤더 아래에 붙는 위치(`--vtop`)는 CSS의 안전영역 계산 대신 헤더 높이를 JS(`syncVtop`)로 읽어 쓴다.
- viewport 메타에 `viewport-fit=cover`는 이미 있었다. 이 앱에는 하단 탭바가 없어 탭바 수정은 해당 없음.
