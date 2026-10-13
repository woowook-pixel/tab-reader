#!/usr/bin/env python3
"""design/shared/icons/apple-touch-icon.datauri.txt의 data 주소를 index.html <head>의 apple-touch-icon 링크에 그대로 넣는다.

사용법 (저장소 루트에서):  python3 tools/inject-apple-icon.py
- 넣기 전에 PNG 서명, 모든 청크 CRC, 180x180을 검사한다. 하나라도 틀리면 index.html을 건드리지 않고 실패한다.
- head에 apple-touch-icon 링크는 1개만 남긴다. data 주소를 손으로 옮겨 적지 않는다.
- design/shared/는 자동 동기화로 덮어써지므로 고치지 않는다. 동기화 뒤에는 .github/workflows/stamp-version.yml이 이 스크립트를 다시 돌린다.
"""
import base64, re, struct, sys, zlib

SRC = 'design/shared/icons/apple-touch-icon.datauri.txt'
HTML = 'index.html'
PREFIX = 'data:image/png;base64,'

uri = open(SRC, encoding='utf-8').read().strip()
if not uri.startswith(PREFIX):
    sys.exit('datauri.txt가 data:image/png;base64, 로 시작하지 않습니다')
data = base64.b64decode(uri[len(PREFIX):], validate=True)
if data[:8] != b'\x89PNG\r\n\x1a\n':
    sys.exit('PNG 서명이 맞지 않습니다')
i, w, h, n = 8, 0, 0, 0
while i < len(data):
    ln, typ = struct.unpack('>I4s', data[i:i + 8])
    body = data[i + 8:i + 8 + ln]
    crc = struct.unpack('>I', data[i + 8 + ln:i + 12 + ln])[0]
    if zlib.crc32(typ + body) & 0xffffffff != crc:
        sys.exit('CRC 오류: ' + typ.decode())
    if typ == b'IHDR':
        w, h = struct.unpack('>II', body[:8])
    n += 1
    i += 12 + ln
if (w, h) != (180, 180):
    sys.exit('180x180이 아닙니다: %dx%d' % (w, h))

html = open(HTML, encoding='utf-8').read()
link = '<link rel="apple-touch-icon" sizes="180x180" href="%s">' % uri
html, k = re.subn(r'<link rel="apple-touch-icon"[^>]*>', lambda m: link, html)
if k != 1:
    sys.exit('index.html에 apple-touch-icon 링크가 %d개 있습니다(1개여야 함)' % k)
open(HTML, 'w', encoding='utf-8').write(html)
print('OK: apple-touch-icon 1개, 180x180, 청크 %d개 CRC 일치, %d자' % (n, len(uri)))
