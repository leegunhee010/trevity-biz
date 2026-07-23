# -*- coding: utf-8 -*-
# 회사소개 v2 — featuring.co/whyfeaturing 구조 참고(비전 히어로/자기정의/이유 지그재그/신뢰 그리드/서비스 분기)
import re

cur = open('about.html', encoding='utf-8').read()

def balanced(html, start, tag='div'):
    depth = 0
    for m in re.finditer(r'<%s\b|</%s>' % (tag, tag), html[start:]):
        depth += 1 if not m.group(0).startswith('</') else -1
        if depth == 0:
            return start + m.end()

head_end = cur.find('</head>') + len('</head>')
head = cur[:head_end]
ds = cur.find('<div class="max-[767px]:hidden"><div class="fixed top-0 z-40 h-[72px]')
hdr = cur[ds:balanced(cur, ds)]
ms = cur.find('<div class="min-[768px]:hidden">')
mhdr = '<div>' + cur[ms:balanced(cur, ms)] + '</div>'
fs = cur.find('<footer')
footer = cur[fs:balanced(cur, fs, 'footer')]
msvg = re.search(r'<svg viewBox="0 0 1000 900".*?</svg>', cur, re.S)
MAP_SVG = msvg.group(0)

REV = 'opacity: 0; transform: translateY(40px); transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;'
PINK = '#fa6781'

STYLE = '''<style id="about2-style">
html{scroll-behavior:smooth}
.ab-label{display:inline-block;font-size:14px;font-weight:800;letter-spacing:2.5px;color:#fa6781;margin-bottom:18px}
.ab-h{font-size:44px;font-weight:800;line-height:1.42;letter-spacing:-0.88px;color:#1f1f1f;margin:0}
.ab-h2{font-size:36px;font-weight:800;line-height:1.45;letter-spacing:-0.72px;color:#1f1f1f;margin:0}
.ab-sub{font-size:18px;line-height:1.8;letter-spacing:-0.36px;color:#595959}
.ab-wrap{max-width:1084px;margin:0 auto;padding:0 20px}
.ab-btn{display:inline-block;height:56px;line-height:56px;padding:0 34px;border-radius:10px;background:#fa6781;color:#fff;font-size:16px;font-weight:700;letter-spacing:-0.32px;text-decoration:none;transition:opacity .15s}
.ab-btn:hover{opacity:.85}
.ab-btn.ghost{background:#fff;color:#434343;border:1.5px solid #e5e7eb;line-height:53px}
.ab-zig{display:flex;gap:64px;align-items:center;flex-wrap:wrap}
.ab-zig>.t{flex:1 1 380px;min-width:320px}
.ab-zig>.v{flex:1 1 420px;min-width:320px}
.ab-zlabel{display:inline-block;font-size:15px;font-weight:800;letter-spacing:-0.3px;color:#fa6781;background:#fff0f3;border-radius:999px;padding:7px 16px;margin-bottom:20px}
.ab-zig h3{font-size:32px;font-weight:800;line-height:1.45;letter-spacing:-0.64px;color:#1f1f1f;margin:0 0 18px}
.ab-zig p{font-size:16.5px;line-height:1.85;letter-spacing:-0.33px;color:#595959;margin:0}
.ab-trust{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.ab-trust>div{background:#fff;border:1px solid #f0f0f0;border-radius:16px;padding:30px 26px}
.ab-trust h4{font-size:17.5px;font-weight:700;letter-spacing:-0.35px;color:#1f1f1f;margin:0 0 10px}
.ab-trust p{font-size:14.5px;line-height:1.7;letter-spacing:-0.29px;color:#737373;margin:0}
.ab-svc{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.ab-svc>a{display:flex;flex-direction:column;background:#fff;border:1px solid #f0f0f0;border-radius:20px;padding:36px 30px;text-decoration:none;transition:transform .25s,box-shadow .25s}
.ab-svc>a:hover{transform:translateY(-4px);box-shadow:0 14px 36px rgba(0,0,0,0.10)}
.ab-svc .tag{font-size:13px;font-weight:800;letter-spacing:1.5px;color:#fa6781;margin-bottom:14px}
.ab-svc h4{font-size:20px;font-weight:800;letter-spacing:-0.4px;color:#1f1f1f;margin:0 0 12px;line-height:1.4}
.ab-svc p{font-size:15px;line-height:1.7;letter-spacing:-0.3px;color:#595959;margin:0 0 22px;flex:1}
.ab-svc .go{font-size:15px;font-weight:700;color:#fa6781}
.ab-port{display:flex;gap:24px;flex-wrap:wrap;justify-content:center}
.ab-port>div{flex:1 1 300px;max-width:348px}
.ab-port .ph{border-radius:20px;overflow:hidden;box-shadow:0 6px 28px rgba(0,0,0,0.09);background:#fff}
.ab-port img{width:100%;display:block}
.ab-port b{display:block;margin-top:16px;font-size:17px;font-weight:700;letter-spacing:-0.34px;color:#1f1f1f;text-align:center}
.ab-port span{display:block;margin-top:4px;font-size:14px;letter-spacing:-0.28px;color:#737373;text-align:center}
.ab-price{background:#fff;border:1.5px solid #ffdae1;border-radius:20px;box-shadow:0 8px 40px rgba(250,103,129,0.10);padding:36px 34px}
.ab-price .row{display:flex;justify-content:space-between;align-items:center;padding:16px 4px;border-bottom:1px solid #f5f5f5}
.ab-price .row:last-child{border-bottom:none}
.ab-price .nm{font-size:16px;font-weight:700;color:#434343;letter-spacing:-0.32px}
.ab-price .pr{font-size:19px;font-weight:800;color:#fa6781;letter-spacing:-0.38px}
.ab-price .cap{margin-top:14px;font-size:13px;color:#8c8c8c;text-align:right}
@media (max-width:1023px){.ab-trust{grid-template-columns:repeat(2,1fr)}.ab-svc{grid-template-columns:1fr}}
@media (max-width:767px){.ab-h{font-size:31px}.ab-h2{font-size:27px}.ab-zig{gap:32px}.ab-zig h3{font-size:24px}.ab-trust{grid-template-columns:1fr}}
</style>'''

B = []

# 1) 비전 히어로
B.append(
'<div style="background:linear-gradient(180deg,#ffe9ee 0%,#fff6f8 60%,#fff 100%);padding:180px 20px 110px;position:relative;overflow:hidden">'
'<div style="position:absolute;top:-140px;right:-90px;width:460px;height:460px;border-radius:50%;background:radial-gradient(circle,#fa678130,#fa678100 70%)"></div>'
'<div style="position:absolute;bottom:-180px;left:-110px;width:520px;height:520px;border-radius:50%;background:radial-gradient(circle,#ec489920,#ec489900 70%)"></div>'
'<div class="ab-wrap" style="position:relative;text-align:center">'
'<div style="' + REV + '">'
'<span class="ab-label">TREVITY VISION</span>'
'<h1 class="ab-h" style="font-size:52px;letter-spacing:-1.04px">베트남의 모든 영향력을,<br>한국 브랜드가 쉽게 쓰도록</h1>'
'<p class="ab-sub" style="margin:26px 0 40px">트래비티는 베트남 현지 인플루언서의 영향력을<br>한국 브랜드가 가장 쉽고, 가장 합리적으로 쓸 수 있게 만드는 글로벌 마케팅 그룹입니다.</p>'
'<div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">'
'<a class="ab-btn" href="./inquiry.html">문의하기</a>'
'<a class="ab-btn ghost" href="./#packages">패키지 보기</a>'
'</div></div></div></div>')

# 2) 자기 정의 (ONLY TREVITY)
B.append(
'<section><div style="padding:130px 20px;background:#fff"><div class="ab-wrap" style="text-align:center">'
'<div style="' + REV + '">'
'<span class="ab-label">ONLY TREVITY</span>'
'<h2 class="ab-h">현지에서 증명된<br>인플루언서 마케팅의 기준</h2>'
'<p class="ab-sub" style="max-width:720px;margin:26px auto 0">트래비티는 단순한 섭외 대행사가 아닙니다.<br>'
'10년 넘게 한국 · 베트남 · 중국을 오가며 6,000개 이상의 캠페인을 만들어 온 마케팅 그룹으로,<br>'
'베트남 틱톡 인플루언서 마케팅의 새로운 기준을 만들고 있습니다.</p>'
'</div></div></div></section>')

# 3) 숫자 밴드
def countup(target, label):
    suffix = ''.join(c for c in target if not c.isdigit() and c != ',')
    return ('<div style="text-align:center;min-width:170px">'
            '<p style="font-size:42px;font-weight:800;letter-spacing:-0.84px;color:#fa6781;line-height:1.2">'
            '<span class="inline-grid tabular-nums"><span class="invisible col-start-1 row-start-1" aria-hidden="true">%s</span>'
            '<span class="col-start-1 row-start-1 text-right">0%s</span></span></p>'
            '<p style="margin-top:8px;font-size:15.5px;letter-spacing:-0.31px;color:#595959">%s</p></div>') % (target, suffix, label)

B.append(
'<section><div style="padding:72px 20px;background:#fff5f7"><div class="ab-wrap">'
'<div style="' + REV + 'display:flex;gap:24px;flex-wrap:wrap;justify-content:space-around">'
+ countup('10년+', '글로벌 마케팅 업력')
+ countup('3개국', '한국 · 베트남 · 중국 거점')
+ countup('6,000+', '수행한 캠페인')
+ countup('100,000+', '인플루언서 풀')
+ '</div></div></div></section>')

# 4) 이유 지그재그 3블록
price_visual = ('<div class="ab-price">'
'<div class="row"><span class="nm">스타터 · 10명</span><span class="pr">200만원</span></div>'
'<div class="row"><span class="nm">그로스 · 20명</span><span class="pr">400만원</span></div>'
'<div class="row"><span class="nm">도미넌트 · 50명</span><span class="pr">1,000만원</span></div>'
'<p class="cap">팔로워 10만~50만 무관 · 1명당 20만원 · 부가세 별도</p></div>')

zigs = [
    ('현지 완결형 네트워크', '기획부터 검수까지,<br>전부 트래비티 안에서 끝납니다',
     '서울의 기획과 촬영, 대구의 광고주 소통, 호치민의 현지 마케터, 중국의 시스템 개발까지.<br>'
     '외주 없이 캠페인의 모든 과정이 내부에서 완결되기 때문에, 빠르고 정확하게 움직입니다.',
     '<div style="background:linear-gradient(180deg,#fbfbfd,#fff);border:1px solid #f0f0f2;border-radius:24px;box-shadow:0 8px 40px rgba(0,0,0,0.07);padding:28px 30px 18px;overflow:hidden">' + MAP_SVG + '</div>', False),
    ('검증된 인플루언서 풀', '팔로워 수가 아니라,<br>제품과의 연관성으로 고릅니다',
     '10만 명이 넘는 현지 인플루언서 풀에서 카테고리, 톤앤매너, 오디언스 반응까지 확인하고 섭외합니다.<br>'
     '뷰티 제품이라면, 뷰티에 실제로 반응하는 팬을 가진 인플루언서에게만 맡깁니다.',
     '<img src="./images/about-tiktok.png" alt="틱톡 마케팅 현장" style="width:100%;border-radius:24px;box-shadow:0 8px 40px rgba(0,0,0,0.10);display:block"/>', True),
    ('균일가 구조', '10만이든 50만이든,<br>1명당 20만원',
     '오랜 기간 쌓아온 직접 컨택 구조 덕분에 가능한 가격입니다.<br>'
     '협상도, 숨은 비용도 없습니다. 직접 섭외하는 것보다 싸고, 훨씬 확실합니다.',
     price_visual, False),
]
zz = []
for label, h, p, visual, flip in zigs:
    t = ('<div class="t"><span class="ab-zlabel">%s</span><h3>%s</h3><p>%s</p></div>' % (label, h, p))
    v = '<div class="v">%s</div>' % visual
    inner = (v + t) if flip else (t + v)
    zz.append('<div class="ab-zig" style="' + REV + '">' + inner + '</div>')

B.append(
'<section><div style="padding:130px 20px;background:#fff"><div class="ab-wrap">'
'<div style="text-align:center;margin-bottom:88px;' + REV + '">'
'<span class="ab-label">WHY TREVITY</span>'
'<h2 class="ab-h2">트래비티여야 하는 이유</h2>'
'</div>'
'<div style="display:flex;flex-direction:column;gap:120px">' + ''.join(zz) + '</div>'
'</div></div></section>')

# 5) 신뢰 그리드
trust = [
    ('10년의 글로벌 업력', '한국과 베트남, 중국을 오가며 쌓아 온 경험이 캠페인 설계의 기준이 됩니다.'),
    ('직접 컨택 구조', '중간 브로커 없이 인플루언서와 직접 소통합니다. 균일가가 가능한 이유입니다.'),
    ('현지 마케터 검수', '베트남 현지 콘텐츠 마케터가 가이드 전달부터 업로드 검수까지 직접 진행합니다.'),
    ('제품 연관성 분석', '팔로워 수가 아니라 카테고리 적합도와 오디언스 반응을 확인하고 섭외합니다.'),
    ('결과 리포트 제공', '캠페인 이후 노출과 반응 데이터를 정리한 리포트로 성과를 확인할 수 있습니다.'),
    ('틱톡샵 연계 설계', '노출로 끝나지 않도록, 틱톡샵 제휴 판매 구조까지 함께 설계해 드립니다.'),
]
B.append(
'<section><div style="padding:130px 20px;background:#fafafa"><div class="ab-wrap">'
'<div style="text-align:center;margin-bottom:56px;' + REV + '">'
'<span class="ab-label">TRUST</span>'
'<h2 class="ab-h2">믿고 맡길 수 있는 이유</h2>'
'</div>'
'<div class="ab-trust" style="' + REV + '">'
+ ''.join('<div><h4>%s</h4><p>%s</p></div>' % t for t in trust)
+ '</div></div></div></section>')

# 6) 제공 서비스 3분기
B.append(
'<section><div style="padding:130px 20px;background:#fff"><div class="ab-wrap">'
'<div style="text-align:center;margin-bottom:56px;' + REV + '">'
'<span class="ab-label">SERVICE</span>'
'<h2 class="ab-h2">목적에 맞게 시작하세요</h2>'
'</div>'
'<div class="ab-svc" style="' + REV + '">'
'<a href="./#packages"><span class="tag">TIKTOK BOOKING</span><h4>틱톡 인플루언서<br>대량 부킹</h4><p>팔로워 10만~50만 인플루언서를 10명부터 50명까지, 1명당 20만원 균일가로 부킹합니다.</p><span class="go">패키지 보기 →</span></a>'
'<a href="./inquiry.html"><span class="tag">K-MARKETING</span><h4>한국 관광객<br>유치 마케팅</h4><p>네이버 블로그 · 카페 · 인스타그램으로 한국 여행객을 베트남 매장의 손님으로 만듭니다.</p><span class="go">문의하기 →</span></a>'
'<a href="./inquiry.html"><span class="tag">TIKTOK SHOP</span><h4>틱톡샵<br>판매 연계 설계</h4><p>부킹으로 끝나지 않습니다. 틱톡샵 제휴 판매 구조까지 캠페인 목적에 맞게 설계합니다.</p><span class="go">문의하기 →</span></a>'
'</div></div></div></section>')

# 7) 포트폴리오
B.append(
'<section><div style="padding:130px 20px;background:#fafafa"><div class="ab-wrap">'
'<div style="text-align:center;margin-bottom:56px;' + REV + '">'
'<span class="ab-label">PORTFOLIO</span>'
'<h2 class="ab-h2">트래비티가 만든 장면들</h2>'
'<p class="ab-sub" style="margin-top:18px">누적 조회 280만, 좋아요 100만. 베트남 현지에서 실제로 진행한 캠페인입니다.</p>'
'</div>'
'<div class="ab-port" style="' + REV + '">'
'<div><div class="ph"><img src="./images/portfolio-hantown.png" alt="HAN TOWN 캠페인"/></div><b>HAN TOWN</b><span>호치민 한식당 · 현지 인플루언서 리뷰 캠페인</span></div>'
'<div><div class="ph"><img src="./images/portfolio-chivago.png" alt="CHIVAGO 캠페인"/></div><b>CHIVAGO</b><span>치킨 프랜차이즈 · 틱톡 확산 캠페인</span></div>'
'<div><div class="ph"><img src="./images/portfolio-seya.png" alt="SEYA 캠페인"/></div><b>SEYA STORE &amp; COOK</b><span>한식 매장 · 현지 커뮤니티 공략 캠페인</span></div>'
'</div></div></div></section>')

# 8) 최종 CTA
B.append(
'<section><div style="padding:110px 20px;background:linear-gradient(135deg,#fa6781,#ec4899);text-align:center">'
'<div style="' + REV + '">'
'<h2 style="font-size:38px;font-weight:800;line-height:1.5;letter-spacing:-0.76px;color:#fff;margin:0 0 14px">트래비티와 함께 시작해 보세요</h2>'
'<p style="font-size:18px;line-height:1.7;letter-spacing:-0.36px;color:#ffe4e9;margin:0 0 36px">베트남 틱톡 인플루언서 부킹부터 상담까지, 하루면 충분합니다.</p>'
'<a href="./inquiry.html" style="display:inline-block;height:58px;line-height:58px;padding:0 40px;border-radius:12px;background:#fff;color:#fa6781;font-size:17px;font-weight:800;letter-spacing:-0.34px;text-decoration:none">문의하기</a>'
'</div></div></section>')

page = (head + STYLE
        + '<body class="max-[767px]:min-w-[360px] min-[767px]:min-w-[1440px]">'
        + hdr + mhdr + ''.join(B) + footer
        + '<script src="./mirror.js?v=2"></script></body></html>')
open('about.html', 'w', encoding='utf-8').write(page)
print('about.html v2 written:', len(page))
