# -*- coding: utf-8 -*-
# index.html tvpick(2x2 카드) → A안 탭 셀렉터(tvpick2)
s = open('index.html', encoding='utf-8').read()
i = s.find('<section class="tvpick">')
j = s.find('</section>', i) + len('</section>')
assert i > 0
reveal = 'style="opacity: 0; transform: translateY(40px); transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;"'

def panel(pid, on, sit, tit, body, bullets, ctas, img, badge):
    b = ''.join(f'<li>{x}</li>' for x in bullets)
    c = ''.join(f'<a class="go{" ghost" if n else ""}" href="{h}">{t}</a>' for n, (h, t) in enumerate(ctas))
    return (f'<div class="tvp2-panel{" on" if on else ""}" id="{pid}">'
            f'<div class="t"><p class="sit">&ldquo;{sit}&rdquo;</p><h3>{tit}</h3><p class="bd">{body}</p>'
            f'<ul class="blt">{b}</ul><div class="ctas">{c}</div></div>'
            f'<div class="v"><img src="{img}" alt=""/><span class="badge">{badge}</span></div></div>')

panels = (
panel('tvp1', True, '베트남 · 중국에 제품을 팔고 싶어요', '한국제품 해외수출 마케팅',
 '쇼피·틱톡샵에 올려두기만 해서는 팔리지 않습니다.<br>팔로워 10만~50만 현지 인플루언서가 직접 올리고, 판매 설계까지 이어갑니다.',
 ['1명당 <b>20만원 균일가</b>, 협상 없음', '한 번에 <b>최대 50명</b>까지 부킹', '틱톡샵 제휴 판매 연계'],
 [('./vietnam-tiktok.html', '자세히 보기 →')],
 './images/landing/home/hero/10.png', '최대 50명 부킹')
+ panel('tvp2', False, '한국에서 매장을 운영해요', '외국인 관광객 마케팅',
 '한국에 와 있는 베트남·중국 인플루언서가 매장을 체험하고 모국 SNS에 올립니다.<br>여행 준비자가 검색하면, 우리 매장이 먼저 나옵니다.',
 ['방한 관광객 · 유학생 <b>검증 체험단</b>', '틱톡 · 샤오홍슈 · 더우인 노출', '검색 상단에 후기가 쌓입니다'],
 [('./tourist-vn.html', '베트남인 체험단 →'), ('./tourist-cn.html', '중국인 체험단 →')],
 './images/landing/home/hero/4.png', '모국 SNS 노출')
+ panel('tvp3', False, '베트남에서 매장을 운영해요', '베트남 현지 매장 마케팅',
 '매장은 베트남에 있는데, 손님은 어디서 데려올까요?<br>로컬, 중국인 관광객, 한국인 관광객 — 세 방향의 손님을 호치민 현지팀이 데려옵니다.',
 ['로컬 손님 — 틱톡 · 페이스북', '중국인 관광객 — 더우인 · 따중디엔핑', '한국인 관광객 — 네이버 블로그'],
 [('./local-vn.html', '자세히 보기 →')],
 './images/landing/home/hero/9.png', '3-타겟 동시 유치')
+ panel('tvp4', False, '호텔 · 펜션을 운영해요', '숙박 체험단',
 '광고는 끄는 순간 사라지지만, 후기는 검색에 남습니다.<br>비어 있는 객실 하루만 내어주시면, 검증된 블로거가 후기를 쌓아 드립니다.',
 ['광고비 · 대행비 · 원고료 <b>0원</b>', '주중 · 비수기 위주로 일정 조율', '후기는 영구 자산으로'],
 [('./stay.html', '자세히 보기 →')],
 './images/landing/home/hero/6.png', '사장님은 0원')
)

sec = '''<section class="tvpick2"><style>
.tvpick2{background:#fff;padding:120px 20px;word-break:keep-all}
.tvpick2-in{max-width:1084px;margin:0 auto;text-align:center}
.tvpick2-label{display:inline-block;font-size:14px;font-weight:800;letter-spacing:2.5px;color:#fa6781;margin-bottom:18px}
.tvpick2-h2{font-size:36px;font-weight:800;letter-spacing:-0.72px;color:#1f1f1f;line-height:1.45;margin:0}
.tvpick2-sub{font-size:16.5px;color:#595959;margin:22px 0 0;letter-spacing:-0.33px}
.tvp2-tabs{display:flex;gap:10px;justify-content:center;margin-top:46px;flex-wrap:wrap}
.tvp2-tab{font-size:15.5px;font-weight:700;letter-spacing:-0.31px;color:#595959;background:#f4f4f6;border:none;border-radius:99px;padding:14px 26px;cursor:pointer;transition:all .22s}
.tvp2-tab:hover{background:#ffe9ee;color:#fa6781}
.tvp2-tab.on{background:#fa6781;color:#fff;box-shadow:0 8px 22px rgba(250,103,129,.35)}
.tvp2-panel{display:none;margin-top:42px;background:linear-gradient(160deg,#fff5f7,#fff);border:1.5px solid #ffe3ea;border-radius:26px;padding:56px 60px;text-align:left}
.tvp2-panel.on{display:flex;gap:56px;align-items:center;animation:tvp2in .45s ease}
@keyframes tvp2in{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
.tvp2-panel .t{flex:1.15;min-width:0}
.tvp2-panel .sit{font-size:15.5px;font-weight:700;color:#8c8c8c;letter-spacing:-0.31px}
.tvp2-panel h3{font-size:31px;font-weight:800;color:#1f1f1f;letter-spacing:-0.62px;line-height:1.4;margin:12px 0 0}
.tvp2-panel .bd{font-size:16px;color:#595959;line-height:1.75;letter-spacing:-0.32px;margin:16px 0 0}
.tvp2-panel .blt{list-style:none;margin:22px 0 0;padding:0}
.tvp2-panel .blt li{position:relative;padding:5px 0 5px 30px;font-size:15.5px;color:#434343;letter-spacing:-0.31px}
.tvp2-panel .blt li b{color:#fa6781}
.tvp2-panel .blt li::before{content:'&#10003;';position:absolute;left:0;top:4px;width:21px;height:21px;border-radius:50%;background:#ffe3ea;color:#fa6781;font-size:12px;font-weight:800;display:flex;align-items:center;justify-content:center}
.tvp2-panel .ctas{display:flex;gap:10px;margin-top:30px;flex-wrap:wrap}
.tvp2-panel .go{display:inline-block;background:#fa6781;color:#fff;font-size:15.5px;font-weight:700;letter-spacing:-0.31px;border-radius:10px;padding:15px 30px;text-decoration:none;box-shadow:0 8px 22px rgba(250,103,129,.28);transition:all .2s}
.tvp2-panel .go:hover{transform:translateY(-2px)}
.tvp2-panel .go.ghost{background:#fff;color:#fa6781;border:1.5px solid #ffc2cd;box-shadow:none}
.tvp2-panel .v{flex:1;position:relative;border-radius:20px;height:330px;min-width:0}
.tvp2-panel .v img{width:100%;height:100%;object-fit:cover;border-radius:20px;display:block;box-shadow:0 18px 52px rgba(31,31,35,.16)}
.tvp2-panel .badge{position:absolute;left:-18px;bottom:24px;background:#fff;border-radius:14px;box-shadow:0 12px 34px rgba(31,31,35,.16);padding:14px 20px;font-size:16px;font-weight:800;color:#fa6781;letter-spacing:-0.32px}
@media (max-width:1023px){.tvpick2{padding:72px 16px}.tvpick2-h2{font-size:26px}.tvp2-tab{font-size:13.5px;padding:11px 16px}
.tvp2-panel{padding:28px 22px;margin-top:28px}.tvp2-panel.on{flex-direction:column-reverse;gap:24px}
.tvp2-panel h3{font-size:22px}.tvp2-panel .v{width:100%;height:210px}.tvp2-panel .badge{left:12px;bottom:12px;font-size:13.5px;padding:10px 14px}}
</style><div class="tvpick2-in"><div REVEAL><span class="tvpick2-label">TREVITY SERVICE</span><h2 class="tvpick2-h2">어떤 사장님이신가요?</h2><p class="tvpick2-sub">상황만 고르세요. 3초 만에 맞는 서비스를 찾아드립니다.</p></div><div REVEAL><div class="tvp2-tabs">
<button class="tvp2-tab on" data-p="tvp1">&#128230; 제품을 수출해요</button>
<button class="tvp2-tab" data-p="tvp2">&#127978; 한국에서 매장해요</button>
<button class="tvp2-tab" data-p="tvp3">&#127470;&#127475; 베트남에서 매장해요</button>
<button class="tvp2-tab" data-p="tvp4">&#127976; 숙박업을 해요</button>
</div>''' + panels + '''</div></div>
<script>(function(){
var tabs=document.querySelectorAll('.tvp2-tab'),panels=document.querySelectorAll('.tvp2-panel');
var idx=0,timer=null,stopped=false;
function show(k){idx=k;tabs.forEach(function(t,n){t.classList.toggle('on',n===k)});panels.forEach(function(p,n){p.classList.toggle('on',n===k)})}
tabs.forEach(function(t,n){t.addEventListener('click',function(){stopped=true;clearInterval(timer);show(n)})});
timer=setInterval(function(){if(!stopped)show((idx+1)%tabs.length)},5000);
var sec=document.querySelector('.tvpick2');
sec.addEventListener('mouseenter',function(){clearInterval(timer)});
sec.addEventListener('mouseleave',function(){if(!stopped){clearInterval(timer);timer=setInterval(function(){if(!stopped)show((idx+1)%tabs.length)},5000)}});
})();</script></section>'''
sec = sec.replace('REVEAL', reveal)

s = s[:i] + sec + s[j:]
open('index.html', 'w', encoding='utf-8').write(s)
print('tvpick2 applied; size', len(s))
