# -*- coding: utf-8 -*-
# 사업 카테고리 6종 서비스 페이지 + 헬프센터 생성, 전 페이지 내비 링크 재연결 (광고주 대상 카피)
import re

def balanced(h, start, tag='div'):
    depth = 0
    for m in re.finditer(r'<%s\b|</%s>' % (tag, tag), h[start:]):
        depth += 1 if not m.group(0).startswith('</') else -1
        if depth == 0:
            return start + m.end()

idx = open('index.html', encoding='utf-8').read()
head_base = idx[:idx.find('</head>') + len('</head>')]
head_base = re.sub(r'<style id="main-style">.*?</style>', '', head_base, flags=re.S)
fs = idx.find('<footer')
footer = idx[fs:balanced(idx, fs, 'footer')]

REV = 'opacity: 0; transform: translateY(40px); transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;'

# ── 새 메뉴 (모든 서브가 실제 페이지/앵커로) ──
MENU = [
    ('트래비티소개', None, [('트래비티', './about.html'), ('트래비티 글로벌', './about.html')]),
    ('체험단 마케팅', None, [('방문체험단', 'https://kr.trevity.com'), ('제품체험단', './experience.html#product')]),
    ('한국제품 해외수출 마케팅', None, [
        ('베트남 인플루언서 틱톡 체험단', './vietnam-tiktok.html'),
        ('중국 인플루언서 샤오홍슈 체험단', './export.html#cn'),
        ('대만 인플루언서 인스타 체험단', './export.html#tw'),
        ('일본 인플루언서 인스타 체험단', './export.html#jp'),
        ('태국 인플루언서 틱톡 체험단', './export.html#th'),
        ('미얀마 인플루언서 틱톡 체험단', './export.html#mm')]),
    ('외국인 관광객 마케팅', None, [
        ('베트남인 관광객 유학생 체험단', './tourist.html#vn'),
        ('중국인 관광객 유학생 체험단', './tourist.html#cn'),
        ('대만인 관광객 유학생 체험단', './tourist.html#tw'),
        ('일본인 관광객 유학생 체험단', './tourist.html#jp'),
        ('태국인 관광객 유학생 체험단', './tourist.html#th'),
        ('미얀마인 관광객 유학생 체험단', './tourist.html#mm')]),
    ('해외 현지 마케팅', None, [
        ('베트남 현지 매장홍보 마케팅', './local.html#vn'),
        ('중국 현지 매장홍보 마케팅', './local.html#cn'),
        ('대만 현지 매장홍보 마케팅', './local.html#tw'),
        ('일본 현지 매장홍보 마케팅', './local.html#jp'),
        ('태국 현지 매장홍보 마케팅', './local.html#th'),
        ('미얀마 현지 매장홍보 마케팅', './local.html#mm')]),
    ('숙박 체험단', None, [
        ('내국인 관광객 호텔 체험단', './stay.html#hotel'),
        ('내국인 관광객 펜션 체험단', './stay.html#pension'),
        ('외국인 관광객 숙박 체험단', './stay.html#foreign')]),
    ('팸투어 마케팅', None, [
        ('내국인 관광객 서포터즈 운영대행', './famtour.html#sp-kr'),
        ('외국인 관광객 서포터즈 운영대행', './famtour.html#sp-fr'),
        ('외국인 메가 인플루언서 팸투어대행', './famtour.html#mega'),
        ('지자체 지역 홍보 대행', './famtour.html#gov')]),
    ('블로그', './blog.html', []),
    ('고객센터', None, [('종합 헬프센터', './help.html'), ('공식대행사', './help.html#agency'), ('제휴 문의', './inquiry.html')]),
]

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
            '<nav class="tvh-nav"><ul>' + ''.join(lis) + '</ul></nav>'
            '<a class="tvh-cta" href="./inquiry.html">문의하기</a>'
            '</div></header>')

SVC_STYLE = '''<style id="svc-style">
html{scroll-behavior:smooth}
.sv-wrap{max-width:1084px;margin:0 auto;padding:0 20px}
.sv-hero{background:linear-gradient(180deg,#ffe9ee,#fff);padding:96px 20px 64px;text-align:center}
.sv-hero .lb{display:inline-block;font-size:14px;font-weight:800;letter-spacing:2px;color:#fa6781;margin-bottom:14px}
.sv-hero h1{font-size:40px;font-weight:800;line-height:1.45;letter-spacing:-0.8px;color:#1f1f1f;margin:0 0 16px}
.sv-hero p{font-size:17.5px;line-height:1.75;letter-spacing:-0.35px;color:#595959;margin:0 0 30px}
.sv-btn{display:inline-block;height:54px;line-height:54px;padding:0 32px;border-radius:10px;background:#fa6781;color:#fff;font-size:16px;font-weight:700;letter-spacing:-0.32px;text-decoration:none}
.sv-btn:hover{opacity:.85}
.sv-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}
.sv-card{background:#fff;border:1px solid #f0f0f0;border-radius:20px;padding:34px 30px;scroll-margin-top:76px}
.sv-card .flag{font-size:30px;margin-bottom:12px;display:block}
.sv-card h3{font-size:20px;font-weight:800;letter-spacing:-0.4px;color:#1f1f1f;margin:0 0 6px;line-height:1.4}
.sv-card .ch{display:inline-block;font-size:12.5px;font-weight:700;color:#fa6781;background:#fff0f3;border-radius:999px;padding:4px 12px;margin-bottom:14px}
.sv-card p{font-size:14.5px;line-height:1.75;letter-spacing:-0.29px;color:#595959;margin:0 0 18px}
.sv-card .go{font-size:14.5px;font-weight:700;color:#fa6781;text-decoration:none}
.sv-steps{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.sv-steps>div{background:#fff;border-radius:16px;padding:28px 22px;border:1px solid #f0f0f0}
.sv-steps .n{font-size:14px;font-weight:800;color:#fa6781;margin-bottom:10px}
.sv-steps h4{font-size:16.5px;font-weight:700;letter-spacing:-0.33px;color:#1f1f1f;margin:0 0 8px}
.sv-steps p{font-size:13.5px;line-height:1.65;letter-spacing:-0.27px;color:#737373;margin:0}
.sv-why{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.sv-why>div{background:#fff5f7;border-radius:16px;padding:30px 26px}
.sv-why h4{font-size:17px;font-weight:700;letter-spacing:-0.34px;color:#1f1f1f;margin:0 0 10px}
.sv-why p{font-size:14px;line-height:1.7;letter-spacing:-0.28px;color:#737373;margin:0}
.sv-shead{text-align:center;margin-bottom:48px}
.sv-shead .lb{display:inline-block;font-size:14px;font-weight:800;letter-spacing:2px;color:#fa6781;margin-bottom:12px}
.sv-shead h2{font-size:32px;font-weight:800;line-height:1.45;letter-spacing:-0.64px;color:#1f1f1f;margin:0}
.faq-item{border-bottom:1px solid #f0f0f0}
.faq-item summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;padding:22px 6px;font-size:17px;font-weight:700;letter-spacing:-0.34px;color:#1f1f1f}
.faq-item summary::-webkit-details-marker{display:none}
.faq-item summary:after{content:'+';font-size:22px;color:#fa6781;font-weight:400}
.faq-item[open] summary:after{content:'−'}
.faq-item .a{padding:0 6px 24px;font-size:15.5px;line-height:1.8;letter-spacing:-0.31px;color:#595959}
@media (max-width:1023px){.sv-steps{grid-template-columns:repeat(2,1fr)}.sv-why{grid-template-columns:1fr}}
@media (max-width:767px){.sv-hero h1{font-size:28px}.sv-grid{grid-template-columns:1fr}.sv-steps{grid-template-columns:1fr}}
</style>'''

STEPS = ('<section><div style="padding:96px 20px;background:#fafafa"><div class="sv-wrap">'
'<div class="sv-shead" style="' + REV + '"><span class="lb">PROCESS</span><h2>진행은 이렇게 흘러갑니다</h2></div>'
'<div class="sv-steps" style="' + REV + '">'
'<div><p class="n">STEP 1</p><h4>문의 접수</h4><p>브랜드와 매장 상황, 목표를 남겨주시면 하루 안에 담당 매니저가 연락드립니다.</p></div>'
'<div><p class="n">STEP 2</p><h4>제안과 견적</h4><p>목적에 맞는 채널과 규모를 설계해 명확한 견적으로 제안드립니다.</p></div>'
'<div><p class="n">STEP 3</p><h4>모집과 선정</h4><p>제품 · 매장과 맞는 체험단과 인플루언서만 선별해 확정합니다.</p></div>'
'<div><p class="n">STEP 4</p><h4>진행과 리포트</h4><p>콘텐츠 가이드와 검수까지 관리하고, 결과 리포트로 성과를 확인해 드립니다.</p></div>'
'</div></div></div></section>')

WHY = ('<section><div style="padding:96px 20px;background:#fff"><div class="sv-wrap">'
'<div class="sv-shead" style="' + REV + '"><span class="lb">WHY TREVITY</span><h2>트래비티가 진행하면 다른 점</h2></div>'
'<div class="sv-why" style="' + REV + '">'
'<div><h4>10만+ 인플루언서 · 체험단 풀</h4><p>아시아 6개국에서 오래 쌓아온 풀에서 목적에 맞는 사람만 선별합니다.</p></div>'
'<div><h4>현지 마케터가 직접</h4><p>모집, 가이드 전달, 콘텐츠 검수까지 각 나라의 현지 마케터가 직접 진행합니다.</p></div>'
'<div><h4>결과 리포트 제공</h4><p>노출과 반응 데이터를 정리한 리포트로 캠페인 성과를 투명하게 보여드립니다.</p></div>'
'</div></div></div></section>')

CTA = ('<section><div style="padding:90px 20px;background:linear-gradient(135deg,#fa6781,#ec4899);text-align:center">'
'<div style="' + REV + '">'
'<h2 style="font-size:32px;font-weight:800;line-height:1.5;letter-spacing:-0.64px;color:#fff;margin:0 0 12px">우리 브랜드에 맞을지 궁금하다면</h2>'
'<p style="font-size:17px;letter-spacing:-0.34px;color:#ffe4e9;margin:0 0 32px">상황을 남겨주시면, 가장 맞는 방법과 견적부터 제안드립니다.</p>'
'<a href="./inquiry.html" style="display:inline-block;height:56px;line-height:56px;padding:0 38px;border-radius:12px;background:#fff;color:#fa6781;font-size:16.5px;font-weight:800;text-decoration:none">문의하기</a>'
'</div></div></section>')

def card(anchor, flag, title, chip, desc, link=None, linktext=None):
    go = '<a class="go" href="%s">%s</a>' % (link or './inquiry.html', linktext or '문의하기 →')
    return ('<div class="sv-card" id="%s"><span class="flag">%s</span><h3>%s</h3>'
            '<span class="ch">%s</span><p>%s</p>%s</div>') % (anchor, flag, title, chip, desc, go)

def page(fname, active, label, h1, sub, cards_html, extra=''):
    head = re.sub(r'<title>[^<]*</title>', '<title>%s | 트래비티</title>' % active if active else '<title>트래비티</title>', head_base)
    body = ('<div class="sv-hero"><div style="' + REV + '">'
            '<span class="lb">%s</span><h1>%s</h1><p>%s</p>'
            '<a class="sv-btn" href="./inquiry.html">문의하기</a></div></div>'
            '<section><div style="padding:80px 20px;background:#fff"><div class="sv-wrap">'
            '<div class="sv-grid" style="' + REV + '">%s</div></div></div></section>'
            ) % (label, h1, sub, cards_html)
    html = (head + SVC_STYLE
            + '<body class="max-[767px]:min-w-[360px] min-[767px]:min-w-[1440px]">'
            + build_header(active) + body + extra + STEPS + WHY + CTA + footer
            + '<script src="./mirror.js?v=2"></script></body></html>')
    open(fname, 'w', encoding='utf-8').write(html)
    print(fname, len(html))

# ── 1. 체험단 마케팅 ──
page('experience.html', '체험단 마케팅', 'EXPERIENCE MARKETING',
     '국내 고객의 진짜 후기가<br>매출이 되는 체험단 마케팅',
     '방문 체험단과 제품 체험단으로, 검색했을 때 믿고 갈 수 있는 후기를 만들어 드립니다.',
     card('visit', '🏬', '방문체험단', '매장 · 식당 · 뷰티샵',
          '검증된 체험단이 매장을 직접 방문해 생생한 후기 콘텐츠를 남깁니다. 트래비티 체험단 플랫폼에서 모집부터 선정, 리뷰 관리까지 한 번에 진행됩니다.',
          'https://kr.trevity.com', '체험단 플랫폼 바로가기 →')
     + card('product', '📦', '제품체험단', '신제품 · 온라인 판매 제품',
            '제품을 배송받은 체험단이 사용 후기를 블로그와 SNS에 남깁니다. 출시 초기에 후기 콘텐츠를 빠르게 쌓아 구매 전환의 기반을 만듭니다.'))

# ── 2. 해외수출 마케팅 ──
ex_cards = (
    card('vn', '🇻🇳', '베트남 인플루언서 틱톡 체험단', '틱톡 · 팔로워 10만~50만',
         '팔로워 10만~50만 현지 인플루언서를 1명당 20만원 균일가로 대량 부킹합니다. 트래비티의 대표 상품입니다.',
         './vietnam-tiktok.html', '상품 자세히 보기 →')
    + card('cn', '🇨🇳', '중국 인플루언서 샤오홍슈 체험단', '샤오홍슈 · 왕홍',
           '중국 소비자가 쇼핑 전 검색하는 샤오홍슈에서, 카테고리에 맞는 왕홍의 체험 콘텐츠로 제품 신뢰를 만듭니다.')
    + card('tw', '🇹🇼', '대만 인플루언서 인스타 체험단', '인스타그램',
           '한국 제품에 우호적인 대만 시장을 인스타그램 인플루언서 체험 콘텐츠로 공략합니다.')
    + card('jp', '🇯🇵', '일본 인플루언서 인스타 체험단', '인스타그램',
           '리뷰를 꼼꼼히 확인하는 일본 소비자에게, 신뢰도 높은 인플루언서의 사용 후기로 다가갑니다.')
    + card('th', '🇹🇭', '태국 인플루언서 틱톡 체험단', '틱톡',
           '동남아 틱톡 강국 태국에서 현지 인플루언서의 숏폼 콘텐츠로 제품을 확산시킵니다.')
    + card('mm', '🇲🇲', '미얀마 인플루언서 틱톡 체험단', '틱톡',
           '경쟁이 덜한 미얀마 시장을 선점할 수 있도록 현지 인플루언서 체험단을 운영합니다.'))
page('export.html', '한국제품 해외수출 마케팅', 'EXPORT MARKETING',
     '수출할 제품,<br>현지 인플루언서가 알립니다',
     '아시아 6개국의 현지 인플루언서 체험단으로, 낯선 시장에서 제품의 첫 신뢰를 만들어 드립니다.',
     ex_cards)

# ── 3. 외국인 관광객 마케팅 ──
def t_card(anchor, flag, country, channel, extra=''):
    return card(anchor, flag, '%s인 관광객 · 유학생 체험단' % country, channel,
                '한국에 있는 %s인 관광객과 유학생이 매장을 직접 체험하고, 모국 SNS에 후기를 올립니다. '
                '같은 나라 여행자들이 검색했을 때 우리 매장이 나오게 만듭니다.%s' % (country, extra))
to_cards = (t_card('vn', '🇻🇳', '베트남', '틱톡 · 페이스북')
    + t_card('cn', '🇨🇳', '중국', '샤오홍슈 · 더우인')
    + t_card('tw', '🇹🇼', '대만', '인스타그램')
    + t_card('jp', '🇯🇵', '일본', '인스타그램 · 트위터')
    + t_card('th', '🇹🇭', '태국', '틱톡 · 페이스북')
    + t_card('mm', '🇲🇲', '미얀마', '페이스북'))
page('tourist.html', '외국인 관광객 마케팅', 'INBOUND MARKETING',
     '한국에 온 외국인 관광객을<br>우리 매장의 손님으로',
     '방한 관광객과 유학생 체험단이 남긴 모국어 후기가, 다음 여행자들을 매장으로 데려옵니다.',
     to_cards)

# ── 4. 해외 현지 마케팅 ──
def l_card(anchor, flag, country, channel):
    return card(anchor, flag, '%s 현지 매장홍보 마케팅' % country, channel,
                '%s에 있는 매장을 현지 고객에게 알립니다. 현지 마케터가 시장에 맞는 채널과 콘텐츠로 방문을 만들어 드립니다.' % country)
lo_cards = (l_card('vn', '🇻🇳', '베트남', '틱톡 · 페이스북')
    + l_card('cn', '🇨🇳', '중국', '더우인 · 따중디엔핑')
    + l_card('tw', '🇹🇼', '대만', '인스타그램 · 구글맵')
    + l_card('jp', '🇯🇵', '일본', '인스타그램 · 타베로그')
    + l_card('th', '🇹🇭', '태국', '틱톡 · 페이스북')
    + l_card('mm', '🇲🇲', '미얀마', '페이스북'))
page('local.html', '해외 현지 마케팅', 'LOCAL MARKETING',
     '해외 매장의 현지 손님,<br>현지 마케터가 만듭니다',
     '베트남 호치민 마케팅 센터를 중심으로, 아시아 6개국 매장의 현지 홍보를 직접 진행합니다.',
     lo_cards)

# ── 5. 숙박 체험단 ──
st_cards = (
    card('hotel', '🏨', '내국인 관광객 호텔 체험단', '블로그 · 인스타그램',
         '호캉스를 검색하는 국내 고객에게, 검증된 체험단의 생생한 투숙 후기로 호텔을 알립니다.')
    + card('pension', '🏡', '내국인 관광객 펜션 체험단', '블로그 · 인스타그램',
           '주말 여행지를 찾는 고객이 검색했을 때 펜션이 보이도록, 후기 콘텐츠를 차곡차곡 쌓아 드립니다.')
    + card('foreign', '🌏', '외국인 관광객 숙박 체험단', '모국 SNS 채널',
           '방한 외국인 체험단의 모국어 숙박 후기로, 해외 여행자들의 예약을 끌어옵니다.'))
page('stay.html', '숙박 체험단', 'STAY MARKETING',
     '빈 객실을 채우는<br>숙박 체험단 마케팅',
     '호텔부터 펜션까지, 내국인과 외국인 체험단의 후기로 예약을 만들어 드립니다.',
     st_cards)

# ── 6. 팸투어 마케팅 ──
fm_cards = (
    card('sp-kr', '📣', '내국인 관광객 서포터즈 운영대행', '모집 · 운영 · 콘텐츠 관리',
         '지역과 시설을 알릴 서포터즈의 모집부터 콘텐츠 관리, 시상까지 운영 전 과정을 대행합니다.')
    + card('sp-fr', '🌐', '외국인 관광객 서포터즈 운영대행', '외국인 크리에이터',
           '한국을 찾은 외국인 크리에이터 서포터즈를 운영해, 해외 채널에 지역 콘텐츠를 퍼뜨립니다.')
    + card('mega', '⭐', '외국인 메가 인플루언서 팸투어대행', '초청 · 일정 · 콘텐츠',
           '수십만~수백만 팔로워의 해외 인플루언서를 초청해, 일정 설계부터 콘텐츠 제작까지 팸투어 전체를 대행합니다.')
    + card('gov', '🏛️', '지자체 지역 홍보 대행', '지자체 · 관광공사',
           '지역 축제와 관광지를 국내외 채널에 알리는 홍보 캠페인을 기획부터 결과 보고까지 수행합니다.'))
page('famtour.html', '팸투어 마케팅', 'FAM TOUR',
     '지역과 시설을 알리는<br>팸투어 · 서포터즈 마케팅',
     '서포터즈 운영부터 해외 메가 인플루언서 팸투어까지, 홍보의 판을 대신 짜 드립니다.',
     fm_cards)

# ── 7. 헬프센터 ──
faqs = [
    ('견적은 어떻게 받을 수 있나요?', '문의하기로 브랜드 · 매장 상황과 목표를 남겨주시면, 하루 안에 담당 매니저가 연락드리고 목적에 맞는 구성과 견적을 제안드립니다.'),
    ('어떤 서비스를 선택해야 할지 모르겠어요.', '괜찮습니다. 판매하는 제품인지 방문 매장인지, 국내 고객인지 해외 고객인지만 알려주시면 가장 맞는 서비스부터 저희가 제안드립니다.'),
    ('진행 기간은 얼마나 걸리나요?', '서비스와 규모에 따라 다르지만, 일반적으로 모집 · 선정에 1~2주, 콘텐츠 발행까지 2~4주 정도 소요됩니다. 일정이 급한 경우 상담 시 말씀해 주세요.'),
    ('결과는 어떻게 확인하나요?', '캠페인 종료 후 노출 · 반응 데이터를 정리한 결과 리포트를 제공해 드립니다. 발행된 콘텐츠 링크도 함께 정리해 드립니다.'),
    ('비용은 선결제인가요?', '서비스별 결제 조건은 상담 시 안내드립니다. 견적서와 계약서를 통해 비용과 범위를 명확히 확정한 뒤 진행합니다.'),
]
faq_html = ''.join('<details class="faq-item"><summary>Q. %s</summary><div class="a">%s</div></details>' % f for f in faqs)
help_body = (
'<div class="sv-hero"><div style="' + REV + '">'
'<span class="lb">HELP CENTER</span><h1>무엇을 도와드릴까요?</h1>'
'<p>자주 묻는 질문을 먼저 확인하시고, 해결되지 않으면 바로 문의를 남겨주세요.</p>'
'<a class="sv-btn" href="./inquiry.html">문의하기</a></div></div>'
'<section><div style="padding:80px 20px;background:#fff"><div class="sv-wrap" style="max-width:820px">'
'<div class="sv-shead" style="' + REV + '"><span class="lb">FAQ</span><h2>자주 묻는 질문</h2></div>'
'<div style="' + REV + '">' + faq_html + '</div></div></div></section>'
'<section id="agency" style="scroll-margin-top:76px"><div style="padding:96px 20px;background:#fafafa"><div class="sv-wrap" style="max-width:820px;text-align:center">'
'<div style="' + REV + '">'
'<span class="lb" style="display:inline-block;font-size:14px;font-weight:800;letter-spacing:2px;color:#fa6781;margin-bottom:12px">OFFICIAL AGENCY</span>'
'<h2 style="font-size:30px;font-weight:800;letter-spacing:-0.6px;color:#1f1f1f;margin:0 0 16px">트래비티 공식대행사</h2>'
'<p style="font-size:16px;line-height:1.8;letter-spacing:-0.32px;color:#595959;margin:0 0 28px">트래비티의 체험단 · 인플루언서 마케팅을 함께 판매할 공식대행사를 찾습니다.<br>'
'광고대행사, 마케팅 에이전시라면 제휴 문의로 연락 주세요. 상품 교육과 정산 조건을 안내드립니다.</p>'
'<a class="sv-btn" href="./inquiry.html">제휴 문의하기</a>'
'</div></div></div></section>')
help_head = re.sub(r'<title>[^<]*</title>', '<title>고객센터 | 트래비티</title>', head_base)
help_html = (help_head + SVC_STYLE
    + '<body class="max-[767px]:min-w-[360px] min-[767px]:min-w-[1440px]">'
    + build_header('고객센터') + help_body + CTA + footer
    + '<script src="./mirror.js?v=2"></script></body></html>')
open('help.html', 'w', encoding='utf-8').write(help_html)
print('help.html', len(help_html))

# ── 8. 기존 페이지 헤더 전부 새 MENU로 교체 ──
ACTIVE = {
    'index.html': None, 'vietnam-tiktok.html': '한국제품 해외수출 마케팅', 'about.html': '트래비티소개',
    'blog.html': '블로그', 'blog-market.html': '블로그', 'blog-midtier.html': '블로그',
    'blog-diy.html': '블로그', 'blog-hantown.html': '블로그', 'inquiry.html': '고객센터',
    'coming-soon.html': None,
}
for f, active in ACTIVE.items():
    t = open(f, encoding='utf-8').read()
    hs = t.find('<header class="tvh">')
    he = balanced(t, hs, 'header')
    t = t[:hs] + build_header(active) + t[he:]
    open(f, 'w', encoding='utf-8').write(t)
    print(f, 'header updated')
print('ALL DONE')
