/* ============================================================
   트래비티 관리자 백엔드 설정
   ------------------------------------------------------------
   아래 두 값을 채우면 자동으로 Supabase 모드로 전환됩니다.
   비워두면 브라우저 저장(localStorage) 모드로 동작합니다.
   값 찾는 곳: Supabase 대시보드 → Project Settings → API
   ============================================================ */
const TV_SUPABASE_URL  = '';
const TV_SUPABASE_ANON = '';

const TV_BACKEND = (TV_SUPABASE_URL && TV_SUPABASE_ANON) ? 'supabase' : 'local';
