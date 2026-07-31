/* ============================================================
   트래비티 관리자 백엔드 설정
   ------------------------------------------------------------
   아래 두 값을 채우면 자동으로 Supabase 모드로 전환됩니다.
   비워두면 브라우저 저장(localStorage) 모드로 동작합니다.
   값 찾는 곳: Supabase 대시보드 → Project Settings → API
   ============================================================ */
const TV_SUPABASE_URL  = 'https://trnfdgzblrtprrbttecp.supabase.co';
const TV_SUPABASE_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRybmZkZ3pibHJ0cHJyYnR0ZWNwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODU0ODAxODUsImV4cCI6MjEwMTA1NjE4NX0.jLx0Kke60dDT6rFj0Pd12UoMO2A86FXquoJwufK9Fm4';

const TV_BACKEND = (TV_SUPABASE_URL && TV_SUPABASE_ANON) ? 'supabase' : 'local';
