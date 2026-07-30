/* 트래비티 화면 편집 모드 — edit-server.py(:5723)가 주입한다.
   켜면 텍스트에 마우스를 올려 클릭 → 그 자리에서 수정 → 포커스 빠지면 HTML 파일에 바로 저장.
   같은 문구가 페이지 안에 여러 번(모바일/PC 중복 스팬) 있으면 전부 함께 바뀐다. */
(function(){
  const TAGS = 'h1,h2,h3,h4,h5,h6,p,span,a,b,strong,em,small,li,td,th,button,div,label,summary,figcaption,blockquote,i,u';
  let on = false;
  let editing = null;   // { el, origNorm, group: [{el, origOuter}] }

  /* ---------- leaf 판정 (site-data.js 규칙과 동일) ---------- */
  function leafText(el){
    const parts = [];
    for(const c of el.childNodes){
      if(c.nodeType === 3) parts.push(c.nodeValue);
      else if(c.nodeType === 1 && c.tagName === 'BR') parts.push('\n');
      else return null;
    }
    const t = parts.join('').split('\n').map(ln=>ln.replace(/\s+/g,' ').trim()).join('\n').trim();
    return t || null;
  }
  function isTarget(el){
    if(!el || !el.matches || !el.matches(TAGS)) return false;
    if(el.closest('#tvedit-bar')) return false;
    const t = leafText(el);
    return !!t && t.length >= 1 && t.length <= 600;
  }

  /* ---------- UI ---------- */
  const css = document.createElement('style');
  css.textContent = `
  #tvedit-bar{position:fixed;right:18px;bottom:18px;z-index:99999;display:flex;gap:8px;align-items:center;
    font-family:Pretendard,-apple-system,sans-serif}
  #tvedit-bar button{border:none;border-radius:99px;padding:12px 20px;font-size:14px;font-weight:700;cursor:pointer;
    box-shadow:0 4px 18px rgba(0,0,0,.18)}
  #tvedit-toggle{background:#191F28;color:#fff}
  #tvedit-toggle.on{background:#fa6781}
  #tvedit-msg{background:#fff;border-radius:8px;padding:9px 14px;font-size:13px;color:#191F28;
    box-shadow:0 4px 14px rgba(0,0,0,.14);display:none;max-width:340px}
  .tvedit-hl{outline:2px dashed #fa6781 !important;outline-offset:2px;cursor:text !important}
  .tvedit-live{outline:2px solid #fa6781 !important;outline-offset:2px;background:#fff5f7}
  `;
  document.head.appendChild(css);

  const bar = document.createElement('div');
  bar.id = 'tvedit-bar';
  bar.innerHTML = `<span id="tvedit-msg"></span><button id="tvedit-toggle">✏️ 편집 켜기</button>`;
  document.body.appendChild(bar);
  const btn = document.getElementById('tvedit-toggle');
  const msg = document.getElementById('tvedit-msg');
  btn.onclick = () => setOn(!on);

  function say(t, ms){
    msg.textContent = t; msg.style.display = 'block';
    clearTimeout(say._t); say._t = setTimeout(()=>{ msg.style.display='none'; }, ms||2600);
  }
  function setOn(v){
    on = v;
    btn.textContent = on ? '✅ 편집 끄기' : '✏️ 편집 켜기';
    btn.classList.toggle('on', on);
    if(on) say('고칠 문구를 클릭하세요. 수정 후 바깥을 클릭하면 파일에 저장됩니다.', 5200);
    else { if(editing) finish(false); clearHl(); }
  }

  let hlEl = null;
  function clearHl(){ if(hlEl){ hlEl.classList.remove('tvedit-hl'); hlEl = null; } }
  document.addEventListener('mouseover', e => {
    if(!on || editing) return;
    clearHl();
    let el = e.target;
    // 가장 가까운 leaf 후보를 찾는다
    while(el && el !== document.body){
      if(isTarget(el)){ hlEl = el; el.classList.add('tvedit-hl'); break; }
      el = el.parentElement;
    }
  }, true);

  document.addEventListener('click', e => {
    if(!on) return;
    if(e.target.closest('#tvedit-bar')) return;
    if(editing){
      if(editing.el.contains(e.target)) return;   // 편집 중인 요소 내부 클릭은 통과
      e.preventDefault(); e.stopPropagation();
      finish(true);
      return;
    }
    let el = e.target;
    while(el && el !== document.body){
      if(isTarget(el)) break;
      el = el.parentElement;
    }
    if(!el || el === document.body) return;
    e.preventDefault(); e.stopPropagation();
    start(el);
  }, true);

  document.addEventListener('keydown', e => {
    if(!editing) return;
    if(e.key === 'Escape'){ e.preventDefault(); finish(false); }
    if(e.key === 'Enter' && !e.shiftKey && editing.el.tagName !== 'P'){ e.preventDefault(); finish(true); }
  }, true);

  /* ---------- 편집 시작/종료 ---------- */
  function cleanOuter(el){
    const c = el.cloneNode(true);
    c.removeAttribute('contenteditable');
    c.classList.remove('tvedit-hl','tvedit-live');
    if(c.getAttribute('class') === '') c.removeAttribute('class');
    return c.outerHTML;
  }
  function start(el){
    clearHl();
    const origNorm = leafText(el);
    // 같은 문구를 가진 leaf 전부 (숨겨진 모바일/PC 쌍둥이 포함) — 편집 전에 원본 캡처
    const group = [];
    document.body.querySelectorAll(TAGS).forEach(x => {
      if(leafText(x) === origNorm) group.push({ el: x, origOuter: cleanOuter(x) });
    });
    editing = { el, origNorm, group };
    el.classList.add('tvedit-live');
    el.setAttribute('contenteditable', 'plaintext-only');
    el.focus();
  }
  async function finish(save){
    const ed = editing; editing = null;
    const el = ed.el;
    el.removeAttribute('contenteditable');
    el.classList.remove('tvedit-live');
    const newNorm = leafText(el);
    if(!save || newNorm === ed.origNorm || newNorm === null){
      // 원복
      ed.group.forEach(g => { if(g.el === el){ const tmp = document.createElement('div'); tmp.innerHTML = g.origOuter; el.replaceWith(tmp.firstChild); } });
      if(!save) say('취소했습니다');
      return;
    }
    // 같은 문구 그룹 전부에 새 내용 반영
    const newHTML = el.innerHTML;
    const reps = [];
    ed.group.forEach(g => {
      if(g.el !== el) g.el.innerHTML = newHTML;
      reps.push({ old: g.origOuter, new: cleanOuter(g.el) });
    });
    say('저장 중…', 8000);
    try{
      const page = location.pathname.replace(/^\//,'') || 'index.html';
      const r = await fetch('/api/bake', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ page, replacements: reps }),
      });
      const j = await r.json();
      const okN = (j.results||[]).filter(x=>x.ok).length;
      if(j.ok && okN){
        say(`✅ 저장됨 — ${page} 파일에 반영 (${okN}곳)`);
        // 런타임 카피 오버라이드가 남아 있으면 충돌하므로 같은 키를 지운다
        try{
          const m = JSON.parse(localStorage.getItem('tv_copy_override')||'{}');
          let h = 5381; const t = ed.origNorm;
          for(let i=0;i<t.length;i++) h = ((h<<5)+h+t.charCodeAt(i))|0;
          delete m['c'+(h>>>0).toString(16)];
          localStorage.setItem('tv_copy_override', JSON.stringify(m));
        }catch(e){}
      } else {
        say('⚠️ 저장 실패 — 파일에서 원문을 찾지 못했습니다. 새로고침 후 다시 시도하세요.', 6000);
      }
    }catch(err){
      say('⚠️ 저장 실패: ' + (err.message||err), 6000);
    }
  }
})();
