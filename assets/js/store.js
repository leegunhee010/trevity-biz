/* 트래비티 store — localStorage MVP. Supabase 키를 채우면 store-supabase.js가 이 인터페이스를 덮어쓴다. */
function tvId(prefix){ return prefix + '_' + Date.now().toString(36) + Math.floor(Math.random()*1e6).toString(36); }
function tvRead(key, fallback){ try{ return JSON.parse(localStorage.getItem(key) || JSON.stringify(fallback)); }catch(e){ return fallback; } }
function tvWrite(key, val){ localStorage.setItem(key, JSON.stringify(val)); }

const Store = {
  /* ---- 문의: 공개 방문자가 씀 ---- */
  async submitInquiry(data){
    const list = tvRead('tv_inquiries', []);
    list.unshift({
      id: tvId('inq'), created_at: new Date().toISOString(),
      name: data.name||'', company: data.company||'', phone: data.phone||'',
      email: data.email||'', message: data.message||'', source_page: data.source_page||'',
      status: 'new', memo: '',
    });
    tvWrite('tv_inquiries', list);
    return { ok:true };
  },
  async allInquiries(){ return tvRead('tv_inquiries', []); },

  async allBlogPosts(){ return TV_BLOG_POSTS; },
  async blogPost(slug){ return TV_BLOG_POSTS.find(p=>p.slug===slug) || null; },

  async allPortfolio(){ return TV_PORTFOLIO; },
  async allPackages(){ return TV_PACKAGES; },
};

const Admin = {
  DEFAULT_PW: 'trevity2026',
  _hash(s){ let h=5381; for(let i=0;i<s.length;i++) h=((h<<5)+h+s.charCodeAt(i))|0; return String(h); },
  password(){ return localStorage.getItem('tv_admin_pw') || this._hash(this.DEFAULT_PW); },
  login(pw){
    if(this._hash(pw) !== this.password()) return false;
    sessionStorage.setItem('tv_admin_in','1'); return true;
  },
  changePassword(pw){ localStorage.setItem('tv_admin_pw', this._hash(pw)); },
  isIn(){ return sessionStorage.getItem('tv_admin_in')==='1'; },
  logout(){ sessionStorage.removeItem('tv_admin_in'); },

  /* ---- 문의 처리 ---- */
  async setInquiryStatus(id, status){
    const list = tvRead('tv_inquiries', []);
    const i = list.findIndex(x=>x.id===id); if(i>=0) list[i].status = status;
    tvWrite('tv_inquiries', list);
  },
  async setInquiryMemo(id, memo){
    const list = tvRead('tv_inquiries', []);
    const i = list.findIndex(x=>x.id===id); if(i>=0) list[i].memo = memo;
    tvWrite('tv_inquiries', list);
  },
  async deleteInquiry(id){
    tvWrite('tv_inquiries', tvRead('tv_inquiries', []).filter(x=>x.id!==id));
  },

  /* ---- 블로그 CRUD (오버라이드는 TV_BLOG_POSTS 위에 얹는다) ---- */
  saveBlogPosts(list){ tvWrite('tv_blog_override', list); TV_BLOG_POSTS.length = 0; TV_BLOG_POSTS.push(...list); },
  async upsertBlogPost(p){
    const list = [...TV_BLOG_POSTS];
    const i = list.findIndex(x=>x.slug===p.slug);
    if(i>=0) list[i] = {...list[i], ...p, updated_at:new Date().toISOString()};
    else list.unshift({...p, created_at:new Date().toISOString(), updated_at:new Date().toISOString()});
    this.saveBlogPosts(list);
  },
  async deleteBlogPost(slug){ this.saveBlogPosts(TV_BLOG_POSTS.filter(p=>p.slug!==slug)); },

  /* ---- 포트폴리오 CRUD ---- */
  savePortfolio(list){ tvWrite('tv_portfolio_override', list); TV_PORTFOLIO.length = 0; TV_PORTFOLIO.push(...list); },
  async upsertPortfolioItem(item){
    const list = [...TV_PORTFOLIO];
    const i = list.findIndex(x=>x.id===item.id);
    if(i>=0) list[i] = {...list[i], ...item};
    else list.push({...item, id: item.id || tvId('pf'), sort_order: list.length});
    this.savePortfolio(list);
  },
  async deletePortfolioItem(id){ this.savePortfolio(TV_PORTFOLIO.filter(x=>x.id!==id)); },
  async movePortfolioItem(id, dir){
    const list = [...TV_PORTFOLIO];
    const i = list.findIndex(x=>x.id===id);
    const j = i + dir;
    if(i<0 || j<0 || j>=list.length) return;
    [list[i], list[j]] = [list[j], list[i]];
    list.forEach((x,idx)=>x.sort_order = idx);
    this.savePortfolio(list);
  },

  /* ---- 카피 오버라이드 ---- */
  async setCopy(key, value){
    const m = tvRead('tv_copy_override', {});
    m[key] = value;
    tvWrite('tv_copy_override', m);
    if(typeof TV_COPY_OVR !== 'undefined') TV_COPY_OVR[key] = value;
  },
  async delCopy(key){
    const m = tvRead('tv_copy_override', {});
    delete m[key];
    tvWrite('tv_copy_override', m);
    if(typeof TV_COPY_OVR !== 'undefined') delete TV_COPY_OVR[key];
  },

  /* ---- 패키지 CRUD (3종 고정 slug, 수정만) ---- */
  savePackages(list){ tvWrite('tv_packages_override', list); TV_PACKAGES.length = 0; TV_PACKAGES.push(...list); },
  async upsertPackage(p){
    const list = [...TV_PACKAGES];
    const i = list.findIndex(x=>x.slug===p.slug);
    if(i>=0) list[i] = {...list[i], ...p}; else list.push(p);
    this.savePackages(list);
  },
};
