# -*- coding: utf-8 -*-
# Rinda 스타일 메가메뉴: 브랜드 카드 + 제목/설명 아이템 (전 페이지)
import glob, re

CSS_ANCHOR = '.tvh-sub:hover>a{background:#fff0f3;color:#fa6781;border-radius:8px}'
CSS_ADD = CSS_ANCHOR + '''
.tvh-mega{display:flex;gap:10px;padding:12px}
.tvh-brand{width:168px;border-radius:12px;background:linear-gradient(150deg,#fa6781,#ff9db0);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7px;padding:22px 14px;flex:none}
.tvh-brand .bl{font-size:23px;font-weight:800;color:#fff;letter-spacing:-0.46px}
.tvh-brand .bt{font-size:10.5px;color:#ffffffcc;letter-spacing:0.8px;text-transform:uppercase}
.tvh-items{display:flex;flex-direction:column;gap:2px;min-width:252px}
.tvh-items a{display:block;padding:10px 14px;border-radius:10px;text-decoration:none;white-space:nowrap}
.tvh-items a:hover{background:#fff0f3}
.tvh-items a b{display:block;font-size:14.5px;font-weight:700;color:#26262b;letter-spacing:-0.29px}
.tvh-items a:hover b{color:#fa6781}
.tvh-items a small{display:block;font-size:12.5px;color:#8c8c8c;margin-top:3px;letter-spacing:-0.25px}
.tvh-items .dv{height:1px;background:#f3f3f5;margin:6px 10px}
.tvh-items a.sub{margin-left:12px;border-left:2px solid #ffd3dc;border-radius:0 10px 10px 0}
@media (max-width:767px){.tvh-mega{display:block;padding:0}.tvh-brand{display:none}.tvh-items{min-width:0}.tvh-items a{padding:11px 36px;white-space:normal}.tvh-items a.sub{margin-left:14px}}'''

def item(href, title, desc, cls='', blank=False):
    t = ' target="_blank"' if blank else ''
    c = f' class="{cls}"' if cls else ''
    return f'<a{c} href="{href}"{t}><b>{title}</b><small>{desc}</small></a>'

BRAND = '<div class="tvh-brand"><span class="bl">trevity</span><span class="bt">global influencer group</span></div>'
def mega(items):
    return '<div class="tvh-dd"><div class="tvh-dd-in tvh-mega">' + BRAND + '<div class="tvh-items">' + items + '</div></div></div>'

# 1) 외국인 관광객 마케팅
old_tour = ('<div class="tvh-dd"><div class="tvh-dd-in">'
            '<a href="./tourist-vn.html">베트남인 관광객 유학생 체험단</a>'
            '<a href="./tourist-cn.html">중국인 관광객 유학생 체험단</a></div></div>')
new_tour = mega(
    item('./tourist-vn.html', '베트남인 관광객·유학생 체험단', '방한 베트남인이 매장을 체험하고 베트남 SNS에 알립니다')
    + item('./tourist-cn.html', '중국인 관광객·유학생 체험단', '샤오홍슈·더우인으로 중국인 손님을 데려옵니다'))

# 2) 해외 현지 마케팅 (tvh-sub 플라이아웃 → 메가 계층)
old_local = ('<div class="tvh-dd"><div class="tvh-dd-in"><div class="tvh-sub"><a href="./local-vn.html">베트남 현지 매장 마케팅<span class="tvh-arr">&#8250;</span></a>'
             '<div class="tvh-sub-dd"><div class="tvh-sub-dd-in">'
             '<a href="./local-vn.html#local">베트남 로컬 손님 유치</a>'
             '<a href="./local-vn.html#chinese">중국인 관광객 손님 유치</a>'
             '<a href="./local-vn.html#korean">한국인 관광객 손님 유치</a>'
             '</div></div></div></div></div>')
new_local = mega(
    item('./local-vn.html', '베트남 현지 매장 마케팅', '세 방향의 손님을 한 번에 — 전체 보기')
    + '<div class="dv"></div>'
    + item('./local-vn.html#local', '베트남 로컬 손님 유치', '로컬 틱톡 · 페이스북 인플루언서', cls='sub')
    + item('./local-vn.html#chinese', '중국인 관광객 손님 유치', '더우인 · 따중디엔핑 후기', cls='sub')
    + item('./local-vn.html#korean', '한국인 관광객 손님 유치', '네이버 블로그 · 인스타그램', cls='sub'))

# 3) 고객센터 (제휴 문의 href는 페이지별 ?svc= 가능 → 정규식)
def customer_new(inq_href):
    return mega(
        item('./help.html', '종합 헬프센터', '자주 묻는 질문과 이용 안내')
        + item('./help.html#agency', '공식대행사', '트래비티 공식 파트너 안내')
        + item(inq_href, '제휴 문의', '함께할 파트너를 찾습니다'))
cust_re = re.compile(r'<div class="tvh-dd"><div class="tvh-dd-in"><a href="\./help\.html">종합 헬프센터</a><a href="\./help\.html#agency">공식대행사</a><a href="(\./inquiry\.html[^"]*)">제휴 문의</a></div></div>')

# 4) 인플루언서라면?
old_infl = ('<div class="tvh-dd"><div class="tvh-dd-in">'
            '<a href="https://kr.trevity.com" target="_blank">한국 인플루언서</a>'
            '<a href="https://vn.trevity.com" target="_blank">베트남 인플루언서</a>'
            '<a href="https://cn.trevity.com" target="_blank">중국 인플루언서</a>'
            '<a href="https://mm.trevity.com" target="_blank">미얀마 인플루언서</a>'
            '</div></div>')
new_infl = mega(
    item('https://kr.trevity.com', '한국 인플루언서', '여행 · 숙박 체험단 신청', blank=True)
    + item('https://vn.trevity.com', '베트남 인플루언서', 'Đăng ký KOC TREVITY', blank=True)
    + item('https://cn.trevity.com', '중국 인플루언서', '达人合作申请', blank=True)
    + item('https://mm.trevity.com', '미얀마 인플루언서', 'TREVITY Creator 신청', blank=True))

# 5) 트래비티소개 dd는 이미 삭제됨 — 없음

n = 0
for f in glob.glob('*.html'):
    if f.startswith('_bak') or f.startswith('_pain') or f in ('rendered.html','featuring-ref.html','trevity-nav.html'):
        continue
    s = open(f, encoding='utf-8').read()
    orig = s
    if CSS_ANCHOR in s:
        s = s.replace(CSS_ANCHOR, CSS_ADD, 1)
    s = s.replace(old_tour, new_tour)
    s = s.replace(old_local, new_local)
    s = cust_re.sub(lambda m: customer_new(m.group(1)), s)
    s = s.replace(old_infl, new_infl)
    if s != orig:
        open(f, 'w', encoding='utf-8').write(s)
        n += 1
print('mega menu applied to', n, 'pages')
