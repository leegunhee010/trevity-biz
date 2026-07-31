# -*- coding: utf-8 -*-
# tvpick2(탭+단일패널) → 링글 aitutor 레이아웃(tvpick3: 아이콘 탭카드 4 + 패널 2장 그리드)
s = open('index.html', encoding='utf-8').read()
i = s.find('<section class="tvpick2">')
j = s.find('</section>', i)
j = s.find('</section>', j + 1)  # 내부 script 뒤 실제 닫힘 — 확인 필요
# tvpick2 구조: <section ...> ... <script>...</script></section> — script 안엔 </section> 없음 → 첫 </section>이 닫힘
j = s.find('</section>', i) + len('</section>')
assert i > 0
reveal = 'style="opacity: 0; transform: translateY(40px); transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;"'

def pair(pid, on, l, r, href):
    def panel(cls, label, h, body, img):
        return (f'<div class="tvp3-panel {cls}"><span class="pl">{label}</span><h3>{h}</h3><p>{body}</p>'
                f'<div class="mock"><img src="{img}" alt=""/></div></div>')
    return (f'<div class="tvp3-pair{" on" if on else ""}" id="{pid}">'
            + panel('a', *l) + panel('b', *r)
            + f'<a class="tvp3-more" href="{href}">서비스 자세히 보기 →</a></div>')

pairs = (
pair('tp1', True,
 ('인플루언서 부킹', '10만~50만 인플루언서가<br>직접 올립니다',
  '팔로워 수가 아니라 제품과의 연관성으로 선별합니다.<br>협상 없이 1명당 20만원 균일가, 한 번에 최대 50명까지.',
  './assets/pick/exp-match.jpg'),
 ('판매 연계', '체험단으로 끝내지 않고<br>판매까지 설계합니다',
  '틱톡샵 제휴 연결부터 판매 설계까지 함께 갑니다.<br>명확한 패키지 가격이라 예산이 흔들리지 않습니다.',
  './assets/pick/exp-price.jpg'),
 './vietnam-tiktok.html')
+ pair('tp2', False,
 ('검증 체험단', '방한 관광객·유학생이<br>매장을 직접 체험합니다',
  '한국에 와 있는 베트남·중국 인플루언서 가운데<br>팔로워와 콘텐츠 이력이 검증된 계정만 방문합니다.',
  './assets/pick/kr-match.jpg'),
 ('모국 SNS 노출', '여행 준비자가 검색하면<br>우리 매장이 나옵니다',
  '후기는 전부 모국어 콘텐츠로 올라갑니다.<br>틱톡·샤오홍슈에서 검색하는 손님에게 먼저 보입니다.',
  './assets/pick/kr-search.jpg'),
 './tourist-vn.html')
+ pair('tp3', False,
 ('로컬 손님', '1억 로컬 시장,<br>틱톡 인플루언서가 엽니다',
  '베트남 사람들은 갈 곳을 틱톡에서 찾습니다.<br>로컬 인플루언서 후기가 검색 상단에 쌓입니다.',
  './assets/pick/vn-search.jpg'),
 ('관광객 손님', '중국인·한국인 관광객까지<br>같이 데려옵니다',
  '더우인·따중디엔핑 후기로 중국인 관광객을,<br>네이버 블로그로 한국인 관광객을 부릅니다.',
  './assets/pick/vn-dianping.jpg'),
 './local-vn.html')
+ pair('tp4', False,
 ('0원 구조', '사장님은 0원,<br>객실 하루가 전부입니다',
  '광고비도, 대행비도, 원고료도 없습니다.<br>비어 있던 주중 객실이 그대로 마케팅이 됩니다.',
  './assets/pick/stay-cost.jpg'),
 ('검색 노출', "'지역 + 후기' 검색에<br>우리 숙소가 나옵니다",
  '광고는 끄면 사라지지만, 후기는 검색에 남습니다.<br>예약 전 검색하는 손님에게 먼저 보입니다.',
  './assets/pick/stay-search.jpg'),
 './stay.html')
)

sec = '''<section class="tvpick3"><style>
.tvpick3{background:#fff;padding:120px 20px;word-break:keep-all}
.tvpick3-in{max-width:1180px;margin:0 auto}
.tvpick3-head{text-align:center;margin-bottom:52px}
.tvpick3-label{display:inline-block;font-size:14px;font-weight:800;letter-spacing:2.5px;color:#fa6781;margin-bottom:18px}
.tvpick3-h2{font-size:36px;font-weight:800;letter-spacing:-0.72px;color:#1f1f1f;line-height:1.45;margin:0}
.tvpick3-sub{font-size:16.5px;color:#595959;margin:22px 0 0;letter-spacing:-0.33px}
.tvp3-tabs{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.tvp3-tab{background:#fff;border:1px solid #e7e7ec;border-radius:14px;padding:20px 20px 18px;text-align:left;cursor:pointer;transition:all .2s;font-family:inherit}
.tvp3-tab .ic{font-size:20px;display:block}
.tvp3-tab .tx{display:block;font-size:15.5px;font-weight:700;color:#26262b;letter-spacing:-0.31px;line-height:1.45;margin-top:12px}
.tvp3-tab:hover{border-color:#ffc2cd}
.tvp3-tab.on{border:1.5px solid #26262b;background:#fff0f4}
.tvp3-pair{display:none;margin-top:22px;position:relative}
.tvp3-pair.on{display:grid;grid-template-columns:1fr 1fr;gap:22px;animation:tvp3in .4s ease}
@keyframes tvp3in{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.tvp3-panel{border-radius:24px;padding:52px 52px 44px;text-align:left;overflow:hidden}
.tvp3-panel.a{background:#fff0f4}
.tvp3-panel.b{background:#fdf4ee}
.tvp3-panel .pl{font-size:13.5px;font-weight:800;color:#fa6781;letter-spacing:-0.27px}
.tvp3-panel h3{font-size:26px;font-weight:800;color:#1f1f1f;letter-spacing:-0.52px;line-height:1.5;margin:14px 0 0}
.tvp3-panel p{font-size:15.5px;color:#595959;line-height:1.75;letter-spacing:-0.31px;margin:16px 0 0}
.tvp3-panel .mock{margin:34px auto 0;max-width:440px;border-radius:18px;overflow:hidden;box-shadow:0 16px 44px rgba(31,31,35,.12)}
.tvp3-panel .mock img{width:100%;display:block}
.tvp3-more{position:absolute;right:6px;top:-44px;font-size:15px;font-weight:700;color:#fa6781;text-decoration:none;letter-spacing:-0.3px}
.tvp3-more:hover{text-decoration:underline}
@media (max-width:1023px){.tvpick3{padding:72px 16px}.tvpick3-h2{font-size:26px}
.tvp3-tabs{grid-template-columns:1fr 1fr;gap:10px}.tvp3-tab{padding:14px}.tvp3-tab .tx{font-size:13.5px;margin-top:8px}
.tvp3-pair.on{grid-template-columns:1fr;gap:14px}.tvp3-panel{padding:30px 24px}.tvp3-panel h3{font-size:21px}
.tvp3-more{position:static;display:inline-block;margin-top:4px}}
</style><div class="tvpick3-in"><div class="tvpick3-head" REVEAL><span class="tvpick3-label">TREVITY SERVICE</span><h2 class="tvpick3-h2">어떤 사장님이신가요?</h2><p class="tvpick3-sub">상황만 고르세요. 맞는 서비스를 바로 보여드립니다.</p></div><div REVEAL><div class="tvp3-tabs">
<button class="tvp3-tab on" data-p="tp1"><span class="ic">&#128230;</span><span class="tx">베트남 · 중국에<br>제품을 팔고 싶어요</span></button>
<button class="tvp3-tab" data-p="tp2"><span class="ic">&#127978;</span><span class="tx">한국에서<br>매장을 운영해요</span></button>
<button class="tvp3-tab" data-p="tp3"><span class="ic">&#127757;</span><span class="tx">베트남에서<br>매장을 운영해요</span></button>
<button class="tvp3-tab" data-p="tp4"><span class="ic">&#127976;</span><span class="tx">호텔 · 펜션을<br>운영해요</span></button>
</div>''' + pairs + '''</div></div>
<script>(function(){
var tabs=document.querySelectorAll('.tvp3-tab'),pairs=document.querySelectorAll('.tvp3-pair');
var idx=0,timer=null,stopped=false;
function show(k){idx=k;tabs.forEach(function(t,n){t.classList.toggle('on',n===k)});pairs.forEach(function(p,n){p.classList.toggle('on',n===k)})}
tabs.forEach(function(t,n){t.addEventListener('click',function(){stopped=true;clearInterval(timer);show(n)})});
timer=setInterval(function(){if(!stopped)show((idx+1)%tabs.length)},6000);
var sec=document.querySelector('.tvpick3');
sec.addEventListener('mouseenter',function(){clearInterval(timer)});
sec.addEventListener('mouseleave',function(){if(!stopped){clearInterval(timer);timer=setInterval(function(){if(!stopped)show((idx+1)%tabs.length)},6000)}});
})();</script></section>'''
sec = sec.replace('REVEAL', reveal)

s = s[:i] + sec + s[j:]
open('index.html', 'w', encoding='utf-8').write(s)
print('tvpick3 applied; size', len(s))
