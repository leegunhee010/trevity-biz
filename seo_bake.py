# -*- coding: utf-8 -*-
"""트래비티 SEO 굽기 모듈 — 인천 퍼스트디자인 관리자(bake_seo_tech/bake_geo/bake_breadcrumb) 이식.
edit-server.py 가 API 로 호출하고, 단독 실행도 가능: python seo_bake.py
모든 결과는 HTML 파일에 직접 박힌다(정적, AI 읽기)."""
import io
import json
import os
import pathlib
import re
import datetime

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / "admin" / "data"
DATA.mkdir(parents=True, exist_ok=True)

# ---------- 페이지 목록: (파일명, 라벨, 우선순위, 변경빈도, 기본 키워드) ----------
PAGES = [
    ("index",          "메인",            1.0, "weekly",  "인플루언서 마케팅, 베트남 마케팅, 틱톡 인플루언서, 체험단 마케팅, 트래비티"),
    ("vietnam-tiktok", "수출 랜딩",        0.9, "weekly",  "베트남 틱톡 인플루언서, 쇼피 마케팅, 틱톡샵 어필리에이트, 베트남 인플루언서 섭외, 동남아 마케팅"),
    ("tourist-vn",     "베트남 관광객",     0.9, "monthly", "베트남인 관광객 마케팅, 방한 베트남인, 외국인 관광객 유치, 베트남 체험단"),
    ("tourist-cn",     "중국 관광객",       0.9, "monthly", "중국인 관광객 마케팅, 샤오홍슈 마케팅, 더우인 마케팅, 중국인 손님 유치"),
    ("local-vn",       "베트남 현지 매장",   0.9, "monthly", "베트남 현지 마케팅, 호치민 매장 마케팅, 베트남 식당 홍보, 베트남 로컬 인플루언서"),
    ("stay",           "숙박 체험단",       0.9, "monthly", "숙박 체험단, 호텔 마케팅, 펜션 홍보, 숙소 인플루언서"),
    ("blog",           "블로그",           0.7, "weekly",  "인플루언서 마케팅 인사이트, 베트남 시장, 틱톡 마케팅"),
    ("help",           "고객센터",          0.6, "monthly", "트래비티 고객센터, 자주 묻는 질문"),
    ("agency",         "공식대행사",        0.6, "monthly", "트래비티 공식대행사, 파트너"),
    ("inquiry",        "문의",             0.6, "monthly", "인플루언서 마케팅 문의, 베트남 마케팅 견적"),
]
PAGE_LABELS = dict((p, l) for p, l, *_ in PAGES)

DEFAULT_SETTINGS = {
    "domain": "https://leegunhee010.github.io/trevity-biz",
    "siteName": "트래비티 TREVITY",
    "headCode": "",
    "favicon": "",
    "ogImage": "",
    "snsKakao": "", "snsInstagram": "", "snsBlog": "", "snsPhone": "",
    "snsNaverTalk": "", "snsInquiry": False,
    "channelTalkKey": "",
    "mailEndpoint": "", "mailTo": "",
}


def settings():
    p = DATA / "settings.json"
    st = dict(DEFAULT_SETTINGS)
    if p.exists():
        st.update(json.loads(p.read_text(encoding="utf-8")))
    return st


def save_settings(st):
    (DATA / "settings.json").write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")


def _page_file(page):
    page = page[:-5] if page.endswith(".html") else page
    return ROOT / f"{page}.html", page


def _read(p):
    return io.open(p, encoding="utf-8").read()


def _write(p, s):
    io.open(p, "w", encoding="utf-8", newline="").write(s)


# ---------- 페이지별 메타 읽기/굽기 ----------
def read_meta(page):
    p, _ = _page_file(page)
    if not p.exists():
        return None
    s = _read(p)
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    k = re.search(r'<meta name="keywords" content="([^"]*)"', s)
    return {"title": (t.group(1).strip() if t else ""),
            "description": (d.group(1) if d else ""),
            "keywords": (k.group(1) if k else "")}


def bake_meta(page, meta):
    """title/description/keywords + og:title/og:description 동기 굽기."""
    p, _ = _page_file(page)
    s = _read(p)
    title = meta.get("title", "")
    desc = meta.get("description", "")
    kw = meta.get("keywords", "")
    if title:
        if re.search(r"<title>.*?</title>", s, re.S):
            s = re.sub(r"<title>.*?</title>", lambda m: f"<title>{title}</title>", s, count=1, flags=re.S)
        else:
            s = s.replace("</head>", f"<title>{title}</title>\n</head>", 1)
        if re.search(r'<meta property="og:title" content="[^"]*"', s):
            s = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1) + title + m.group(2), s)
        else:
            s = s.replace("</head>", f'<meta property="og:title" content="{title}"/>\n</head>', 1)
    if desc:
        if re.search(r'<meta name="description" content="[^"]*"', s):
            s = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + desc + m.group(2), s)
        else:
            s = s.replace("</head>", f'<meta name="description" content="{desc}"/>\n</head>', 1)
        if re.search(r'<meta property="og:description" content="[^"]*"', s):
            s = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1) + desc + m.group(2), s)
        else:
            s = s.replace("</head>", f'<meta property="og:description" content="{desc}"/>\n</head>', 1)
    # keywords 는 빈 값이어도 지정되면 교체
    if re.search(r'<meta name="keywords" content="[^"]*"', s):
        s = re.sub(r'(<meta name="keywords" content=")[^"]*(")', lambda m: m.group(1) + kw + m.group(2), s)
    elif kw:
        s = s.replace("</head>", f'<meta name="keywords" content="{kw}"/>\n</head>', 1)
    _write(p, s)
    ov = json.loads((DATA / "seo_overrides.json").read_text(encoding="utf-8")) if (DATA / "seo_overrides.json").exists() else {}
    ov[_page_file(page)[1]] = {"title": title, "description": desc, "keywords": kw}
    (DATA / "seo_overrides.json").write_text(json.dumps(ov, ensure_ascii=False, indent=1), encoding="utf-8")


# ---------- 회사 엔티티 (푸터 실데이터 기반) ----------
def organization_ld(domain):
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": domain + "/#organization",
        "name": "트래비티 TREVITY",
        "legalName": "주식회사 퍼스트마케팅컴퍼니",
        "url": domain + "/",
        "description": ("한국·베트남·중국을 잇는 글로벌 인플루언서 마케팅 그룹. "
                        "한국제품 해외수출, 외국인 관광객 유치, 베트남 현지 매장 마케팅, 숙박 체험단을 운영합니다."),
        "email": "notice@trevity.com",
        "telephone": "+82-70-4212-8266",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "국채보상로 488 섬유회관 3층",
            "addressLocality": "중구",
            "addressRegion": "대구광역시",
            "addressCountry": "KR",
        },
        "areaServed": [{"@type": "Country", "name": n} for n in ["대한민국", "베트남", "중국"]],
        "brand": {"@type": "Brand", "name": "TREVITY"},
    }


def localbusiness_ld(domain):
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": domain + "/#localbusiness",
        "name": "트래비티 TREVITY",
        "description": "글로벌 인플루언서 마케팅 그룹 — 베트남 틱톡 인플루언서 부킹, 외국인 관광객 마케팅, 현지 매장 마케팅, 숙박 체험단.",
        "url": domain + "/",
        "telephone": "+82-70-4212-8266",
        "email": "notice@trevity.com",
        "priceRange": "₩₩",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "국채보상로 488 섬유회관 3층",
            "addressLocality": "중구",
            "addressRegion": "대구광역시",
            "addressCountry": "KR",
        },
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "10:00", "closes": "18:00",
        }],
        "parentOrganization": {"@type": "Organization", "name": "주식회사 퍼스트마케팅컴퍼니"},
    }


# ---------- FAQ 자동 추출 (Q. 아코디언 + details/summary) ----------
def extract_faq(s):
    """① <details><summary>Q...</summary>답</details>  ② <h5>Q. 질문</h5>+<span>답변</span> 쌍."""
    out = []
    for m in re.finditer(r"<details[^>]*>\s*<summary[^>]*>(.*?)</summary>(.*?)</details>", s, re.S):
        q = re.sub(r"<[^>]+>", " ", m.group(1)).strip()
        q = re.sub(r"^\s*Q\.\s*", "", re.sub(r"\s+", " ", q))
        a = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(2))).strip()
        if q and a:
            out.append((q, a))
    for m in re.finditer(r"<h5[^>]*>\s*Q\.\s*(.*?)</h5>(.*?)(?=<h5[^>]*>\s*Q\.|</section>|$)", s, re.S):
        q = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        am = re.search(r'<span[^>]*text-\[16px\][^>]*>(.*?)</span>', m.group(2), re.S)
        if not am:
            am = re.search(r"<span[^>]*>(.*?)</span>", m.group(2), re.S)
        a = re.sub(r"<[^>]+>", " ", am.group(1)).strip() if am else ""
        a = re.sub(r"\s+", " ", a)
        if q and a:
            out.append((q, a))
    return out


# ---------- 블로그 데이터 (rss용) ----------
def blog_posts():
    p = ROOT / "assets" / "js" / "data.js"
    if not p.exists():
        return []
    s = _read(p)
    m = re.search(r"const TV_BLOG_POSTS = (\[.*?\]);", s, re.S)
    if not m:
        return []
    try:
        return json.loads(m.group(1))
    except Exception:
        return []


# ---------- 기술 SEO 일괄 굽기 ----------
def bake_technical():
    st = settings()
    domain = st["domain"].rstrip("/")
    today = datetime.date.today().isoformat()
    urls = []
    changed = 0

    for page, label, prio, freq, kw in PAGES:
        p = ROOT / f"{page}.html"
        if not p.exists():
            continue
        s = _read(p)
        url = domain + ("/" if page == "index" else f"/{page}.html")
        urls.append((url, prio, freq))

        # 1) canonical
        link = f'<link rel="canonical" href="{url}">'
        if re.search(r'<link\s+rel="canonical"[^>]*>', s):
            s = re.sub(r'<link\s+rel="canonical"[^>]*>', link, s, count=1)
        else:
            s = s.replace("</head>", link + "\n</head>", 1)
        # 2) og:url
        if re.search(r'<meta\s+property="og:url"[^>]*>', s):
            s = re.sub(r'(<meta\s+property="og:url"\s+content=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), s)
        else:
            s = s.replace("</head>", f'<meta property="og:url" content="{url}"/>\n</head>', 1)
        # 3) keywords 기본값 (없을 때만 — 관리자 수정분 보존)
        if not re.search(r'<meta\s+name="keywords"', s):
            s = s.replace("</head>", f'<meta name="keywords" content="{kw}"/>\n</head>', 1)

        # 4) BreadcrumbList (index 제외, 마커 재실행 안전)
        s = re.sub(r"<!--crumb-ld-->.*?<!--/crumb-ld-->", "", s, flags=re.S)
        if page != "index":
            crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "홈", "item": domain + "/"},
                {"@type": "ListItem", "position": 2, "name": label, "item": url},
            ]}
            s = s.replace("</head>", "<!--crumb-ld--><script type=\"application/ld+json\">"
                          + json.dumps(crumb, ensure_ascii=False) + "</script><!--/crumb-ld-->\n</head>", 1)

        # 5) Organization + LocalBusiness — 인천 방식대로 전 페이지(회사 엔티티 사이트 전역)
        s = re.sub(r"<!--org-ld-->.*?<!--/org-ld-->", "", s, flags=re.S)
        lds = [organization_ld(domain), localbusiness_ld(domain)]
        block = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>" for x in lds)
        s = s.replace("</head>", "<!--org-ld-->" + block + "<!--/org-ld-->\n</head>", 1)

        # 6) FAQPage JSON-LD 자동 (Q. 아코디언 있는 페이지)
        s = re.sub(r"<!--faq-ld-->.*?<!--/faq-ld-->", "", s, flags=re.S)
        qa = extract_faq(s)
        if qa:
            ld = {"@context": "https://schema.org", "@type": "FAQPage",
                  "mainEntity": [{"@type": "Question", "name": q,
                                  "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}
            s = s.replace("</head>", "<!--faq-ld--><script type=\"application/ld+json\">"
                          + json.dumps(ld, ensure_ascii=False) + "</script><!--/faq-ld-->\n</head>", 1)

        _write(p, s)
        changed += 1

    # 7) sitemap.xml (게시판 정적 글 페이지 포함)
    for c in blog_posts():
        if c.get("published") is False:
            continue
        if (ROOT / f"blog-{c.get('slug','')}.html").exists():
            urls.append((f"{domain}/blog-{c['slug']}.html", 0.6, "yearly"))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, prio, freq in urls:
        sm.append(f"  <url><loc>{url}</loc><lastmod>{today}</lastmod>"
                  f"<changefreq>{freq}</changefreq><priority>{prio}</priority></url>")
    sm.append("</urlset>")
    _write(ROOT / "sitemap.xml", "\n".join(sm))

    # 8) robots.txt
    _write(ROOT / "robots.txt",
           "User-agent: *\nAllow: /\nDisallow: /admin/\n\n"
           f"Sitemap: {domain}/sitemap.xml\n")

    # 9) rss.xml (블로그 글 — data.js 시드 기준)
    items = []
    for c in blog_posts():
        if c.get("published") is False:
            continue
        link = f"{domain}/blog-{c.get('slug','')}.html"
        items.append(f"    <item><title>{c.get('title','')}</title>"
                     f"<link>{link}</link>"
                     f"<description>{c.get('excerpt','')}</description>"
                     f"<pubDate>{c.get('created_at','')}</pubDate></item>")
    rss = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<rss version="2.0"><channel>\n'
           "    <title>트래비티 블로그</title>\n"
           f"    <link>{domain}/blog.html</link>\n"
           "    <description>인플루언서 마케팅·베트남 시장 인사이트</description>\n"
           "    <language>ko</language>\n" + "\n".join(items) +
           "\n</channel></rss>")
    _write(ROOT / "rss.xml", rss)

    return {"pages": changed, "sitemapUrls": len(urls)}


# ---------- 설정 굽기 (headCode·파비콘·og:image·SNS) ----------
def _all_html_files():
    return [ROOT / f"{p}.html" for p, *_ in PAGES if (ROOT / f"{p}.html").exists()] + \
           ([ROOT / "blog-post.html"] if (ROOT / "blog-post.html").exists() else [])


def bake_settings():
    st = settings()
    head = (st.get("headCode") or "").strip()
    favicon = (st.get("favicon") or "").lstrip("/")
    ogimage = (st.get("ogImage") or "").lstrip("/")
    domain = st["domain"].rstrip("/")
    for p in _all_html_files():
        s = _read(p)
        s = re.sub(r"<!--head-code-->.*?<!--/head-code-->", "", s, flags=re.S)
        if head:
            s = s.replace("</head>", f"<!--head-code-->{head}<!--/head-code-->\n</head>", 1)
        if favicon:
            # 상대경로 고정 (하위 경로 배포에서 절대경로는 404)
            if re.search(r'<link[^>]*rel="(?:shortcut )?icon"[^>]*>', s):
                s = re.sub(r'<link[^>]*rel="(?:shortcut )?icon"[^>]*>',
                           f'<link rel="icon" href="./{favicon}">', s, count=1)
            else:
                s = s.replace("</head>", f'<link rel="icon" href="./{favicon}">\n</head>', 1)
        if ogimage:
            if re.search(r'<meta property="og:image" content="[^"]*"', s):
                s = re.sub(r'(<meta property="og:image" content=")[^"]*(")',
                           lambda m: m.group(1) + f"{domain}/{ogimage}" + m.group(2), s)
            else:
                s = s.replace("</head>", f'<meta property="og:image" content="{domain}/{ogimage}"/>\n</head>', 1)
        # 채널톡 플러그인 (전 페이지, 마커 재실행 안전)
        s = re.sub(r"<!--chtalk-->.*?<!--/chtalk-->", "", s, flags=re.S)
        key = (st.get("channelTalkKey") or "").strip()
        if key:
            ch = ('<!--chtalk--><script>(function(){var w=window;if(w.ChannelIO)return;var ch=function(){ch.c(arguments)};'
                  'ch.q=[];ch.c=function(a){ch.q.push(a)};w.ChannelIO=ch;function l(){if(w.ChannelIOInitialized)return;'
                  'w.ChannelIOInitialized=true;var x=document.createElement("script");x.type="text/javascript";x.async=true;'
                  'x.src="https://cdn.channel.io/plugin/ch-plugin-web.js";var s=document.getElementsByTagName("script")[0];'
                  's.parentNode.insertBefore(x,s)}if(document.readyState==="complete"){l()}else{w.addEventListener("load",l)}})();'
                  f'ChannelIO("boot",{{"pluginKey":"{key}"}});</script><!--/chtalk-->')
            s = s.replace("</body>", ch + "\n</body>", 1)
        _write(p, s)

    # 문의 메일 발송 설정 → inquiry.html 에 주입
    mp = ROOT / "inquiry.html"
    if mp.exists():
        s = _read(mp)
        s = re.sub(r"<!--mail-cfg-->.*?<!--/mail-cfg-->", "", s, flags=re.S)
        ep = (st.get("mailEndpoint") or "").strip()
        if ep:
            s = s.replace("</head>", f'<!--mail-cfg--><script>window.TV_MAIL_ENDPOINT={json.dumps(ep)};</script><!--/mail-cfg-->\n</head>', 1)
        _write(mp, s)
    return len(_all_html_files())


def bake_sns():
    st = settings()
    kakao = (st.get("snsKakao") or "").strip()
    insta = (st.get("snsInstagram") or "").strip()
    blog = (st.get("snsBlog") or "").strip()
    phone = (st.get("snsPhone") or "").strip()
    ntalk = (st.get("snsNaverTalk") or "").strip()
    inquiry_btn = bool(st.get("snsInquiry"))
    btns = []
    if inquiry_btn:
        btns.append('<a class="sns-fab sns-inq" href="./inquiry.html" aria-label="문의하기">'
                    '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#fff" stroke-width="2">'
                    '<path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 9 9 0 0 1-3.8-.8L3 20l1-4.9a8.4 8.4 0 1 1 17-3.6z"/></svg></a>')
    if ntalk:
        btns.append(f'<a class="sns-fab sns-ntalk" href="{ntalk}" target="_blank" rel="noopener" aria-label="네이버 톡톡"><b>톡톡</b></a>')
    if kakao:
        btns.append(f'<a class="sns-fab sns-kakao" href="{kakao}" target="_blank" rel="noopener" aria-label="카카오톡 상담">'
                    '<svg viewBox="0 0 24 24" width="24" height="24"><path fill="#3C1E1E" d="M12 3C6.5 3 2 6.5 2 10.8c0 2.8 1.9 5.2 4.7 6.6-.2.7-.7 2.6-.8 3-.1.5.2.5.4.4.2-.1 2.6-1.8 3.6-2.5.7.1 1.4.2 2.1.2 5.5 0 10-3.5 10-7.8S17.5 3 12 3z"/></svg></a>')
    if insta:
        btns.append(f'<a class="sns-fab sns-insta" href="{insta}" target="_blank" rel="noopener" aria-label="인스타그램">'
                    '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#fff" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1.2" fill="#fff" stroke="none"/></svg></a>')
    if blog:
        btns.append(f'<a class="sns-fab sns-blog" href="{blog}" target="_blank" rel="noopener" aria-label="블로그"><b>blog</b></a>')
    if phone:
        tel = "tel:" + phone.replace(" ", "").replace("-", "")
        btns.append(f'<a class="sns-fab sns-phone" href="{tel}" aria-label="전화 상담">'
                    '<svg viewBox="0 0 24 24" width="23" height="23" fill="#fff"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .8-.3 1l-2.2 2.2z"/></svg></a>')
    if not btns:
        widget = ""
    else:
        css = ('<style>.sns-float{position:fixed;right:18px;bottom:24px;z-index:9000;display:flex;flex-direction:column;gap:12px}'
               '.sns-fab{width:54px;height:54px;border-radius:50%;display:flex;align-items:center;justify-content:center;'
               'box-shadow:0 6px 16px rgba(0,0,0,.18);transition:transform .18s ease;text-decoration:none}'
               '.sns-fab:hover{transform:translateY(-3px)}'
               '.sns-kakao{background:#FEE500}.sns-insta{background:linear-gradient(45deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888)}'
               '.sns-blog{background:#03C75A}.sns-blog b{color:#fff;font-size:13px;font-weight:800;font-style:normal}'
               '.sns-ntalk{background:#03C75A}.sns-ntalk b{color:#fff;font-size:12px;font-weight:800;font-style:normal}'
               '.sns-inq{background:#fa6781}'
               '.sns-phone{background:#fa6781}'
               '@media(max-width:767px){.sns-float{right:12px;bottom:16px}.sns-fab{width:48px;height:48px}}</style>')
        widget = "<!--sns-float-->" + css + '<div class="sns-float">' + "".join(btns) + "</div><!--/sns-float-->"
    for p in _all_html_files():
        s = _read(p)
        s = re.sub(r"<!--sns-float-->.*?<!--/sns-float-->", "", s, flags=re.S)
        if widget:
            s = s.replace("</body>", widget + "\n</body>", 1)
        _write(p, s)
    return len(btns)


# ---------- 게시판(블로그) — data.js 저장 + 정적 페이지 굽기 ----------
def save_blog_posts(posts):
    p = ROOT / "assets" / "js" / "data.js"
    s = _read(p)
    new = "const TV_BLOG_POSTS = " + json.dumps(posts, ensure_ascii=False) + ";"
    s = re.sub(r"const TV_BLOG_POSTS = \[.*?\];", lambda m: new, s, count=1, flags=re.S)
    _write(p, s)


def _blog_chrome():
    """blog.html에서 head 링크·스타일·헤더·푸터를 추출해 정적 글 페이지 틀로 쓴다."""
    s = _read(ROOT / "blog.html")
    head_end = s.find("</head>")
    head = s[:head_end]
    links = "\n".join(re.findall(r'<link[^>]*>', head))
    styles = "\n".join(re.findall(r"<style[^>]*>.*?</style>", head, re.S))
    hs = s.find("<header"); he = s.find("</header>") + len("</header>")
    fs = s.find("<footer"); fe = s.find("</footer>") + len("</footer>")
    return links, styles, s[hs:he], s[fs:fe]


def bake_post(post):
    """글 1건 → blog-<slug>.html 정적 페이지 (Article JSON-LD 포함, AI 읽기)."""
    st = settings()
    domain = st["domain"].rstrip("/")
    links, styles, header, footer = _blog_chrome()
    slug = post["slug"]
    url = f"{domain}/blog-{slug}.html"
    title = post.get("title", "").replace('"', "&quot;")
    desc = re.sub(r"<[^>]+>", " ", post.get("excerpt", "")).strip().replace('"', "&quot;")
    thumb = post.get("thumbnail_url", "")
    date = str(post.get("created_at", ""))[:10]
    ld = {"@context": "https://schema.org", "@type": "Article",
          "headline": title, "description": desc,
          "datePublished": date, "dateModified": str(post.get("updated_at", ""))[:10] or date,
          "author": {"@type": "Organization", "name": "트래비티 TREVITY"},
          "publisher": {"@type": "Organization", "name": "주식회사 퍼스트마케팅컴퍼니"},
          "mainEntityOfPage": url}
    if thumb:
        ld["image"] = domain + "/" + thumb.lstrip("./")
    crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "홈", "item": domain + "/"},
        {"@type": "ListItem", "position": 2, "name": "블로그", "item": domain + "/blog.html"},
        {"@type": "ListItem", "position": 3, "name": title, "item": url},
    ]}
    kw = post.get("category", "") + ", 트래비티, 인플루언서 마케팅"
    og_img = (domain + "/" + thumb.lstrip("./")) if thumb else ""
    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | 트래비티</title>
<meta name="description" content="{desc}"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:type" content="article"/>
<meta property="og:url" content="{url}"/>
{f'<meta property="og:image" content="{og_img}"/>' if og_img else ''}
<meta name="keywords" content="{kw}"/>
<link rel="canonical" href="{url}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(crumb, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(organization_ld(domain), ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(localbusiness_ld(domain), ensure_ascii=False)}</script>
{links}
{styles}
</head>
<body class="max-[767px]:min-w-[360px] min-[767px]:min-w-[1440px]">
{header}
<div class="tv-bloghero"><p style="font-size:40px;font-weight:800;letter-spacing:-0.8px;color:#1f1f1f;margin:0">{post.get("category", "블로그")}</p></div>
<div style="max-width:760px;margin:0 auto;padding:40px 20px 100px;word-break:keep-all">
  <article>
    <h1 style="font-size:28px;font-weight:800;margin-bottom:10px;line-height:1.4">{title}</h1>
    <p style="color:#8B95A1;font-size:13px;margin-bottom:28px">{date} · {post.get("read_minutes", 4)}분 분량</p>
    {f'<img src="{thumb}" alt="{title}" style="width:100%;border-radius:12px;margin-bottom:28px">' if thumb else ''}
    <div style="line-height:1.85;font-size:16px">{post.get("body_html", "")}</div>
    <p style="margin-top:40px"><a href="./blog.html" style="color:#fa6781;font-weight:700;text-decoration:none">← 블로그 목록으로</a></p>
  </article>
</div>
{footer}
</body>
</html>'''
    _write(ROOT / f"blog-{slug}.html", html)
    return f"blog-{slug}.html"


def bake_board():
    """전체 글 굽기: 정적 글 페이지 + blog.html 목록 카드(정적, 크롤러용) + rss."""
    posts = [p for p in blog_posts() if p.get("published") is not False]
    posts.sort(key=lambda p: str(p.get("created_at", "")), reverse=True)
    files = [bake_post(p) for p in posts]
    # blog.html .tv-grid 에 정적 카드 굽기 (JS 렌더는 같은 내용으로 다시 그림)
    bp = ROOT / "blog.html"
    s = _read(bp)
    cards = "".join(
        f'<article class="tv-card" data-cat="{p.get("category","")}" data-title="{p.get("title","")}">'
        f'<a href="./blog-{p["slug"]}.html">'
        f'<div class="tv-thumb"><img src="{p.get("thumbnail_url","")}" alt="{p.get("title","")}" loading="lazy"/></div>'
        f'<div class="tv-card-body"><span class="tv-chip">{p.get("category","")}</span><h3>{p.get("title","")}</h3>'
        f'<div class="tv-meta"><time>{str(p.get("created_at",""))[:10]}</time><span>{p.get("read_minutes",4)}분 분량</span></div></div>'
        f'</a></article>' for p in posts)
    # 마커 기반 교체 — 카드 내부 </div> 때문에 regex 로 grid 경계를 잡으면 구조가 깨진다(2026-07-31 실제 사고)
    if "<!--bd-cards-->" not in s:
        s = s.replace('<div class="tv-grid">', '<div class="tv-grid"><!--bd-cards--><!--/bd-cards-->', 1)
    s = re.sub(r"<!--bd-cards-->.*?<!--/bd-cards-->",
               lambda m: "<!--bd-cards-->" + cards + "<!--/bd-cards-->", s, flags=re.S)
    _write(bp, s)
    # rss 갱신
    bake_technical()
    return files


if __name__ == "__main__":
    r = bake_technical()
    n = bake_settings()
    print(f"기술 SEO: {r['pages']}페이지 canonical/JSON-LD | sitemap {r['sitemapUrls']}개 URL | robots·rss 생성 | 설정 {n}페이지")
