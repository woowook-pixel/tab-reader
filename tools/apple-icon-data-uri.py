#!/usr/bin/env python3
"""apple-touch-icon을 data 주소로 index.html의 <head>에 직접 넣는다.

iOS Safari가 파일 주소의 apple-touch-icon을 받아 오지 못하고 회색 글자 타일을 보여 주는 경우의 대응이다.
아이콘 그림(apple-touch-icon.png, 180x180)을 바꿨다면 이 스크립트를 다시 실행해 data 주소를 새로 만든다.

사용법 (저장소 루트에서):  python3 tools/apple-icon-data-uri.py [PNG 경로]
  1) PNG에서 IHDR/PLTE/tRNS/IDAT/IEND 외의 조각(메타데이터)을 지워 표준 PNG로 다시 저장
  2) index.html의 <link rel="apple-touch-icon" ...> 한 줄을 data 주소 링크로 교체
"""
import base64, re, struct, sys

png_path = sys.argv[1] if len(sys.argv) > 1 else 'apple-touch-icon.png'
html_path = 'index.html'
KEEP = {b'IHDR', b'PLTE', b'tRNS', b'IDAT', b'IEND'}

data = open(png_path, 'rb').read()
assert data[:8] == b'\x89PNG\r\n\x1a\n', 'PNG 파일이 아닙니다'
out, i, dropped = [data[:8]], 8, []
while i < len(data):
    n = struct.unpack('>I', data[i:i + 4])[0]
    kind = data[i + 4:i + 8]
    chunk = data[i:i + 12 + n]
    (out.append(chunk) if kind in KEEP else dropped.append(kind.decode('latin1')))
    i += 12 + n
clean = b''.join(out)
w, h = struct.unpack('>II', clean[16:24])
assert (w, h) == (180, 180), f'180x180이어야 합니다 (현재 {w}x{h})'
open(png_path, 'wb').write(clean)

uri = 'data:image/png;base64,' + base64.b64encode(clean).decode()
link = f'<link rel="apple-touch-icon" sizes="180x180" href="{uri}">'
html = open(html_path, encoding='utf-8').read()
html, count = re.subn(r'<link rel="apple-touch-icon"[^>]*>', lambda m: link, html, count=1)
assert count == 1, 'index.html에서 apple-touch-icon 링크를 찾지 못했습니다'
open(html_path, 'w', encoding='utf-8').write(html)
print(f'{png_path}: {len(data)}B -> {len(clean)}B, 지운 조각: {dropped or "없음"}, data 주소 {len(uri)}자')
