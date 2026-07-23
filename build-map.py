# -*- coding: utf-8 -*-
# 도트 매트릭스 아시아 지도 SVG 생성 → about.html의 지도 카드 교체
import json, math

geo = json.load(open('world.geo.json', encoding='utf-8'))

# 아시아 범위 (경도 60~150, 위도 -12~55)
LON0, LON1, LAT0, LAT1 = 80.0, 150.0, -11.0, 52.0
W, H = 1000.0, 900.0
STEP = 0.92  # 도트 간격(도)

def proj(lon, lat):
    x = (lon - LON0) / (LON1 - LON0) * W
    y = (LAT1 - lat) / (LAT1 - LAT0) * H
    return x, y

def point_in_ring(lon, lat, ring):
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if ((yi > lat) != (yj > lat)) and (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside

def point_in_feature(lon, lat, geom):
    t = geom['type']
    polys = geom['coordinates'] if t == 'MultiPolygon' else [geom['coordinates']]
    for poly in polys:
        if point_in_ring(lon, lat, poly[0]):
            ok = True
            for hole in poly[1:]:
                if point_in_ring(lon, lat, hole):
                    ok = False
                    break
            if ok:
                return True
    return False

# 아시아 근방 피처만 프리필터(바운딩박스)
def fbox(geom):
    xs, ys = [], []
    polys = geom['coordinates'] if geom['type'] == 'MultiPolygon' else [geom['coordinates']]
    for poly in polys:
        for pt in poly[0]:
            xs.append(pt[0]); ys.append(pt[1])
    return min(xs), max(xs), min(ys), max(ys)

feats = []
for f in geo['features']:
    x0, x1, y0, y1 = fbox(f['geometry'])
    if x1 < LON0 - 2 or x0 > LON1 + 2 or y1 < LAT0 - 2 or y0 > LAT1 + 2:
        continue
    feats.append((f['properties'].get('name', ''), f['geometry'], (x0, x1, y0, y1)))
print('asia features:', len(feats))

HIGHLIGHT = {'South Korea', 'Vietnam'}
dots_gray, dots_pink = [], []
lat = LAT0
while lat <= LAT1:
    lon = LON0
    while lon <= LON1:
        hit = None
        for name, geom, (x0, x1, y0, y1) in feats:
            if lon < x0 or lon > x1 or lat < y0 or lat > y1:
                continue
            if point_in_feature(lon, lat, geom):
                hit = name
                break
        if hit is not None:
            x, y = proj(lon, lat)
            (dots_pink if hit in HIGHLIGHT else dots_gray).append((round(x, 1), round(y, 1)))
        lon += STEP
    lat += STEP
print('dots:', len(dots_gray), 'gray /', len(dots_pink), 'pink')

CITIES = {
    'SEOUL':     (126.98, 37.57),
    'DAEGU':     (128.60, 35.87),
    'HOCHIMINH': (106.70, 10.78),
    'CHINA':     (116.40, 39.90),
}
P = {k: proj(*v) for k, v in CITIES.items()}

def curve(a, b, bend=-60):
    (x1, y1), (x2, y2) = P[a], P[b]
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + bend
    return 'M%.0f,%.0f Q%.0f,%.0f %.0f,%.0f' % (x1, y1, mx, my, x2, y2)

svg = []
svg.append('<svg viewBox="0 0 1000 900" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block">')
svg.append('<style>'
  '.tvpulse{animation:tvpulse 2.2s ease-out infinite;transform-origin:center;transform-box:fill-box}'
  '@keyframes tvpulse{0%{opacity:.85;transform:scale(.4)}70%{opacity:0;transform:scale(2.6)}100%{opacity:0;transform:scale(2.6)}}'
  '.tvdash{stroke-dasharray:3 7;animation:tvdash 1.6s linear infinite}'
  '@keyframes tvdash{to{stroke-dashoffset:-10}}'
  '</style>')
svg.append('<g fill="#dfe3e8">' + ''.join('<circle cx="%s" cy="%s" r="2.1"/>' % d for d in dots_gray) + '</g>')
svg.append('<g fill="#f8b9c6">' + ''.join('<circle cx="%s" cy="%s" r="2.3"/>' % d for d in dots_pink) + '</g>')
# 연결선 (서울 허브)
for a, b, bend in [('SEOUL', 'CHINA', -28), ('SEOUL', 'HOCHIMINH', -95), ('SEOUL', 'DAEGU', 14)]:
    svg.append('<path d="%s" fill="none" stroke="#fa6781" stroke-width="2" class="tvdash" opacity="0.75"/>' % curve(a, b, bend))
# 핀 + 라벨
LABELS = {
    'SEOUL':     ('서울 · 디자인/촬영 스튜디오', 14, -14, 'end'),
    'DAEGU':     ('대구 · 마케팅 센터', 16, 26, 'start'),
    'HOCHIMINH': ('호치민 · 마케팅 센터', -14, 8, 'end'),
    'CHINA':     ('중국 · 개발 센터', -16, -12, 'end'),
}
for city, (x, y) in P.items():
    txt, dx, dy, anchor = LABELS[city]
    svg.append('<g>'
        '<circle cx="%.0f" cy="%.0f" r="9" fill="#fa6781" opacity="0.55" class="tvpulse"/>'
        '<circle cx="%.0f" cy="%.0f" r="5.5" fill="#fa6781" stroke="#fff" stroke-width="2"/>' % (x, y, x, y))
    tx, ty = x + dx, y + dy
    svg.append('<text x="%.0f" y="%.0f" text-anchor="%s" '
               'style="font-size:16px;font-weight:800;letter-spacing:0.4px;fill:#1f1f1f">%s</text>' % (tx, ty, anchor, city))
    svg.append('<text x="%.0f" y="%.0f" text-anchor="%s" '
               'style="font-size:12.5px;fill:#737373">%s</text></g>' % (tx, ty + 17, anchor, txt))
svg.append('</svg>')
svg_markup = ''.join(svg)
print('svg size:', len(svg_markup))

# about.html 지도 교체
html = open('about.html', encoding='utf-8').read()
import re
m = re.search(r'<div style="background:linear-gradient\(180deg,#fbfbfd,#fff\).*?</svg></div>', html, re.S)
assert m, 'map card not found'
card = ('<div style="background:linear-gradient(180deg,#fbfbfd,#fff);border:1px solid #f0f0f2;border-radius:24px;'
        'box-shadow:0 8px 40px rgba(0,0,0,0.07);padding:36px 40px 24px;overflow:hidden">' + svg_markup + '</div>')
html = html[:m.start()] + card + html[m.end():]
open('about.html', 'w', encoding='utf-8').write(html)
print('map replaced in about.html')
