/* ============================================================
   트래비티 이미지 업로드 — 관리자에서 파일을 직접 올린다.
   서버가 없는 로컬 모드: 브라우저에서 리사이즈·압축 후 IndexedDB에 저장,
   데이터에는 'tvimg:<id>' 참조만 넣고 부팅 시 실제 이미지로 치환.
   Supabase 모드에서는 store-supabase.js가 _store()만 갈아끼워 Storage로 올린다.
   ============================================================ */
const TvImg = {
  DB: 'trevity_img', STORE: 'img',
  MAXW: 1600,
  QUALITY: 0.86,
  _db: null,
  _cache: {},

  open(){
    if(this._db) return Promise.resolve(this._db);
    return new Promise((res, rej)=>{
      const rq = indexedDB.open(this.DB, 1);
      rq.onupgradeneeded = e => {
        const db = e.target.result;
        if(!db.objectStoreNames.contains(this.STORE)) db.createObjectStore(this.STORE);
      };
      rq.onsuccess = e => { this._db = e.target.result; res(this._db); };
      rq.onerror   = e => rej(e.target.error);
    });
  },
  async _tx(mode, fn){
    const db = await this.open();
    return new Promise((res, rej)=>{
      const tx = db.transaction(this.STORE, mode);
      const rq = fn(tx.objectStore(this.STORE));
      rq.onsuccess = () => res(rq.result);
      rq.onerror   = () => rej(rq.error);
    });
  },
  put(id, dataUrl){ return this._tx('readwrite', s => s.put(dataUrl, id)); },
  get(id){         return this._tx('readonly',  s => s.get(id)); },
  del(id){         return this._tx('readwrite', s => s.delete(id)); },
  keys(){          return this._tx('readonly',  s => s.getAllKeys()); },
  values(){        return this._tx('readonly',  s => s.getAll()); },

  _load(file){
    return new Promise((res, rej)=>{
      if(!/^image\//.test(file.type)) return rej(new Error('이미지 파일만 올릴 수 있습니다'));
      const fr = new FileReader();
      fr.onerror = () => rej(new Error('파일을 읽지 못했습니다'));
      fr.onload = () => {
        const img = new Image();
        img.onerror = () => rej(new Error('이미지를 열지 못했습니다'));
        img.onload = () => res(img);
        img.src = fr.result;
      };
      fr.readAsDataURL(file);
    });
  },

  async compress(file){
    const img = await this._load(file);
    const keepAlpha = /png|webp|svg/i.test(file.type);
    const scale = Math.min(1, this.MAXW / img.width);
    const w = Math.round(img.width * scale);
    const h = Math.round(img.height * scale);
    const cv = document.createElement('canvas');
    cv.width = w; cv.height = h;
    const cx = cv.getContext('2d');
    cx.imageSmoothingQuality = 'high';
    if(!keepAlpha){ cx.fillStyle = '#fff'; cx.fillRect(0,0,w,h); }
    cx.drawImage(img, 0, 0, w, h);
    const out = keepAlpha ? cv.toDataURL('image/png') : cv.toDataURL('image/jpeg', this.QUALITY);
    return { dataUrl: out, w, h, bytes: Math.round(out.length * 0.75) };
  },

  _newId(){
    return 'i' + Date.now().toString(36) + Math.floor(Math.random()*1e6).toString(36);
  },
  async _store(dataUrl){
    const id = this._newId();
    await this.put(id, dataUrl);
    this._cache[id] = dataUrl;
    return 'tvimg:' + id;
  },
  async save(file){
    const { dataUrl, w, h, bytes } = await this.compress(file);
    const ref = await this._store(dataUrl);
    return { ref, dataUrl, w, h, bytes };
  },

  isRef(v){ return typeof v === 'string' && v.startsWith('tvimg:'); },
  resolve(v){ if(!this.isRef(v)) return v; return this._cache[v.slice(6)] || ''; },

  async loadCache(){
    try{
      const [keys, vals] = await Promise.all([this.keys(), this.values()]);
      keys.forEach((k,i)=>{ this._cache[k] = vals[i]; });
      return true;
    }catch(e){ return false; }
  },

  async usage(){
    let used = 0, count = 0;
    try{ const vals = await this.values(); count = vals.length; vals.forEach(v => used += v.length * 0.75); }catch(e){}
    let quota = 0;
    try{ const est = await navigator.storage.estimate(); quota = est.quota || 0; }catch(e){}
    return { count, used, quota };
  },

  async gc(){
    const used = new Set();
    const walk = obj => {
      if(!obj || typeof obj !== 'object') return;
      Object.values(obj).forEach(v=>{
        if(typeof v === 'string'){ if(this.isRef(v)) used.add(v.slice(6)); }
        else walk(v);
      });
    };
    ['tv_blog_override','tv_portfolio_override'].forEach(k=>{
      try{ walk(JSON.parse(localStorage.getItem(k)||'null')); }catch(e){}
    });
    const keys = await this.keys();
    const dead = keys.filter(k=>!used.has(k));
    for(const k of dead){ await this.del(k); delete this._cache[k]; }
    return dead.length;
  },
};

function fmtBytes(n){
  if(n < 1024) return n + ' B';
  if(n < 1024*1024) return (n/1024).toFixed(0) + ' KB';
  return (n/1024/1024).toFixed(1) + ' MB';
}
