# -*- coding: utf-8 -*-
# tourist-vn.html -> local-vn.html (베트남 현지 매장 마케팅, 타겟 3종)
import re
s = open('tourist-vn.html', encoding='utf-8').read()

# ---- head ----
s = s.replace('<title>트래비티 | 베트남인 관광객·유학생 체험단</title>', '<title>트래비티 | 베트남 현지 매장 마케팅</title>')
s = re.sub(r'(<meta name="description" content=")[^"]*(")',
           r'\g<1>베트남에서 매장을 운영하시나요? 베트남 로컬, 중국인 관광객, 한국인 관광객 — 세 방향의 손님을 트래비티가 데려옵니다. 무료 상담.\g<2>', s, count=1)
s = s.replace('content="트래비티 | 베트남인 관광객·유학생 체험단"', 'content="트래비티 | 베트남 현지 매장 마케팅"')

# ---- 추천 스트립 ----
s = s.replace('<li>관광 상권에서 매장을 운영하시는 분</li>', '<li>베트남에서 매장을 운영하시는 분</li>')
s = s.replace('<li>베트남 손님을 늘리고 싶은 분</li>', '<li>로컬 손님을 늘리고 싶은 분</li>')
s = s.replace('<li>베트남 SNS에 매장 후기가 하나도 없는 분</li>', '<li>중국인·한국인 관광객까지 잡고 싶은 분</li>')
s = s.replace('<li>외국인 체험단 모집이 막막한 분</li>', '<li>현지 마케팅이 막막한 분</li>')

# ---- 히어로 ----
s = s.replace('<h1 class="tvhero2-tit">Vietnam Visitors</h1>', '<h1 class="tvhero2-tit">Vietnam Local</h1>')
s = s.replace('한국에서 매장을 운영하시는데, 베트남 손님 잡기가 쉽지 않으셨죠?',
              '매장은 베트남에 있는데, 손님을 어디서 데려와야 할지 막막하셨죠?')
s = s.replace('한국에 와 있는 베트남인 관광객·유학생 인플루언서가 매장을 직접 체험하고, 베트남 SNS에 알립니다.',
              '베트남 로컬, 중국인 관광객, 한국인 관광객 — 세 방향의 손님을 트래비티가 데려옵니다.')

# ---- WHY 섹션: 베트남 시장 스탯 ----
s = s.replace('왜 지금,<br>베트남 손님일까요?', '베트남 시장,<br>기다리기엔 너무 큽니다')
s = s.replace('감이 아니라 숫자입니다. 베트남은 이미 한국에서 가장 큰 외국인 손님 시장이 됐습니다.',
              '감이 아니라 숫자입니다. 매장 앞을 지나가는 손님만으로는 아까운 시장입니다.')
# card1: 인구
s = s.replace('>550,000+<', '>100,000,000+<')
s = s.replace('연간 방한 베트남인', '베트남 인구')
s = s.replace('한 해 55만 명이 한국을 찾고, 해마다 늘고 있습니다', '인구 1억을 돌파한, 동남아에서 가장 빠르게 크는 소비 시장입니다')
s = s.replace('<p class="tvwhy-src">한국관광공사 · 2025</p>', '<p class="tvwhy-src">베트남 통계총국 · 2023</p>')
# card2: 틱톡 사용자
s = s.replace('>338,557<', '>67,000,000<')
s = s.replace('국내 체류 베트남인', '베트남 틱톡 사용자')
s = s.replace('미국·일본보다 많은 체류 외국인 2위 규모입니다', '베트남 사람들은 갈 곳과 살 것을 틱톡에서 찾습니다')
s = s.replace('<p class="tvwhy-src">법무부 출입국 통계 · 2025.7</p>', '<p class="tvwhy-src">TikTok 광고 데이터 · 2025</p>')
# card3: 광고 도달
s = s.replace('>107,807<', '>40,000,000<')
s = s.replace('베트남인 유학생', '광고 도달 가능 인구')
s = s.replace('국내 유학생 3명 중 1명이 베트남 학생, 압도적 1위입니다', '틱톡 한 채널로만 4,000만 명에게 매장을 알릴 수 있습니다')
s = s.replace('<p class="tvwhy-src">교육부 · 2025.8</p>', '<p class="tvwhy-src">TikTok 광고 데이터 · 2025</p>')
# card4: 동남아 2위
s = s.replace('외국인 입국자 국가', '동남아 틱톡 사용률')
s = s.replace('<p class="tvwhy-num">1위</p>', '<p class="tvwhy-num">2위</p>')
s = s.replace('25년 만에 중국을 제치고 베트남이 입국자 1위에 올랐습니다', '트렌드를 이끄는 세대가 전부 틱톡 위에서 움직입니다')
s = s.replace('<p class="tvwhy-src">출입국 통계 · 2026</p>', '<p class="tvwhy-src">TikTok 광고 데이터 · 2025</p>')
# punch
s = s.replace('베트남 손님은 이미 한국에 와 있습니다.<br>이제 <b>내 매장이 보이게 만들</b> 차례입니다.',
              '손님은 이미 매장 근처에 있습니다.<br>이제 <b>내 매장이 보이게 만들</b> 차례입니다.')

# ---- tvsvc: 타겟 3종 지그재그로 전면 교체 ----
i = s.find('<section class="tvsvc">')
j = s.find('</section>', i) + len('</section>')
old_sec = s[i:j]
# 기존 스타일 블록 재사용을 위해 style 추출
m = re.search(r'<style>.*?</style>', old_sec, re.S)
style = m.group(0)
reveal = 'style="opacity: 0; transform: translateY(40px); transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;"'

mock_local = ('<div class="vbox"><div class="mt-head"><span class="tt">틱톡 검색 · 호치민</span><span class="bd">예시 화면</span></div>'
 '<div style="display:flex;align-items:center;gap:10px;background:#f6f6f8;border-radius:12px;padding:12px 16px;font-size:15px;color:#3c3c43;font-weight:600">🔍 quán ngon gần đây <span style="color:#9a9aa2;font-weight:500">(근처 맛집)</span></div>'
 '<div style="display:flex;gap:10px;margin-top:14px">'
 '<div style="flex:1;border-radius:12px;background:linear-gradient(160deg,#ffe3ea,#ffd0da);height:110px;position:relative"><span style="position:absolute;left:8px;bottom:8px;font-size:12px;font-weight:700;color:#e14e6c;background:#ffffffd9;border-radius:6px;padding:2px 8px">우리 매장 후기</span><span style="position:absolute;right:8px;top:8px;font-size:12px;font-weight:700;color:#fff;background:#fa6781;border-radius:6px;padding:2px 8px">조회 18만</span></div>'
 '<div style="flex:1;border-radius:12px;background:linear-gradient(160deg,#ffe9ef,#ffdbe3);height:110px;position:relative"><span style="position:absolute;left:8px;bottom:8px;font-size:12px;font-weight:700;color:#e14e6c;background:#ffffffd9;border-radius:6px;padding:2px 8px">우리 매장 후기</span><span style="position:absolute;right:8px;top:8px;font-size:12px;font-weight:700;color:#fff;background:#fa6781;border-radius:6px;padding:2px 8px">조회 7.2만</span></div>'
 '<div style="flex:1;border-radius:12px;background:linear-gradient(160deg,#eceef2,#dfe2e8);height:110px;position:relative"><span style="position:absolute;left:8px;bottom:8px;font-size:12px;font-weight:700;color:#70707a;background:#ffffffd9;border-radius:6px;padding:2px 8px">다른 영상</span></div>'
 '</div><p style="margin:14px 0 0;font-size:12.5px;color:#8c8c8c;text-align:center">로컬 인플루언서 후기가 검색 상단에 쌓입니다</p></div>')

mock_cn = ('<div class="vbox"><div class="mt-head"><span class="tt">따중디엔핑 · 매장 페이지</span><span class="bd">예시 화면</span></div>'
 '<div style="display:flex;align-items:center;gap:14px;padding:6px 0 14px;border-bottom:1px solid #f4f4f6">'
 '<div style="width:56px;height:56px;border-radius:12px;background:linear-gradient(135deg,#ffd9e1,#fdb0c0);display:flex;align-items:center;justify-content:center;font-size:26px">🍲</div>'
 '<div><div style="font-size:17px;font-weight:800;color:#26262b">우리 매장 (호치민 7군)</div><div style="font-size:13.5px;color:#8b8b92;margin-top:3px">한식당 · 韩国料理</div></div>'
 '<div style="margin-left:auto;text-align:right"><div style="font-size:24px;font-weight:900;color:#fa6781">★ 4.8</div><div style="font-size:12px;color:#8b8b92">리뷰 214</div></div></div>'
 '<div style="display:flex;flex-direction:column;gap:9px;padding-top:12px">'
 '<div style="display:flex;gap:10px;align-items:center"><span style="width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#fa6781,#ff9db0);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;color:#fff">W</span><span style="font-size:14px;color:#3c3c43">好吃！베트남 여행 중 최고 한식당 <b style="color:#fa6781">★★★★★</b></span></div>'
 '<div style="display:flex;gap:10px;align-items:center"><span style="width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#ff8fa5,#ffc2cd);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;color:#fff">L</span><span style="font-size:14px;color:#3c3c43">더우인 보고 왔어요, 줄 서서 먹는 집 <b style="color:#fa6781">★★★★★</b></span></div>'
 '</div><p style="margin:14px 0 0;font-size:12.5px;color:#8c8c8c;text-align:center">중국 인플루언서 후기 → 디엔핑 별점으로 이어집니다</p></div>')

mock_kr = ('<div class="vbox"><div class="mt-head"><span class="tt">네이버 검색 · 한국</span><span class="bd">예시 화면</span></div>'
 '<div style="display:flex;align-items:center;gap:10px;background:#f6f6f8;border-radius:12px;padding:12px 16px;font-size:15px;color:#3c3c43;font-weight:600">🔍 호치민 맛집</div>'
 '<div style="display:flex;flex-direction:column;gap:10px;margin-top:14px">'
 '<div style="background:#f8f8fa;border-radius:12px;padding:13px 16px"><div style="font-size:14.5px;font-weight:800;color:#26262b">호치민 7군 한식당, 여기 안 가면 후회 🍖</div><div style="font-size:12.5px;color:#8b8b92;margin-top:4px">블로그 · 방문 후기 · <span style="color:#fa6781;font-weight:700">우리 매장</span></div></div>'
 '<div style="background:#f8f8fa;border-radius:12px;padding:13px 16px"><div style="font-size:14.5px;font-weight:800;color:#26262b">호치민 여행 3일차, 숨은 맛집 발견!</div><div style="font-size:12.5px;color:#8b8b92;margin-top:4px">블로그 · 체험단 리뷰 · <span style="color:#fa6781;font-weight:700">우리 매장</span></div></div>'
 '</div><p style="margin:14px 0 0;font-size:12.5px;color:#8c8c8c;text-align:center">한국인 여행자는 네이버에서 검색합니다 — V-마케팅 연계</p></div>')

sec = ('<section class="tvsvc">' + style
 + '<div class="tvsvc-wrap"><div class="tvsvc-head" ' + reveal + '>'
 + '<span class="tvsvc-label">TREVITY SERVICE</span><h2 class="tvsvc-h2">베트남 현지 매장,<br>손님은 세 방향에서 옵니다</h2>'
 + '<p class="tvsvc-sub">로컬 손님도, 베트남에 온 중국인·한국인 관광객도 전부 SNS를 보고 매장을 고릅니다.<br>세 타겟 모두 — 모집도, 소통도, 검수도 트래비티 팀이 처음부터 끝까지 대신합니다.</p></div>'
 + '<div style="display:flex;flex-direction:column;gap:120px">'
 # target 1: local
 + '<div class="ab-zig" id="local" style="scroll-margin-top:90px;opacity: 0; transform: translateY(40px); transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;"><div class="t"><span class="ab-zlabel">타겟 ① 베트남 로컬 손님</span>'
 + '<h3>1억 로컬 시장,<br>틱톡 인플루언서가 엽니다</h3>'
 + '<p>베트남 사람들은 갈 곳을 틱톡에서 찾습니다. 검증된 로컬 인플루언서가 매장을 직접 체험하고 틱톡·페이스북에 올리면, 근처 로컬 손님에게 우리 매장이 먼저 보입니다.<br>섭외부터 검수까지 호치민 현지팀이 직접 움직입니다.</p></div>'
 + '<div class="v">' + mock_local + '</div></div>'
 # target 2: chinese tourists
 + '<div class="ab-zig" id="chinese" style="scroll-margin-top:90px;opacity: 0; transform: translateY(40px); transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;"><div class="v">' + mock_cn + '</div>'
 + '<div class="t"><span class="ab-zlabel">타겟 ② 베트남에 온 중국인 관광객</span>'
 + '<h3>더우인과 디엔핑으로,<br>중국인 관광객을 데려옵니다</h3>'
 + '<p>베트남을 찾는 중국인 관광객은 더우인과 따중디엔핑을 보고 갈 곳을 정합니다. 중국 인플루언서가 매장을 체험하고 후기를 남기면, 별점과 함께 중국인 손님이 이어집니다.<br>중국어 소통도 트래비티가 대신합니다.</p></div></div>'
 # target 3: korean tourists
 + '<div class="ab-zig" id="korean" style="scroll-margin-top:90px;opacity: 0; transform: translateY(40px); transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;"><div class="t"><span class="ab-zlabel">타겟 ③ 베트남에 온 한국인 관광객</span>'
 + '<h3>한국인 여행자는<br>네이버에서 검색합니다</h3>'
 + '<p>"호치민 맛집", "다낭 마사지" — 한국인 관광객은 떠나기 전에 네이버 블로그부터 찾습니다. 체험단 리뷰와 블로그 상위노출로, 여행 계획 단계부터 우리 매장을 심어 둡니다.<br>인스타그램 해시태그 확산까지 함께 설계합니다.</p></div>'
 + '<div class="v">' + mock_kr + '</div></div>'
 + '</div></div></section>')
s = s[:i] + sec + s[j:]

# ---- 페인포인트 ----
s = s.replace("한국 매장을 위한 <span class=\"gra\">'베트남 손님 마케팅'</span><br>혼자 해보려니 막막하지 않았나요?",
              "베트남 매장을 위한 <span class=\"gra\">'현지 손님 마케팅'</span><br>혼자 해보려니 막막하지 않았나요?")
s = s.replace('<strong>“베트남인 관광객·유학생 체험단”</strong> 이런 분들이 찾고 계세요!',
              '<strong>“베트남 현지 매장 마케팅”</strong> 이런 분들이 찾고 계세요!')
s = s.replace('./assets/pain-vn/', './assets/pain-lvn/')
s = s.replace('베트남 여행자가 검색해도 <strong>우리 매장은 나오지 않아요</strong>', '로컬 손님이 검색해도 <strong>우리 매장은 나오지 않아요</strong>')
s = s.replace('한국 리뷰는 많은데 <strong>베트남 SNS엔 후기가 하나도 없어요</strong>', '교민 손님 후기뿐, <strong>로컬 후기는 하나도 없어요</strong>')
s = s.replace('틱톡인지 페이스북인지 <strong>어디에 알려야 할지 모르겠어요</strong>', '틱톡인지 페이스북인지 잘로인지 <strong>어디에 알려야 할지 모르겠어요</strong>')

# ---- FAQ ----
s = s.replace('한국에 체류 중인 베트남인 관광객과 유학생 가운데, 팔로워 규모와 콘텐츠 이력이 검증된 계정만 선별합니다. 매장 방문이 가능한 일정과 지역까지 확인한 뒤 확정합니다.',
              '목적에 따라 다릅니다. 로컬 손님은 베트남 현지 인플루언서, 중국인 관광객은 중국 인플루언서, 한국인 관광객은 네이버 블로그 체험단이 맡습니다. 세 타겟을 함께 진행할 수도 있습니다.')
s = s.replace('Q. 체험단은 어떤 사람들인가요?', 'Q. 어떤 손님을 데려올 수 있나요?')
s = s.replace('Q. 후기는 어떤 채널에 올라가나요?', 'Q. 채널은 어디에 올라가나요?')
s = s.replace('베트남인이 가장 많이 쓰는 틱톡과 페이스북이 중심입니다. 계정 성격과 매장 특성에 따라 인스타그램을 병행하기도 합니다. 모두 베트남어 콘텐츠로 올라가, 한국 여행을 준비하는 현지 사람들에게 직접 닿습니다.',
              '로컬 타겟은 틱톡·페이스북, 중국인 관광객은 더우인·따중디엔핑, 한국인 관광객은 네이버 블로그·인스타그램입니다. 타겟별로 실제 그 손님이 보는 채널에만 올립니다.')
s = s.replace('음식점·카페·뷰티샵·쇼핑·체험 시설 등 외국인 손님이 방문할 수 있는 매장이라면 진행 가능합니다. 상권과 업종에 맞춰 어울리는 체험단을 매칭해 드립니다.',
              '음식점·카페·뷰티샵·마사지·쇼핑 등 손님이 방문하는 매장이라면 진행 가능합니다. 호치민·다낭 등 지역과 업종에 맞춰 어울리는 인플루언서를 매칭해 드립니다.')

# ---- CTA ----
s = s.replace('소중한 매장, 이제 베트남 손님에게 알려보세요', '소중한 매장, 이제 세 방향의 손님에게 알려보세요')
s = s.replace('방문 체험으로 끝나지 않습니다.', '한 타겟으로 끝나지 않습니다.')
s = s.replace('검색하면 나오는 매장이 될 때까지 함께 해드립니다.', '로컬·중국인·한국인 — 검색하면 나오는 매장이 될 때까지 함께 해드립니다.')

# ---- 내비 active ----
s = s.replace('<li class="on"><a href="./tourist-vn.html">외국인 관광객 마케팅</a>', '<li><a href="./tourist-vn.html">외국인 관광객 마케팅</a>')
s = s.replace('<li><a href="./local-vn.html">해외 현지 마케팅</a>', '<li class="on"><a href="./local-vn.html">해외 현지 마케팅</a>')

open('local-vn.html', 'w', encoding='utf-8').write(s)
print('local-vn.html written, size', len(s))
