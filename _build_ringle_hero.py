# -*- coding: utf-8 -*-
# index.html 히어로 → 링글 스타일 콜라주 히어로
import re
s = open('index.html', encoding='utf-8').read()

# 히어로 섹션 경계: tvhero2 포함 <section> ~ 다음 tvpick 직전
k = s.find('tvhero2')
sec_start = s.rfind('<section', 0, k)
pick_start = s.find('<section class="tvpick">')
assert sec_start > 0 and pick_start > sec_start
between = s[sec_start:pick_start]
# 스와이퍼 포함 히어로 섹션이 여러 </section>으로 끝날 수 있으니 tvpick 직전까지 통째 교체
reveal = 'style="opacity: 0; transform: translateY(40px); transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;"'

def cnt(target):
    return ('<span class="inline-grid tabular-nums"><span class="invisible col-start-1 row-start-1" aria-hidden="true">'
            + target + '</span><span class="col-start-1 row-start-1 text-right">0'
            + re.sub(r'[0-9,]', '', target) + '</span></span>')

hero = '''<section class="tvring"><style>
.tvring{background:radial-gradient(120% 90% at 50% 0%,#ffeef2 0%,#fff7f9 45%,#ffffff 100%);padding:96px 20px 90px;word-break:keep-all;overflow:hidden}
.tvring-head{text-align:center;max-width:900px;margin:0 auto}
.tvring-head h1{font-size:46px;font-weight:800;line-height:1.4;letter-spacing:-0.92px;color:#1f1f1f;margin:0}
.tvring-head h1 em{font-style:normal;color:#fa6781}
.tvring-sub{font-size:18px;line-height:1.7;letter-spacing:-0.36px;color:#8c8c92;margin:22px 0 0}
.tvring-cta{display:inline-block;margin-top:34px;background:#fa6781;color:#fff;font-size:17px;font-weight:700;letter-spacing:-0.34px;border-radius:10px;padding:17px 44px;text-decoration:none;box-shadow:0 10px 30px rgba(250,103,129,0.35);transition:all .25s}
.tvring-cta:hover{transform:translateY(-2px);box-shadow:0 14px 36px rgba(250,103,129,0.45)}
.tvring-stage{position:relative;max-width:1500px;margin:74px auto 0;height:540px}
.tvring-videos{position:absolute;left:50%;top:26px;transform:translateX(-50%);display:flex;width:740px;border-radius:16px;overflow:hidden;box-shadow:0 24px 70px rgba(31,31,35,0.16)}
.tvring-vt{position:relative;width:50%;height:430px}
.tvring-vt video{width:100%;height:100%;object-fit:cover;display:block}
.tvring-tag{position:absolute;left:0;bottom:0;background:#1f1f23e0;color:#fff;font-size:17px;font-weight:600;letter-spacing:-0.34px;padding:9px 20px;border-radius:0 10px 0 0}
.tvring-card{position:absolute;border-radius:18px}
.tvc-satis{left:14%;top:60px;width:222px;height:196px;background:linear-gradient(160deg,#fa6781,#ff9db0);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;box-shadow:0 18px 50px rgba(250,103,129,0.30)}
.tvc-satis .l{font-size:16.5px;font-weight:700;color:#fff}
.tvc-satis .n{font-size:56px;font-weight:900;color:#fff;letter-spacing:-1.1px;line-height:1}
.tvc-satis .n i{font-style:normal;font-size:30px;font-weight:800}
.tvc-arrow{left:9.5%;top:305px;width:152px;height:152px;background:#ffe3ea;display:flex;align-items:center;justify-content:center}
.tvc-arrow svg{width:74px;height:74px}
.tvc-thumb{left:20%;top:245px;width:158px;height:238px;overflow:hidden;box-shadow:0 18px 44px rgba(31,31,35,0.22);z-index:3}
.tvc-thumb img{width:100%;height:100%;object-fit:cover;display:block}
.tvc-thumb span{position:absolute;left:0;right:0;bottom:0;padding:12px 14px;background:linear-gradient(0deg,#1f1f23d9,transparent);color:#fff;font-size:14px;font-weight:700;line-height:1.4}
.tvc-thumb span small{display:block;font-size:11.5px;font-weight:500;color:#ffffffb3;margin-top:2px}
.tvc-prof{right:16.5%;top:0;width:196px;background:#fff;box-shadow:0 18px 50px rgba(31,31,35,0.14);padding:12px;z-index:3}
.tvc-prof img{width:100%;height:172px;object-fit:cover;border-radius:12px;display:block}
.tvc-prof b{display:block;font-size:15.5px;font-weight:800;color:#26262b;margin:12px 2px 0;letter-spacing:-0.31px}
.tvc-prof small{display:block;font-size:12.5px;color:#8c8c92;margin:4px 2px 0;letter-spacing:-0.25px}
.tvc-prof .chips{display:flex;gap:5px;margin:10px 2px 4px}
.tvc-prof .chips span{font-size:11px;font-weight:700;color:#fa6781;background:#fff0f3;border-radius:6px;padding:4px 8px}
.tvc-total{right:8%;top:330px;width:330px;height:142px;background:linear-gradient(160deg,#fff0f3,#ffe3ea);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px}
.tvc-total .l{font-size:15px;font-weight:700;color:#e14e6c}
.tvc-total .n{font-size:44px;font-weight:900;color:#fa6781;letter-spacing:-0.88px;line-height:1}
.tvf1{animation:tvbob 5.2s ease-in-out infinite alternate}
.tvf2{animation:tvbob 6.1s .4s ease-in-out infinite alternate}
.tvf3{animation:tvbob 5.6s .8s ease-in-out infinite alternate}
.tvf4{animation:tvbob 5.9s .2s ease-in-out infinite alternate}
.tvf5{animation:tvbob 5.4s .6s ease-in-out infinite alternate}
@keyframes tvbob{from{transform:translateY(0)}to{transform:translateY(-12px)}}
@media (max-width:1280px){.tvc-satis{left:4%}.tvc-arrow{left:1%}.tvc-thumb{left:12%}.tvc-prof{right:5%}.tvc-total{right:1%}}
@media (max-width:1023px){.tvring{padding:64px 20px 60px}.tvring-head h1{font-size:30px}.tvring-sub{font-size:15px}.tvring-cta{font-size:15.5px;padding:14px 34px}
.tvring-stage{height:auto;margin-top:44px}.tvring-videos{position:static;transform:none;width:100%;max-width:520px;margin:0 auto}.tvring-vt{height:300px}
.tvc-arrow,.tvc-thumb,.tvc-prof{display:none}
.tvc-satis{position:static;width:auto;height:auto;flex-direction:row;justify-content:center;gap:12px;padding:16px;margin:14px auto 0;max-width:520px}
.tvc-satis .n{font-size:34px}
.tvc-total{position:static;width:auto;height:auto;padding:16px;margin:12px auto 0;max-width:520px}
.tvc-total .n{font-size:32px}}
</style>
<div class="tvring-head" REVEAL>
<h1>해외 마케팅은 실전처럼.<br>검증된 인플루언서와의 <em>1:1 맞춤 마케팅</em></h1>
<p class="tvring-sub">제품 판매부터 매장 손님까지 만드는<br>사장님을 위한 인플루언서 마케팅, 트래비티</p>
<a class="tvring-cta" href="./inquiry.html">트래비티 시작하기</a>
</div>
<div class="tvring-stage" REVEAL>
<div class="tvring-card tvc-satis tvf1"><span class="l">재계약율</span><span class="n">''' + cnt('70%+') + '''</span></div>
<div class="tvring-card tvc-arrow tvf2"><svg viewBox="0 0 24 24" fill="none"><path d="M5 19L19 5M19 5H9M19 5V15" stroke="#fa6781" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
<div class="tvring-card tvc-thumb tvf3"><img src="./images/landing/home/hero/6.png" alt=""/><span>뷰티 세럼 캠페인<small>베트남 틱톡</small></span></div>
<div class="tvring-videos"><div class="tvring-vt"><video src="./videos/landing/home/1.mp4" autoplay muted loop playsinline></video><span class="tvring-tag">Influencer</span></div><div class="tvring-vt"><video src="./videos/landing/home/2.mp4" autoplay muted loop playsinline></video><span class="tvring-tag">Live Review</span></div></div>
<div class="tvring-card tvc-prof tvf4"><img src="./images/landing/home/hero/1.png" alt=""/><b>@beauty.linh</b><small>Beauty Creator · 팔로워 32만</small><div class="chips"><span>VN 틱톡</span><span>뷰티</span></div></div>
<div class="tvring-card tvc-total tvf5"><span class="l">누적 콘텐츠 조회수</span><span class="n">''' + cnt('2,800,000+') + '''</span></div>
</div></section>'''
hero = hero.replace('REVEAL', reveal)

s = s[:sec_start] + hero + s[pick_start:]
open('index.html', 'w', encoding='utf-8').write(s)
print('ringle hero applied; size', len(s))
