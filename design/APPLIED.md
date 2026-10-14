# 공통 디자인 적용 현황 (Strum)

- 공통 파일: design/shared (자동 동기화, 직접 고치지 않음). 정적 사이트(빌드 없음)라서 `index.html`이 `design/shared/tokens.css`, `design/shared/symbols.js`, `design/shared/icons/strum.svg`를 상대 경로로 바로 불러온다(import·복사 스크립트 없음). 중앙 주소는 쓰지 않는다.
- 적용한 CHANGELOG 번호: 002, 003, 004, 005, 006, 009, 011, 012, 013
- 예전 복사본(`design/tokens.css`, `design/icons/`, `design/DESIGN.md`)은 지웠다.

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

- `apple-touch-icon` → (006에서 data 주소로 되돌림, 아래 참고)
- `manifest.webmanifest` icons → `design/shared/icons/strum-192.png`, `strum-512.png`(any, maskable)
- favicon(svg) → `design/shared/icons/strum.svg`. 64px PNG favicon 링크는 구형 브라우저용 대체로 그대로 둠.
- 예전 아이콘 파일(`apple-touch-icon.png`, `icon-192/512.png`, `favicon.svg`)은 화면에서 쓰지 않아 지웠다. `favicon-64.png`는 head의 PNG favicon 링크가 쓰므로 남겼다.

## 005 기호 추가

- `<head>`에 `design/shared/symbols.js`(defer)를 추가했다. 기호는 `<pf-sym name="...">`, JS에서 만드는 곳은 `SYM(name)` 헬퍼를 쓴다.
- 바꾼 글자 기호: 목록 끝 `→` → arrow-right, 코드 찾기 행 `↗` → arrow-up-right, 백업 펼침 `→`(회전) → arrow-down(열리면 180도 회전), `+ 새 곡` → plus + 글자, `← 악보` → arrow-left + 글자.
- 글자 앞에 붙인 기호: 편집 edit, 보기 설정 settings, PLAY play / STOP stop(`setPlay`가 `innerHTML`로 갱신), 이 곡 삭제 close(문구 바뀔 때는 글자 노드만 갱신). 검색 입력창 앞 search.
- 기호는 글자색을 따르고 Ember는 쓰지 않았다. 기호 옆 간격은 `.pf-action`, `.fr-play`, `#del`에 `gap`을 줘서 맞췄다. 기호 스크립트를 못 받으면 글자만 남는다.
- 이 앱에 없는 항목(설정 새로고침, 공유, 링크 복사, 순서 변경, 모두 지우기, 탭바)은 해당 없음.
- 남겨 둔 텍스트 기호: 스텝퍼(조옮김, 글자 크기, 이미지 배율, 재생 속도)의 `−`/`+`(빼기 기호가 중앙에 없어 한 쌍을 그대로 둠), 코드 운지 그림 안의 `×`(뮤트 표시, 그림의 일부).

## 006 홈 아이콘 회색 글자 수정

- `apple-touch-icon`은 `design/shared/icons/apple-touch-icon.datauri.txt`의 data 주소를 `tools/inject-apple-icon.py`가 그대로 읽어 `<head>`에 넣는다(손으로 옮기지 않음). 넣기 전에 PNG 서명, 청크 CRC, 180x180을 검사하고 링크는 1개만 남긴다. GitHub Action(`stamp-version.yml`)이 main에 올라올 때마다 이 스크립트를 다시 돌려, 동기화로 아이콘이 바뀌어도 맞춰진다.
- favicon과 manifest icons는 중앙 주소 그대로 둔다.

## 009 제목 줄 배치

- 공통 `.pf-titleblock`(제목 왼쪽, 보조 라벨 오른쪽 아래)을 그대로 쓴다. 악보 목록(`#count` + "악보")과 악보 보기(`#vartist` + 곡 제목)는 이미 `.pf-titleblock > .pf-eyebrow + .pf-title` 구조라 마크업은 그대로다. 앱이 제목 줄 배치를 직접 준 스타일은 없었다.
- 악보 보기 제목 블록에만 앱 부제(`.fr-vsub`, 키·카포 등)가 하나 더 있어, 제목 줄 아래 한 줄로 가도록 `order:3; flex-basis:100%` 한 줄을 앱 CSS에 두었다.
- 새 곡·로그인 화면은 제목만 있어 변화 없음. 제목 아래 여백(`padding-bottom`)은 제목 줄 배치가 아니라 다음 내용과의 간격이라 그대로 뒀다.

## 011 워드마크 옆 작은 앱 아이콘

- 최상위 화면(로그인, 악보 목록)의 상단 바 왼쪽을 `<span class="pf-brand"><span class="pf-wordmark">Strum</span><img class="pf-brand-icon" src="design/shared/icons/strum.svg" alt="" width="20" height="20"></span>`로 바꿨다. 주소는 favicon과 같은 상대 경로. alt는 비움(옆에 글자로 앱 이름이 있음).
- 하위 화면(악보 보기, 편집)은 넣지 않았다. 크기와 간격은 공통 CSS(`.pf-brand`, `.pf-brand-icon`)에 맡겼고 앱 CSS는 건드리지 않았다.

## 012 워드마크 옆 앱 캐릭터

- 최상위 화면(로그인, 악보 목록)의 `.pf-brand` 안 `img.pf-brand-icon`(011)을 `<picture>`로 바꿨다: `prefers-reduced-motion: reduce`이면 `design/shared/characters/strum-still.png`, 아니면 `strum.gif`를 `img.pf-brand-character`(alt 비움, 24x24)로 보여 준다. 주소는 favicon과 같은 상대 경로. 하위 화면(악보 보기, 편집)과 다른 곳에는 넣지 않았다. 크기·간격은 공통 CSS에 맡겼다.
- 상단 흐림 점검: 해당 없음. `backdrop-filter`, `filter: blur`, 상단 가림막·그라데이션 요소가 없고, `.pf-header` 위를 덮는 고정 요소도 없다(고정 요소는 하단 재생 바, 설정 패널, 시트용 어두운 막, 새 버전 띠뿐). 반투명 값은 버튼 누름 상태 `:active`의 opacity(`index.html` 46·62·91·126·130·143·180줄)와 시트 뒤 어두운 막(`.scrim`, 156줄)뿐이다. 악보 보기에서 오른쪽으로 쓸어 돌아갈 때만 `#view`에 일시적으로 `opacity`/`transform`이 걸렸다 풀린다(1741~1753줄).

## 013 탭바 잘림 수정, 상단 캐릭터 새 디자인

- 상단 캐릭터: 최상위 화면(로그인, 악보 목록)의 `img.pf-brand-character`의 `width`/`height` 속성을 24x24에서 이 앱 값 68x28로 바꿨다(`strum.gif`는 272x112 = 4배). 크기는 공통 CSS가 정하며 앱 CSS에서 주지 않았다. `<picture>`의 still.png `source`는 그대로.
- 탭바: 이 앱에는 하단 탭바(`.pf-tabbar`)가 없어 해당 없음. 지운 탭바 스타일도 없다. 악보 보기 아래의 재생 바(`.fr-dock`)는 탭바가 아니라 이 앱 고유 요소라 그대로 두었고, 그 위에 뜨는 새 버전 띠의 `bottom`만 재생 바 높이(65px)에 맞춰 둔 기존 값을 유지했다.

## 하단 바 잘림 수정 (013 보완)

- 증상(캡처): iPhone 홈 화면 앱에서 재생 조작 바(`.fr-dock`)가 화면 아래로 약 59pt 밀려 아래쪽이 잘린다(바 윗선 812pt + 바 높이 약 98pt가 화면 852pt를 넘음). 59pt는 상태 표시줄 높이와 같다.
- 소스 점검: 013은 이미 적용되어 있고(이 앱에는 탭바가 없어 지울 탭바 스타일 없음), 화면 전체를 감싼 `100vh`/스크롤 상자 없음, 하단 바는 모두 `position: fixed`이며 `env(safe-area-inset-bottom)`을 쓴다. 안전 영역 34px을 가정한 390x844, 375x667 Chromium 화면에서는 바가 화면 맨 아래에 정확히 닿는다. 즉 CSS 계산 문제가 아니다.
- 원인(추정): 이 앱은 `apple-mobile-web-app-status-bar-style: default`(불투명 상태 표시줄)인데 viewport 메타에 `viewport-fit=cover`가 있어, 레이아웃 높이는 화면 전체(852pt)로 잡히고 실제 웹 화면은 상태 표시줄 아래에서 시작해 아래쪽 약 59pt가 화면 밖으로 나간다.
- 고친 방식: viewport 메타에서 `viewport-fit=cover`를 뺐다(`index.html` 6줄). 상태 표시줄은 그대로 불투명이고 헤더 위치는 같으며, 하단 바는 화면 안쪽(홈 표시줄 위)에 놓인다. 공통 CSS가 권하는 `viewport-fit=cover`(002)와 다르므로, 이 앱만의 예외다.
- 확인 필요: 실제 아이폰에서는 확인하지 못했다. 병합·배포 뒤 홈 화면 항목을 지우고 다시 추가해 바 전체가 보이는지 확인한다. 그래도 같으면 상태 표시줄 스타일을 `black-translucent`로 바꾸고 `viewport-fit=cover`를 되살리는 방식을 시험한다(상태 표시줄 글자가 흰색이 되는 점 주의).
