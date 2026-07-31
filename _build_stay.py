# -*- coding: utf-8 -*-
# tourist-vn.html -> stay.html (숙박 체험단 — 업주 0원 모델). 구 stay.html은 백업.
import re, shutil
shutil.copy('stay.html', '_bak_stay_services.html')
s = open('tourist-vn.html', encoding='utf-8').read()

# ---- head ----
s = s.replace('<title>트래비티 | 베트남인 관광객·유학생 체험단</title>', '<title>트래비티 | 숙박 체험단 — 대행비 0원</title>')
s = re.sub(r'(<meta name="description" content=")[^"]*(")',
           r'\g<1>호텔·펜션 사장님은 0원. 빈 객실 하루만 내어주시면 검증된 블로거 체험단이 후기를 쌓아 드립니다. 광고비도, 대행비도 없습니다.\g<2>', s, count=1)
s = s.replace('content="트래비티 | 베트남인 관광객·유학생 체험단"', 'content="트래비티 | 숙박 체험단 — 대행비 0원"')

# ---- 추천 스트립 ----
s = s.replace('<li>관광 상권에서 매장을 운영하시는 분</li>', '<li>호텔·펜션·풀빌라 운영하시는 분</li>')
s = s.replace('<li>베트남 손님을 늘리고 싶은 분</li>', '<li>주중 공실이 고민인 분</li>')
s = s.replace('<li>베트남 SNS에 매장 후기가 하나도 없는 분</li>', '<li>네이버에 우리 숙소 후기가 없는 분</li>')
s = s.replace('<li>외국인 체험단 모집이 막막한 분</li>', '<li>광고비 지출이 부담스러운 분</li>')

# ---- 히어로 ----
s = s.replace('<h1 class="tvhero2-tit">Vietnam Visitors</h1>', '<h1 class="tvhero2-tit">Stay Review</h1>')
s = s.replace('한국에서 매장을 운영하시는데, 베트남 손님 잡기가 쉽지 않으셨죠?',
              '빈 객실은 그대로 비용인데, 홍보에 돈 쓰기는 아까우셨죠?')
s = s.replace('한국에 와 있는 베트남인 관광객·유학생 인플루언서가 매장을 직접 체험하고, 베트남 SNS에 알립니다.',
              '대행비 0원 — 객실 하루만 내어주시면, 검증된 블로거 체험단이 후기를 쌓아 드립니다.')

# ---- WHY 섹션: 왜 0원인가 ----
s = s.replace('<span class="tvwhy-label">WHY VIETNAM</span>', '<span class="tvwhy-label">WHY FREE</span>')
s = s.replace('왜 지금,<br>베트남 손님일까요?', '사장님은 0원,<br>어떻게 가능할까요?')
s = s.replace('감이 아니라 숫자입니다. 베트남은 이미 한국에서 가장 큰 외국인 손님 시장이 됐습니다.',
              '트래비티는 체험단 운영에서 수익을 얻는 구조입니다. 그래서 사장님께는 비용을 받지 않습니다.')
# card1
s = s.replace('>550,000+<', '>0원<')
s = s.replace('연간 방한 베트남인', '광고비 · 대행비')
s = s.replace('한 해 55만 명이 한국을 찾고, 해마다 늘고 있습니다', '사장님이 내시는 현금 비용은 없습니다. 정말 0원입니다')
s = s.replace('<p class="tvwhy-src">한국관광공사 · 2025</p>', '<p class="tvwhy-src">트래비티 숙박 체험단</p>')
# card2
s = s.replace('>338,557<', '>1박<')
s = s.replace('국내 체류 베트남인', '사장님이 준비할 것')
s = s.replace('미국·일본보다 많은 체류 외국인 2위 규모입니다', '비어 있는 객실 하루가 전부입니다. 주중·비수기 위주로 조율합니다')
s = s.replace('<p class="tvwhy-src">법무부 출입국 통계 · 2025.7</p>', '<p class="tvwhy-src">일정은 사장님이 정합니다</p>')
# card3
s = s.replace('>107,807<', '>영구<')
s = s.replace('베트남인 유학생', '후기가 남는 기간')
s = s.replace('국내 유학생 3명 중 1명이 베트남 학생, 압도적 1위입니다', '광고는 끄면 사라지지만, 블로그 후기는 검색에 계속 남습니다')
s = s.replace('<p class="tvwhy-src">교육부 · 2025.8</p>', '<p class="tvwhy-src">네이버 검색 노출</p>')
# card4
s = s.replace('외국인 입국자 국가', '내국인 + 외국인')
s = s.replace('<p class="tvwhy-num">1위</p>', '<p class="tvwhy-num">둘 다</p>')
s = s.replace('25년 만에 중국을 제치고 베트남이 입국자 1위에 올랐습니다', '네이버 블로거부터 외국인 인플루언서까지 함께 설계합니다')
s = s.replace('<p class="tvwhy-src">출입국 통계 · 2026</p>', '<p class="tvwhy-src">숙소 상황에 맞춰 제안</p>')
# punch
s = s.replace('베트남 손님은 이미 한국에 와 있습니다.<br>이제 <b>내 매장이 보이게 만들</b> 차례입니다.',
              '비어 있던 객실 하루가,<br><b>검색에 평생 남는 후기</b>로 바뀝니다.')

# ---- tvsvc 지그재그 3종 교체 ----
i = s.find('<section class="tvsvc">')
j = s.find('</section>', i) + len('</section>')
old_sec = s[i:j]
m = re.search(r'<style>.*?</style>', old_sec, re.S)
style = m.group(0)
reveal = 'style="opacity: 0; transform: translateY(40px); transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;"'

mock_cost = ('<div class="vbox pink"><div class="ab-price">'
 '<div class="row"><span class="nm">포털 키워드 광고</span><span class="pr" style="color:#9e9e9e">월 50만원~</span></div>'
 '<div class="row"><span class="nm">인플루언서 직접 섭외</span><span class="pr" style="color:#9e9e9e">건당 15만원~</span></div>'
 '<div class="row"><span class="nm">트래비티 숙박 체험단</span><span class="pr">0원 + 객실 1박</span></div>'
 '<p class="cap">광고비 · 대행비 · 원고료 전부 없음</p></div></div>')

mock_match = ('<div class="vbox"><div class="mt-head"><span class="tt">체험단 매칭 리포트 · 가평 풀빌라</span><span class="bd">예시 화면</span></div>'
 '<div class="mt-row"><span class="mt-av" style="background:linear-gradient(135deg,#fa6781,#ff9db0)">J</span><div class="mt-mid"><div class="mt-top"><span class="mt-nm">여행에미치다_J</span><span class="mt-fl">일 방문 5,200</span></div><div class="mt-bar"><i style="width:95%"></i></div><span class="mt-in">숙소 리뷰 전문 · 상위노출 이력</span></div><span class="mt-tag mt-ok">추천</span></div>'
 '<div class="mt-row"><span class="mt-av" style="background:linear-gradient(135deg,#ff8fa5,#ffc2cd)">S</span><div class="mt-mid"><div class="mt-top"><span class="mt-nm">주말엔_캠핑</span><span class="mt-fl">일 방문 3,800</span></div><div class="mt-bar"><i style="width:90%"></i></div><span class="mt-in">가족 여행 · 펜션 리뷰 다수</span></div><span class="mt-tag mt-ok">추천</span></div>'
 '<div class="mt-row"><span class="mt-av" style="background:#d9d9de">D</span><div class="mt-mid"><div class="mt-top"><span class="mt-nm">일상다반사_D</span><span class="mt-fl">일 방문 240</span></div><div class="mt-bar low"><i style="width:12%"></i></div><span class="mt-in">방문자 기준 미달</span></div><span class="mt-tag mt-no">제외</span></div>'
 '<div class="mt-row"><span class="mt-av" style="background:#d9d9de">B</span><div class="mt-mid"><div class="mt-top"><span class="mt-nm">맛집만_다녀요</span><span class="mt-fl">일 방문 4,100</span></div><div class="mt-bar low"><i style="width:20%"></i></div><span class="mt-in">숙소 콘텐츠 이력 없음</span></div><span class="mt-tag mt-no">제외</span></div>'
 '<p class="mt-cap">방문자 수 · 블로그 지수 · 콘텐츠 이력까지 확인합니다</p></div>')

mock_search = ('<div class="vbox"><div class="mt-head"><span class="tt">네이버 검색</span><span class="bd">예시 화면</span></div>'
 '<div style="display:flex;align-items:center;gap:10px;background:#f6f6f8;border-radius:12px;padding:12px 16px;font-size:15px;color:#3c3c43;font-weight:600">🔍 가평 풀빌라 후기</div>'
 '<div style="display:flex;flex-direction:column;gap:10px;margin-top:14px">'
 '<div style="background:#fff2f5;border-radius:12px;padding:13px 16px"><div style="font-size:14.5px;font-weight:800;color:#26262b">수영장 뷰가 미쳤다… 가평 풀빌라 1박 후기 🏊</div><div style="font-size:12.5px;color:#8b8b92;margin-top:4px">블로그 · 체험단 리뷰 · <span style="color:#fa6781;font-weight:700">우리 숙소</span></div></div>'
 '<div style="background:#fff2f5;border-radius:12px;padding:13px 16px"><div style="font-size:14.5px;font-weight:800;color:#26262b">아이랑 가평 여행, 숙소는 여기로 정착</div><div style="font-size:12.5px;color:#8b8b92;margin-top:4px">블로그 · 체험단 리뷰 · <span style="color:#fa6781;font-weight:700">우리 숙소</span></div></div>'
 '</div><p style="margin:14px 0 0;font-size:12.5px;color:#8c8c8c;text-align:center">예약 전 검색하는 손님에게 우리 숙소가 먼저 보입니다</p></div>')

sec = ('<section class="tvsvc">' + style
 + '<div class="tvsvc-wrap"><div class="tvsvc-head" ' + reveal + '>'
 + '<span class="tvsvc-label">TREVITY STAY</span><h2 class="tvsvc-h2">호텔 · 펜션<br>숙박 체험단</h2>'
 + '<p class="tvsvc-sub">비어 있는 객실 하루를 내어주시면, 검증된 블로거가 하루 머물고 후기를 남깁니다.<br>모집도, 선별도, 검수도 — 트래비티가 처음부터 끝까지 대신합니다.</p></div>'
 + '<div style="display:flex;flex-direction:column;gap:120px">'
 + '<div class="ab-zig" ' + reveal + '><div class="t"><span class="ab-zlabel">비용 구조</span>'
 + '<h3>사장님은 0원,<br>객실 하루가 전부입니다</h3>'
 + '<p>광고비도, 대행비도, 원고료도 받지 않습니다. 트래비티는 체험단 운영에서 수익을 얻는 구조라 사장님께는 비용을 청구하지 않습니다.<br>비어 있던 주중 객실이 그대로 마케팅이 됩니다.</p></div>'
 + '<div class="v">' + mock_cost + '</div></div>'
 + '<div class="ab-zig" ' + reveal + '><div class="v">' + mock_match + '</div>'
 + '<div class="t"><span class="ab-zlabel">검증된 체험단</span>'
 + '<h3>아무나 보내지 않고,<br>검색에 남는 계정만 보냅니다</h3>'
 + '<p>일 방문자 수, 블로그 지수, 숙소 콘텐츠 이력까지 확인한 블로거만 선별해 보냅니다.<br>외국인 관광객을 받는 숙소라면, 외국인 인플루언서 체험단도 함께 설계해 드립니다.</p></div></div>'
 + '<div class="ab-zig" ' + reveal + '><div class="t"><span class="ab-zlabel">검색 노출</span>'
 + '<h3>손님이 검색하면,<br>우리 숙소가 나옵니다</h3>'
 + '<p>숙소를 고르는 손님은 예약 전에 네이버부터 검색합니다. "지역명 + 후기"에 우리 숙소 글이 쌓이면, 검색이 곧 예약으로 이어집니다.<br>광고와 달리, 한 번 쌓인 후기는 사라지지 않습니다.</p></div>'
 + '<div class="v">' + mock_search + '</div></div>'
 + '</div></div></section>')
s = s[:i] + sec + s[j:]

# ---- 페인포인트 ----
s = s.replace("한국 매장을 위한 <span class=\"gra\">'베트남 손님 마케팅'</span><br>혼자 해보려니 막막하지 않았나요?",
              "숙소 사장님을 위한 <span class=\"gra\">'0원 후기 마케팅'</span><br>광고만으로는 힘들지 않으셨나요?")
s = s.replace('<strong>“베트남인 관광객·유학생 체험단”</strong> 이런 분들이 찾고 계세요!',
              '<strong>“숙박 체험단”</strong> 이런 분들이 찾고 계세요!')
s = s.replace('./assets/pain-vn/tp1.jpg', './assets/pain-stay/st1.jpg')
s = s.replace('./assets/pain-vn/tp2.jpg', './assets/pain-stay/st2.jpg')
s = s.replace('./assets/pain-vn/tp3.jpg', './assets/pain-stay/st3.jpg')
s = s.replace('./assets/pain-vn/tp4.jpg', './assets/pain-stay/st4.jpg')
s = s.replace('./assets/pain-vn/tp5.jpg', './assets/pain-stay/st5.jpg')
s = s.replace('베트남 여행자가 검색해도 <strong>우리 매장은 나오지 않아요</strong>', '후기를 검색하면 <strong>경쟁 숙소만 나와요</strong>')
s = s.replace('번역기로 베트남어 게시물을 올려봐도 <strong>반응이 없어요</strong>', '광고비는 쓰는 만큼만 나오고 <strong>끄면 사라져요</strong>')
s = s.replace('한국 리뷰는 많은데 <strong>베트남 SNS엔 후기가 하나도 없어요</strong>', '주중 공실은 <strong>그대로 고정비 손실이에요</strong>')
s = s.replace('체험단을 모집해 보려 해도 <strong>연락할 방법이 없어요</strong>', '블로거한테 직접 연락하면 <strong>원고료부터 달라고 해요</strong>')
s = s.replace('틱톡인지 페이스북인지 <strong>어디에 알려야 할지 모르겠어요</strong>', '네이버인지 인스타인지 <strong>어디에 알려야 할지 모르겠어요</strong>')

# ---- 비교 섹션 ----
s = s.replace('직접 모집 vs 트래비티,', '직접 섭외 vs 트래비티,')
s = s.replace('같은 체험단을 모은다면', '같은 블로거 체험단이라면')
s = s.replace('직접 모집하면', '직접 섭외하면')
s = s.replace('검증된 풀에서 매장에 맞는 체험단만 추천', '검증된 풀에서 숙소에 맞는 블로거만 추천')
s = s.replace('목적과 규모에 맞춘 명확한 견적 제안', '광고비 · 대행비 · 원고료 전부 0원')
s = s.replace('베트남어 되는 마케터가 가이드 전달부터 검수까지 직접', '전담 마케터가 가이드 전달부터 원고 검수까지 직접')
s = s.replace('문의 한 번으로 모집부터 후기까지 완료', '문의 한 번으로 모집부터 후기 업로드까지 완료')
s = s.replace('그 수고를 전부,<br class="mn:hidden"> <span style="color:#fa6781">트래비티가 대신</span>합니다.',
              '그 수고를 전부 덜어드리는데,<br class="mn:hidden"> 사장님은 <span style="color:#fa6781">0원</span>입니다.')

# ---- FAQ ----
s = s.replace('Q. 어떤 손님을 데려올 수 있나요?', 'Q. 어떤 손님을 데려올 수 있나요?')  # (vn파일 기준 원문 유지용 no-op)
s = s.replace('Q. 체험단은 어떤 사람들인가요?', 'Q. 정말 0원인가요? 어떻게 가능한가요?')
s = s.replace('한국에 체류 중인 베트남인 관광객과 유학생 가운데, 팔로워 규모와 콘텐츠 이력이 검증된 계정만 선별합니다. 매장 방문이 가능한 일정과 지역까지 확인한 뒤 확정합니다.',
              '네, 사장님이 내시는 현금 비용은 없습니다. 트래비티는 체험단 운영 과정에서 수익을 얻는 구조라, 사장님께는 객실 1박 제공 외에 어떤 비용도 청구하지 않습니다.')
s = s.replace('Q. 후기는 어떤 채널에 올라가나요?', 'Q. 어떤 블로거가 오나요?')
s = s.replace('베트남인이 가장 많이 쓰는 틱톡과 페이스북이 중심입니다. 계정 성격과 매장 특성에 따라 인스타그램을 병행하기도 합니다. 모두 베트남어 콘텐츠로 올라가, 한국 여행을 준비하는 현지 사람들에게 직접 닿습니다.',
              '일 방문자 수, 블로그 지수, 숙소 리뷰 이력까지 확인해 검색 상위노출이 가능한 블로거만 선별합니다. 외국인 관광객을 받는 숙소라면 외국인 인플루언서 체험단도 함께 제안드립니다.')
s = s.replace('Q. 비용은 어떻게 되나요?', 'Q. 일정은 어떻게 정하나요?')
s = s.replace('매장 상황과 목표 규모에 따라 인원과 채널을 설계해 명확한 견적으로 제안드립니다. 상담과 견적 제안은 무료이며, 숨은 비용 없이 확정된 금액으로만 진행합니다.',
              '사장님이 정하시는 대로 갑니다. 예약이 비는 주중·비수기 위주로 일정을 조율해, 어차피 비어 있을 객실만 활용하도록 설계합니다. 성수기·주말은 피해 드립니다.')
s = s.replace('Q. 어떤 업종이든 가능한가요?', 'Q. 어떤 숙소든 가능한가요?')
s = s.replace('음식점·카페·뷰티샵·쇼핑·체험 시설 등 외국인 손님이 방문할 수 있는 매장이라면 진행 가능합니다. 상권과 업종에 맞춰 어울리는 체험단을 매칭해 드립니다.',
              '호텔·펜션·풀빌라·게스트하우스·글램핑 등 숙박업이라면 진행 가능합니다. 숙소 성격과 지역에 맞는 블로거를 매칭해 드립니다.')

# ---- CTA ----
s = s.replace('소중한 매장, 이제 베트남 손님에게 알려보세요', '비어 있는 객실, 이제 후기로 바꿔보세요')
s = s.replace('방문 체험으로 끝나지 않습니다.', '후기 한 편으로 끝나지 않습니다.')
s = s.replace('검색하면 나오는 매장이 될 때까지 함께 해드립니다.', '검색하면 나오는 숙소가 될 때까지 함께 해드립니다.')

# ---- 내비 active ----
s = s.replace('<li class="on"><a href="./tourist-vn.html">외국인 관광객 마케팅</a>', '<li><a href="./tourist-vn.html">외국인 관광객 마케팅</a>')
s = s.replace('<li><a href="./stay.html">숙박 체험단</a></li>', '<li class="on"><a href="./stay.html">숙박 체험단</a></li>')

open('stay.html', 'w', encoding='utf-8').write(s)
print('stay.html rebuilt, size', len(s))
