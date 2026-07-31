# -*- coding: utf-8 -*-
"""
help.html -> GitBook(docs.salesmap.kr) 스타일 '트래비티 가이드북' 재구축
- 사이트 헤더/푸터 유지, 그 사이 = 검색바 + 좌측 사이드바 트리 + 본문 아티클(해시 라우팅)
- 콘텐츠 데이터는 _build_help.py 에서 그대로 임포트(TOPICS/STEPS/CONSULT/COMMON_FAQ/GLOSSARY)
재실행 가능. 백업: help.html.bak_predocs
"""
import io, os, re, shutil, importlib.util

os.chdir(r"C:\Users\이건희\creplanet-clone")
spec = importlib.util.spec_from_file_location('bh', '_build_help.py')
bh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bh)

PINK = '#fa6781'

CSS = """
<style>
.tvdoc-sw{background:#fff;border-bottom:1px solid #ececf0;padding:14px 20px}
.tvdoc-sw-in{max-width:680px;margin:0 auto;display:flex;align-items:center;gap:10px;background:#f4f4f6;border-radius:10px;padding:11px 16px}
.tvdoc-sw-in svg{width:16px;height:16px;stroke:#9a9aa2;fill:none;stroke-width:2;stroke-linecap:round;flex:none}
.tvdoc-sw-in input{flex:1;border:none;background:none;outline:none;font-size:14.5px;font-family:inherit;color:#26262b;letter-spacing:-0.29px}
.tvdoc-sw-in kbd{flex:none;font-size:11.5px;color:#9a9aa2;background:#fff;border:1px solid #e5e5ea;border-radius:6px;padding:3px 7px;font-family:inherit}
.tvdoc{display:flex;max-width:1480px;margin:0 auto;align-items:flex-start;word-break:keep-all}
.tvdoc-side{width:288px;flex:none;position:sticky;top:57px;max-height:calc(100vh - 57px);overflow-y:auto;padding:30px 18px 60px;border-right:1px solid #ececf0}
.tvdoc-g{margin-bottom:26px}
.tvdoc-g>span{display:flex;align-items:center;gap:8px;font-size:12.5px;font-weight:800;color:#26262b;letter-spacing:-0.25px;padding:0 12px;margin-bottom:8px}
.tvdoc-g>span svg{width:15px;height:15px;stroke:#fa6781;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.tvdoc-g a{display:flex;align-items:center;gap:8px;font-size:14px;color:#595959;text-decoration:none;padding:8px 12px;border-radius:8px;letter-spacing:-0.28px}
.tvdoc-g a:hover{background:#f7f7f9;color:#26262b}
.tvdoc-g a.on{background:#fff0f4;color:#fa6781;font-weight:700}
.tvdoc-g a .mk{margin-left:auto;font-size:10.5px;font-weight:700;color:#b3b3ba;letter-spacing:0}
.tvdoc-g a.on .mk{color:#ffb8c6}
.tvdoc-g a .ext{margin-left:auto;color:#c9c9cf;font-size:12px}
.tvdoc-main{flex:1;min-width:0;padding:44px 60px 90px}
.tvdoc-art{display:none;max-width:760px;margin:0 auto}
.tvdoc-art.on{display:block;animation:tvdocin .35s ease}
@keyframes tvdocin{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.tvdoc-bc{font-size:13px;color:#9a9aa2;letter-spacing:-0.26px;margin-bottom:18px}
.tvdoc-bc b{color:#fa6781;font-weight:700}
.tvdoc-hero{background:#111114;border-radius:14px;padding:64px 30px;text-align:center;margin-bottom:34px}
.tvdoc-hero p{font-size:15px;color:#b9b9c0;letter-spacing:-0.3px;margin:0}
.tvdoc-hero p b{color:#fff}
.tvdoc-hero h2{font-size:52px;font-weight:900;color:#fff;letter-spacing:-1px;margin:10px 0 0}
.tvdoc-art h1{font-size:36px;font-weight:800;color:#1f1f1f;letter-spacing:-0.72px;margin:0 0 6px}
.tvdoc-art h1 em{font-style:normal;font-size:16px;font-weight:700;color:#b3b3ba;margin-left:10px;letter-spacing:0.5px}
.tvdoc-mkt{display:inline-block;font-size:12.5px;font-weight:700;color:#fa6781;background:#fff0f4;border-radius:99px;padding:5px 12px;margin:8px 0 0}
.tvdoc-hr{height:1px;background:#ececf0;border:none;margin:24px 0 26px}
.tvdoc-art p.lead{font-size:16px;line-height:1.85;color:#434343;letter-spacing:-0.32px;margin:0 0 8px}
.tvdoc-cards{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:28px}
.tvdoc-card{display:block;border:1px solid #ececf0;border-radius:12px;padding:22px 24px;text-decoration:none;transition:all .2s}
.tvdoc-card:hover{border-color:#ffb8c6;box-shadow:0 8px 26px rgba(250,103,129,.10)}
.tvdoc-card b{display:block;font-size:15.5px;font-weight:800;color:#26262b;letter-spacing:-0.31px}
.tvdoc-card small{display:block;font-size:13.5px;color:#8c8c92;margin-top:6px;line-height:1.6;letter-spacing:-0.27px}
.tvdoc-tbl{width:100%;border-collapse:collapse;margin:6px 0 4px}
.tvdoc-tbl th{width:150px;text-align:left;font-size:13.5px;font-weight:700;color:#8c8c92;padding:13px 0;vertical-align:top;letter-spacing:-0.27px;border-bottom:1px solid #f3f3f5}
.tvdoc-tbl td{font-size:14.5px;color:#26262b;padding:13px 0;line-height:1.65;letter-spacing:-0.29px;border-bottom:1px solid #f3f3f5}
.tvdoc-tbl tr:last-child th,.tvdoc-tbl tr:last-child td{border-bottom:none}
.tvdoc-tbl td b{color:#fa6781}
.tvdoc-fit{display:flex;gap:6px;flex-wrap:wrap}
.tvdoc-fit span{font-size:12.5px;font-weight:600;color:#595959;background:#f4f4f6;border-radius:99px;padding:5px 11px}
.tvdoc-h3{font-size:19px;font-weight:800;color:#1f1f1f;letter-spacing:-0.38px;margin:38px 0 6px}
details.tvdoc-q{border-bottom:1px solid #f3f3f5}
details.tvdoc-q summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:14px;padding:16px 2px;font-size:15px;font-weight:700;color:#26262b;letter-spacing:-0.3px}
details.tvdoc-q summary::-webkit-details-marker{display:none}
details.tvdoc-q summary::after{content:'+';font-size:18px;color:#c9c9cf;font-weight:400;flex:none;transition:transform .2s}
details.tvdoc-q[open] summary::after{transform:rotate(45deg);color:#fa6781}
details.tvdoc-q .a{padding:0 2px 18px;font-size:14.5px;line-height:1.8;color:#595959;letter-spacing:-0.29px}
details.tvdoc-q .a b{color:#fa6781}
.tvdoc-dl div{padding:16px 2px;border-bottom:1px solid #f3f3f5}
.tvdoc-dl dt{font-size:15px;font-weight:800;color:#26262b;letter-spacing:-0.3px}
.tvdoc-dl dd{margin:6px 0 0;font-size:14.5px;line-height:1.75;color:#595959;letter-spacing:-0.29px}
.tvdoc-step{display:flex;gap:18px;padding:18px 2px;border-bottom:1px solid #f3f3f5}
.tvdoc-step i{font-style:normal;flex:none;width:30px;height:30px;border-radius:50%;background:#fff0f4;color:#fa6781;font-size:13px;font-weight:800;display:flex;align-items:center;justify-content:center}
.tvdoc-step b{display:block;font-size:15.5px;font-weight:800;color:#26262b;letter-spacing:-0.31px}
.tvdoc-step p{margin:5px 0 0;font-size:14.5px;line-height:1.7;color:#595959;letter-spacing:-0.29px}
.tvdoc-go{display:inline-block;margin-top:26px;font-size:14.5px;font-weight:700;color:#fa6781;text-decoration:none;letter-spacing:-0.29px}
.tvdoc-go:hover{text-decoration:underline}
.tvdoc-help{margin-top:52px;padding-top:22px;border-top:1px solid #ececf0;display:flex;align-items:center;gap:14px;font-size:13.5px;color:#8c8c92}
.tvdoc-help button{border:1px solid #e5e5ea;background:#fff;border-radius:99px;width:34px;height:34px;font-size:16px;cursor:pointer;transition:all .15s}
.tvdoc-help button:hover{border-color:#ffb8c6;transform:scale(1.08)}
@media (max-width:1023px){.tvdoc{flex-direction:column}.tvdoc-side{position:static;width:100%;max-height:none;border-right:none;border-bottom:1px solid #ececf0;padding:20px 16px}.tvdoc-main{padding:30px 20px 60px}.tvdoc-hero h2{font-size:34px}.tvdoc-art h1{font-size:26px}.tvdoc-cards{grid-template-columns:1fr}.tvdoc-tbl th{width:104px}}
</style>
"""

IC = {
 'start': '<svg viewBox="0 0 24 24"><path d="M12 3l2.2 5.8L20 11l-5.8 2.2L12 19l-2.2-5.8L4 11l5.8-2.2z"/></svg>',
 'ch': '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M10 9.5l4.5 2.5L10 14.5z"/></svg>',
 'flow': '<svg viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h10"/></svg>',
 'sup': '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 114.1 1.9c-.8.7-1.6 1.1-1.6 2.1"/><path d="M12 16.5h.01"/></svg>',
}

def esc_id(k): return 't-' + k

# ── 사이드바
def sidebar():
    g1 = ('<div class="tvdoc-g"><span>' + IC['start'] + '시작하기</span>'
          '<a href="#welcome" data-art="welcome" class="on">Welcome</a>'
          '<a href="#glossary" data-art="glossary">필수 용어 사전</a></div>')
    ch = ''.join(f'<a href="#{esc_id(t["key"])}" data-art="{esc_id(t["key"])}">{t["name"]}<span class="mk">{t["market"]}</span></a>' for t in bh.TOPICS)
    g2 = '<div class="tvdoc-g"><span>' + IC['ch'] + '채널 가이드</span>' + ch + '</div>'
    g3 = ('<div class="tvdoc-g"><span>' + IC['flow'] + '진행 안내</span>'
          '<a href="#flow" data-art="flow">이용 흐름</a>'
          '<a href="#consult" data-art="consult">상담에서 확정하는 항목</a></div>')
    g4 = ('<div class="tvdoc-g"><span>' + IC['sup'] + '지원</span>'
          '<a href="#faq" data-art="faq">자주 묻는 질문</a>'
          '<a href="./agency.html">공식대행사<span class="ext">&#8599;</span></a>'
          '<a href="./inquiry.html">문의하기<span class="ext">&#8599;</span></a></div>')
    return '<aside class="tvdoc-side">' + g1 + g2 + g3 + g4 + '</aside>'

def helpful():
    return ('<div class="tvdoc-help"><span>도움이 되었나요?</span>'
            '<button type="button" onclick="this.parentNode.innerHTML=\'<span>답변 감사합니다! 더 궁금한 점은 문의하기로 남겨주세요.</span>\'">&#128522;</button>'
            '<button type="button" onclick="this.parentNode.innerHTML=\'<span>답변 감사합니다! 부족한 부분은 계속 채워가겠습니다.</span>\'">&#128533;</button></div>')

def art(aid, group, inner, on=False):
    return (f'<article class="tvdoc-art{" on" if on else ""}" id="{aid}">'
            f'<p class="tvdoc-bc"><b>트래비티 가이드북</b> &rsaquo; {group}</p>' + inner + helpful() + '</article>')

# ── Welcome
first_topic = esc_id(bh.TOPICS[0]['key'])
welcome = art('welcome', '시작하기',
 '<div class="tvdoc-hero"><p>사장님을 위한 해외 인플루언서 마케팅 가이드, <b>트래비티</b></p><h2>TREVITY</h2></div>'
 '<h1>Welcome</h1><hr class="tvdoc-hr"/>'
 '<p class="lead">인플루언서 마케팅이 처음이신 분들을 위한 기초 안내부터, 채널별 비용과 진행 방식까지. 이 가이드북 하나로 트래비티의 모든 서비스를 파악하실 수 있습니다.</p>'
 '<p class="lead">왼쪽 목차에서 궁금한 채널을 고르시거나, 아래에서 시작해 보세요.</p>'
 f'<div class="tvdoc-cards"><a class="tvdoc-card" href="#{first_topic}" data-art="{first_topic}"><b>채널 가이드 보기</b><small>틱톡부터 네이버 블로그까지, 채널별 비용과 진행 방식을 안내합니다.</small></a>'
 '<a class="tvdoc-card" href="#glossary" data-art="glossary"><b>필수 용어 사전</b><small>KOL, 시딩, 어필리에이트 — 상담 전에 알아두면 좋은 용어들입니다.</small></a></div>', on=True)

# ── 용어사전
gl = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in bh.GLOSSARY)
glossary = art('glossary', '시작하기',
 '<h1>필수 용어 사전</h1><hr class="tvdoc-hr"/>'
 '<p class="lead">상담에서 자주 나오는 용어들입니다. 몰라도 진행에는 문제 없지만, 알고 계시면 대화가 빨라집니다.</p>'
 '<dl class="tvdoc-dl">' + gl + '</dl>')

# ── 채널 아티클
def topic_art(t):
    fit = '<div class="tvdoc-fit">' + ''.join(f'<span>{x}</span>' for x in t['fit']) + '</div>'
    period = t['period'] if t['period'] else '상담 시 안내'
    cost = t['cost'] if t['cost'] else '상담 시 안내'
    rows = (f'<tr><th>이런 제품 · 매장</th><td>{fit}</td></tr>'
            f'<tr><th>콘텐츠</th><td>{t["content"]}</td></tr>'
            f'<tr><th>노출되는 곳</th><td>{t["reach"]}</td></tr>'
            f'<tr><th>비용</th><td>{cost}</td></tr>'
            f'<tr><th>진행 기간</th><td>{period}</td></tr>')
    faq = ''.join(f'<details class="tvdoc-q"><summary>{q}</summary><div class="a">{a}</div></details>' for q, a in t['faq'])
    inner = (f'<h1>{t["name"]}<em>{t["en"]}</em></h1><span class="tvdoc-mkt">{t["market"]} 시장</span><hr class="tvdoc-hr"/>'
             f'<p class="lead">{t["lead"]}</p>'
             '<h3 class="tvdoc-h3">한눈에 보기</h3><table class="tvdoc-tbl">' + rows + '</table>'
             '<h3 class="tvdoc-h3">자주 묻는 질문</h3>' + faq
             + f'<a class="tvdoc-go" href="{t["link"]}">이 채널로 진행하기 &#8594;</a>')
    return art(esc_id(t['key']), '채널 가이드', inner)

topics_html = ''.join(topic_art(t) for t in bh.TOPICS)

# ── 이용 흐름
st = ''.join(f'<div class="tvdoc-step"><i>{n+1}</i><div><b>{a}</b><p>{b}</p></div></div>' for n, (a, b) in enumerate(bh.STEPS))
flow = art('flow', '진행 안내',
 '<h1>이용 흐름</h1><hr class="tvdoc-hr"/>'
 '<p class="lead">문의부터 결과 리포트까지, 모든 진행은 트래비티 담당 매니저가 챙깁니다.</p>' + st)

# ── 상담 확정 항목
cs = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in bh.CONSULT)
consult = art('consult', '진행 안내',
 '<h1>상담에서 확정하는 항목</h1><hr class="tvdoc-hr"/>'
 '<p class="lead">아래 항목들은 제품과 상황에 따라 달라져서, 일괄 안내 대신 상담에서 명확한 기준으로 정해 드립니다. 상담 전에 미리 생각해 오시면 진행이 빨라집니다.</p>'
 '<dl class="tvdoc-dl">' + cs + '</dl>')

# ── 공통 FAQ
fq = ''.join(f'<details class="tvdoc-q"><summary>{q}</summary><div class="a">{a}</div></details>' for q, a in bh.COMMON_FAQ)
faq = art('faq', '지원',
 '<h1>자주 묻는 질문</h1><hr class="tvdoc-hr"/>'
 '<p class="lead">채널별 질문은 각 채널 가이드에, 공통 질문은 여기에 모았습니다.</p>' + fq
 + '<a class="tvdoc-go" href="./inquiry.html">더 궁금한 점 문의하기 &#8594;</a>')

SEARCH = ('<div class="tvdoc-sw"><div class="tvdoc-sw-in">'
 '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>'
 '<input id="tvdoc-q" type="text" placeholder="Ask or search..." autocomplete="off"/>'
 '<kbd>Ctrl K</kbd></div></div>')

JS = """
<script>
(function(){
  var links=document.querySelectorAll('[data-art]');
  var arts=document.querySelectorAll('.tvdoc-art');
  function show(id){
    var t=document.getElementById(id); if(!t) return;
    arts.forEach(function(a){a.classList.toggle('on',a.id===id)});
    document.querySelectorAll('.tvdoc-side a').forEach(function(l){l.classList.toggle('on',l.dataset.art===id)});
    window.scrollTo(0,0);
  }
  links.forEach(function(l){l.addEventListener('click',function(){show(l.dataset.art)})});
  if(location.hash){var id=location.hash.slice(1);if(document.getElementById(id))show(id);}
  window.addEventListener('hashchange',function(){var id=location.hash.slice(1);if(document.getElementById(id))show(id);});
  var q=document.getElementById('tvdoc-q');
  q.addEventListener('input',function(){
    var v=q.value.trim().toLowerCase();
    document.querySelectorAll('.tvdoc-side a').forEach(function(l){
      l.style.display=(!v||l.textContent.toLowerCase().indexOf(v)>-1)?'':'none';
    });
  });
  document.addEventListener('keydown',function(e){
    if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();q.focus();}
  });
})();
</script>
"""

def main():
    src = 'help.html'
    s = io.open(src, encoding='utf-8').read()
    shutil.copy2(src, src + '.bak_predocs')
    m_head = re.search(r'</header>', s)
    m_foot = re.search(r'<footer\b', s)
    if not m_head or not m_foot:
        # 컴파일 마크업이라 <footer> 태그가 없을 수 있음 — 푸터 시작 휴리스틱
        m_foot = re.search(r'<div class="[^"]*bg-gray-90[^"]*"', s)
    body = (CSS + SEARCH + '<div class="tvdoc">' + sidebar()
            + '<main class="tvdoc-main">' + welcome + glossary + topics_html + flow + consult + faq
            + '</main></div>' + JS)
    out = s[:m_head.end()] + '\n' + body + '\n' + s[m_foot.start():]
    out = out.replace('<title>고객센터 | 트래비티</title>', '<title>트래비티 가이드북 | 헬프센터</title>')
    io.open(src, 'w', encoding='utf-8').write(out)
    print('done. 채널', len(bh.TOPICS), '| size', len(out))

if __name__ == '__main__':
    main()
