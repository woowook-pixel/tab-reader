# 공통 디자인 적용 현황 (Strum)

- 사용 중인 공통 CSS: v1 (https://personal-design-rho.vercel.app/v1/tokens.css)
- 적용한 CHANGELOG 번호: 002, 003, 004
- 참고: 이 저장소는 예전 복사본 `design/tokens.css`도 계속 불러온다(`index.html`의 `<link>` 두 줄, 복사본이 먼저, 중앙 CSS가 그 다음). 복사본을 지우고 중앙 CSS만 쓰려면 `design/tokens.css` 링크를 지우면 된다.

## 002 상단 헤더 위치·높이 통일

- 모든 화면(악보 목록, 악보 보기, 새 곡)의 상단 바를 `.pf-header > .pf-topbar > (.pf-wordmark, .pf-actions > .pf-action)` 구조로 바꿨다.
- 앱이 직접 주던 화면 위 여백, 안전영역 계산, 상단 바 높이·고정(sticky) 규칙, 워드마크·오른쪽 버튼의 크기·자간·여백을 지우고 공통 클래스에 맡겼다.
- 제목 블록(`.pf-titleblock`)은 헤더 바로 다음에 두고, 앱이 준 제목 위 여백을 지웠다(위 여백은 중앙 CSS의 `.pf-header + .pf-titleblock`이 24px로 준다).
- 화면 좌우 여백(`var(--pf-side)`)은 각 화면 바깥 상자(`#lib`, `#view`, `#edit`)가 갖고, 헤더가 음수 여백으로 화면 끝까지 채운다.
- 악보 보기의 섹션 탭이 헤더 아래에 붙는 위치(`--vtop`)는 CSS의 안전영역 계산 대신 헤더 높이를 JS(`syncVtop`)로 읽어 쓴다.
- viewport 메타에 `viewport-fit=cover`는 이미 있었다. 이 앱에는 하단 탭바가 없어 탭바 수정은 해당 없음.

## 003 새 버전 알림 띠

- `index.html` 끝에 `.pf-update.pf-no-tabbar` 띠를 넣었다(탭바가 없는 앱이라 `pf-no-tabbar`를 항상 붙임). 악보 보기에는 아래 재생 바가 있어 `body.reading`일 때만 그 높이만큼 띠를 올린다(CSS 한 줄).
- 확인 시점: 앱이 열릴 때, 앱으로 돌아올 때(`visibilitychange`), 5분마다. `version.json`을 `cache: 'no-store'`로 받아 코드의 `APP_VERSION`과 비교한다. 받지 못하거나 오프라인이면 아무것도 띄우지 않는다.
- "나중에"는 이번 세션 동안 같은 버전을 다시 띄우지 않는다. "새로고침"은 서비스 워커 `update()`를 부른 뒤 `location.reload()`한다.
- 버전 값 만들기: 이 저장소는 빌드 단계가 없는 정적 사이트(GitHub Pages)라서 `.github/workflows/stamp-version.yml`이 main에 올라올 때마다 `version.json`과 `APP_VERSION`을 같은 커밋 SHA 12자로 바꿔 한 번 더 커밋한다. 병합 직후 몇십 초 동안은 `dev`로 같아서 띠가 뜨지 않는다.

## 004 홈 아이콘을 중앙 픽셀 아이콘으로

- `apple-touch-icon` → `https://personal-design-rho.vercel.app/icons/pixel/strum-180.png`(예전에 넣은 data 주소 링크를 대체)
- `manifest.webmanifest` icons → `strum-192.png`, `strum-512.png`(any, maskable)
- favicon(svg) → `.../strum.svg`. 64px PNG favicon 링크는 구형 브라우저용 대체로 그대로 둠.
- 저장소 안의 기존 아이콘 파일은 지우지 않았다. `tools/apple-icon-data-uri.py`는 이제 `apple-touch-icon` 링크를 data 주소로 덮어쓰므로, 중앙 주소를 쓰는 동안은 실행하지 않는다.
