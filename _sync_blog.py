# -*- coding: utf-8 -*-
"""수파베이스 blog_posts → 정적 페이지 자동 동기화 (GitHub Actions에서 주기 실행).
변경이 없으면 아무것도 안 하고 종료. 변경이 있으면:
  data.js TV_BLOG_POSTS 교체 → blog-<slug>.html 전체 굽기 → 목록·sitemap·rss 갱신 → 삭제된 글 파일 제거
로컬에서도 그대로 실행 가능: python _sync_blog.py
"""
import json, pathlib, re, sys, urllib.request

ROOT = pathlib.Path(__file__).parent
sys.stdout.reconfigure(encoding="utf-8")

# 공개 anon 키 (RLS로 보호되는 읽기 전용 접근 — 브라우저에도 노출되는 값)
cfg = (ROOT / "assets" / "js" / "config.js").read_text(encoding="utf-8")
SB_URL = re.search(r"TV_SUPABASE_URL\s*=\s*'([^']+)'", cfg).group(1)
SB_KEY = re.search(r"TV_SUPABASE_ANON\s*=\s*'([^']+)'", cfg).group(1)

req = urllib.request.Request(
    SB_URL + "/rest/v1/blog_posts"
    "?select=slug,title,category,thumbnail_url,excerpt,body_html,read_minutes,published,created_at"
    "&published=eq.true&order=created_at.desc",
    headers={"apikey": SB_KEY, "Authorization": "Bearer " + SB_KEY})
posts = json.load(urllib.request.urlopen(req, timeout=30))

import seo_bake
current = seo_bake.blog_posts()
if json.dumps(posts, sort_keys=True, ensure_ascii=False) == json.dumps(current, sort_keys=True, ensure_ascii=False):
    print("변경 없음 — 종료")
    sys.exit(0)

seo_bake.save_blog_posts(posts)
files = seo_bake.bake_board()
print("구움:", files)

# 삭제·비공개된 글의 정적 파일 제거
keep = {f"blog-{p['slug']}.html" for p in posts} | {"blog-post.html"}
for f in ROOT.glob("blog-*.html"):
    if f.name not in keep:
        f.unlink()
        print("삭제:", f.name)
