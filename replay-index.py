# -*- coding: utf-8 -*-
# index.html 전체 재구축: rendered.html(원본 스냅샷) → 모든 변환 리플레이 → 새 nav
import re

html = open('rendered.html', encoding='utf-8').read()

def balanced(h, start, tag='div'):
    depth = 0
    for m in re.finditer(r'<%s\b|</%s>' % (tag, tag), h[start:]):
        depth += 1 if not m.group(0).startswith('</') else -1
        if depth == 0:
            return start + m.end()

# ── A. 미러 기본 처리 ──
html = re.sub(r'<script\b[^>]*>.*?</script>', '', html, flags=re.S)
html = re.sub(r'<script\b[^>]*/>', '', html)
html = html.replace('https://www.biz.creplanet.co.kr/', './').replace('https://biz.creplanet.co.kr/', './')
html = html.replace('https://static-creplanet.s3.ap-northeast-2.amazonaws.com/assets/biz/', './')
html = re.sub(r'(src|href|poster)="/(?!/)', r'\1="./', html)
for q in ["url('/", 'url("/', 'url(/']:
    html = html.replace(q + 'images', q.replace('/', './') if False else q[:-1] + './images')
html = html.replace("url('./images".replace('./', '/'), "url('./images")  # no-op 안전
html = re.sub(r'<link[^>]*(?:as="script"|\.js"[^>]*)/?>', '', html)
# body 스크롤락 제거
html = html.replace('<body class="max-[767px]:min-w-[360px] min-[767px]:min-w-[1440px]" style="position: fixed; top: 0px; overflow-y: auto; width: 100%;">',
                    '<body class="max-[767px]:min-w-[360px] min-[767px]:min-w-[1440px]">')
# 모달 오버레이 제거
i = html.find('class="fixed top-0 left-0 isolate z-[1000] size-full contain-layout bg-black/40 center"')
if i >= 0:
    s = html.rfind('<div', 0, i)
    html = html[:s] + html[balanced(html, s):]
print('A done. overlay removed:', i >= 0)

# ── B. 컬러: 크리플래닛 레드 → 트래비티 핑크 ──
HEX = {'fc4243': 'fa6781', 'ff4d4f': 'fb7288', 'ff706b': 'fa98a9', 'ff9b94': 'fcb3c0',
       'ffc3bd': 'ffdae1', 'ffe9e6': 'ffe4e9', 'fff2f0': 'fff0f3', 'fff6f5': 'fff5f7',
       'fff1f0': 'ffeff2', 'ffa39e': 'fcaebc', 'ff8787': 'fb92a5', 'ff0b7d': 'ec4899',
       'ffccc7': 'ffd6de', 'd9363e': 'c8354f', 'cf1322': 'b52f47', 'a8071a': 'a72b41'}
for o, n in HEX.items():
    html = re.sub('#' + o, '#' + n, html, flags=re.I)
for pat, rep in [
    (r'rgb\(\s*252,\s*66,\s*67\s*\)', 'rgb(250, 103, 129)'),
    (r'rgba\(\s*252,\s*66,\s*67', 'rgba(250, 103, 129'),
    (r'rgba\(\s*255,\s*112,\s*107', 'rgba(250, 152, 169'),
    (r'rgba\(\s*255,\s*38,\s*5', 'rgba(250, 103, 129'),
    (r'rgba\(\s*255,\s*77,\s*79', 'rgba(251, 114, 136')]:
    html = re.sub(pat, rep, html)
print('B done')

# ── C. 스킨 스타일 ──
skin = ('<style id="trevity-skin">\nhtml{scroll-behavior:smooth}\n'
        'img[src*="request-form"],img[src*="recommendation-list"],img[src*="price-search-mockup"],'
        'img[src*="influence-analysis-mockup"],img[src*="card-1-collage"],img[src*="card-2-collage"],'
        'img[src*="card-3-collage"],img[src*="point-1"],img[src*="point-2"],img[src*="example1"],'
        'img[src*="example2"],img[src*="example3"],img[src*="mascot"]'
        '{filter:hue-rotate(-12deg) saturate(.92) brightness(1.02)}\n</style>')
html = html.replace('</head>', skin + '</head>')

# ── D. 구헤더/배너 제거 + 패딩 ──
m = re.search(r'<div class="fixed top-0 z-40 flex h-\[72px\][^"]*"', html)
if m:
    html = html[:m.start()] + html[balanced(html, m.start()):]
html = re.sub(r'<a target="_blank" class="relative block" href="\./blog/2026-influencer-marketing-trend-report"></a>', '', html)
# 로고줄+데스크톱 헤더 래퍼 통삭제
i = html.find('<div class="max-[767px]:hidden"><div><div class="fixed left-0 top-[72px]')
if i >= 0:
    html = html[:i] + html[balanced(html, i):]
# 모바일 헤더(안쪽 div만!) 삭제
i = html.find('<div class="min-[768px]:hidden">')
if i >= 0:
    html = html[:i] + html[balanced(html, i):]
html = html.replace('class="max-[767px]:pt-[120px] min-[768px]:pt-[184px]"',
                    'class="max-[767px]:pt-[48px] min-[768px]:pt-[72px]"')
print('D done. sections:', html.count('<section'))
open('index.html', 'w', encoding='utf-8').write(html)

# ── E1. rebrand.py 실행 ──
import subprocess, sys
r = subprocess.run([sys.executable, 'rebrand.py'], capture_output=True)
print('rebrand:', r.returncode)
html = open('index.html', encoding='utf-8').read()

# ── E2. 리브랜드 후속 fix ──
for o, n in [
    ("캠페인 이후에는 <span", "직접 섭외보다 <span"),
    ("우리 브랜드에 팔로워 10만~50만 KOL을 빠르게 찾고 싶다면?", "베트남 TikTok KOL을 대량으로 부킹하고 싶다면?"),
    ("브랜드에 팔로워 10만~50만 KOL을 빠르게 찾고 싶다면?", "베트남 TikTok KOL을 대량으로 부킹하고 싶다면?"),
    # 히어로 v2
    ("팔로워 10만~50만 KOL을 제일 저렴하게 부킹하세요", "10만~50만 팔로워 KOL, 무조건 1명당 20만원"),
    ("제일 저렴하게 부킹하세요", "무조건 1명당 20만원"),
    ("팔로워 10만이든 50만이든, 1명당 20만원 균일가.", "직접 섭외보다 싸게, 베트남에서 제일 저렴하게 부킹하세요."),
    ("팔로워 10만~50만 KOL을", "10만~50만 팔로워 KOL,"),
]:
    html = html.replace(o, n)

# ── E3. 분석 시스템 섹션 삭제 ──
i = html.find('단가는 얼마인지,')
if i > 0:
    s = html.rfind('<section', 0, i)
    html = html[:s] + html[balanced(html, s, 'section'):]
print('E3 done. sections:', html.count('<section'))
open('index.html', 'w', encoding='utf-8').write(html)

# ── E4. copy-v2.py 실행 ──
r = subprocess.run([sys.executable, 'copy-v2.py'], capture_output=True)
print('copy-v2:', r.returncode)
html = open('index.html', encoding='utf-8').read()

# ── E5. copy-v2 후속 fix ──
for o, n in [
    ("가능합니다. TikTok Affiliate 연결, 틱톡샵 연계 판매 설계까지 캠페인 목적에 맞게 함께 트래비티의 균일가보다 비쌉니다.",
     "가능합니다. 틱톡샵 제휴(어필리에이트) 연결부터 판매 설계까지 캠페인 목적에 맞게 함께 준비해 드립니다."),
    ("현지 뷰티 KOL", "현지 뷰티 인플루언서"),
    (">TikTok<", ">틱톡<"),
    ("너무</span> 부킹하세요</span>", "너무</span> 아깝지 않으세요?</span>"),
]:
    html = html.replace(o, n)

# ── E6. POINT 섹션 → 스탯 앞으로 ──
def extract_section(h, marker):
    i = h.find(marker)
    s = h.rfind('<section', 0, i)
    return s, balanced(h, s, 'section')
ps, pe = extract_section(html, '트래비티가 필요한 이유')
point = html[ps:pe]
html = html[:ps] + html[pe:]
ss, _ = extract_section(html, '말이 아닌 숫자로')
html = html[:ss] + point + html[ss:]

# ── E7. 히어로 v3 ──
for o, n in [
    ("베트남 틱톡 인플루언서 부킹,<br>팔로워 10만~50만 누구든<br>1명당 20만원",
     "팔로워가 10만이어도,<br>50만이어도 가격은 하나.<br>1명당 20만원"),
    ("베트남 틱톡 인플루언서 부킹,<br>팔로워 10만~50만 누구든 1명당 20만원",
     "팔로워가 10만이어도, 50만이어도<br>가격은 하나. 1명당 20만원"),
    ("베트남에서 가장 합리적인 가격으로 대량 부킹해 드립니다.",
     "베트남 틱톡 대량 부킹, 트래비티라서 가능한 가격입니다."),
]:
    html = html.replace(o, n)

# ── E8. 비교 섹션 삽입 ──
def row(mark, color, text, last=False):
    bb = '' if last else 'border-bottom:1px solid rgba(0,0,0,0.06);'
    return ('<div style="display:flex;gap:12px;align-items:flex-start;padding:14px 0;%s">'
            '<span style="flex:none;width:22px;height:22px;border-radius:50%%;background:%s;color:#fff;font-size:13px;font-weight:700;display:flex;align-items:center;justify-content:center;margin-top:1px">%s</span>'
            '<p style="font-size:16px;line-height:1.6;letter-spacing:-0.32px;color:#434343">%s</p></div>') % (bb, color, mark, text)
L = ["한 명 한 명 직접 연락 — 답장은 절반도 오지 않습니다", "단가 협상 — 외국 브랜드에는 부르는 게 값입니다",
     "가이드 전달 — 언어도, 정서도 다릅니다", "일정 관리 — 업로드가 밀려도 책임질 사람이 없습니다",
     "시간은 시간대로, 비용은 비용대로 듭니다"]
R = ["10만+ 풀에서 제품에 맞는 인플루언서만 추천", "협상 없이, 누구든 1명당 20만원 균일가",
     "현지 마케터가 가이드 전달부터 검수까지 직접", "업로드 일정 관리와 이슈 대응까지 전담",
     "의뢰서 한 장으로 최대 50명까지 부킹 완료"]
lrows = ''.join(row('✕', '#bfbfbf', t, i == 4) for i, t in enumerate(L))
rrows = ''.join(row('✓', '#fa6781', t, i == 4) for i, t in enumerate(R))
REV = 'opacity: 0; transform: translateY(40px); transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;'
compare = (
'<section><div style="padding:24px 20px 56px;background:#fff">'
'<div style="max-width:1084px;margin:0 auto"><div style="' + REV + '">'
'<div style="text-align:center;margin-bottom:56px">'
'<p style="color:#fa6781;font-size:18px;font-weight:700;letter-spacing:-0.36px;margin-bottom:12px">직접 해보시면 압니다</p>'
'<h2 style="font-size:36px;font-weight:700;line-height:1.5;letter-spacing:-0.72px;color:#1f1f1f">직접 섭외 vs 트래비티,<br>같은 50명을 부킹한다면</h2></div>'
'<div style="display:flex;gap:24px;flex-wrap:wrap;justify-content:center">'
'<div style="flex:1 1 320px;max-width:530px;background:#f7f7f7;border-radius:16px;padding:40px 32px">'
'<p style="font-size:20px;font-weight:700;letter-spacing:-0.4px;color:#8c8c8c;margin-bottom:20px">직접 섭외하면</p>' + lrows + '</div>'
'<div style="flex:1 1 320px;max-width:530px;background:#fff0f3;border-radius:16px;padding:40px 32px;border:1.5px solid #fa6781;position:relative">'
'<p style="font-size:20px;font-weight:700;letter-spacing:-0.4px;color:#fa6781;margin-bottom:20px">트래비티에 맡기면</p>' + rrows + '</div></div>'
'<p style="text-align:center;margin-top:48px;font-size:22px;font-weight:700;letter-spacing:-0.44px;line-height:1.5;color:#1f1f1f">그 수고를 전부 더해도,<br class="mn:hidden"> <span style="color:#fa6781">1명당 20만원 균일가</span>보다 비쌉니다.</p>'
'</div></div></div></section>')
i = html.find('말이 아닌 숫자로')
ss = html.rfind('<section', 0, i)
html = html[:ss] + compare + html[ss:]

# ── E9. 패키지: 앵커 + 가격 강조 + 배지 ──
j = html.find('어떤 규모로 시작해 볼까요?')
ps = html.rfind('<section', 0, j)
pe = balanced(html, ps, 'section')
pkg = html[ps:pe]
pkg = pkg.replace('<section', '<section id="packages" style="scroll-margin-top:90px"', 1)
for price in ['200만원', '400만원', '1,000만원']:
    pkg = pkg.replace('= ' + price, '= <span style="color:#fa6781;font-weight:800">' + price + '</span>')
badge = '<span style="margin-left:8px;border-radius:999px;background:#fa6781;color:#fff;font-size:12px;font-weight:600;padding:3px 10px;line-height:1.4;white-space:nowrap">가장 많이 선택</span>'
pkg = pkg.replace('그로스 · 20명</span></div>', '그로스 · 20명</span>' + badge + '</div>', 1)
html = html[:ps] + pkg + html[pe:]

# ── E10. 링크/푸터 ──
html = html.replace('href="./blog"', 'href="./blog.html"')
html = html.replace('href="./inquiry"', 'href="./inquiry.html"')
m = re.search(r'<a target="_blank" href="https://clacorp\.career\.greetinghr\.com/ko/intro">(<span[^>]*>)팀 소개(</span>)</a>', html)
if m:
    html = html[:m.start()] + '<a href="./about.html">' + m.group(1) + '회사소개' + m.group(2) + '</a>' + html[m.end():]

# ── F. 새 nav + mirror.js ──
import importlib.util
spec = importlib.util.spec_from_file_location('bn', 'build-nav.py')
# build-nav.py는 실행 시 파일들을 수정하므로 import 대신 헤더 생성부만 재현
CS = './coming-soon.html'
MENU = [
    ('트래비티소개', None, [('트래비티', './about.html'), ('트래비티 글로벌', CS)]),
    ('체험단 마케팅', None, [('방문체험단', 'https://kr.trevity.com'), ('제품체험단', CS)]),
    ('한국제품 해외수출 마케팅', None, [
        ('베트남 인플루언서 틱톡 체험단', './'), ('중국 인플루언서 샤오홍슈 체험단', CS),
        ('대만 인플루언서 인스타 체험단', CS), ('일본 인플루언서 인스타 체험단', CS),
        ('태국 인플루언서 틱톡 체험단', CS), ('미얀마 인플루언서 틱톡 체험단', CS)]),
    ('외국인 관광객 마케팅', None, [
        ('베트남인 관광객 유학생 체험단', CS), ('중국인 관광객 유학생 체험단', CS),
        ('대만인 관광객 유학생 체험단', CS), ('일본인 관광객 유학생 체험단', CS),
        ('태국인 관광객 유학생 체험단', CS), ('미얀마인 관광객 유학생 체험단', CS)]),
    ('해외 현지 마케팅', None, [
        ('베트남 현지 매장홍보 마케팅', CS), ('중국 현지 매장홍보 마케팅', CS),
        ('대만 현지 매장홍보 마케팅', CS), ('일본 현지 매장홍보 마케팅', CS),
        ('태국 현지 매장홍보 마케팅', CS), ('미얀마 현지 매장홍보 마케팅', CS)]),
    ('숙박 체험단', None, [
        ('내국인 관광객 호텔 체험단', CS), ('내국인 관광객 펜션 체험단', CS), ('외국인 관광객 숙박 체험단', CS)]),
    ('팸투어 마케팅', None, [
        ('내국인 관광객 서포터즈 운영대행', CS), ('외국인 관광객 서포터즈 운영대행', CS),
        ('외국인 메가 인플루언서 팸투어대행', CS), ('지자체 지역 홍보 대행', CS)]),
    ('블로그', './blog.html', []),
    ('고객센터', None, [('종합 헬프센터', CS), ('공식대행사', CS), ('제휴 문의', './inquiry.html')]),
]
src = open('build-nav.py', encoding='utf-8').read()
STYLE = re.search(r"STYLE = '''(.*?)'''", src, re.S).group(1)

def build_header(active_top):
    lis = []
    for title, direct, subs in MENU:
        on = ' class="on"' if title == active_top else ''
        if direct and not subs:
            lis.append('<li%s><a href="%s">%s</a></li>' % (on, direct, title))
        else:
            dd = ''.join('<a href="%s"%s>%s</a>' % (h, ' target="_blank"' if h.startswith('http') else '', t) for t, h in subs)
            lis.append('<li%s><a href="%s">%s</a><div class="tvh-dd"><div class="tvh-dd-in">%s</div></div></li>' % (on, subs[0][1], title, dd))
    return ('<header class="tvh"><div class="tvh-in">'
            '<a class="tvh-logo" href="./"><img src="./trevity-logo.png" alt="trevity"/></a>'
            '<input type="checkbox" id="tvh-mtg" class="tvh-mtg"/>'
            '<label for="tvh-mtg" class="tvh-burger" aria-label="메뉴"><span></span><span></span><span></span></label>'
            '<nav class="tvh-nav"><ul>' + ''.join(lis) + '</ul>'
            '<a class="tvh-cta" href="./inquiry.html">문의하기</a></nav>'
            '</div></header>')

html = html.replace('</head>', STYLE + '</head>')
bodytag = re.search(r'<body[^>]*>', html)
html = html[:bodytag.end()] + build_header('한국제품 해외수출 마케팅') + html[bodytag.end():]
if 'mirror.js' not in html:
    html = html.replace('</body>', '<script src="./mirror.js?v=2"></script></body>')
open('index.html', 'w', encoding='utf-8').write(html)
print('F done. final size:', len(html))

# ── 검증 배터리 ──
checks = {
    'sections(11)': html.count('<section'),
    '크리플래닛': html.count('크리플래닛'),
    'KOL잔여': html.count('KOL'),
    'TikTok잔여': html.count('TikTok'),
    'VAT잔여': html.count('VAT'),
    '히어로v3': html.count('팔로워가 10만이어도'),
    '비교섹션': html.count('직접 섭외 vs 트래비티'),
    '배지': html.count('가장 많이 선택'),
    'packages앵커': html.count('id="packages"'),
    '스타터카드': html.count('스타터 · 10명'),
    '새nav': html.count('class="tvh"'),
    'mirror': html.count('mirror.js?v=2'),
    'footer': html.count('<footer'),
    '영상': html.count('<video'),
}
for k, v in checks.items():
    print(k, '=', v)
