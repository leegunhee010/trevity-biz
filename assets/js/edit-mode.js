/* 트래비티 화면 편집 모드 — edit-server.py(:5723)가 주입한다.
   켜면 텍스트에 마우스를 올려 클릭 → 그 자리에서 수정 → 포커스 빠지면 HTML 파일에 바로 저장.
   같은 문구가 페이지 안에 여러 번(모바일/PC 중복 스팬) 있으면 전부 함께 바뀐다. */
(function(){
  /* 편집 UI는 관리자가 의도적으로 연 세션에서만 노출:
     ?edit=1 로 진입하면 세션 내내 유지, 편집 끄기+ESC 로 세션 종료.
     (일반 방문 화면에는 아무것도 안 보임) */
  if(window.__tvedit_loaded) return;   // 서버 주입 + 로더 중복 방지
  window.__tvedit_loaded = 1;
  if(/[?&]edit=1/.test(location.search)) sessionStorage.setItem('tvedit_sess', '1');
  if(sessionStorage.getItem('tvedit_sess') !== '1') return;

  /* 저장 방식:
     - 편집 서버(localhost:5723)로 열었을 때 → HTML 파일에 직접 굽기 (정적)
     - 그 외(라이브·:5695 등, 수파베이스 연결 시) → site_copy 오버라이드 저장 → 전 페이지 즉시 반영
       (관리자 로그인 필요 — /admin/ 에서 로그인한 세션이 공유됨) */
  const BAKE_MODE = location.hostname === 'localhost' && location.port === '5723';
  const SB_OK = () => typeof TV_BACKEND !== 'undefined' && TV_BACKEND === 'supabase'
                   && typeof TvData !== 'undefined';
  const sbAdmin = () => SB_OK() && TvData.admin;

  /* ---------- GitHub 직접 굽기 (라이브에서 저장 = HTML 커밋) ----------
     관리자 설정에서 토큰을 넣어두면 site_copy(JS 오버라이드) 대신
     GitHub API로 HTML 파일에 바로 커밋한다 → 깜빡임 없음, AI가 새 카피를 읽음. */
  const GH = { owner: 'leegunhee010', repo: 'trevity-biz', branch: 'main' };
  const GH_PAGES = ['index','vietnam-tiktok','tourist-vn','tourist-cn','local-vn','stay',
    'experience','export','famtour','blog','help','agency','about','inquiry','coming-soon',
    'blog-post','blog-market','blog-midtier','blog-diy','blog-hantown'];
  const ghToken = () => localStorage.getItem('tv_gh_token') || '';
  function b64decodeUtf8(b64){
    const bin = atob(b64.replace(/\n/g, ''));
    const bytes = Uint8Array.from(bin, c => c.charCodeAt(0));
    return new TextDecoder().decode(bytes);
  }
  function b64encodeUtf8(text){
    const bytes = new TextEncoder().encode(text);
    let bin = '';
    for(let i = 0; i < bytes.length; i += 0x8000)
      bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
    return btoa(bin);
  }
  async function ghGet(path){
    const r = await fetch(`https://api.github.com/repos/${GH.owner}/${GH.repo}/contents/${path}?ref=${GH.branch}`,
      { headers: { Authorization: 'Bearer ' + ghToken(), Accept: 'application/vnd.github+json' } });
    if(r.status === 404) return null;
    if(!r.ok) throw new Error('GitHub 읽기 실패 ' + r.status + (r.status===401?' — 토큰을 확인하세요':''));
    const j = await r.json();
    return { text: b64decodeUtf8(j.content), sha: j.sha };
  }
  async function ghPut(path, content, sha, msg, isBase64){
    const body = { message: msg, branch: GH.branch, content: isBase64 ? content : b64encodeUtf8(content) };
    if(sha) body.sha = sha;
    const r = await fetch(`https://api.github.com/repos/${GH.owner}/${GH.repo}/contents/${path}`,
      { method: 'PUT', headers: { Authorization: 'Bearer ' + ghToken(), Accept: 'application/vnd.github+json',
        'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    if(!r.ok) throw new Error('GitHub 저장 실패 ' + r.status + (r.status===401?' — 토큰을 확인하세요':''));
  }
  /* reps [{old,new}] 를 현재 페이지 우선 → 전 페이지에 적용. 바뀐 파일명 목록 반환 */
  async function ghBake(reps, progress){
    const cur = (location.pathname.split('/').pop() || 'index.html').replace('.html','') || 'index';
    const order = [cur, ...GH_PAGES.filter(p => p !== cur)];
    const changed = [];
    for(let i = 0; i < order.length; i++){
      const path = order[i] + '.html';
      if(progress) progress(`저장 중… (${i+1}/${order.length}) ${path}`);
      let f;
      try{ f = await ghGet(path); }catch(e){ if(i===0) throw e; continue; }
      if(!f) continue;
      let t = f.text, hits = 0;
      for(const rep of reps){
        for(const o of [rep.old, rep.old.replace(/<br>/g,'<br/>')]){
          const c = t.split(o).length - 1;
          if(c){ t = t.split(o).join(rep.new); hits += c; break; }
        }
      }
      if(hits){
        await ghPut(path, t, f.sha, `copy: 화면편집 — ${path} (${hits}곳)`);
        changed.push(path + ':' + hits);
      }
      // 첫(현재) 페이지에서 전부 반영됐고 공유 문구가 아니면 조기 종료 판단이 어려우니 전체 스캔 유지
    }
    return changed;
  }

  const TAGS = 'h1,h2,h3,h4,h5,h6,p,span,a,b,strong,em,small,li,td,th,button,div,label,summary,figcaption,blockquote,i,u';
  let on = false;
  let editing = null;   // { el, origNorm, group: [{el, origOuter}] }

  /* ---------- 편집 대상 판정 ----------
     순수 텍스트뿐 아니라 색상 강조 <span>·<b>·<br> 등 인라인 자식을 품은
     제목/문장도 편집 가능 (강조 스팬 있는 히어로 제목이 클릭 안 되던 문제). */
  const INLINE = { BR:1, B:1, STRONG:1, EM:1, I:1, U:1, SPAN:1, MARK:1, SMALL:1, A:1, SUB:1, SUP:1, TIME:1, DEL:1, INS:1 };
  function allInline(el){
    for(const c of el.children){
      if(!INLINE[c.tagName]) return false;
      if(!allInline(c)) return false;
    }
    return true;
  }
  function tvText(el){
    // 인라인 자식 포함 전체 텍스트를 <br>=\n 규칙으로 정규화
    const parts = [];
    (function walk(n){
      for(const c of n.childNodes){
        if(c.nodeType === 3) parts.push(c.nodeValue);
        else if(c.nodeType === 1){
          if(c.tagName === 'BR') parts.push('\n');
          else walk(c);
        }
      }
    })(el);
    const t = parts.join('').split('\n').map(ln=>ln.replace(/\s+/g,' ').trim()).join('\n').trim();
    return t || null;
  }
  function isTarget(el){
    if(!el || !el.matches || !el.matches(TAGS)) return false;
    if(el.closest('#tvedit-bar')) return false;
    if(el.querySelector && el.querySelector('svg,img,video,iframe,input,select,textarea,button')) return false;
    if(!allInline(el)) return false;
    // 부모가 이미 편집 대상이면 부모(줄 전체)를 잡는다 → 중첩 편집 방지
    const t = tvText(el);
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
  body.tvedit-on img:hover{outline:2px dashed #4a9eff;outline-offset:2px;cursor:pointer}
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
    document.body.classList.toggle('tvedit-on', on);
    if(on) say('문구를 클릭해 수정, 이미지를 클릭해 교체하세요. 저장은 파일에 바로 반영됩니다.', 5200);
    else {
      if(editing) finish(false); clearHl();
      // 편집 끄기 = 편집 세션 종료 → 일반 화면으로 (버튼도 사라짐)
      sessionStorage.removeItem('tvedit_sess');
      bar.remove();
    }
  }

  /* ---------- 이미지·영상·배경 교체 ----------
     대상: <img src>, <video src/poster>, style="background-image:url(...)" 인 요소.
     교체하면 같은 주소를 쓰는 모든 페이지 파일에 반영된다. */
  function bgUrl(el){
    const st = el.getAttribute && el.getAttribute('style');
    if(!st) return null;
    const m = st.match(/background(?:-image)?\s*:[^;]*url\(\s*['"]?([^'")]+)['"]?\s*\)/);
    return m ? m[1] : null;
  }
  function mediaTarget(el){
    // 클릭 지점에서 위로 올라가며 img/video/배경이미지 요소를 찾는다
    let cur = el;
    for(let i=0; cur && cur !== document.body && i < 5; i++){
      if(cur.tagName === 'IMG' && cur.getAttribute('src') && cur.getAttribute('src').indexOf('data:') !== 0)
        return { el: cur, kind: 'img', src: cur.getAttribute('src') };
      if(cur.tagName === 'VIDEO')
        return { el: cur, kind: 'video', src: cur.getAttribute('src'), poster: cur.getAttribute('poster') };
      const b = bgUrl(cur);
      if(b && b.indexOf('data:') !== 0) return { el: cur, kind: 'bg', src: b };
      cur = cur.parentElement;
    }
    return null;
  }
  function sendReplace(oldSrc, file, after){
    const fr = new FileReader();
    fr.onload = async () => {
      say('저장 중…', 12000);
      try{
        const page = location.pathname.replace(/^\//,'') || 'index.html';
        const r = await fetch('/api/image-replace', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ page, oldSrc, image: { name: file.name, data: fr.result } }),
        });
        const j = await r.json();
        if(j.ok){ after(j.newSrc); say(`✅ 교체됨 — ${(j.files||[]).length}개 파일 반영`); }
        else say('⚠️ 교체 실패: ' + (j.error || '파일에서 원본 주소를 찾지 못했습니다'), 6000);
      }catch(err){ say('⚠️ 교체 실패: ' + (err.message||err), 6000); }
    };
    fr.readAsDataURL(file);
  }
  function pickFile(accept, cb){
    const inp = document.createElement('input');
    inp.type = 'file'; inp.accept = accept;
    inp.onchange = () => { if(inp.files && inp.files[0]) cb(inp.files[0]); };
    inp.click();
  }
  function replaceMedia(t){
    /* 라이브 모드 이미지: GitHub 토큰 있으면 저장소에 업로드+src 커밋, 없으면 Storage+오버라이드 */
    if(!BAKE_MODE){
      if(t.kind !== 'img'){ say('영상·배경 교체는 로컬 화면 편집(편집서버-시작.bat)에서 지원됩니다.', 5000); return; }
      if(ghToken()){
        pickFile('image/*', f => {
          const fr = new FileReader();
          fr.onload = async () => {
            try{
              say('이미지 커밋 중…', 20000);
              const ext = (f.name.match(/\.\w+$/) || ['.jpg'])[0].toLowerCase();
              const name = 'rp_' + Date.now().toString(36) + ext;
              await ghPut('images/uploads/' + name, fr.result.split(',')[1], null, 'img: 화면편집 업로드 ' + name, true);
              const oldSrc = t.el.getAttribute('src');
              const orig = t.el.outerHTML;
              t.el.src = './images/uploads/' + name;
              const changed = await ghBake([{ old: orig, new: t.el.outerHTML }], m => say(m, 20000));
              say(changed.length ? `✅ 이미지 HTML에 커밋됨 — ${changed.join(', ')}` :
                  '⚠️ 파일에서 원본 이미지를 찾지 못했습니다', 7000);
            }catch(err){ say('⚠️ ' + (err.message||err), 7000); }
          };
          fr.readAsDataURL(f);
        });
        return;
      }
      if(!sbAdmin()){ say('⚠️ 이미지 교체는 관리자 로그인이 필요합니다 — /admin/ 에서 로그인하세요.', 6000); return; }
      pickFile('image/*', f => {
        say('업로드 중…', 12000);
        TvImg.save(f).then(async r => {
          const origSrc = (t.el.dataset.tvimgk || ('img:' + t.el.getAttribute('src'))).replace(/^img:/, '');
          await Admin.setCopy('img:' + origSrc, r.ref);
          t.el.src = r.ref;
          t.el.dataset.tvimgk = 'img:' + origSrc;
          say('✅ 이미지 교체됨(임시) — GitHub 토큰을 넣으면 HTML에 바로 박힙니다.');
        }).catch(err => say('⚠️ 업로드 실패: ' + (err.message||err), 6000));
      });
      return;
    }
    if(t.kind === 'img'){
      pickFile('image/*', f => sendReplace(t.src, f, ns => { t.el.src = ns; }));
      return;
    }
    if(t.kind === 'bg'){
      pickFile('image/*', f => sendReplace(t.src, f, ns => {
        t.el.style.backgroundImage = "url('" + ns + "')";
      }));
      return;
    }
    if(t.kind === 'video'){
      // 포스터/영상 중 선택
      const what = t.poster ? (confirm('확인 = 영상(mp4) 교체 / 취소 = 썸네일(포스터) 교체') ? 'src' : 'poster') : 'src';
      if(what === 'src'){
        pickFile('video/mp4,video/webm', f => {
          if(f.size > 40*1024*1024){ say('⚠️ 영상은 40MB 이하만 가능합니다', 5000); return; }
          sendReplace(t.src, f, ns => { t.el.src = ns; t.el.load && t.el.load(); });
        });
      } else {
        pickFile('image/*', f => sendReplace(t.poster, f, ns => { t.el.poster = ns; }));
      }
    }
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
    // 텍스트 leaf 우선, 아니면 이미지·영상·배경
    let el = e.target;
    while(el && el !== document.body){
      if(isTarget(el)) break;
      el = el.parentElement;
    }
    if(el && el !== document.body){
      e.preventDefault(); e.stopPropagation();
      start(el);
      return;
    }
    const mt = mediaTarget(e.target);
    if(mt){
      e.preventDefault(); e.stopPropagation();
      replaceMedia(mt);
    }
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
    c.removeAttribute('data-tvck');
    c.removeAttribute('data-tvimgk');
    c.classList.remove('tvedit-hl','tvedit-live');
    if(c.getAttribute('class') === '') c.removeAttribute('class');
    return c.outerHTML;
  }
  function start(el){
    clearHl();
    if(!BAKE_MODE && !sbAdmin() && !ghToken()){
      say('⚠️ 저장하려면 관리자 로그인이 필요합니다 — /admin/ 에서 로그인 후 다시 열어주세요.', 6000);
      return;
    }
    const origNorm = tvText(el);
    const origInner = el.innerHTML;
    // 재편집이면 applyCopy가 태그해둔 원래 키를 사용 (원문이 이미 오버라이드된 상태)
    const copyKey = el.dataset.tvck || tvCopyKey(origNorm);
    // 같은 문구+같은 마크업의 쌍둥이(모바일/PC 중복)만 함께 수정 — 편집 전에 원본 캡처
    const group = [];
    document.body.querySelectorAll(TAGS).forEach(x => {
      if(x === el || (isTarget(x) && tvText(x) === origNorm && x.innerHTML === origInner))
        group.push({ el: x, origOuter: cleanOuter(x) });
    });
    if(!group.some(g => g.el === el)) group.push({ el, origOuter: cleanOuter(el) });
    editing = { el, origNorm, copyKey, group };
    el.classList.add('tvedit-live');
    el.setAttribute('contenteditable', 'true');
    el.focus();
  }
  async function finish(save){
    const ed = editing; editing = null;
    const el = ed.el;
    el.removeAttribute('contenteditable');
    el.classList.remove('tvedit-live');
    const newNorm = tvText(el);
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

    /* 라이브 모드: GitHub 토큰이 있으면 HTML에 바로 커밋(깜빡임 없음),
       없으면 site_copy 오버라이드(즉시 반영되지만 JS 스왑) */
    if(!BAKE_MODE){
      if(ghToken()){
        try{
          const changed = await ghBake(reps, m => say(m, 20000));
          if(changed.length){
            say(`✅ HTML에 커밋됨 — ${changed.join(', ')} (라이브 반영 1~2분)`);
          } else {
            say('⚠️ 파일에서 원문을 찾지 못했습니다 — 새로고침(Ctrl+F5) 후 다시 수정해 보세요.', 7000);
          }
        }catch(err){
          say('⚠️ ' + (err.message||err), 7000);
        }
        return;
      }
      try{
        const tmp = document.createElement('div'); tmp.innerHTML = newHTML;
        // 편집기 잔여 속성 정리 후 HTML 그대로 저장 (강조 스팬 유지)
        tmp.querySelectorAll('[contenteditable]').forEach(x=>x.removeAttribute('contenteditable'));
        await Admin.setCopy(ed.copyKey, 'HTML::' + tmp.innerHTML);
        ed.group.forEach(g => { g.el.dataset.tvck = ed.copyKey; });
        say('✅ 저장됨(임시 반영) — 관리자 설정에 GitHub 토큰을 넣으면 HTML에 바로 박힙니다.');
      }catch(err){
        say('⚠️ 저장 실패: ' + (err.message||err) + ' — 관리자 로그인 상태를 확인하세요.', 6000);
      }
      return;
    }

    try{
      const page = location.pathname.replace(/^\//,'') || 'index.html';
      const r = await fetch('/api/bake', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ page, replacements: reps }),
      });
      const j = await r.json();
      const files = j.files || [];
      if(j.ok && files.length){
        const label = files.length === 1
          ? `${files[0].file} (${files[0].n}곳)`
          : `${files.length}개 파일 · 총 ${files.reduce((s,f)=>s+f.n,0)}곳`;
        say(`✅ 저장됨 — ${label} HTML에 반영`);
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
