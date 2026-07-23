# -*- coding: utf-8 -*-
# 시트 구조대로 내비게이션 재편: 9개 대메뉴 + 드롭다운 (데스크톱 hover / 모바일 details 아코디언)
import re

CS = './coming-soon.html'
MENU = [
    ('트래비티소개', None, [('트래비티', './about.html'), ('트래비티 글로벌', CS)]),
    ('체험단 마케팅', None, [('방문체험단', 'https://kr.trevity.com'), ('제품체험단', CS)]),
    ('한국제품 해외수출 마케팅', None, [
        ('베트남 인플루언서 틱톡 체험단', './vietnam-tiktok.html'),
        ('중국 인플루언서 샤오홍슈 체험단', CS),
        ('대만 인플루언서 인스타 체험단', CS),
        ('일본 인플루언서 인스타 체험단', CS),
        ('태국 인플루언서 틱톡 체험단', CS),
        ('미얀마 인플루언서 틱톡 체험단', CS)]),
    ('외국인 관광객 마케팅', None, [
        ('베트남인 관광객 유학생 체험단', CS),
        ('중국인 관광객 유학생 체험단', CS),
        ('대만인 관광객 유학생 체험단', CS),
        ('일본인 관광객 유학생 체험단', CS),
        ('태국인 관광객 유학생 체험단', CS),
        ('미얀마인 관광객 유학생 체험단', CS)]),
    ('해외 현지 마케팅', None, [
        ('베트남 현지 매장홍보 마케팅', CS),
        ('중국 현지 매장홍보 마케팅', CS),
        ('대만 현지 매장홍보 마케팅', CS),
        ('일본 현지 매장홍보 마케팅', CS),
        ('태국 현지 매장홍보 마케팅', CS),
        ('미얀마 현지 매장홍보 마케팅', CS)]),
    ('숙박 체험단', None, [
        ('내국인 관광객 호텔 체험단', CS),
        ('내국인 관광객 펜션 체험단', CS),
        ('외국인 관광객 숙박 체험단', CS)]),
    ('팸투어 마케팅', None, [
        ('내국인 관광객 서포터즈 운영대행', CS),
        ('외국인 관광객 서포터즈 운영대행', CS),
        ('외국인 메가 인플루언서 팸투어대행', CS),
        ('지자체 지역 홍보 대행', CS)]),
    ('블로그', './blog.html', []),
    ('고객센터', None, [('종합 헬프센터', CS), ('공식대행사', CS), ('제휴 문의', './inquiry.html')]),
]

STYLE = '''<style id="tvnav-style">
.tvh{position:fixed;top:0;left:0;width:100%;z-index:60;background:#fff;border-bottom:1px solid #eee}
.tvh-in{max-width:1400px;margin:0 auto;height:56px;display:flex;align-items:center;justify-content:space-between;padding:0 24px;gap:12px}
.tvh-logo img{height:34px;width:auto;display:block}
.tvh-nav{display:flex;align-items:center;flex:1;justify-content:center}
.tvh-nav>ul{list-style:none;display:flex;align-items:center;margin:0;padding:0}
.tvh-nav>ul>li{position:relative}
.tvh-nav>ul>li>a{display:block;padding:18px 11px;font-size:14px;font-weight:600;letter-spacing:-0.28px;color:#434343;text-decoration:none;white-space:nowrap}
.tvh-nav>ul>li>a:hover,.tvh-nav>ul>li.on>a{color:#fa6781}
.tvh-dd{display:none;position:absolute;top:100%;left:50%;transform:translateX(-50%);padding-top:0;z-index:61}
.tvh-nav>ul>li:hover .tvh-dd{display:block}
.tvh-dd-in{background:#fff;border:1px solid #f0f0f0;border-radius:14px;box-shadow:0 14px 40px rgba(0,0,0,0.12);padding:10px;min-width:236px}
.tvh-dd-in a{display:block;padding:10px 14px;border-radius:8px;font-size:14px;letter-spacing:-0.28px;color:#595959;text-decoration:none;white-space:nowrap}
.tvh-dd-in a:hover{background:#fff0f3;color:#fa6781}
.tvh-cta{display:inline-block;margin-left:10px;height:40px;line-height:40px;padding:0 20px;border-radius:8px;background:#fa6781;color:#fff;font-size:14px;font-weight:700;letter-spacing:-0.28px;text-decoration:none;white-space:nowrap}
.tvh-cta:hover{opacity:.85}
.tvh-mtg{display:none}
.tvh-burger{display:none;width:40px;height:40px;flex-direction:column;justify-content:center;gap:5px;cursor:pointer;padding:8px;box-sizing:border-box}
.tvh-burger span{display:block;height:2px;background:#1f1f1f;border-radius:2px}
@media (max-width:767px){
.tvh-in{height:48px;padding:0 16px}
.tvh-logo img{height:26px}
.tvh-burger{display:flex}
.tvh-nav{display:none;position:fixed;top:48px;left:0;width:100%;height:calc(100vh - 48px);background:#fff;overflow-y:auto;flex-direction:column;align-items:stretch;justify-content:flex-start;padding:8px 0 40px}
.tvh-mtg:checked~.tvh-nav{display:flex}
.tvh-nav>ul{flex-direction:column;align-items:stretch}
.tvh-nav>ul>li>a{padding:14px 24px;font-size:16px}
.tvh-dd{display:block;position:static;transform:none;padding:0}
.tvh-dd-in{border:none;box-shadow:none;border-radius:0;padding:0 0 8px;background:#fbfbfb}
.tvh-dd-in a{padding:11px 36px;font-size:14.5px}
.tvh-cta{order:2;margin-left:auto;height:32px;line-height:32px;padding:0 12px;font-size:13px}
.tvh-burger{order:3}
}
</style>'''


def build_header(active_top):
    lis = []
    for title, direct, subs in MENU:
        on = ' class="on"' if title == active_top else ''
        if direct and not subs:
            lis.append('<li%s><a href="%s">%s</a></li>' % (on, direct, title))
        else:
            dd = ''.join('<a href="%s"%s>%s</a>' % (h, ' target="_blank"' if h.startswith('http') else '', t) for t, h in subs)
            top_href = subs[0][1] if subs else '#'
            lis.append('<li%s><a href="%s">%s</a><div class="tvh-dd"><div class="tvh-dd-in">%s</div></div></li>' % (on, top_href, title, dd))
    return ('<header class="tvh"><div class="tvh-in">'
            '<a class="tvh-logo" href="./"><img src="./trevity-logo.png" alt="trevity"/></a>'
            '<input type="checkbox" id="tvh-mtg" class="tvh-mtg"/>'
            '<label for="tvh-mtg" class="tvh-burger" aria-label="메뉴"><span></span><span></span><span></span></label>'
            '<nav class="tvh-nav"><ul>' + ''.join(lis) + '</ul></nav>'
            '<a class="tvh-cta" href="./inquiry.html">문의하기</a>'
            '</div></header>')


def balanced(html, start, tag='div'):
    depth = 0
    for m in re.finditer(r'<%s\b|</%s>' % (tag, tag), html[start:]):
        depth += 1 if not m.group(0).startswith('</') else -1
        if depth == 0:
            return start + m.end()


FILES = {
    'index.html': '한국제품 해외수출 마케팅',
    'about.html': '트래비티소개',
    'blog.html': '블로그',
    'blog-market.html': '블로그',
    'blog-midtier.html': '블로그',
    'blog-diy.html': '블로그',
    'blog-hantown.html': '블로그',
    'inquiry.html': '고객센터',
}

for f, active in FILES.items():
    html = open(f, encoding='utf-8').read()
    # 스타일 주입(중복 방지)
    html = re.sub(r'<style id="tvnav-style">.*?</style>', '', html, flags=re.S)
    html = html.replace('</head>', STYLE + '</head>')
    # 기존 데스크톱 헤더 제거 → 새 헤더 삽입
    ds = html.find('<div class="max-[767px]:hidden"><div class="fixed top-0 z-40 h-[72px]')
    assert ds >= 0, f
    de = balanced(html, ds)
    html = html[:ds] + build_header(active) + html[de:]
    # 기존 모바일 헤더 블록 제거
    ms = html.find('<div><div class="min-[768px]:hidden">')
    if ms >= 0:
        me = balanced(html, ms)
        html = html[:ms] + html[me:]
    open(f, 'w', encoding='utf-8').write(html)
    print(f, 'nav swapped')

# 준비 중 페이지 생성 (index에서 head/footer 재사용)
idx = open('index.html', encoding='utf-8').read()
head = idx[:idx.find('</head>') + len('</head>')]
head = re.sub(r'<title>[^<]*</title>', '<title>준비 중 | 트래비티</title>', head)
fs = idx.find('<footer')
footer = idx[fs:balanced(idx, fs, 'footer')]
cs_page = (head
    + '<body class="max-[767px]:min-w-[360px] min-[767px]:min-w-[1440px]">'
    + build_header(None)
    + '<div style="min-height:64vh;display:flex;align-items:center;justify-content:center;padding:140px 20px 100px;background:linear-gradient(180deg,#fff6f8,#fff)">'
    '<div style="text-align:center">'
    '<div style="width:72px;height:72px;border-radius:50%;background:#fff0f3;display:flex;align-items:center;justify-content:center;margin:0 auto 24px">'
    '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#fa6781" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div>'
    '<h1 style="font-size:32px;font-weight:800;letter-spacing:-0.64px;color:#1f1f1f;margin:0 0 12px">페이지 준비 중입니다</h1>'
    '<p style="font-size:16.5px;line-height:1.75;letter-spacing:-0.33px;color:#595959;margin:0 0 32px">해당 서비스는 곧 오픈 예정입니다.<br>지금 바로 상담이 필요하시면 문의를 남겨주세요.</p>'
    '<div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap">'
    '<a href="./inquiry.html" style="display:inline-block;height:52px;line-height:52px;padding:0 30px;border-radius:10px;background:#fa6781;color:#fff;font-size:15.5px;font-weight:700;text-decoration:none">문의하기</a>'
    '<a href="./" style="display:inline-block;height:52px;line-height:49px;padding:0 30px;border-radius:10px;background:#fff;color:#434343;border:1.5px solid #e5e7eb;font-size:15.5px;font-weight:700;text-decoration:none">홈으로</a>'
    '</div></div></div>'
    + footer + '</body></html>')
open('coming-soon.html', 'w', encoding='utf-8').write(cs_page)
print('coming-soon.html written:', len(cs_page))
