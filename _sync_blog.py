# -*- coding: utf-8 -*-
"""수파베이스 → 정적 사이트 자동 동기화 (GitHub Actions에서 주기 실행).
① blog_posts: 변경 시 data.js 교체 → blog-<slug>.html 굽기 → 목록·sitemap·rss → 삭제글 파일 제거
② site_copy의 seo::<page> 행: 페이지별 title/description/keywords를 HTML에 굽기
③ site_copy의 seocfg::settings 행: 파비콘·OG·헤드코드·채널톡·플로팅 버튼·문의메일을 전 페이지에 굽기
변경이 없으면 파일이 그대로라 커밋도 안 생긴다 (모든 굽기는 마커 기반 재실행-안전).
로컬에서도 그대로 실행 가능: python _sync_blog.py
"""
import json, pathlib, re, sys, urllib.request

ROOT = pathlib.Path(__file__).parent
sys.stdout.reconfigure(encoding="utf-8")

# 공개 anon 키 (RLS로 보호되는 읽기 전용 접근 — 브라우저에도 노출되는 값)
cfg = (ROOT / "assets" / "js" / "config.js").read_text(encoding="utf-8")
SB_URL = re.search(r"TV_SUPABASE_URL\s*=\s*'([^']+)'", cfg).group(1)
SB_KEY = re.search(r"TV_SUPABASE_ANON\s*=\s*'([^']+)'", cfg).group(1)


def sb_get(path):
    req = urllib.request.Request(SB_URL + path,
        headers={"apikey": SB_KEY, "Authorization": "Bearer " + SB_KEY})
    return json.load(urllib.request.urlopen(req, timeout=30))


import seo_bake

# ---------- ① 블로그 ----------
posts = sb_get("/rest/v1/blog_posts"
               "?select=slug,title,category,thumbnail_url,excerpt,body_html,read_minutes,published,created_at"
               "&published=eq.true&order=created_at.desc")
if json.dumps(posts, sort_keys=True, ensure_ascii=False) == \
   json.dumps(seo_bake.blog_posts(), sort_keys=True, ensure_ascii=False):
    print("블로그: 변경 없음")
else:
    seo_bake.save_blog_posts(posts)
    print("블로그 구움:", seo_bake.bake_board())
    keep = {f"blog-{p['slug']}.html" for p in posts} | {"blog-post.html"}
    for f in ROOT.glob("blog-*.html"):
        if f.name not in keep:
            f.unlink()
            print("삭제:", f.name)

# ---------- ② ③ SEO 메타 · 사이트 설정 (site_copy의 seo* 키) ----------
rows = sb_get("/rest/v1/site_copy?select=key,value&key=like.seo%2A")
valid_pages = {p for p, *_ in seo_bake.PAGES}
for row in rows:
    k = row["key"]
    try:
        data = json.loads(row["value"])
    except Exception:
        print("무시(JSON 아님):", k)
        continue
    if k.startswith("seo::"):
        page = k[5:]
        if page in valid_pages:
            seo_bake.bake_meta(page, data)
            print("메타 구움:", page)
    elif k == "seocfg::settings":
        st = seo_bake.settings()
        allowed = set(seo_bake.DEFAULT_SETTINGS) - {"domain", "siteName"}   # 도메인은 로컬 도구에서만
        upd = {kk: vv for kk, vv in data.items() if kk in allowed}
        if any(st.get(kk) != vv for kk, vv in upd.items()):
            st.update(upd)
            seo_bake.save_settings(st)
            n = seo_bake.bake_settings()
            b = seo_bake.bake_sns()
            print(f"설정 구움: {n}페이지, 플로팅 버튼 {b}개")
        else:
            print("설정: 변경 없음")
