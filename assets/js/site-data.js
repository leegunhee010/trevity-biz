/* 공개 페이지 부트스트랩 — local/Supabase 어느 모드든 TV_BLOG_POSTS 등 전역 배열을 채운 뒤 resolve된다. */
async function TvBoot(){
  if(typeof TvData !== 'undefined'){ await TvData.boot(); return; }
  // 로컬 모드: store.js의 오버라이드를 전역 배열에 얹는다
  const override = (key, seedArr) => {
    try{
      const raw = localStorage.getItem(key);
      if(raw){ const list = JSON.parse(raw); seedArr.length = 0; seedArr.push(...list); }
    }catch(e){}
  };
  override('tv_blog_override', TV_BLOG_POSTS);
  override('tv_portfolio_override', TV_PORTFOLIO);
  override('tv_packages_override', TV_PACKAGES);
  try{
    const c = JSON.parse(localStorage.getItem('tv_copy_override') || '{}');
    if(typeof TV_COPY_OVR !== 'undefined') Object.assign(TV_COPY_OVR, c);
  }catch(e){}
  try{ await TvImg.loadCache(); }catch(e){}
}

/* ---------- 카피 오버라이드 적용 ----------
   copy-data.js의 추출 규칙과 동일하게 leaf 텍스트를 정규화·해시해서
   TV_COPY_OVR에 오버라이드가 있으면 교체한다. (모든 페이지 공통) */
const TV_COPY_TAGS = 'h1,h2,h3,h4,h5,h6,p,span,a,b,strong,em,small,li,td,th,button,div,label,summary,figcaption,blockquote,i,u';
function tvCopyKey(t){
  let h = 5381;
  for(let i=0;i<t.length;i++) h = ((h<<5)+h+t.charCodeAt(i))|0;
  return 'c' + (h>>>0).toString(16);
}
function tvLeafText(el){
  const parts = [];
  for(const c of el.childNodes){
    if(c.nodeType === 3) parts.push(c.nodeValue);
    else if(c.nodeType === 1 && c.tagName === 'BR') parts.push('\n');
    else return null;
  }
  const t = parts.join('').split('\n').map(ln=>ln.replace(/\s+/g,' ').trim()).join('\n').trim();
  return t || null;
}
function applyCopy(){
  if(typeof TV_COPY_OVR === 'undefined' || !Object.keys(TV_COPY_OVR).length) return;
  document.body.querySelectorAll(TV_COPY_TAGS).forEach(el=>{
    if(el.closest('script,style')) return;
    const t = tvLeafText(el);
    if(!t || t.length < 2 || t.length > 600) return;
    const v = TV_COPY_OVR[tvCopyKey(t)];
    if(v === undefined || v === null || v === t) return;
    el.innerHTML = esc(v).replace(/\n/g,'<br>');
  });
}

/* ---------- 블로그 목록 (blog.html) ---------- */
function renderBlogList(){
  const grid = document.querySelector('.tv-grid');
  if(!grid) return;
  const posts = TV_BLOG_POSTS.filter(p=>p.published !== false)
    .sort((a,b)=>String(b.created_at||'').localeCompare(String(a.created_at||'')));

  const catCounts = {};
  posts.forEach(p=>{ catCounts[p.category] = (catCounts[p.category]||0) + 1; });
  document.querySelectorAll('.tv-cats li').forEach(li=>{
    const cat = li.getAttribute('data-cat');
    const span = li.querySelector('span:last-child');
    if(!span) return;
    span.textContent = cat==='all' ? `(${posts.length})` : `(${catCounts[cat]||0})`;
  });

  grid.innerHTML = posts.map(p => `
    <article class="tv-card" data-cat="${esc(p.category)}" data-title="${esc(p.title)}">
      <a href="./blog-${encodeURIComponent(p.slug)}.html">
        <div class="tv-thumb"><img src="${esc(TvImg.resolve(p.thumbnail_url))}" alt="${esc(p.title)}" loading="lazy"></div>
        <div class="tv-card-body"><span class="tv-chip">${esc(p.category)}</span><h3>${esc(p.title)}</h3>
        <div class="tv-meta"><time>${esc(String(p.created_at||'').slice(0,10))}</time><span>${p.read_minutes||4}분 분량</span></div></div>
      </a></article>`).join('') || '<p style="padding:40px;color:#8B95A1">아직 글이 없습니다.</p>';
}
function esc(s){ return String(s??'').replace(/[&<>"']/g, m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m])); }

/* ---------- 포트폴리오 롤/히어로 (index.html 및 5개 페이지) ----------
   selector는 "행" 엘리먼트 자체를 가리켜야 한다 (innerHTML 교체 대상).
   행이 여러 개면 selector가 여러 엘리먼트에 매치되게 넘긴다. */
function renderPortfolioRoll(selector, placement){
  const rows = document.querySelectorAll(selector);
  const items = TV_PORTFOLIO.filter(x=>x.placement===placement && x.active!==false).sort((a,b)=>a.sort_order-b.sort_order);
  if(!items.length || !rows.length) return;
  rows.forEach((row, ri) => {
    const slice = ri % 2 === 0 ? items : [...items].reverse();
    const repeated = [...slice, ...slice, ...slice, ...slice];
    row.innerHTML = repeated.map(it => it.media_type === 'video'
      ? `<video src="${esc(it.url)}" muted loop playsinline autoplay preload="metadata" poster="${esc(it.poster_url)}"></video>`
      : `<img src="${esc(TvImg.resolve(it.url))}" alt="${esc(it.alt)}" loading="lazy"/>`
    ).join('');
  });
}

/* ---------- 히어로 영상벽 (local-vn/stay/tourist-vn/tourist-cn/vietnam-tiktok) ----------
   원본 swiper-slide 마크업(사이즈 클래스 포함)을 그대로 재생성한다.
   아이템이 없으면 정적 원본 마크업을 그대로 둔다. */
function renderHeroWall(selector){
  const wrap = document.querySelector(selector);
  const items = TV_PORTFOLIO.filter(x=>x.placement==='hero-wall' && x.active!==false).sort((a,b)=>a.sort_order-b.sort_order);
  if(!wrap || !items.length) return;
  const slide = it => `<div class="swiper-slide mn:!w-[256px] !w-[128px]" style="margin-right:10px"><div class="mn:rounded-[16px] overflow-hidden rounded-[8px]"><div class="size-full">${
    it.media_type === 'video'
      ? `<video src="${esc(it.url)}" poster="${esc(it.poster_url)}" muted loop playsinline autoplay preload="metadata" class="h-[220px] w-[128px] object-cover mn:h-[440px] mn:w-[256px]" aria-label="${esc(it.alt||'트래비티 인플루언서 콘텐츠')}"></video>`
      : `<img loading="lazy" src="${esc(TvImg.resolve(it.url))}" alt="${esc(it.alt||'')}" class="h-[220px] w-[128px] object-cover mn:h-[440px] mn:w-[256px]" style="background:#fff"/>`
  }</div></div></div>`;
  wrap.innerHTML = items.map(slide).join('');
}

/* ---------- 패키지 카드 (vietnam-tiktok.html) ----------
   [data-pkg-label="slug"] 스팬 → "스타터 · 10명" 형식
   [data-pkg-price="slug"] h6 → "10명 × 20만원 = 200만원 (부가세 별도)" 형식 */
function renderPackages(){
  if(!TV_PACKAGES.length) return;
  TV_PACKAGES.forEach(p=>{
    const label = `${p.name} · ${p.influencer_count}명`;
    document.querySelectorAll(`[data-pkg-label="${p.slug}"]`).forEach(el=>{ el.textContent = label; });
    const per = p.influencer_count ? Math.round(p.price_krw / p.influencer_count / 10000) : 0;
    const tot = Math.round(p.price_krw / 10000).toLocaleString('ko-KR');
    document.querySelectorAll(`[data-pkg-price="${p.slug}"]`).forEach(el=>{
      el.innerHTML = `${p.influencer_count}명 × ${per}만원 = <span style="color:#fa6781;font-weight:800">${tot}만원</span> (부가세 별도)`;
    });
  });
}
