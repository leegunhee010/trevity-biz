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
  try{ await TvImg.loadCache(); }catch(e){}
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
      <a href="./blog-post.html?slug=${encodeURIComponent(p.slug)}">
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

/* ---------- 패키지 카드 (vietnam-tiktok.html) ---------- */
function renderPackages(containerSelector){
  const el = document.querySelector(containerSelector);
  if(!el) return;
  const pkgs = TV_PACKAGES.slice().sort((a,b)=>a.sort_order-b.sort_order);
  const cards = el.querySelectorAll('[data-pkg-slug]');
  cards.forEach(card => {
    const slug = card.getAttribute('data-pkg-slug');
    const p = pkgs.find(x=>x.slug===slug);
    if(!p) return;
    const nameEl = card.querySelector('[data-pkg-name]');
    const cntEl = card.querySelector('[data-pkg-count]');
    const priceEl = card.querySelector('[data-pkg-price]');
    const descEl = card.querySelector('[data-pkg-desc]');
    if(nameEl) nameEl.textContent = p.name;
    if(cntEl) cntEl.textContent = p.influencer_count + '명';
    if(priceEl) priceEl.textContent = p.price_krw.toLocaleString('ko-KR') + '원';
    if(descEl) descEl.textContent = p.description;
  });
}
