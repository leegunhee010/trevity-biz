# -*- coding: utf-8 -*-
svg = open('_map_patched.svg.txt', encoding='utf-8').read()
s = open('vietnam-tiktok.html', encoding='utf-8').read()
i = s.find('<section class="tvsvc">')
j = s.find('</section>', i) + len('</section>')
assert i > 0

rows = '''<div class="mt-head"><span class="tt">인플루언서 매칭 리포트 · 뷰티 세럼</span><span class="bd">예시 화면</span></div>
<div class="mt-row"><span class="mt-av" style="background:linear-gradient(135deg,#fa6781,#ff9db0)">L</span><div class="mt-mid"><div class="mt-top"><span class="mt-nm">@beauty.linh</span><span class="mt-fl">팔로워 32만</span></div><div class="mt-bar"><i style="width:96%"></i></div><span class="mt-in">뷰티 리뷰 · 연관성 96%</span></div><span class="mt-tag mt-ok">추천</span></div>
<div class="mt-row"><span class="mt-av" style="background:linear-gradient(135deg,#ff8fa5,#ffc2cd)">M</span><div class="mt-mid"><div class="mt-top"><span class="mt-nm">@skincare.mai</span><span class="mt-fl">팔로워 45만</span></div><div class="mt-bar"><i style="width:91%"></i></div><span class="mt-in">스킨케어 · 연관성 91%</span></div><span class="mt-tag mt-ok">추천</span></div>
<div class="mt-row"><span class="mt-av" style="background:#d9d9de">T</span><div class="mt-mid"><div class="mt-top"><span class="mt-nm">@dance.trang</span><span class="mt-fl">팔로워 51만</span></div><div class="mt-bar low"><i style="width:18%"></i></div><span class="mt-in">댄스 · 카테고리 불일치</span></div><span class="mt-tag mt-no">제외</span></div>
<div class="mt-row"><span class="mt-av" style="background:#d9d9de">H</span><div class="mt-mid"><div class="mt-top"><span class="mt-nm">@daily.huong</span><span class="mt-fl">팔로워 8천</span></div><div class="mt-bar low"><i style="width:8%"></i></div><span class="mt-in">일상 · 팔로워 구간 미달</span></div><span class="mt-tag mt-no">제외</span></div>
<p class="mt-cap">10만 풀에서 제품과 맞는 계정만 남깁니다</p>'''

css = '''<style>
.tvsvc{background:#fff;padding:120px 20px;word-break:keep-all}
.tvsvc-wrap{max-width:1084px;margin:0 auto}
.tvsvc-head{text-align:center;margin-bottom:88px}
.tvsvc-label{display:inline-block;font-size:14px;font-weight:800;letter-spacing:2.5px;color:#fa6781;margin-bottom:18px}
.tvsvc-h2{font-size:36px;font-weight:800;line-height:1.45;letter-spacing:-0.72px;color:#1f1f1f;margin:0}
.tvsvc-sub{font-size:16.5px;line-height:1.85;letter-spacing:-0.33px;color:#595959;margin:26px auto 0;max-width:680px}
.tvsvc .ab-zig{display:flex;gap:64px;align-items:center;flex-wrap:wrap}
.tvsvc .ab-zig>.t{flex:1 1 380px;min-width:320px}
.tvsvc .ab-zig>.v{flex:1 1 420px;min-width:320px}
.tvsvc .ab-zig h3{font-size:32px;font-weight:800;line-height:1.45;letter-spacing:-0.64px;color:#1f1f1f;margin:0 0 18px}
.tvsvc .ab-zig p{font-size:16.5px;line-height:1.85;letter-spacing:-0.33px;color:#595959;margin:0}
.tvsvc .ab-zlabel{display:inline-block;font-size:15px;font-weight:800;letter-spacing:-0.3px;color:#fa6781;background:#fff0f3;border-radius:999px;padding:7px 16px;margin-bottom:20px}
.tvsvc .vbox{height:430px;background:linear-gradient(180deg,#fbfbfd,#fff);border:1px solid #f0f0f2;border-radius:24px;box-shadow:0 8px 40px rgba(0,0,0,0.07);padding:26px 34px;display:flex;flex-direction:column;justify-content:center;overflow:hidden}
.tvsvc .vbox.pink{border:1.5px solid #ffdae1;box-shadow:0 8px 40px rgba(250,103,129,0.10)}
.tvsvc .vbox svg{height:100%;width:auto;max-width:100%;margin:0 auto;display:block}
.tvsvc .mt-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}
.tvsvc .mt-head .tt{font-size:15.5px;font-weight:800;color:#1f1f1f;letter-spacing:-0.31px}
.tvsvc .mt-head .bd{font-size:12px;font-weight:700;color:#fa6781;background:#fff0f3;border-radius:999px;padding:5px 12px}
.tvsvc .mt-row{display:flex;align-items:center;gap:13px;padding:11px 4px;border-bottom:1px solid #f5f5f5}
.tvsvc .mt-row:last-of-type{border-bottom:none}
.tvsvc .mt-av{width:40px;height:40px;border-radius:50%;flex:none;display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:800;color:#fff}
.tvsvc .mt-mid{flex:1;min-width:0}
.tvsvc .mt-top{display:flex;justify-content:space-between;align-items:baseline;gap:8px}
.tvsvc .mt-nm{font-size:14.5px;font-weight:700;color:#333;letter-spacing:-0.29px}
.tvsvc .mt-fl{font-size:12px;color:#8c8c8c;flex:none}
.tvsvc .mt-bar{height:4px;border-radius:99px;background:#f3f3f5;margin:5px 0 4px;overflow:hidden}
.tvsvc .mt-bar i{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,#ff9db0,#fa6781)}
.tvsvc .mt-bar.low i{background:#d9d9de}
.tvsvc .mt-in{font-size:12px;color:#8c8c8c;letter-spacing:-0.24px}
.tvsvc .mt-tag{flex:none;font-size:12.5px;font-weight:700;border-radius:8px;padding:6px 11px}
.tvsvc .mt-ok{color:#fa6781;background:#fff0f3}
.tvsvc .mt-no{color:#9e9e9e;background:#f4f4f5}
.tvsvc .mt-cap{margin-top:12px;font-size:12px;color:#8c8c8c;text-align:center}
.tvsvc .ab-price .row{display:flex;justify-content:space-between;align-items:center;padding:17px 4px;border-bottom:1px solid #f5f5f5}
.tvsvc .ab-price .row:last-child{border-bottom:none}
.tvsvc .ab-price .nm{font-size:16px;font-weight:700;color:#434343;letter-spacing:-0.32px}
.tvsvc .ab-price .pr{font-size:19px;font-weight:800;color:#fa6781;letter-spacing:-0.38px}
.tvsvc .ab-price .cap{margin-top:16px;font-size:13px;color:#8c8c8c;text-align:right}
@media (max-width:767px){.tvsvc{padding:72px 20px}.tvsvc-h2{font-size:27px}.tvsvc-head{margin-bottom:56px}.tvsvc .ab-zig{gap:32px}.tvsvc .ab-zig h3{font-size:24px}.tvsvc .vbox{height:360px;padding:20px 18px}}
</style>'''

reveal = 'style="opacity: 0; transform: translateY(40px); transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;"'

sec = ('<section class="tvsvc">' + css
+ '<div class="tvsvc-wrap"><div class="tvsvc-head" ' + reveal + '>'
+ '<span class="tvsvc-label">TREVITY SERVICE</span><h2 class="tvsvc-h2">베트남 인플루언서<br>제품 체험단</h2>'
+ '<p class="tvsvc-sub">제품은 이미 베트남에 올라가 있습니다. 이제 팔아 줄 사람을 붙일 차례입니다.<br>섭외도, 소통도, 검수도 — 현지의 트래비티 팀이 처음부터 끝까지 대신합니다.</p></div>'
+ '<div style="display:flex;flex-direction:column;gap:120px">'
# zig 1: local network + animated map
+ '<div class="ab-zig" ' + reveal + '><div class="t"><span class="ab-zlabel">베트남 현지 완결 네트워크</span>'
+ '<h3>호치민에서 다낭까지,<br>현지팀이 직접 움직입니다</h3>'
+ '<p>메일만 주고받는 대행이 아닙니다. 호치민·다낭에 상주하는 로컬 마케터가 인플루언서를 직접 만나고, 가이드를 전하고, 콘텐츠를 검수합니다.<br>언어와 정서의 벽은 트래비티가 대신 넘겠습니다.</p></div>'
+ '<div class="v"><div class="vbox">' + svg + '</div></div></div>'
# zig 2: matching mockup + pool copy
+ '<div class="ab-zig" ' + reveal + '><div class="v"><div class="vbox">' + rows + '</div></div>'
+ '<div class="t"><span class="ab-zlabel">검증된 인플루언서 풀</span>'
+ '<h3>팔로워 수가 아니라,<br>제품과의 연관성으로 고릅니다</h3>'
+ '<p>10만 명의 풀에서 아무나 뽑지 않습니다. 카테고리 연관성, 오디언스 반응, 톤앤매너까지 확인해 제품과 맞는 계정만 남깁니다.<br>뷰티 제품이라면, 뷰티를 다뤄 온 인플루언서에게만 맡깁니다.</p></div></div>'
# zig 3: price
+ '<div class="ab-zig" ' + reveal + '><div class="t"><span class="ab-zlabel">명확한 가격</span>'
+ '<h3>10만이든 50만이든,<br>1명당 20만원 균일가</h3>'
+ '<p>협상도, 숨은 비용도 없습니다. 누구를 골라도 같은 가격이라 예산이 흔들리지 않습니다.<br>체험단으로 끝내지 않고, 틱톡샵 제휴 판매 설계까지 함께 갑니다.</p></div>'
+ '<div class="v"><div class="vbox pink"><div class="ab-price">'
+ '<div class="row"><span class="nm">스타터 · 10명</span><span class="pr">200만원</span></div>'
+ '<div class="row"><span class="nm">그로스 · 20명</span><span class="pr">400만원</span></div>'
+ '<div class="row"><span class="nm">도미넌트 · 50명</span><span class="pr">1,000만원</span></div>'
+ '<p class="cap">팔로워 10만~50만 누구든 · 1명당 20만원 · 부가세 별도</p>'
+ '</div></div></div></div>'
+ '</div></div></section>')

s = s[:i] + sec + s[j:]
open('vietnam-tiktok.html', 'w', encoding='utf-8').write(s)
print('tvsvc rebuilt; size', len(s))
