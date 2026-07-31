# -*- coding: utf-8 -*-
# vietnam-tiktok.html -> index.html (그룹 메인 = 오늘 만든 랜딩 4종의 총합 라우팅)
import re, shutil
shutil.copy('index.html', '_bak_index_prev.html')
s = open('vietnam-tiktok.html', encoding='utf-8').read()

# ---- head ----
s = s.replace('<title>트래비티 | 베트남 틱톡 인플루언서 대량 부킹</title>',
              '<title>트래비티 TREVITY | 글로벌 인플루언서 마케팅 그룹</title>')
s = re.sub(r'(<meta name="description" content=")[^"]*(")',
           r'\g<1>제품을 팔 때도, 매장에 손님을 모을 때도 — 한국·베트남·중국을 잇는 인플루언서 마케팅. 수출·관광객·현지 매장·숙박까지 트래비티가 연결합니다.\g<2>', s, count=1)
s = s.replace('content="트래비티 | 베트남인 관광객·유학생 체험단"', 'content="트래비티 TREVITY | 글로벌 인플루언서 마케팅 그룹"')

# ---- 추천 스트립: 상황 4종 ----
s = s.replace('<li>베트남 쇼피·틱톡샵에 입점하신 분</li>', '<li>해외에 제품을 팔고 싶은 분</li>')
s = s.replace('<li>틱톡샵 어필리에이트 신청자가 없는 분</li>', '<li>한국 매장에 외국인 손님을 원하는 분</li>')
s = s.replace('<li>팔로워 1,000명대 시딩만 반복 중인 분</li>', '<li>베트남 현지에서 매장을 하시는 분</li>')
s = s.replace('<li>베트남 인플루언서 섭외가 막막한 분</li>', '<li>호텔·펜션 공실이 고민인 분</li>')

# ---- 히어로 ----
s = s.replace('<h1 class="tvhero2-tit">Vietnam TikTok KOL</h1>', '<h1 class="tvhero2-tit">TREVITY</h1>')
s = s.replace('.tvhero2-tit{font-size:96px;', '.tvhero2-tit{font-size:120px;')
s = s.replace('베트남에 제품은 올려두셨는데, 인플루언서 마케팅은 쉽지 않으셨죠?',
              '제품을 팔 때도, 매장에 손님을 모을 때도 — 결국 답은 인플루언서입니다.')
s = s.replace('검증된 10만~50만 인플루언서를 1명당 20만원 균일가로, 트래비티가 대신 부킹해 드립니다.',
              '한국 · 베트남 · 중국을 잇는 10만+ 그룹 인플루언서 풀, 트래비티가 연결합니다.')

# ---- tvsvc -> 상황 선택(tvpick) ----
i = s.find('<section class="tvsvc">')
j = s.find('</section>', i) + len('</section>')
reveal = 'style="opacity: 0; transform: translateY(40px); transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;"'
pick = '''<section class="tvpick"><style>
.tvpick{background:#fff;padding:120px 20px;word-break:keep-all}
.tvpick-in{max-width:1084px;margin:0 auto;text-align:center}
.tvpick-label{display:inline-block;font-size:14px;font-weight:800;letter-spacing:2.5px;color:#fa6781;margin-bottom:18px}
.tvpick-h2{font-size:36px;font-weight:800;line-height:1.45;letter-spacing:-0.72px;color:#1f1f1f;margin:0}
.tvpick-sub{font-size:16.5px;line-height:1.85;letter-spacing:-0.33px;color:#595959;margin:24px auto 0}
.tvpick-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:56px;text-align:left}
.tvpick-card{display:block;background:#fff;border:1.5px solid #f0f0f2;border-radius:20px;padding:38px 36px;text-decoration:none;transition:all .25s;position:relative}
.tvpick-card:hover{border-color:#ffb8c6;box-shadow:0 14px 44px rgba(250,103,129,0.14);transform:translateY(-4px)}
.tvpick-sit{font-size:15px;font-weight:700;color:#8c8c8c;letter-spacing:-0.3px}
.tvpick-tit{font-size:24px;font-weight:800;color:#1f1f1f;letter-spacing:-0.48px;line-height:1.45;margin-top:10px}
.tvpick-hook{font-size:15.5px;color:#595959;line-height:1.7;letter-spacing:-0.31px;margin-top:12px}
.tvpick-hook b{color:#fa6781}
.tvpick-chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:18px}
.tvpick-chip{font-size:12.5px;font-weight:700;color:#fa6781;background:#fff0f3;border-radius:99px;padding:6px 12px}
.tvpick-go{position:absolute;right:30px;top:38px;font-size:22px;color:#d9d9de;font-weight:700;transition:all .25s}
.tvpick-card:hover .tvpick-go{color:#fa6781;transform:translateX(4px)}
@media (max-width:900px){.tvpick{padding:72px 20px}.tvpick-h2{font-size:26px}.tvpick-grid{grid-template-columns:1fr;gap:12px;margin-top:36px}.tvpick-tit{font-size:20px}}
</style><div class="tvpick-in"><div REVEAL><span class="tvpick-label">TREVITY SERVICE</span><h2 class="tvpick-h2">어떤 사장님이신가요?</h2><p class="tvpick-sub">상황만 고르세요. 맞는 서비스로 바로 안내해 드립니다.</p></div><div class="tvpick-grid" REVEAL>
<a class="tvpick-card" href="./vietnam-tiktok.html"><span class="tvpick-go">&#8594;</span><p class="tvpick-sit">"베트남 · 중국에 제품을 팔고 싶어요"</p><h3 class="tvpick-tit">한국제품 해외수출 마케팅</h3><p class="tvpick-hook">팔로워 10만~50만 현지 인플루언서가 직접 올립니다.<br><b>1명당 20만원 균일가</b>, 한 번에 최대 50명까지.</p><div class="tvpick-chips"><span class="tvpick-chip">베트남 틱톡</span><span class="tvpick-chip">틱톡샵 연계</span></div></a>
<a class="tvpick-card" href="./tourist-vn.html"><span class="tvpick-go">&#8594;</span><p class="tvpick-sit">"한국에서 매장을 운영해요"</p><h3 class="tvpick-tit">외국인 관광객 마케팅</h3><p class="tvpick-hook">한국에 와 있는 외국인 인플루언서가 매장을 체험하고 모국 SNS에 알립니다.<br><b>여행 준비자가 검색하면 우리 매장이 나오게.</b></p><div class="tvpick-chips"><span class="tvpick-chip">베트남인 체험단</span><span class="tvpick-chip">중국인 체험단</span></div></a>
<a class="tvpick-card" href="./local-vn.html"><span class="tvpick-go">&#8594;</span><p class="tvpick-sit">"베트남에서 매장을 운영해요"</p><h3 class="tvpick-tit">베트남 현지 매장 마케팅</h3><p class="tvpick-hook">로컬, 중국인 관광객, 한국인 관광객 — <b>세 방향의 손님</b>을 데려옵니다.<br>호치민 현지팀이 직접 움직입니다.</p><div class="tvpick-chips"><span class="tvpick-chip">로컬 틱톡</span><span class="tvpick-chip">더우인 · 디엔핑</span><span class="tvpick-chip">네이버 블로그</span></div></a>
<a class="tvpick-card" href="./stay.html"><span class="tvpick-go">&#8594;</span><p class="tvpick-sit">"호텔 · 펜션을 운영해요"</p><h3 class="tvpick-tit">숙박 체험단</h3><p class="tvpick-hook">비어 있는 객실 하루만 내어주세요.<br>광고비도 대행비도 <b>0원</b>, 후기는 검색에 평생 남습니다.</p><div class="tvpick-chips"><span class="tvpick-chip">사장님 0원</span><span class="tvpick-chip">블로거 체험단</span></div></a>
</div></div></section>'''
pick = pick.replace('REVEAL', reveal)
s = s[:i] + pick + s[j:]

# ---- tvpain -> 글로벌 거점 지도(tvglobal) ----
i = s.find('<section class="tvpain">')
j = s.find('</section>', i) + len('</section>')
pain_sec = s[i:j]
# 지도 SVG는 기존 페이지 것 재사용
mi = s.find('<svg viewBox=')  # 이미 tvsvc가 사라졌으므로 없음 -> vietnam-tiktok 원본에서 가져오기
src = open('local-vn.html', encoding='utf-8').read()
sm = re.search(r'<svg viewBox=.*?</svg>', src, re.S)
if not sm:
    src2 = open('tourist-vn.html', encoding='utf-8').read()
    sm = re.search(r'<svg viewBox=.*?</svg>', src2, re.S)
svg = sm.group(0)
glob_sec = ('<section class="tvglobal"><style>'
 '.tvglobal{background:#fff5f7;padding:110px 20px;word-break:keep-all}'
 '.tvglobal-in{max-width:1084px;margin:0 auto;text-align:center}'
 '.tvglobal-label{display:inline-block;font-size:14px;font-weight:800;letter-spacing:2.5px;color:#fa6781;margin-bottom:18px}'
 '.tvglobal-h2{font-size:36px;font-weight:800;line-height:1.45;letter-spacing:-0.72px;color:#1f1f1f;margin:0}'
 '.tvglobal-sub{font-size:16.5px;line-height:1.85;letter-spacing:-0.33px;color:#595959;margin:24px auto 0;max-width:640px}'
 '.tvglobal-map{max-width:780px;margin:52px auto 0;background:linear-gradient(180deg,#fbfbfd,#fff);border:1px solid #f0f0f2;border-radius:24px;box-shadow:0 8px 40px rgba(0,0,0,0.07);padding:34px 40px}'
 '.tvglobal-map svg{width:100%;height:auto;display:block}'
 '@media (max-width:767px){.tvglobal{padding:70px 20px}.tvglobal-h2{font-size:26px}.tvglobal-map{padding:18px 16px;margin-top:34px}}'
 '</style><div class="tvglobal-in"><div ' + reveal + '><span class="tvglobal-label">GLOBAL NETWORK</span>'
 '<h2 class="tvglobal-h2">서울에서 호치민까지,<br>현지팀이 직접 움직입니다</h2>'
 '<p class="tvglobal-sub">서울 · 대구 · 대련 · 호치민 4개 거점의 현지 마케터가 섭외부터 검수까지 중간 업체 없이 직접 진행합니다.</p></div>'
 '<div class="tvglobal-map" ' + reveal + '>' + svg + '</div></div></section>')
s = s[:i] + glob_sec + s[j:]

# ---- 비교 섹션 삭제 ----
k = s.find('직접 섭외 vs')
sec_start = s.rfind('<section', 0, k)
sec_end = s.find('</section>', k) + len('</section>')
s = s[:sec_start] + s[sec_end:]

# ---- 패키지 섹션 삭제 ----
k = s.find('id="packages"')
if k > 0:
    sec_start = s.rfind('<section', 0, k)
    sec_end = s.find('</section>', k) + len('</section>')
    s = s[:sec_start] + s[sec_end:]

# ---- FAQ 섹션 삭제 ----
k = s.find('자주 묻는 질문')
if k > 0:
    sec_start = s.rfind('<section', 0, k)
    sec_end = s.find('</section>', k) + len('</section>')
    s = s[:sec_start] + s[sec_end:]

# ---- 숫자 밴드: 그룹 프레임 ----
s = s.replace(' 인플루언서 풀이<br>증명합니다</h3>', ' 트래비티 그룹이<br>증명합니다</h3>')
s = s.replace(' 인플루언서 풀이 증명합니다</h1>', ' 트래비티 그룹이 증명합니다</h1>')
s = s.replace('>베트남 최대 인플루언서</span>', '>아시아 6개국 그룹 전체</span>')
s = s.replace('>베트남 최대 인플루언서 풀 보유</span>', '>아시아 6개국 그룹 전체 풀 기준</span>')
s = s.replace('보유 인플루언서', '그룹 인플루언서 풀')

# ---- CTA ----
s = s.replace('소중한 제품, 이제 검증된 인플루언서에게 맡겨보세요', '제품이든 매장이든, 손님이 모이게 만들어 드립니다')
s = s.replace('부킹으로 끝나지 않습니다.', '어떤 상황이든 시작은 같습니다.')
s = s.replace('틱톡샵 제휴 판매 설계까지 함께 해드립니다.', '상황을 남겨주시면, 가장 맞는 방법과 견적부터 제안드립니다.')

# ---- 내비 active 해제 ----
s = s.replace('<li class="on"><a href="./vietnam-tiktok.html">한국제품 해외수출 마케팅</a>', '<li><a href="./vietnam-tiktok.html">한국제품 해외수출 마케팅</a>')

open('index.html', 'w', encoding='utf-8').write(s)
print('index.html rebuilt, size', len(s))
