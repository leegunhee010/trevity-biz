/* ============================================================
   트래비티 관리자 로직
   ============================================================ */
function esc(s){ return String(s??'').replace(/[&<>"']/g, m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m])); }
function av(id){ const el=document.getElementById(id); return el ? el.value.trim() : ''; }
function today(){ const d=new Date(); return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0'); }
function toastA(msg){
  let el=document.querySelector('.toast');
  if(!el){ el=document.createElement('div'); el.className='toast'; document.body.appendChild(el); }
  el.textContent=msg; el.classList.add('show');
  clearTimeout(el._t); el._t=setTimeout(()=>el.classList.remove('show'),2400);
}

/* ---------- 이미지 업로드 위젯 ---------- */
function imgSrc(v){ return TvImg.isRef(v) ? (TvImg.resolve(v) || '') : (v || ''); }
function uploader(id, value, opts){
  opts = opts || {};
  const v = value || '';
  const src = TvImg.isRef(v) ? TvImg.resolve(v) : v;
  return `
  <div class="upl" id="${id}-box" ondragover="uplDrag(event,1)" ondragleave="uplDrag(event,0)" ondrop="uplDrop(event,'${id}')">
    <input type="hidden" id="${id}" value="${esc(v)}">
    <div class="upl-prev" id="${id}-prev">${src?`<img src="${esc(src)}" alt="">`:`<span class="ph">이미지 없음</span>`}</div>
    <div class="upl-side">
      <div class="upl-acts">
        <button type="button" class="btn btn-primary btn-sm" onclick="document.getElementById('${id}-file').click()">파일 선택</button>
        <button type="button" class="btn btn-ghost btn-sm" onclick="uplClear('${id}')">비우기</button>
      </div>
      <input type="file" id="${id}-file" accept="image/*" hidden onchange="uplPick(this,'${id}')">
      <p class="upl-hint" id="${id}-info">${opts.hint||'파일을 끌어다 놓아도 됩니다. 자동으로 1600px·JPEG로 압축됩니다.'}</p>
      <details class="upl-url"><summary>URL로 넣기</summary>
        <input class="srch" style="width:100%;margin-top:8px" placeholder="https://..."
          value="${TvImg.isRef(v)?'':esc(v)}" onchange="uplSetUrl('${id}',this.value)"></details>
    </div>
  </div>`;
}
function uplDrag(e, on){ e.preventDefault(); e.currentTarget.classList.toggle('over', !!on); }
function uplDrop(e, id){
  e.preventDefault(); e.currentTarget.classList.remove('over');
  const f = e.dataTransfer.files && e.dataTransfer.files[0];
  if(f) uplStore(f, id);
}
function uplPick(input, id){ if(input.files[0]) uplStore(input.files[0], id); input.value=''; }
async function uplStore(file, id){
  const info = document.getElementById(id+'-info');
  if(info) info.textContent = '압축하는 중…';
  try{
    const r = await TvImg.save(file);
    document.getElementById(id).value = r.ref;
    document.getElementById(id+'-prev').innerHTML = `<img src="${r.dataUrl||r.ref}" alt="">`;
    if(info) info.textContent = `${r.w}×${r.h} · ${fmtBytes(r.bytes)} 로 저장됨`;
  }catch(err){
    if(info) info.textContent = err.message || '업로드에 실패했습니다';
    toastA(err.message || '업로드 실패');
  }
}
function uplClear(id){
  document.getElementById(id).value = '';
  document.getElementById(id+'-prev').innerHTML = `<span class="ph">이미지 없음</span>`;
  const info = document.getElementById(id+'-info');
  if(info) info.textContent = '파일을 끌어다 놓아도 됩니다.';
}
function uplSetUrl(id, url){
  const u = String(url||'').trim();
  document.getElementById(id).value = u;
  document.getElementById(id+'-prev').innerHTML = u ? `<img src="${esc(u)}" alt="">` : `<span class="ph">이미지 없음</span>`;
}

/* ---------- 운영 데이터 캐시 ---------- */
const ADM = { inqs:[] };
const isSB = () => typeof TvData !== 'undefined' && typeof TV_BACKEND !== 'undefined' && TV_BACKEND === 'supabase';

async function admDo(promise, reload){
  try{
    await promise;
    if(reload === 0){ await refreshAdm(); renderAll(); }
    else location.reload();
  }catch(e){
    console.error(e);
    toastA('저장에 실패했습니다: ' + (e.message||e));
  }
}
async function refreshAdm(){
  ADM.inqs = await Store.allInquiries() || [];
  ADM.inqs.sort((a,b)=>String(b.created_at).localeCompare(String(a.created_at)));
}

/* ---------- 로그인 ---------- */
function doAdminLogin(){
  const err = document.getElementById('gate-err');
  err.style.display = 'none';
  if(isSB()){
    const email = av('gate-email'), pw = av('gate-pw');
    if(!email){ err.textContent='관리자 이메일을 입력하세요'; err.style.display='block'; return; }
    Admin.loginEmail(email, pw).then(r=>{
      if(!r.ok){ err.textContent = r.err; err.style.display='block'; return; }
      boot();
    });
    return;
  }
  const pw = av('gate-pw');
  if(Admin.login(pw)){ boot(); }
  else { err.textContent='비밀번호가 올바르지 않습니다'; err.style.display='block'; }
}
async function boot(){
  document.getElementById('gate').classList.add('hidden');
  document.getElementById('app').classList.remove('hidden');
  try{ await TvImg.loadCache(); }catch(e){}
  try{ await refreshAdm(); }catch(e){ console.error('운영 데이터 로드 실패', e); }
  renderAll();
}

/* ---------- 사이드바 · 탭 ---------- */
const TABS = ['dash','inq','blog','board','seo','copy','settings'];
/* 로컬(편집 서버 사용 가능)에서는 정적 굽기 게시판, 라이브에서는 수파베이스 블로그 편집기 */
const IS_LOCAL_TOOLS = ['localhost','127.0.0.1'].indexOf(location.hostname) >= 0;
const NAV = [
  { id:'dash',     label:'대시보드', title:'대시보드',        desc:'문의·콘텐츠 현황 한눈에 보기' },
  { id:'inq',      label:'문의함',   title:'문의함',          desc:'inquiry.html로 들어온 문의' },
  IS_LOCAL_TOOLS
    ? { id:'board', label:'게시판',   title:'게시판 관리',      desc:'HTML 본문 → 정적 페이지 굽기' }
    : { id:'blog',  label:'블로그',   title:'블로그 관리',      desc:'글 작성·수정 — 저장 즉시 사이트 반영' },
  { id:'copy',     label:'카피',     title:'포트폴리오 · 패키지', desc:'이미지 롤과 vietnam-tiktok 패키지 가격' },
  { id:'seo',      label:'SEO',     title:'SEO 관리',        desc:'메타·구조화데이터·sitemap·플로팅버튼·메일' },
  { id:'settings', label:'설정',     title:'설정',            desc:'관리자 비밀번호와 연결 상태' },
];
let curTab = 'dash';

/* 편집 서버(:5723) 주소 — 관리자를 어느 포트로 열든 게시판/SEO는 편집 서버 API를 쓴다 */
const EDIT_ORIGIN = 'http://localhost:5723';

function renderNav(){
  const newCnt = ADM.inqs.filter(i=>i.status==='new').length;
  const counts = { inq:newCnt||'', board:TV_BLOG_POSTS.length, copy:'', dash:'', seo:'', settings:'' };
  document.getElementById('sb-nav').innerHTML = NAV.map(n=>navBtn(n,counts)).join('')
    + `<div class="grp">도구</div>`
    + `<button onclick="openEditMode()"><span>✏️ 화면 편집 (사이트 보면서 수정)</span></button>`;
}
/* 화면 편집 열기 — 라이브에서는 같은 사이트를 ?edit=1 로, 로컬에서는 편집 서버로 */
async function openEditMode(){
  if(!IS_LOCAL_TOOLS){
    window.open(new URL('../?edit=1', location.href).href, '_blank');
    return;
  }
  try{
    await fetch(EDIT_ORIGIN + '/api/settings', { signal: AbortSignal.timeout(1500) });
    window.open(EDIT_ORIGIN + '/?edit=1', '_blank');
  }catch(e){
    alert('편집 서버가 꺼져 있습니다.\n\n사이트 폴더의 [편집서버-시작.bat] 을 더블클릭해 켠 다음\n다시 이 버튼을 눌러주세요.');
  }
}

/* ---------- 게시판 · SEO (편집 서버 UI 내장) ---------- */
function renderBoard(){
  if(!IS_LOCAL_TOOLS) return;   // 라이브에서는 블로그 탭(수파베이스)이 대신한다
  const el = document.getElementById('tab-board');
  if(el.dataset.loaded) return;
  el.dataset.loaded = '1';
  el.innerHTML = `<p class="tool-note">편집 서버가 켜져 있어야 합니다 (python edit-server.py · 자동으로 켜져 있으면 그대로 사용).
    저장하면 blog-슬러그.html 정적 페이지로 구워집니다.</p>
    <iframe class="tool-frame" src="${EDIT_ORIGIN}/board.html"></iframe>`;
}
function renderSeo(){
  const el = document.getElementById('tab-seo');
  if(el.dataset.loaded) return;
  el.dataset.loaded = '1';
  if(!IS_LOCAL_TOOLS){
    el.innerHTML = `<div class="card"><h3>SEO 관리는 로컬 도구입니다</h3>
      <p class="note">메타·sitemap·구조화데이터는 HTML 파일에 직접 굽는 작업이라 내 컴퓨터에서 실행합니다.<br>
      사이트 폴더의 <b>편집서버-시작.bat</b> 을 켠 뒤 <b>http://localhost:5723/admin/</b> 의 SEO 탭에서 편집하고,
      끝나면 push(또는 클로드에게 "올려줘")하면 라이브에 반영됩니다.</p></div>`;
    return;
  }
  el.innerHTML = `<p class="tool-note">메타·sitemap·robots·rss·구조화데이터·플로팅 버튼·문의 메일 설정 — 저장 즉시 HTML에 구워집니다.</p>
    <iframe class="tool-frame" src="${EDIT_ORIGIN}/seo.html"></iframe>`;
}
function navBtn(n, counts){
  const c = counts[n.id];
  return `<button class="${curTab===n.id?'on':''}" onclick="showTab('${n.id}')"><span>${n.label}</span>
    ${c!=='' && c!==undefined ? `<span class="cnt">${c}</span>` : ''}</button>`;
}
function showTab(name){
  curTab = name;
  TABS.forEach(x=>document.getElementById('tab-'+x).classList.toggle('hidden', x!==name));
  const n = NAV.find(x=>x.id===name) || NAV[0];
  document.getElementById('pg-title').textContent = n.title;
  document.getElementById('pg-desc').textContent = n.desc;
  renderNav();
  toggleSb(false);
  window.scrollTo(0,0);
}
function toggleSb(open){
  document.getElementById('sb').classList.toggle('open', !!open);
  document.getElementById('sb-backdrop').classList.toggle('open', !!open);
}
function renderAll(){
  renderNav(); renderDash(); renderInq(); renderBlog(); renderBoard(); renderSeo(); renderCopy(); renderSettings();
  showTab(curTab);
}

/* ============================================================
   대시보드
   ============================================================ */
function renderDash(){
  const newCnt = ADM.inqs.filter(i=>i.status==='new').length;
  document.getElementById('tab-dash').innerHTML = `
    <div class="kpi">
      <div class="kpi-card"><div class="lbl">누적 문의</div><div class="num">${ADM.inqs.length}</div><div class="sub">미처리 <b>${newCnt}</b>건</div></div>
      <div class="kpi-card"><div class="lbl">블로그 글</div><div class="num">${TV_BLOG_POSTS.length}</div><div class="sub">발행됨</div></div>
      <div class="kpi-card"><div class="lbl">포트폴리오</div><div class="num">${TV_PORTFOLIO.length}</div><div class="sub">등록된 미디어</div></div>
      <div class="kpi-card"><div class="lbl">패키지</div><div class="num">${TV_PACKAGES.length}</div><div class="sub">vietnam-tiktok.html</div></div>
    </div>
    <div class="card"><div class="card-head"><h3>최근 문의</h3><span class="sp"></span><button class="btn btn-ghost btn-sm" onclick="showTab('inq')">전체 보기</button></div>
      <div class="tbl-wrap"><table><thead><tr><th style="width:96px">일시</th><th>회사 · 담당자</th><th>내용</th><th style="width:76px">상태</th></tr></thead><tbody>${
        ADM.inqs.length ? ADM.inqs.slice(0,5).map(i=>`
          <tr><td>${esc(String(i.created_at).slice(0,10))}</td><td><b>${esc(i.company)}</b><div class="sub">${esc(i.name)}</div></td>
          <td style="max-width:320px"><div style="white-space:pre-wrap">${esc(i.message).slice(0,60)}</div></td>
          <td><span class="pill-st st-${i.status}">${INQ_ST[i.status]}</span></td></tr>`).join('')
        : `<tr class="empty-row"><td colspan="4">아직 접수된 문의가 없습니다</td></tr>`
      }</tbody></table></div></div>`;
}

/* ============================================================
   문의함
   ============================================================ */
const INQ_ST = { new:'신규', doing:'처리중', done:'완료' };
let inqFilter = 'all';

function renderInq(){
  const all = ADM.inqs;
  const cnt = k => all.filter(i=>i.status===k).length;
  const list = inqFilter==='all' ? all : all.filter(i=>i.status===inqFilter);

  document.getElementById('tab-inq').innerHTML = `
    <div class="card"><p class="note">inquiry.html에서 방문자가 제출한 문의입니다.</p>
    <div class="bar">
      <button class="btn btn-sm ${inqFilter==='all'?'btn-primary':'btn-ghost'}" onclick="inqFilter='all';renderInq()">전체 ${all.length}</button>
      <button class="btn btn-sm ${inqFilter==='new'?'btn-primary':'btn-ghost'}" onclick="inqFilter='new';renderInq()">신규 ${cnt('new')}</button>
      <button class="btn btn-sm ${inqFilter==='doing'?'btn-primary':'btn-ghost'}" onclick="inqFilter='doing';renderInq()">처리중 ${cnt('doing')}</button>
      <button class="btn btn-sm ${inqFilter==='done'?'btn-primary':'btn-ghost'}" onclick="inqFilter='done';renderInq()">완료 ${cnt('done')}</button>
      <span class="grow"></span><button class="btn btn-ghost btn-sm" onclick="exportInquiries()">CSV 내보내기</button>
    </div>
    <div class="tbl-wrap"><table><thead><tr><th style="width:96px">일시</th><th>회사</th><th>담당자 · 연락처</th><th>내용 · 메모</th><th style="width:150px">상태</th><th style="width:60px"></th></tr></thead><tbody>${
      list.length ? list.map(i=>`
        <tr><td>${esc(String(i.created_at).slice(0,10))}<div class="sub">${esc(String(i.created_at).slice(11,16))}</div></td>
        <td><b>${esc(i.company)}</b><div class="sub">${esc(i.source_page)}</div></td>
        <td>${esc(i.name)}<div class="sub">${esc(i.phone)} · ${esc(i.email)}</div></td>
        <td style="max-width:280px"><div style="white-space:pre-wrap;line-height:1.6">${esc(i.message)}</div>
          <input class="srch" style="margin-top:8px;width:100%" placeholder="메모" value="${esc(i.memo)}"
            onchange="admDo(Admin.setInquiryMemo('${i.id}', this.value), 0)"></td>
        <td><select class="srch" style="width:100%" onchange="admDo(Admin.setInquiryStatus('${i.id}', this.value), 0)">
          <option value="new" ${i.status==='new'?'selected':''}>신규</option>
          <option value="doing" ${i.status==='doing'?'selected':''}>처리중</option>
          <option value="done" ${i.status==='done'?'selected':''}>완료</option></select></td>
        <td><button class="btn btn-ghost btn-sm" onclick="if(confirm('삭제할까요?')){admDo(Admin.deleteInquiry('${i.id}'), 0);}">삭제</button></td></tr>`).join('')
      : `<tr class="empty-row"><td colspan="6">해당하는 문의가 없습니다</td></tr>`
    }</tbody></table></div></div>`;
}
function exportInquiries(){
  const rows = [['일시','회사','담당자','연락처','이메일','내용','유입페이지','상태','메모']];
  ADM.inqs.forEach(i=>rows.push([i.created_at,i.company,i.name,i.phone,i.email,i.message,i.source_page,INQ_ST[i.status],i.memo]));
  const csv = rows.map(r=>r.map(v=>`"${String(v??'').replace(/"/g,'""')}"`).join(',')).join('\n');
  downloadFile('trevity-문의_'+today()+'.csv', '﻿'+csv, 'text/csv');
}
function downloadFile(name, content, mime){
  const blob = new Blob([content], {type:(mime||'text/plain')+';charset=utf-8'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = name;
  document.body.appendChild(a); a.click();
  setTimeout(()=>{ URL.revokeObjectURL(a.href); a.remove(); }, 400);
}

/* ============================================================
   블로그 CRUD
   ============================================================ */
let bEditing = null;
let RTE_BLOG = null;
let bHtmlMode = false;

function toggleBlogHtml(){
  const ta = document.getElementById('b-html');
  const rte = document.getElementById('rte-b-body');
  const tb = rte ? rte.parentElement.querySelector('.ql-toolbar') : null;
  const btn = document.getElementById('b-htmlbtn');
  if(!ta || !rte) return;
  if(!bHtmlMode){
    ta.value = RTE_BLOG ? RTE_BLOG.root.innerHTML : '';
    rte.style.display = 'none'; if(tb) tb.style.display = 'none';
    ta.style.display = 'block';
    btn.textContent = '✏️ 에디터로 보기';
    bHtmlMode = true;
  }else{
    if(RTE_BLOG){ RTE_BLOG.root.innerHTML = ''; RTE_BLOG.clipboard.dangerouslyPasteHTML(ta.value); }
    ta.style.display = 'none';
    rte.style.display = ''; if(tb) tb.style.display = '';
    btn.textContent = '</> HTML 직접입력';
    bHtmlMode = false;
  }
}

function initBlogEditor(html){
  bHtmlMode = false;
  if(typeof Quill === 'undefined') return;
  const el = document.getElementById('rte-b-body');
  if(!el) return;
  RTE_BLOG = new Quill(el, {
    theme: 'snow',
    placeholder: '여기에 본문을 작성하세요…',
    modules: { toolbar: [
      [{ header:[2,3,false] }], ['bold','italic','underline'],
      [{ list:'ordered' }, { list:'bullet' }], ['blockquote','link','image'], ['clean'],
    ] },
  });
  if(html) RTE_BLOG.clipboard.dangerouslyPasteHTML(html);
}
function blogBodyGet(){
  if(bHtmlMode){
    const ta = document.getElementById('b-html');
    return ta ? ta.value.trim() : '';
  }
  if(!RTE_BLOG) return '';
  const html = RTE_BLOG.root.innerHTML;
  return html.replace(/<[^>]*>/g,'').trim() ? html : '';
}

const BLOG_CATS = ['베트남 시장','인플루언서 부킹','틱톡 마케팅','캠페인 사례'];

function renderBlog(){
  const el = document.getElementById('tab-blog');
  if(bEditing !== null){
    el.innerHTML = blogForm(bEditing);
    const p = bEditing ? TV_BLOG_POSTS.find(x=>x.slug===bEditing) : null;
    initBlogEditor(p ? p.body_html : '');
    return;
  }
  el.innerHTML = `
    <div class="card"><p class="note">blog.html 목록과 blog-post.html?slug=... 상세에 노출됩니다.</p>
    <div class="bar"><span class="grow"></span><button class="btn btn-primary btn-sm" onclick="bEditing='';renderBlog()">+ 새 글 작성</button></div>
    <div class="tbl-wrap"><table><thead><tr><th style="width:76px">썸네일</th><th>제목</th><th>분류</th><th>발행</th><th style="width:120px"></th></tr></thead><tbody>${
      TV_BLOG_POSTS.length ? TV_BLOG_POSTS.map(p=>`
        <tr><td><img class="thumb-sm" src="${esc(imgSrc(p.thumbnail_url))}" alt=""></td>
        <td><b>${esc(p.title)}</b><div class="sub">/${esc(p.slug)}</div></td><td>${esc(p.category)}</td>
        <td>${p.published?'게시중':'비공개'}</td>
        <td><button class="btn btn-ghost btn-sm" onclick="bEditing='${p.slug}';renderBlog()">수정</button>
          <button class="btn btn-ghost btn-sm" onclick="if(confirm('삭제할까요?')){admDo(Admin.deleteBlogPost('${p.slug}'), 0);}">삭제</button></td></tr>`).join('')
      : `<tr class="empty-row"><td colspan="5">글이 없습니다</td></tr>`
    }</tbody></table></div></div>`;
}

function blogForm(slug){
  const p = slug ? TV_BLOG_POSTS.find(x=>x.slug===slug) : null;
  return `
    <div class="card"><div class="bar"><h3 style="margin:0">${p?'글 수정':'새 글 작성'}</h3><span class="grow"></span>
      <button class="btn btn-ghost btn-sm" onclick="bEditing=null;renderBlog()">취소</button>
      <button class="btn btn-primary btn-sm" onclick="saveBlogPost('${slug||''}')">저장</button></div>
    <div class="fgrid two">
      <div class="fld"><label>제목</label><input id="b-title" value="${esc(p?p.title:'')}"></div>
      <div class="fld"><label>URL 슬러그 (영문/숫자/하이픈)</label><input id="b-slug" value="${esc(p?p.slug:'')}" ${p?'readonly':''}></div>
    </div>
    <div class="fgrid two">
      <div class="fld"><label>분류</label><select id="b-cat">${BLOG_CATS.map(c=>`<option ${p&&p.category===c?'selected':''}>${c}</option>`).join('')}</select></div>
      <div class="fld"><label>읽는 시간(분)</label><input id="b-min" type="number" value="${p?p.read_minutes:4}"></div>
    </div>
    <div class="sect"><h4>썸네일</h4>${uploader('b-thumb', p?p.thumbnail_url:'', {hint:'목록 카드와 상세 상단에 쓰입니다. 16:9 권장.'})}</div>
    <div class="fld"><label>요약 (목록 카드에 표시)</label><textarea id="b-excerpt">${esc(p?p.excerpt:'')}</textarea></div>
    <div class="sect"><h4 style="display:flex;align-items:center;gap:10px">본문
      <button class="btn btn-ghost btn-sm" id="b-htmlbtn" onclick="toggleBlogHtml()" style="font-weight:600">&lt;/&gt; HTML 직접입력</button></h4>
      <div class="rte" id="rte-b-body"></div>
      <textarea id="b-html" spellcheck="false" style="display:none;width:100%;min-height:320px;font-family:ui-monospace,Consolas,monospace;font-size:13px;line-height:1.6;padding:12px;border:1px solid var(--adm-line);border-radius:8px" placeholder="<p>HTML을 그대로 붙여넣으세요</p>"></textarea></div>
    <div class="fld" style="margin-top:16px"><label style="display:flex;align-items:center;gap:8px;font-weight:600">
      <input type="checkbox" id="b-pub" ${!p||p.published?'checked':''} style="width:auto"> 발행 (체크 해제 시 blog.html에서 숨김)</label></div>
    <div class="bar" style="margin-top:22px"><span class="grow"></span>
      <button class="btn btn-ghost" onclick="bEditing=null;renderBlog()">취소</button>
      <button class="btn btn-primary" onclick="saveBlogPost('${slug||''}')">저장</button></div></div>`;
}

function saveBlogPost(oldSlug){
  const title = av('b-title'), slug = av('b-slug');
  if(!title){ toastA('제목을 입력하세요'); return; }
  if(!slug || !/^[a-z0-9-]+$/.test(slug)){ toastA('슬러그는 영문 소문자·숫자·하이픈만 가능합니다'); return; }
  toastA('저장하는 중…');
  admDo(Admin.upsertBlogPost({
    slug, title, category: av('b-cat'), thumbnail_url: av('b-thumb'),
    excerpt: av('b-excerpt'), body_html: blogBodyGet(),
    read_minutes: Number(av('b-min'))||4, published: document.getElementById('b-pub').checked,
  }), 0);
  bEditing = null;
}

/* ============================================================
   카피 — 텍스트 전체 편집 + 포트폴리오 이미지 + 패키지 가격
   ============================================================ */
let pfEditing = null;
let copyPage = 'index';
let copySearch = '';

const COPY_PAGE_LABELS = {
  'index':'메인', 'vietnam-tiktok':'수출 랜딩', 'local-vn':'베트남 현지', 'stay':'숙박',
  'tourist-vn':'베트남 관광객', 'tourist-cn':'중국 관광객',  'help':'고객센터', 'agency':'공식대행사', 'inquiry':'문의', 'blog':'블로그',
};

function copyEntries(){
  let list = TV_COPY_DEFAULTS;
  if(copySearch){
    const q = copySearch.toLowerCase();
    list = list.filter(e => e.t.toLowerCase().includes(q) || (TV_COPY_OVR[e.k]||'').toLowerCase().includes(q));
  } else {
    list = list.filter(e => e.pg.includes(copyPage));
  }
  return list;
}

function renderCopyText(){
  const box = document.getElementById('copy-text-list');
  if(!box) return;
  const list = copyEntries();
  const ovrCnt = Object.keys(TV_COPY_OVR).length;
  document.getElementById('copy-ovr-cnt').textContent = ovrCnt ? `수정된 카피 ${ovrCnt}건` : '';
  box.innerHTML = list.slice(0, 400).map(e=>{
    const raw = TV_COPY_OVR[e.k];
    const cur = raw !== undefined
      ? String(raw).replace(/^HTML::/,'').replace(/<br\s*\/?>/g,'\n').replace(/<[^>]+>/g,'')
      : e.t;
    const changed = raw !== undefined;
    const openPg = e.pg.includes(copyPage) ? copyPage : e.pg[0];
    const field = `<textarea class="srch" style="width:100%;min-height:44px;font-size:14px;line-height:1.6" rows="${Math.max(1, cur.split('\n').length)}"
        data-copy-key="${e.k}" onchange="saveCopyField(this)">${esc(cur)}</textarea>`;
    return `<div style="padding:10px 0;border-bottom:1px solid var(--adm-line)">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:5px">
        <span style="font-size:11px;color:${changed?'var(--tv-primary)':'var(--adm-sub)'};font-weight:700">${changed?'수정됨':'기본'}</span>
        <span style="font-size:11px;color:var(--adm-sub)">${e.pg.map(p=>COPY_PAGE_LABELS[p]||p).join(' · ')}</span>
        <button class="btn btn-ghost btn-sm" style="padding:2px 10px;font-size:11px;margin-left:auto"
          onclick="window.open('../${openPg}.html?edit=1&find=${e.k}','_blank')">📍 페이지에서 열기</button>
        ${changed?`<button class="btn btn-ghost btn-sm" style="padding:2px 8px;font-size:11px" onclick="resetCopyField('${e.k}')">기본값으로</button>`:''}
      </div>${field}</div>`;
  }).join('') || `<p class="note" style="margin:0">해당하는 카피가 없습니다.</p>`;
}
function saveCopyField(el){
  const key = el.getAttribute('data-copy-key');
  const def = TV_COPY_DEFAULTS.find(e=>e.k===key);
  const v = el.value;
  if(def && v === def.t){ admDo(Admin.delCopy(key), 0); return; }
  admDo(Admin.setCopy(key, v), 0);
  toastA('저장됨 — 사이트 새로고침 시 반영');
}
function resetCopyField(key){
  admDo(Admin.delCopy(key), 0);
}

function renderCopy(){
  const el = document.getElementById('tab-copy');
  const home = TV_PORTFOLIO.filter(x=>x.placement==='home-roll').sort((a,b)=>a.sort_order-b.sort_order);
  const hero = TV_PORTFOLIO.filter(x=>x.placement==='hero-wall').sort((a,b)=>a.sort_order-b.sort_order);

  el.innerHTML = `
    <div class="card"><div class="card-head"><h3>텍스트 카피 (전 페이지 ${TV_COPY_DEFAULTS.length}개 항목)</h3><span class="sp"></span><span class="note" style="margin:0" id="copy-ovr-cnt"></span></div>
      <div class="bar">
        <select class="srch" style="min-width:150px" onchange="copyPage=this.value;copySearch='';document.getElementById('copy-srch').value='';renderCopyText()">${
          Object.keys(COPY_PAGE_LABELS).map(p=>`<option value="${p}" ${copyPage===p?'selected':''}>${COPY_PAGE_LABELS[p]} (${p})</option>`).join('')
        }</select>
        <input class="srch grow" id="copy-srch" placeholder="전체 페이지에서 문구 검색…" value="${esc(copySearch)}"
          oninput="copySearch=this.value;renderCopyText()">
      </div>
      <p class="note" style="margin-bottom:6px">💡 <b>📍 페이지에서 열기</b>를 누르면 실제 화면의 그 문구로 바로 이동해 보면서 수정할 수 있습니다(추천). 여기서 직접 고쳐도 되고, 같은 문구는 전 페이지에서 한 번에 바뀝니다.</p>
      <div id="copy-text-list" style="max-height:560px;overflow-y:auto"></div>
    </div>` + `
    <div class="card"><div class="card-head"><h3>포트폴리오 — 메인 페이지 롤 (index.html)</h3><span class="sp"></span>
      <button class="btn btn-primary btn-sm" onclick="pfEditing='home-roll';renderCopy()">+ 추가</button></div>
      ${pfEditing==='home-roll' ? pfForm('home-roll') : ''}
      ${pfList(home)}
    </div>
    <div class="card"><div class="card-head"><h3>포트폴리오 — 히어로 영상벽 (local-vn/stay/tourist-vn/tourist-cn/vietnam-tiktok 5개 페이지 공용)</h3><span class="sp"></span>
      <button class="btn btn-primary btn-sm" onclick="pfEditing='hero-wall';renderCopy()">+ 추가</button></div>
      ${pfEditing==='hero-wall' ? pfForm('hero-wall') : ''}
      ${pfList(hero)}
    </div>
    <div class="card"><div class="card-head"><h3>vietnam-tiktok.html 패키지 가격</h3></div>
      ${TV_PACKAGES.slice().sort((a,b)=>a.sort_order-b.sort_order).map(pkgForm).join('')}
    </div>`;
  renderCopyText();
}

function pfList(items){
  if(!items.length) return `<p class="note" style="margin:0">아직 없습니다.</p>`;
  return `<div class="tbl-wrap"><table><thead><tr><th style="width:76px">미리보기</th><th>종류</th><th>주소</th><th style="width:150px"></th></tr></thead><tbody>${
    items.map((it,i)=>`
      <tr><td>${it.media_type==='video'
          ? `<img class="thumb-sm" src="${esc(it.poster_url)}" alt="">`
          : `<img class="thumb-sm" src="${esc(it.url)}" alt="">`}</td>
      <td>${it.media_type==='video'?'영상':'이미지'}</td>
      <td style="max-width:280px;word-break:break-all">${esc(it.url)}</td>
      <td>
        <button class="btn btn-ghost btn-sm" onclick="admDo(Admin.movePortfolioItem('${it.id}',-1),0)" ${i===0?'disabled':''}>↑</button>
        <button class="btn btn-ghost btn-sm" onclick="admDo(Admin.movePortfolioItem('${it.id}',1),0)" ${i===items.length-1?'disabled':''}>↓</button>
        <button class="btn btn-ghost btn-sm" onclick="if(confirm('삭제할까요?')){admDo(Admin.deletePortfolioItem('${it.id}'),0);}">삭제</button>
      </td></tr>`).join('')
  }</tbody></table></div>`;
}

function pfForm(placement){
  return `<div class="sect" style="margin-top:0;padding-top:16px">
    <div class="fgrid two">
      <div class="fld"><label>종류</label><select id="pf-type"><option value="image">이미지</option><option value="video">영상</option></select></div>
      <div class="fld"><label>대체 텍스트(alt)</label><input id="pf-alt" placeholder="트래비티 인플루언서 콘텐츠"></div>
    </div>
    <div class="fld"><label>이미지 파일(이미지일 때) 또는 영상 URL(영상일 때)</label>${uploader('pf-url', '', {hint:'영상이면 아래 URL로 넣기에 mp4 주소를 직접 입력하세요.'})}</div>
    <div class="fld"><label>영상 포스터 이미지(영상일 때만)</label>${uploader('pf-poster', '', {hint:'영상 로딩 전 보여줄 썸네일'})}</div>
    <div class="bar"><span class="grow"></span><button class="btn btn-ghost btn-sm" onclick="pfEditing=null;renderCopy()">취소</button>
      <button class="btn btn-primary btn-sm" onclick="savePortfolioItem('${placement}')">추가</button></div>
  </div>`;
}
function savePortfolioItem(placement){
  const url = av('pf-url');
  if(!url){ toastA('이미지 또는 영상 주소를 넣으세요'); return; }
  admDo(Admin.upsertPortfolioItem({
    placement, media_type: document.getElementById('pf-type').value,
    url, poster_url: av('pf-poster'), alt: av('pf-alt'), active: true,
  }), 0);
  pfEditing = null;
}

function pkgForm(p){
  return `<div class="sect" style="margin-top:0;padding-top:16px;border-top:1px solid var(--adm-line)">
    <h4>${esc(p.name)} (${esc(p.slug)})</h4>
    <div class="fgrid">
      <div class="fld"><label>이름</label><input id="pkg-name-${p.slug}" value="${esc(p.name)}"></div>
      <div class="fld"><label>인플루언서 인원수</label><input id="pkg-cnt-${p.slug}" type="number" value="${p.influencer_count}"></div>
      <div class="fld"><label>가격(원, 부가세 별도)</label><input id="pkg-price-${p.slug}" type="number" value="${p.price_krw}"></div>
    </div>
    <div class="fld"><label>설명</label><input id="pkg-desc-${p.slug}" value="${esc(p.description)}"></div>
    <button class="btn btn-primary btn-sm" onclick="savePackage('${p.slug}')">저장</button>
  </div>`;
}
function savePackage(slug){
  admDo(Admin.upsertPackage({
    slug, name: av('pkg-name-'+slug), influencer_count: Number(av('pkg-cnt-'+slug))||0,
    price_krw: Number(av('pkg-price-'+slug))||0, description: av('pkg-desc-'+slug),
    sort_order: TV_PACKAGES.find(x=>x.slug===slug)?.sort_order ?? 0,
  }), 0);
}

/* ============================================================
   설정
   ============================================================ */
function renderSettings(){
  document.getElementById('tab-settings').innerHTML = `
    <div class="card"><h3>연결 상태</h3>
      <p class="note">백엔드: <b>${isSB() ? 'Supabase (실서비스)' : '브라우저 저장 (로컬 테스트)'}</b>
      ${isSB() ? '' : '<br>supabase/README.md를 따라 프로젝트를 만들고 assets/js/config.js에 키를 넣으면 실서비스 모드로 전환됩니다.'}</p></div>
    ${isSB() ? '' : `
    <div class="card"><h3>관리자 비밀번호 변경</h3>
      <div class="fgrid two"><div class="fld"><label>새 비밀번호</label><input id="set-pw" type="password"></div>
      <div class="fld"><label>새 비밀번호 확인</label><input id="set-pw2" type="password"></div></div>
      <button class="btn btn-primary btn-sm" onclick="changePw()">변경</button></div>`}
    <div class="card"><h3>업로드 이미지 저장공간</h3>
      <p class="note">${isSB() ? 'Supabase Storage에 저장됩니다.' : '이 브라우저 안에 저장됩니다(IndexedDB). Supabase 연결 시 자동으로 Storage로 전환됩니다.'}</p>
      <div id="img-usage"><p class="note" style="margin:0">불러오는 중…</p></div>
      <div class="bar" style="margin:14px 0 0"><button class="btn btn-ghost btn-sm" onclick="runGc()">사용하지 않는 이미지 정리</button></div></div>`;
  renderStorage();
}
async function renderStorage(){
  const el = document.getElementById('img-usage');
  if(!el) return;
  const u = await TvImg.usage();
  const pct = u.quota ? Math.min(100, (u.used / u.quota) * 100) : 0;
  el.innerHTML = isSB()
    ? `<p class="note" style="margin:0">Supabase Storage 사용량은 대시보드에서 확인하세요.</p>`
    : `<p class="note" style="margin:0">업로드 이미지 <b>${u.count}장</b> · ${fmtBytes(u.used)}${u.quota?` / 여유 ${fmtBytes(u.quota)} (${pct.toFixed(1)}%)`:''}</p>`;
}
async function runGc(){
  const n = await TvImg.gc();
  toastA(n ? `사용하지 않는 이미지 ${n}장을 정리했습니다` : '정리할 이미지가 없습니다');
  renderStorage();
}
function changePw(){
  const a=av('set-pw'), b=av('set-pw2');
  if(a.length<4){ toastA('4자 이상 입력하세요'); return; }
  if(a!==b){ toastA('두 비밀번호가 다릅니다'); return; }
  Admin.changePassword(a); toastA('비밀번호가 변경되었습니다');
  document.getElementById('set-pw').value=''; document.getElementById('set-pw2').value='';
}

/* ---------- Supabase 모드면 로그인 폼을 이메일 방식으로 전환 ---------- */
if(isSB()){
  document.getElementById('gate-email-fld').style.display = 'block';
  document.getElementById('gate-hint').style.display = 'none';
}
