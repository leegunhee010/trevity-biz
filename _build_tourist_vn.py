# -*- coding: utf-8 -*-
# vietnam-tiktok.html -> tourist-vn.html (베트남인 관광객·유학생 체험단 랜딩)
import re
s = open('vietnam-tiktok.html', encoding='utf-8').read()

# ---------- head ----------
s = s.replace('<title>트래비티 | 베트남 틱톡 인플루언서 대량 부킹</title>',
              '<title>트래비티 | 베트남인 관광객·유학생 체험단</title>')
s = re.sub(r'(<meta name="description" content=")[^"]*(")',
           r'\g<1>한국에 있는 베트남인 관광객·유학생 인플루언서가 매장을 직접 체험하고 베트남 SNS에 알립니다. 베트남 여행자가 검색하면 우리 매장이 나오게. 무료 상담.\g<2>', s, count=1)

# ---------- 추천 스트립 ----------
s = s.replace('<li>베트남 쇼피·틱톡샵에 입점하신 분</li>', '<li>관광 상권에서 매장을 운영하시는 분</li>')
s = s.replace('<li>틱톡샵 어필리에이트 신청자가 없는 분</li>', '<li>베트남 손님을 늘리고 싶은 분</li>')
s = s.replace('<li>팔로워 1,000명대 시딩만 반복 중인 분</li>', '<li>베트남 SNS에 매장 후기가 하나도 없는 분</li>')
s = s.replace('<li>베트남 인플루언서 섭외가 막막한 분</li>', '<li>외국인 체험단 모집이 막막한 분</li>')

# ---------- 히어로 ----------
s = s.replace('<h1 class="tvhero2-tit">Vietnam TikTok KOL</h1>', '<h1 class="tvhero2-tit">Vietnam Visitors</h1>')
s = s.replace('베트남에 제품은 올려두셨는데, 인플루언서 마케팅은 쉽지 않으셨죠?',
              '한국에서 매장을 운영하시는데, 베트남 손님 잡기가 쉽지 않으셨죠?')
s = s.replace('검증된 10만~50만 인플루언서를 1명당 20만원 균일가로, 트래비티가 대신 부킹해 드립니다.',
              '한국에 와 있는 베트남인 관광객·유학생 인플루언서가 매장을 직접 체험하고, 베트남 SNS에 알립니다.')

# ---------- 서비스 소개 (tvsvc) ----------
s = s.replace('<h2 class="tvsvc-h2">베트남 인플루언서<br>제품 체험단</h2>',
              '<h2 class="tvsvc-h2">베트남인 관광객·유학생<br>매장 체험단</h2>')
s = s.replace('제품은 이미 베트남에 올라가 있습니다. 이제 팔아 줄 사람을 붙일 차례입니다.<br>섭외도, 소통도, 검수도 — 현지의 트래비티 팀이 처음부터 끝까지 대신합니다.',
              '손님이 찾아오길 기다리지 않아도 됩니다. 한국에 와 있는 베트남 인플루언서가 매장을 직접 찾아가고,<br>모집도, 소통도, 검수도 — 트래비티 팀이 처음부터 끝까지 대신합니다.')
# zig1
s = s.replace('<span class="ab-zlabel">베트남 현지 완결 네트워크</span>', '<span class="ab-zlabel">방한 베트남인 네트워크</span>')
s = s.replace('<h3>섭외부터 검수까지,<br>호치민 현지팀이 직접 움직입니다</h3>',
              '<h3>관광객부터 유학생까지,<br>한국 안에서 바로 움직입니다</h3>')
s = s.replace('메일만 주고받는 대행이 아닙니다. 호치민에 상주하는 로컬 마케터가 인플루언서를 직접 만나고, 가이드를 전하고, 콘텐츠를 검수합니다.<br>언어와 정서의 벽은 트래비티가 대신 넘겠습니다.',
              '베트남에서 섭외해 데려오는 게 아닙니다. 이미 한국에 와 있는 베트남인 관광객·유학생 인플루언서가 매장을 방문하고, 틱톡·페이스북에 후기를 올립니다.<br>모집과 소통은 베트남어가 되는 트래비티 팀이 직접 합니다.')
# zig2 mockup header + rows
s = s.replace('인플루언서 매칭 리포트 · 뷰티 세럼', '체험단 매칭 리포트 · 홍대 음식점')
s = s.replace('<span class="mt-in">뷰티 리뷰 · 연관성 96%</span>', '<span class="mt-in">서울 유학생 · 맛집 리뷰 96%</span>')
s = s.replace('<span class="mt-in">스킨케어 · 연관성 91%</span>', '<span class="mt-in">방한 여행 브이로그 · 91%</span>')
s = s.replace('<span class="mt-in">댄스 · 카테고리 불일치</span>', '<span class="mt-in">체류 일정 불일치</span>')
s = s.replace('<span class="mt-in">일상 · 팔로워 구간 미달</span>', '<span class="mt-in">팔로워 구간 미달</span>')
s = s.replace('10만 풀에서 제품과 맞는 계정만 남깁니다', '10만 풀에서 매장과 맞는 계정만 남깁니다')
s = s.replace('<h3>팔로워 수가 아니라,<br>제품과의 연관성으로 고릅니다</h3>',
              '<h3>아무나 부르지 않고,<br>매장과 맞는 계정만 고릅니다</h3>')
s = s.replace('10만 명의 풀에서 아무나 뽑지 않습니다. 카테고리 연관성, 오디언스 반응, 톤앤매너까지 확인해 제품과 맞는 계정만 남깁니다.<br>뷰티 제품이라면, 뷰티를 다뤄 온 인플루언서에게만 맡깁니다.',
              '10만 명의 풀에서 팔로워, 콘텐츠 이력, 오디언스 반응까지 확인해 매장과 맞는 계정만 남깁니다.<br>맛집이라면 맛집 리뷰를, 뷰티샵이라면 뷰티 콘텐츠를 다뤄 온 계정에게만 맡깁니다.')
# zig3: 가격 -> 검색 노출
s = s.replace('<span class="ab-zlabel">명확한 가격</span>', '<span class="ab-zlabel">모국 SNS 노출</span>')
s = s.replace('<h3>10만이든 50만이든,<br>1명당 20만원 균일가</h3>',
              '<h3>베트남 여행자가 검색하면,<br>우리 매장이 나옵니다</h3>')
s = s.replace('협상도, 숨은 비용도 없습니다. 누구를 골라도 같은 가격이라 예산이 흔들리지 않습니다.<br>체험단으로 끝내지 않고, 틱톡샵 제휴 판매 설계까지 함께 갑니다.',
              '한국 여행을 준비하는 베트남 사람들은 자국 SNS에서 먼저 검색합니다.<br>체험단 후기가 쌓이면, 같은 나라 여행자가 검색했을 때 우리 매장이 먼저 보입니다.')
# zig3 visual: price card -> search result mockup
price_card = re.search(r'<div class="vbox pink"><div class="ab-price">.*?</div></div></div>', s, re.S)
assert price_card
search_mock = ('<div class="vbox pink"><div class="mt-head"><span class="tt">틱톡 검색 · 베트남</span><span class="bd">예시 화면</span></div>'
 '<div style="display:flex;align-items:center;gap:10px;background:#f6f6f8;border-radius:12px;padding:12px 16px;font-size:15px;color:#3c3c43;font-weight:600">🔍 quán ngon Seoul <span style="color:#9a9aa2;font-weight:500">(서울 맛집)</span></div>'
 '<div style="display:flex;gap:10px;margin-top:14px">'
 '<div style="flex:1;border-radius:12px;background:linear-gradient(160deg,#ffe3ea,#ffd0da);height:110px;position:relative"><span style="position:absolute;left:8px;bottom:8px;font-size:12px;font-weight:700;color:#e14e6c;background:#ffffffd9;border-radius:6px;padding:2px 8px">우리 매장 후기</span><span style="position:absolute;right:8px;top:8px;font-size:12px;font-weight:700;color:#fff;background:#fa6781;border-radius:6px;padding:2px 8px">조회 21만</span></div>'
 '<div style="flex:1;border-radius:12px;background:linear-gradient(160deg,#ffe9ef,#ffdbe3);height:110px;position:relative"><span style="position:absolute;left:8px;bottom:8px;font-size:12px;font-weight:700;color:#e14e6c;background:#ffffffd9;border-radius:6px;padding:2px 8px">우리 매장 후기</span><span style="position:absolute;right:8px;top:8px;font-size:12px;font-weight:700;color:#fff;background:#fa6781;border-radius:6px;padding:2px 8px">조회 9.8만</span></div>'
 '<div style="flex:1;border-radius:12px;background:linear-gradient(160deg,#eceef2,#dfe2e8);height:110px;position:relative"><span style="position:absolute;left:8px;bottom:8px;font-size:12px;font-weight:700;color:#70707a;background:#ffffffd9;border-radius:6px;padding:2px 8px">다른 영상</span></div>'
 '</div>'
 '<p style="margin:14px 0 0;font-size:12.5px;color:#8c8c8c;text-align:center">체험단 후기가 검색 결과 상단에 쌓입니다</p></div>')
s = s[:price_card.start()] + search_mock + '</div>' + s[price_card.end():]

# ---------- 페인포인트 마퀴 ----------
s = s.replace("베트남 진출 브랜드를 위한 <span class=\"gra\">'틱톡 인플루언서 마케팅'</span><br>혼자 진행하려니 힘들지 않았나요?",
              "한국 매장을 위한 <span class=\"gra\">'베트남 손님 마케팅'</span><br>혼자 해보려니 막막하지 않았나요?")
s = s.replace('<strong>“베트남 인플루언서 제품 체험단”</strong> 이런 분들이 찾고 계세요!',
              '<strong>“베트남인 관광객·유학생 체험단”</strong> 이런 분들이 찾고 계세요!')
cards_old = [
    ('pp1', '쇼피·틱톡샵에 올려는 뒀는데 <strong>어필리에이트를 아무도 가져가지 않아요</strong>'),
    ('pp2', '커미션을 높여 걸어둬도 <strong>신규 상품이라 담아 주질 않아요</strong>'),
    ('pp3', '팔로워 1,000명대 시딩만 반복하다 <strong>재고만 줄어들었어요</strong>'),
    ('pp4', '인플루언서에게 직접 DM을 보내도 <strong>답장은 절반도 오지 않아요</strong>'),
    ('pp5', '외국 브랜드에는 <strong>단가가 부르는 게 값이에요</strong>'),
]
cards_new = [
    ('pain-vn/tp1', '베트남 여행자가 검색해도 <strong>우리 매장은 나오지 않아요</strong>'),
    ('pain-vn/tp2', '번역기로 베트남어 게시물을 올려봐도 <strong>반응이 없어요</strong>'),
    ('pain-vn/tp3', '한국 리뷰는 많은데 <strong>베트남 SNS엔 후기가 하나도 없어요</strong>'),
    ('pain-vn/tp4', '체험단을 모집해 보려 해도 <strong>연락할 방법이 없어요</strong>'),
    ('pain-vn/tp5', '틱톡인지 페이스북인지 <strong>어디에 알려야 할지 모르겠어요</strong>'),
]
old_html = ''.join(f'<div class="tvpain-card"><img src="./assets/pain/{n}.jpg" alt=""/><p>{t}</p></div>' for n,t in cards_old)
new_html = ''.join(f'<div class="tvpain-card"><img src="./assets/{n}.jpg" alt=""/><p>{t}</p></div>' for n,t in cards_new)
assert s.count('<div class="tvpain-mq">' + old_html*4 + '</div>') == 1
s = s.replace('<div class="tvpain-mq">' + old_html*4 + '</div>', '<div class="tvpain-mq">' + new_html*4 + '</div>')

# ---------- 비교 섹션 ----------
s = s.replace('직접 섭외 vs 트래비티,', '직접 모집 vs 트래비티,')
s = s.replace('같은 50명을 부킹한다면', '같은 체험단을 모은다면')
s = s.replace('직접 섭외하면', '직접 모집하면')
s = s.replace('10만+ 풀에서 제품에 맞는 인플루언서만 추천', '10만+ 풀에서 매장에 맞는 체험단만 추천')
s = s.replace('협상 없이, 누구든 1명당 20만원 균일가', '목적과 규모에 맞춘 명확한 견적 제안')
s = s.replace('현지 마케터가 가이드 전달부터 검수까지 직접', '베트남어 되는 마케터가 가이드 전달부터 검수까지 직접')
s = s.replace('의뢰서 한 장으로 최대 50명까지 부킹 완료', '문의 한 번으로 모집부터 후기까지 완료')
s = s.replace('그 수고를 전부 더해도,<br>1명당 20만원 균일가보다 비쌉니다.', '그 수고를 전부,<br>트래비티가 대신합니다.')
s = s.replace('그 수고를 전부 더해도, 1명당 20만원 균일가보다 비쌉니다.', '그 수고를 전부, 트래비티가 대신합니다.')

# ---------- 패키지 섹션 삭제 (고정가 없음) ----------
k = s.find('id="packages"')
if k > 0:
    sec_start = s.rfind('<section', 0, k)
    sec_end = s.find('</section>', k) + len('</section>')
    s = s[:sec_start] + s[sec_end:]
    print('packages section removed')

# ---------- FAQ ----------
faq = [
    ('Q. 팔로워 10만~50만인데 정말 1명당 20만원인가요?', 'Q. 체험단은 어떤 사람들인가요?'),
    ('A. 팔로워 10만~50만 구간이라면 규모와 관계없이 1명당 20만원 균일가입니다(부가세 별도). 오랜 기간 쌓아온 10만 명 이상의 현지 인플루언서 풀과 직접 컨택 구조이기에 가능한 가격입니다.',
     'A. 한국에 체류 중인 베트남인 관광객과 유학생 가운데, 팔로워 규모와 콘텐츠 이력이 검증된 계정만 선별합니다. 매장 방문이 가능한 일정과 지역까지 확인한 뒤 확정합니다.'),
    ('Q. 일반 체험단 시딩과는 뭐가 다른가요?', 'Q. 후기는 어떤 채널에 올라가나요?'),
    ('A. 팔로워 1,000명대 시딩은 누구나 틱톡에서 직접 할 수 있고, 실제 판매로 이어지기 어렵습니다. 트래비티는 팔로워 10만~50만의 검증된 인플루언서만 부킹하며, 팔로워 수가 아니라 제품과의 연관성, 오디언스 반응까지 확인하고 섭외합니다.',
     'A. 베트남인이 가장 많이 쓰는 틱톡과 페이스북이 중심입니다. 계정 성격과 매장 특성에 따라 인스타그램을 병행하기도 합니다. 모두 베트남어 콘텐츠로 올라가, 현지 여행 준비자에게 직접 닿습니다.'),
    ('Q. 직접 섭외하는 것보다 나은 점이 뭔가요?', 'Q. 비용은 어떻게 되나요?'),
    ('A. 직접 섭외는 컨택·단가 협상·가이드라인 전달·일정 컨트롤을 전부 브랜드가 감당해야 하고, 현지 언어·정서 차이로 단가도 올라갑니다. 트래비티는 베트남 현지 로컬 콘텐츠 마케터가 섭외부터 가이드·검수까지 직접 진행하기 때문에 직접 하는 것보다 싸고 확실합니다.',
     'A. 매장 상황과 목표 규모에 따라 인원과 채널을 설계해 명확한 견적으로 제안드립니다. 상담과 견적 제안은 무료이며, 숨은 비용 없이 확정된 금액으로만 진행합니다.'),
    ('Q. 틱톡샵 제휴 판매 연계도 가능한가요?', 'Q. 어떤 업종이든 가능한가요?'),
    ('A. 가능합니다. 틱톡샵 제휴(어필리에이트) 연결부터 판매 설계까지 캠페인 목적에 맞게 함께 준비해 드립니다. 제품 통관·현지 배송 관련 사항은 상담 시 함께 안내드립니다.',
     'A. 음식점·카페·뷰티샵·쇼핑·체험 시설 등 외국인 손님이 방문할 수 있는 매장이라면 진행 가능합니다. 상권과 업종에 맞춰 어울리는 체험단을 매칭해 드립니다.'),
]
for old, new in faq:
    if s.count(old) == 0:
        print('!! FAQ not found:', old[:30])
    s = s.replace(old, new)

# ---------- 최종 CTA ----------
s = s.replace('소중한 제품, 이제 검증된 인플루언서에게 맡겨보세요', '소중한 매장, 이제 베트남 손님에게 알려보세요')
s = s.replace('부킹으로 끝나지 않습니다.', '방문 체험으로 끝나지 않습니다.')
s = s.replace('틱톡샵 제휴 판매 설계까지 함께 해드립니다.', '검색하면 나오는 매장이 될 때까지 함께 해드립니다.')

# ---------- 내비 active ----------
s = s.replace('<li class="on"><a href="./vietnam-tiktok.html">한국제품 해외수출 마케팅</a>', '<li><a href="./vietnam-tiktok.html">한국제품 해외수출 마케팅</a>')
s = s.replace('<li><a href="./tourist.html#vn">외국인 관광객 마케팅</a>', '<li class="on"><a href="./tourist.html#vn">외국인 관광객 마케팅</a>')

open('tourist-vn.html', 'w', encoding='utf-8').write(s)
print('tourist-vn.html written, size', len(s))
