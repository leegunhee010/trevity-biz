# -*- coding: utf-8 -*-
# 메인 홈 구축: 기존 index(상품 랜딩) → vietnam-tiktok.html 이동, 새 index.html = 그룹 메인
import re, shutil

def balanced(h, start, tag='div'):
    depth = 0
    for m in re.finditer(r'<%s\b|</%s>' % (tag, tag), h[start:]):
        depth += 1 if not m.group(0).startswith('</') else -1
        if depth == 0:
            return start + m.end()

# 1) 상품 랜딩 이동
shutil.copyfile('index.html', 'vietnam-tiktok.html')
print('vietnam-tiktok.html created')

# 2) 전 페이지 링크 업데이트: 베트남 틱톡 메뉴 → vietnam-tiktok.html, 패키지 앵커도 이동
FILES = ['vietnam-tiktok.html', 'about.html', 'blog.html', 'blog-market.html', 'blog-midtier.html',
         'blog-diy.html', 'blog-hantown.html', 'inquiry.html', 'coming-soon.html', 'build-nav.py']
for f in FILES:
    t = open(f, encoding='utf-8').read()
    t = t.replace('<a href="./">베트남 인플루언서 틱톡 체험단</a>', '<a href="./vietnam-tiktok.html">베트남 인플루언서 틱톡 체험단</a>')
    t = t.replace("('베트남 인플루언서 틱톡 체험단', './')", "('베트남 인플루언서 틱톡 체험단', './vietnam-tiktok.html')")
    if f != 'vietnam-tiktok.html':
        t = t.replace('href="./#packages"', 'href="./vietnam-tiktok.html#packages"')
    open(f, 'w', encoding='utf-8').write(t)
print('links updated')

# 3) 새 메인 조립 (상품 페이지에서 부품 추출)
src = open('vietnam-tiktok.html', encoding='utf-8').read()
head = src[:src.find('</head>') + len('</head>')]
head = re.sub(r'<title>[^<]*</title>', '<title>트래비티 | 아시아 체험단 마케팅 그룹</title>', head)
head = re.sub(r'(<meta name="description" content=")[^"]*(")',
              r'\1한국과 아시아 6개국을 잇는 체험단 마케팅 그룹 트래비티. 해외수출 인플루언서 체험단부터 외국인 관광객 마케팅, 숙박 체험단, 팸투어까지.\2', head)
hs = src.find('<header class="tvh">')
header = src[hs:balanced(src, hs, 'header')]
# 메인에선 활성 메뉴 없음
header = header.replace(' class="on"', '')
fs = src.find('<footer')
footer = src[fs:balanced(src, fs, 'footer')]

REV = 'opacity: 0; transform: translateY(40px); transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;'

STYLE = '''<style id="main-style">
html{scroll-behavior:smooth}
.mh-wrap{max-width:1180px;margin:0 auto;padding:0 20px}
.mh-label{display:inline-block;font-size:14px;font-weight:800;letter-spacing:2.5px;color:#fa6781;margin-bottom:16px}
.mh-h2{font-size:36px;font-weight:800;line-height:1.45;letter-spacing:-0.72px;color:#1f1f1f;margin:0}
.mh-sub{font-size:17.5px;line-height:1.75;letter-spacing:-0.35px;color:#595959}
.mh-btn{display:inline-block;height:56px;line-height:56px;padding:0 34px;border-radius:10px;background:#fa6781;color:#fff;font-size:16px;font-weight:700;letter-spacing:-0.32px;text-decoration:none;transition:opacity .15s}
.mh-btn:hover{opacity:.85}
.mh-btn.ghost{background:#fff;color:#434343;border:1.5px solid #e5e7eb;line-height:53px}
.mh-svc{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.mh-svc>a{display:flex;flex-direction:column;background:#fff;border:1px solid #f0f0f0;border-radius:20px;padding:34px 30px;text-decoration:none;transition:transform .25s,box-shadow .25s,border-color .25s}
.mh-svc>a:hover{transform:translateY(-4px);box-shadow:0 14px 36px rgba(0,0,0,0.10);border-color:#ffdae1}
.mh-svc .ico{width:48px;height:48px;border-radius:12px;background:#fff0f3;display:flex;align-items:center;justify-content:center;margin-bottom:18px;font-size:22px}
.mh-svc h3{font-size:19px;font-weight:800;letter-spacing:-0.38px;color:#1f1f1f;margin:0 0 10px;line-height:1.4}
.mh-svc p{font-size:14.5px;line-height:1.7;letter-spacing:-0.29px;color:#737373;margin:0 0 18px;flex:1}
.mh-svc .go{font-size:14.5px;font-weight:700;color:#fa6781}
.mh-hot{display:flex;gap:48px;align-items:center;flex-wrap:wrap;background:linear-gradient(135deg,#fff0f3,#fff6f8);border:1.5px solid #ffdae1;border-radius:24px;padding:52px 56px}
.mh-hot .t{flex:1 1 380px}
.mh-hot .v{flex:1 1 320px;max-width:420px}
.mh-hot .badge{display:inline-block;background:#fa6781;color:#fff;font-size:13px;font-weight:800;border-radius:999px;padding:6px 14px;margin-bottom:16px;letter-spacing:0.5px}
.mh-hot h3{font-size:30px;font-weight:800;line-height:1.45;letter-spacing:-0.6px;color:#1f1f1f;margin:0 0 14px}
.mh-hot p{font-size:16px;line-height:1.75;letter-spacing:-0.32px;color:#595959;margin:0 0 26px}
.mh-port{display:flex;gap:24px;flex-wrap:wrap;justify-content:center}
.mh-port>div{flex:1 1 300px;max-width:372px}
.mh-port .ph{border-radius:20px;overflow:hidden;box-shadow:0 6px 28px rgba(0,0,0,0.09);background:#fff}
.mh-port img{width:100%;display:block}
.mh-port b{display:block;margin-top:14px;font-size:16.5px;font-weight:700;letter-spacing:-0.33px;color:#1f1f1f;text-align:center}
.mh-blog{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.mh-blog>a{background:#fff;border:1px solid #f0f0f0;border-radius:16px;padding:24px 22px;text-decoration:none;transition:transform .2s,box-shadow .2s;display:flex;flex-direction:column}
.mh-blog>a:hover{transform:translateY(-3px);box-shadow:0 10px 28px rgba(0,0,0,0.08)}
.mh-blog .chip{font-size:12px;font-weight:700;color:#fa6781;margin-bottom:10px}
.mh-blog h4{font-size:15.5px;font-weight:700;line-height:1.5;letter-spacing:-0.31px;color:#1f1f1f;margin:0;flex:1}
.mh-blog time{margin-top:14px;font-size:12.5px;color:#9ca3af}
@media (max-width:1023px){.mh-svc{grid-template-columns:repeat(2,1fr)}.mh-blog{grid-template-columns:repeat(2,1fr)}}
@media (max-width:767px){.mh-h2{font-size:27px}.mh-svc{grid-template-columns:1fr}.mh-blog{grid-template-columns:1fr}.mh-hot{padding:32px 24px}}
</style>'''


def countup(target, label):
    suffix = ''.join(c for c in target if not c.isdigit() and c != ',')
    return ('<div style="text-align:center;min-width:150px">'
            '<p style="font-size:40px;font-weight:800;letter-spacing:-0.8px;color:#fa6781;line-height:1.2">'
            '<span class="inline-grid tabular-nums"><span class="invisible col-start-1 row-start-1" aria-hidden="true">%s</span>'
            '<span class="col-start-1 row-start-1 text-right">0%s</span></span></p>'
            '<p style="margin-top:8px;font-size:15px;letter-spacing:-0.3px;color:#595959">%s</p></div>') % (target, suffix, label)


B = []

# 히어로
B.append(
'<div style="background:linear-gradient(180deg,#ffe9ee 0%,#fff6f8 60%,#fff 100%);padding:120px 20px 90px;position:relative;overflow:hidden">'
'<div style="position:absolute;top:-140px;right:-90px;width:460px;height:460px;border-radius:50%;background:radial-gradient(circle,#fa678130,#fa678100 70%)"></div>'
'<div style="position:absolute;bottom:-180px;left:-110px;width:520px;height:520px;border-radius:50%;background:radial-gradient(circle,#ec489920,#ec489900 70%)"></div>'
'<div class="mh-wrap" style="position:relative;text-align:center">'
'<div style="' + REV + '">'
'<span class="mh-label">TREVITY MARKETING GROUP</span>'
'<h1 style="font-size:50px;font-weight:800;line-height:1.4;letter-spacing:-1px;color:#1f1f1f;margin:0">'
'한국과 아시아를 잇는<br><span style="color:#fa6781">체험단 마케팅</span>의 모든 것</h1>'
'<p class="mh-sub" style="margin:24px 0 38px">해외수출 인플루언서 체험단부터 외국인 관광객 유치, 현지 매장 홍보, 숙박 · 팸투어까지.<br>'
'아시아 6개국의 영향력을 브랜드와 매장의 손님으로 만듭니다.</p>'
'<div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-bottom:64px">'
'<a class="mh-btn" href="./inquiry.html">문의하기</a>'
'<a class="mh-btn ghost" href="#services">서비스 둘러보기</a></div>'
'<div style="display:flex;gap:24px;flex-wrap:wrap;justify-content:center">'
+ countup('10년+', '글로벌 마케팅 업력')
+ countup('6개국', '아시아 마케팅 커버리지')
+ countup('6,000+', '수행한 캠페인')
+ countup('100,000+', '인플루언서 풀')
+ '</div></div></div></div>')

# 서비스 그리드 (시트 구조 6개 사업)
svcs = [
    ('🇰🇷', '체험단 마케팅', '방문 체험단과 제품 체험단으로 국내 고객의 진짜 후기를 만듭니다.', 'https://kr.trevity.com', '체험단 플랫폼 바로가기 →'),
    ('🚀', '한국제품 해외수출 마케팅', '베트남 틱톡부터 중국 샤오홍슈, 일본 · 대만 인스타까지. 현지 인플루언서 체험단으로 수출 제품을 알립니다.', './vietnam-tiktok.html', '베트남 틱톡 체험단 보기 →'),
    ('🧳', '외국인 관광객 마케팅', '한국에 온 아시아 6개국 관광객 · 유학생 체험단으로 국내 매장을 알립니다.', './coming-soon.html', '자세히 보기 →'),
    ('🏪', '해외 현지 마케팅', '베트남 · 중국 · 일본 등 현지 매장의 홍보를 현지 마케터가 직접 진행합니다.', './coming-soon.html', '자세히 보기 →'),
    ('🏨', '숙박 체험단', '호텔 · 펜션 · 숙박업소를 내국인과 외국인 관광객 체험단으로 채웁니다.', './coming-soon.html', '자세히 보기 →'),
    ('🎌', '팸투어 마케팅', '서포터즈 운영대행부터 메가 인플루언서 팸투어, 지자체 지역 홍보까지 대행합니다.', './coming-soon.html', '자세히 보기 →'),
]
cards = ''.join(
    '<a href="%s"%s><div class="ico">%s</div><h3>%s</h3><p>%s</p><span class="go">%s</span></a>'
    % (h, ' target="_blank"' if h.startswith('http') else '', ico, t, d, go)
    for ico, t, d, h, go in svcs)
B.append(
'<section id="services" style="scroll-margin-top:70px"><div style="padding:110px 20px;background:#fff"><div class="mh-wrap">'
'<div style="text-align:center;margin-bottom:52px;' + REV + '">'
'<span class="mh-label">SERVICE</span>'
'<h2 class="mh-h2">여섯 개의 방법으로,<br>손님을 만들어 드립니다</h2></div>'
'<div class="mh-svc" style="' + REV + '">' + cards + '</div>'
'</div></div></section>')

# 대표 상품 하이라이트
B.append(
'<section><div style="padding:40px 20px 110px;background:#fff"><div class="mh-wrap">'
'<div class="mh-hot" style="' + REV + '">'
'<div class="t"><span class="badge">지금 가장 주목받는 서비스</span>'
'<h3>베트남 틱톡 인플루언서,<br>10만이든 50만이든 1명당 20만원</h3>'
'<p>팔로워 10만~50만의 검증된 현지 인플루언서를 10명부터 50명까지 균일가로 대량 부킹합니다. 섭외부터 검수까지 현지 마케터가 직접 진행합니다.</p>'
'<a class="mh-btn" href="./vietnam-tiktok.html">자세히 보기</a></div>'
'<div class="v"><img src="./images/about-tiktok.png" alt="베트남 틱톡 체험단" style="width:100%;border-radius:20px;box-shadow:0 10px 36px rgba(0,0,0,0.12);display:block"/></div>'
'</div></div></div></section>')

# 포트폴리오
B.append(
'<section><div style="padding:110px 20px;background:#fafafa"><div class="mh-wrap">'
'<div style="text-align:center;margin-bottom:52px;' + REV + '">'
'<span class="mh-label">PORTFOLIO</span>'
'<h2 class="mh-h2">트래비티가 만든 장면들</h2>'
'<p class="mh-sub" style="margin-top:16px">누적 조회 280만, 좋아요 100만. 현지에서 실제로 진행한 캠페인입니다.</p></div>'
'<div class="mh-port" style="' + REV + '">'
'<div><div class="ph"><img src="./images/portfolio-hantown.png" alt="HAN TOWN"/></div><b>HAN TOWN · 호치민 한식당</b></div>'
'<div><div class="ph"><img src="./images/portfolio-chivago.png" alt="CHIVAGO"/></div><b>CHIVAGO · 치킨 프랜차이즈</b></div>'
'<div><div class="ph"><img src="./images/portfolio-seya.png" alt="SEYA"/></div><b>SEYA STORE &amp; COOK · 한식 매장</b></div>'
'</div></div></div></section>')

# 블로그
B.append(
'<section><div style="padding:110px 20px;background:#fff"><div class="mh-wrap">'
'<div style="text-align:center;margin-bottom:52px;' + REV + '">'
'<span class="mh-label">BLOG</span>'
'<h2 class="mh-h2">진행 전에 읽어두면 좋은 이야기</h2></div>'
'<div class="mh-blog" style="' + REV + '">'
'<a href="./blog-market.html"><span class="chip">베트남 시장</span><h4>동남아 틱톡 사용률 2위, 베트남 시장이 특별한 이유</h4><time>2026.07.21</time></a>'
'<a href="./blog-midtier.html"><span class="chip">인플루언서 부킹</span><h4>팔로워 10만~50만, 왜 이 구간이 가장 효율적일까요?</h4><time>2026.07.19</time></a>'
'<a href="./blog-diy.html"><span class="chip">틱톡 마케팅</span><h4>직접 섭외해 보면 알게 되는 것들 — 9단계의 함정</h4><time>2026.07.16</time></a>'
'<a href="./blog-hantown.html"><span class="chip">캠페인 사례</span><h4>호치민 한식당 HAN TOWN, 리뷰 캠페인 기록</h4><time>2026.07.14</time></a>'
'</div>'
'<div style="text-align:center;margin-top:36px"><a href="./blog.html" style="font-size:15.5px;font-weight:700;color:#fa6781;text-decoration:none">블로그 전체 보기 →</a></div>'
'</div></div></section>')

# CTA
B.append(
'<section><div style="padding:100px 20px;background:linear-gradient(135deg,#fa6781,#ec4899);text-align:center">'
'<div style="' + REV + '">'
'<h2 style="font-size:36px;font-weight:800;line-height:1.5;letter-spacing:-0.72px;color:#fff;margin:0 0 12px">어디서부터 시작할지 모르겠다면</h2>'
'<p style="font-size:17.5px;line-height:1.7;letter-spacing:-0.35px;color:#ffe4e9;margin:0 0 34px">브랜드와 매장 상황을 남겨주시면, 가장 맞는 방법부터 제안해 드립니다.</p>'
'<a href="./inquiry.html" style="display:inline-block;height:58px;line-height:58px;padding:0 40px;border-radius:12px;background:#fff;color:#fa6781;font-size:17px;font-weight:800;letter-spacing:-0.34px;text-decoration:none">문의하기</a>'
'</div></div></section>')

page = (head + STYLE
        + '<body class="max-[767px]:min-w-[360px] min-[767px]:min-w-[1440px]">'
        + header + ''.join(B) + footer
        + '<script src="./mirror.js?v=2"></script></body></html>')
open('index.html', 'w', encoding='utf-8').write(page)
print('new main index.html written:', len(page))
