/* ============================================================
   트래비티 — Supabase 백엔드
   config.js 에 URL/키가 채워져 있을 때만 동작하며, store.js(localStorage)의
   Store / Admin / TvImg 를 같은 인터페이스로 덮어씁니다.
   ============================================================ */
if (typeof TV_BACKEND !== 'undefined' && TV_BACKEND === 'supabase') {

const SB = supabase.createClient(TV_SUPABASE_URL, TV_SUPABASE_ANON, {
  auth: { persistSession: true, autoRefreshToken: true },
});
window.SB = SB;

const TvData = {
  session: null,
  admin: false,

  async boot(){
    const { data:{ session } } = await SB.auth.getSession();
    this.session = session;
    if(session){
      const { data:adm } = await SB.from('admins').select('user_id').eq('user_id', session.user.id).maybeSingle();
      this.admin = !!adm;
    }
    await this.loadContent();
  },

  async loadContent(){
    // 관리자는 미발행/비활성 항목도 목록에서 봐야 하므로 필터를 생략한다.
    // (RLS가 비관리자에게는 published/active 행만 허용하므로 안전)
    let bpQ = SB.from('blog_posts').select('*');
    let pfQ = SB.from('portfolio_items').select('*');
    if(!this.admin){
      bpQ = bpQ.eq('published', true);
      pfQ = pfQ.eq('active', true);
    }
    const [bp, pf, pk] = await Promise.all([
      bpQ.order('created_at', {ascending:false}),
      pfQ.order('sort_order'),
      SB.from('packages').select('*').order('sort_order'),
    ]);
    if(bp.error) console.error('트래비티 콘텐츠 로드 실패(blog_posts)', bp.error);
    if(pf.error) console.error('트래비티 콘텐츠 로드 실패(portfolio_items)', pf.error);
    if(pk.error) console.error('트래비티 콘텐츠 로드 실패(packages)', pk.error);

    TV_BLOG_POSTS.length = 0;
    (bp.data||[]).forEach(p => TV_BLOG_POSTS.push(p));
    TV_PORTFOLIO.length = 0;
    (pf.data||[]).forEach(p => TV_PORTFOLIO.push(p));
    TV_PACKAGES.length = 0;
    (pk.data||[]).forEach(p => TV_PACKAGES.push(p));
  },
};
window.TvData = TvData;

Object.assign(Store, {
  async submitInquiry(data){
    const { error } = await SB.from('inquiries').insert({
      name: data.name||'', company: data.company||'', phone: data.phone||'',
      email: data.email||'', message: data.message||'', source_page: data.source_page||'',
    });
    if(error) return { ok:false, err: error.message };
    return { ok:true };
  },
  async allInquiries(){
    const { data, error } = await SB.from('inquiries').select('*').order('created_at', {ascending:false});
    if(error){ console.error(error); return []; }
    return data;
  },
  async allBlogPosts(){ return TV_BLOG_POSTS; },
  async blogPost(slug){
    if(TvData.admin){
      const { data } = await SB.from('blog_posts').select('*').eq('slug', slug).maybeSingle();
      return data || null;
    }
    return TV_BLOG_POSTS.find(p=>p.slug===slug) || null;
  },
  async allPortfolio(){ return TV_PORTFOLIO; },
  async allPackages(){ return TV_PACKAGES; },
});

Object.assign(Admin, {
  isIn(){ return !!TvData.session && TvData.admin; },
  async loginEmail(email, pw){
    const { error } = await SB.auth.signInWithPassword({ email, password: pw });
    if(error) return { ok:false, err:error.message };
    await TvData.boot();
    if(!TvData.admin){ await SB.auth.signOut(); return { ok:false, err:'관리자 계정이 아닙니다' }; }
    return { ok:true };
  },
  async logout(){ await SB.auth.signOut(); TvData.session=null; TvData.admin=false; },

  async setInquiryStatus(id, status){
    const { error } = await SB.from('inquiries').update({status}).eq('id', id);
    if(error) throw new Error(error.message);
  },
  async setInquiryMemo(id, memo){
    const { error } = await SB.from('inquiries').update({memo}).eq('id', id);
    if(error) throw new Error(error.message);
  },
  async deleteInquiry(id){
    const { error } = await SB.from('inquiries').delete().eq('id', id);
    if(error) throw new Error(error.message);
  },

  async upsertBlogPost(p){
    const { error } = await SB.from('blog_posts').upsert({
      ...p, updated_at: new Date().toISOString(),
    }, { onConflict: 'slug' });
    if(error) throw new Error(error.message);
  },
  async deleteBlogPost(slug){
    const { error } = await SB.from('blog_posts').delete().eq('slug', slug);
    if(error) throw new Error(error.message);
  },

  async upsertPortfolioItem(item){
    const { error } = await SB.from('portfolio_items').upsert(item);
    if(error) throw new Error(error.message);
  },
  async deletePortfolioItem(id){
    const { error } = await SB.from('portfolio_items').delete().eq('id', id);
    if(error) throw new Error(error.message);
  },
  async movePortfolioItem(id, dir){
    const list = [...TV_PORTFOLIO];
    const i = list.findIndex(x=>x.id===id);
    const j = i + dir;
    if(i<0 || j<0 || j>=list.length) return;
    [list[i], list[j]] = [list[j], list[i]];
    await Promise.all(list.map((x,idx)=> SB.from('portfolio_items').update({sort_order:idx}).eq('id', x.id)));
  },

  async upsertPackage(p){
    const { error } = await SB.from('packages').upsert(p, { onConflict: 'slug' });
    if(error) throw new Error(error.message);
  },
});

const BUCKET = 'trevity-images';
Object.assign(TvImg, {
  async _store(dataUrl){
    const blob = await (await fetch(dataUrl)).blob();
    const ext  = blob.type === 'image/png' ? 'png' : 'jpg';
    const path = `${new Date().getFullYear()}/${Date.now().toString(36)}${Math.floor(Math.random()*1e9).toString(36)}.${ext}`;
    const { error } = await SB.storage.from(BUCKET).upload(path, blob, {
      contentType: blob.type, cacheControl: '31536000', upsert: false,
    });
    if(error) throw new Error('업로드 실패: ' + error.message);
    return SB.storage.from(BUCKET).getPublicUrl(path).data.publicUrl;
  },
  isRef(){ return false; },
  resolve(v){ return v; },
  async loadCache(){ return true; },
  async usage(){ return { count:0, used:0, quota:0 }; },
  async gc(){ return 0; },
});

}
