# -*- coding: utf-8 -*-
"""
공식대행사 = 별도 서브페이지 agency.html 생성 + 전 페이지 링크 재연결
- 셸(head / 헤더 / 푸터)은 help.html 에서 그대로 가져옴 -> 나브·푸터 자동 동기
- 디자인 언어는 _build_help.py 의 .tvhc-* CSS 를 공유(단일 소스)
- ./help.html#agency -> ./agency.html 로 전 페이지 치환
재실행 가능. 백업: *.bak_agency
"""
import io, os, re, glob, shutil

os.chdir(r"C:\Users\이건희\creplanet-clone")

# 디자인 언어 단일 소스 — 헬프센터와 동일 CSS/컴포넌트 재사용
from _build_help import CSS, ARROW, acc_item

SHELL = 'help.html'
OUT = 'agency.html'

# ── 함께 판매하는 상품 (실제 운영 중인 4종)
PRODUCTS = [
    ('한국제품 해외수출', '베트남 현지 인플루언서를 부킹해 제품을 알립니다', './vietnam-tiktok.html'),
    ('외국인 관광객 유치', '방한 베트남인·중국인이 매장을 체험하고 현지 SNS에 남깁니다', './tourist-vn.html'),
    ('해외 현지 매장 마케팅', '베트남에 있는 매장의 로컬 손님을 늘립니다', './local-vn.html'),
    ('숙박 체험단', '호텔·펜션의 빈 객실을 후기로 바꿉니다', './stay.html'),
]

# ── 공식대행사에게 제공되는 것 (확정된 것만)
PROVIDE = [
    ('상품 교육',
     '상품 구성과 단가, 진행 절차, 실제 사례를 전달드립니다. 고객사에 바로 제안하실 수 있는 수준까지 안내합니다.'),
    ('정산 조건 안내',
     '제휴 상담에서 정산 조건을 확정해 드립니다.'),
    ('현지 실행 전담',
     '섭외부터 가이드라인, 촬영, 검수까지 트래비티가 직접 진행합니다. '
     '서울·대련·호치민·대구 4개 거점의 현지 마케터가 중간 업체 없이 처리합니다.'),
    ('영업과 고객 관리에 집중',
     '대행사는 고객 발굴과 관계에 집중하시면 됩니다. 해외 실행 리스크를 안고 가실 필요가 없습니다.'),
]

STEPS = [
    ('제휴 문의', '회사 정보와 주력 고객사 업종을 남겨주세요.'),
    ('상담', '담당자가 연락드려 어떤 상품이 고객사에 맞는지 함께 확인합니다.'),
    ('상품 교육', '제휴 확정 후 상품 구성과 단가, 진행 절차를 전달드립니다.'),
    ('판매 시작', '고객사 제안부터 실행까지 트래비티가 함께 붙습니다.'),
]

# ── 상담에서 확정하는 항목 (지어내지 않는다)
CONSULT = [
    ('정산 조건', '수수료 구조와 정산 주기'),
    ('계약 기간', '제휴 계약의 기간과 갱신 방식'),
    ('지역 · 업종 배분', '지역이나 업종에 대한 우선권 여부'),
    ('최소 진행 조건', '제휴 유지에 필요한 최소 조건이 있는지'),
]

FAQ = [
    ('어떤 회사를 찾고 있나요?',
     '광고대행사와 마케팅 에이전시를 우선으로 보고 있습니다. '
     '이미 고객사를 보유하고 계시고, 해외 마케팅 제안이 필요한 상황이라면 잘 맞습니다.'),
    ('해외 마케팅 경험이 없어도 되나요?',
     '실행은 트래비티가 전담하기 때문에 해외 경험이 없어도 됩니다. '
     '상품 교육에서 고객사에 설명하실 수 있는 수준까지 안내드립니다.'),
    ('어떤 상품을 판매할 수 있나요?',
     '해외수출, 외국인 관광객 유치, 해외 현지 매장, 숙박 체험단 네 가지 모두 가능합니다. '
     '고객사 상황에 맞는 것만 골라 진행하셔도 됩니다.'),
    ('실행은 누가 하나요?',
     '트래비티가 합니다. 인플루언서 섭외, 가이드라인 전달, 촬영과 검수까지 '
     '<b>서울·대련·호치민·대구 4개 거점</b>의 현지 마케터가 직접 진행합니다.'),
    ('정산 조건이나 지역 독점이 궁금합니다.',
     '회사 규모와 주력 업종에 따라 조건이 달라져 제휴 상담에서 확정해 드립니다. '
     '아래로 문의 주시면 담당자가 연락드립니다.'),
]


def build_body():
    o = []
    o.append('<div class="tvhc">')
    o.append('<style>%s</style>' % CSS)

    # 히어로
    o.append('<section class="tvhc-hero"><div class="tvhc-w">')
    o.append('<span class="tvhc-label">OFFICIAL AGENCY</span>')
    o.append('<h1 class="tvhc-h1">트래비티 공식대행사를<br/>모집합니다</h1>')
    o.append('<p class="tvhc-sub">체험단과 인플루언서 마케팅을 고객사에 제안하고 계신다면, '
             '해외 실행은 트래비티가 맡습니다. 광고대행사·마케팅 에이전시와 함께 판매합니다.</p>')
    o.append('<a class="tvhc-cta" href="./inquiry.html">제휴 문의하기</a>')
    o.append('</div></section>')

    # 함께 판매하는 상품
    o.append('<section class="tvhc-sec" id="products" style="scroll-margin-top:76px"><div class="tvhc-w">')
    o.append('<span class="tvhc-label">PRODUCTS</span>')
    o.append('<h2 class="tvhc-h2">함께 판매하는 상품</h2>')
    o.append('<dl class="tvhc-facts">')
    for name, desc, link in PRODUCTS:
        o.append('<div class="tvhc-fact"><dt>%s</dt><dd style="font-weight:600;font-size:15px;'
                 'line-height:1.7;color:#595959">%s</dd>'
                 '<a class="tvhc-more" style="margin-top:16px;font-size:14px" href="%s">자세히%s</a>'
                 '</div>' % (name.upper() if False else name, desc, link, ARROW))
    o.append('</dl></div></section>')

    # 제공되는 것
    o.append('<section class="tvhc-sec"><div class="tvhc-w">')
    o.append('<span class="tvhc-label">WHAT YOU GET</span>')
    o.append('<h2 class="tvhc-h2">대행사가 받는 것</h2>')
    o.append('<div class="tvhc-consult">')
    for name, desc in PROVIDE:
        o.append('<div class="tvhc-crow"><strong>%s</strong>'
                 '<span style="color:#595959">%s</span></div>' % (name, desc))
    o.append('</div></div></section>')

    # 절차
    o.append('<section class="tvhc-sec" id="process" style="scroll-margin-top:76px"><div class="tvhc-w">')
    o.append('<span class="tvhc-label">PROCESS</span>')
    o.append('<h2 class="tvhc-h2">문의부터 판매까지</h2>')
    o.append('<div class="tvhc-steps">')
    for i, (name, desc) in enumerate(STEPS, 1):
        o.append('<div class="tvhc-step"><em>STEP %d</em><strong>%s</strong><span>%s</span></div>'
                 % (i, name, desc))
    o.append('</div></div></section>')

    # 상담에서 확정
    o.append('<section class="tvhc-sec"><div class="tvhc-w">')
    o.append('<span class="tvhc-label">TERMS</span>')
    o.append('<h2 class="tvhc-h2">상담에서 확정하는 항목</h2>')
    o.append('<p class="tvhc-sub">아래 조건은 회사 규모와 주력 업종에 따라 달라집니다. '
             '일괄로 안내드리기보다 제휴 상담에서 정확한 기준을 드립니다.</p>')
    o.append('<div class="tvhc-consult">')
    for name, desc in CONSULT:
        o.append('<div class="tvhc-crow"><strong>%s</strong><span>%s</span></div>' % (name, desc))
    o.append('</div></div></section>')

    # FAQ
    o.append('<section class="tvhc-sec" id="faq" style="scroll-margin-top:76px"><div class="tvhc-w">')
    o.append('<span class="tvhc-label">FAQ</span>')
    o.append('<h2 class="tvhc-h2">자주 묻는 질문</h2>')
    o.append('<div class="tvhc-acc">')
    for q, a in FAQ:
        o.append(acc_item(q, a))
    o.append('</div></div></section>')

    # CTA
    o.append('<section class="tvhc-sec" id="contact" style="scroll-margin-top:76px;padding-bottom:110px">'
             '<div class="tvhc-w">')
    o.append('<span class="tvhc-label">CONTACT</span>')
    o.append('<h2 class="tvhc-h2">함께할 파트너를 찾습니다</h2>')
    o.append('<p class="tvhc-sub">회사 정보와 주력 고객사 업종을 남겨주시면 담당자가 연락드립니다.</p>')
    o.append('<dl class="tvhc-ch">'
             '<div class="tvhc-chi"><dt>전화</dt><dd>070-4212-8266'
             '<small>평일 10:00 ~ 18:00</small></dd></div>'
             '<div class="tvhc-chi"><dt>이메일</dt><dd>notice@trevity.com'
             '<small>주말·공휴일 제외</small></dd></div>'
             '<div class="tvhc-chi"><dt>온라인</dt><dd>제휴 문의'
             '<small>하루 안에 담당자가 연락드립니다</small></dd></div></dl>')
    o.append('<a class="tvhc-cta" href="./inquiry.html">제휴 문의하기</a>')
    o.append('</div></section>')

    o.append('</div>')
    return '\n'.join(o)


def main():
    shell = io.open(SHELL, encoding='utf-8').read()
    m_head = re.search(r'</header>', shell)
    m_foot = re.search(r'<footer\b', shell)
    if not m_head or not m_foot:
        print('ABORT: 셸 경계를 못 찾음'); return 1

    pre = shell[:m_head.end()]
    post = shell[m_foot.start():]

    # 타이틀 교체
    pre, n = re.subn(r'<title>[^<]*</title>', '<title>공식대행사 | 트래비티</title>', pre, count=1)
    print('title 교체: %d' % n)

    out = pre + '\n' + build_body() + '\n' + post
    if os.path.exists(OUT):
        shutil.copy2(OUT, OUT + '.bak_agency')
    io.open(OUT, 'w', encoding='utf-8').write(out)
    print('생성: %s (%d chars)' % (OUT, len(out)))

    # 전 페이지 링크 재연결
    print()
    print('=== ./help.html#agency -> ./agency.html ===')
    cnt = 0
    for f in sorted(x for x in glob.glob('*.html') if not x.startswith('_')):
        s = io.open(f, encoding='utf-8').read()
        if './help.html#agency' not in s:
            continue
        n = s.count('./help.html#agency')
        s = s.replace('./help.html#agency', './agency.html')
        shutil.copy2(f, f + '.bak_agency')
        io.open(f, 'w', encoding='utf-8').write(s)
        print('  %-22s %d개 치환' % (f, n))
        cnt += 1
    print('총 %d개 파일' % cnt)

    # 잔여 확인
    left = []
    for f in sorted(x for x in glob.glob('*.html') if not x.startswith('_')):
        s = io.open(f, encoding='utf-8').read()
        if '#agency' in s:
            left.append(f)
    print('잔여 #agency 참조: %s' % (left if left else '없음'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
