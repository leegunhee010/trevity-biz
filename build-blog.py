# -*- coding: utf-8 -*-
# 블로그 리스트(blog.html) + 상세 4페이지 생성, 메뉴 연결
import re

idx = open('index.html', encoding='utf-8').read()

def balanced(html, start, tag='div'):
    depth = 0
    for m in re.finditer(r'<%s\b|</%s>' % (tag, tag), html[start:]):
        depth += 1 if not m.group(0).startswith('</') else -1
        if depth == 0:
            return start + m.end()

head_end = idx.find('</head>') + len('</head>')
head = idx[:head_end]
ds = idx.find('<div class="max-[767px]:hidden"><div class="fixed top-0 z-40 h-[72px]')
hdr = idx[ds:balanced(idx, ds)]
ms = idx.find('<div class="min-[768px]:hidden">')
mhdr = '<div>' + idx[ms:balanced(idx, ms)] + '</div>'
fs = idx.find('<footer')
footer = idx[fs:balanced(idx, fs, 'footer')]

# 블로그 메뉴 활성화 버전 헤더
def activate_blog(h):
    return h.replace(
        '<a href="./blog" class="center h-full"><button type="button" class="center h-full px-[16px] text-gray-600 hover:text-red-500"><div class="flex items-center gap-[8px]"><span class="text-[16px] font-[500] leading-[1.5] -tracking-[0.32px]">블로그</span>',
        '<a href="./blog.html" class="center h-full"><button type="button" class="center h-full px-[16px] text-red-500"><div class="flex items-center gap-[8px]"><span class="text-[16px] font-[700] leading-[1.5] -tracking-[0.32px]">블로그</span>')

POSTS = [
    dict(slug='blog-market', cat='베트남 시장', title='동남아 틱톡 사용률 2위, 베트남 시장이 특별한 이유',
         date='2026.07.21', read='4분 분량', thumb='images/blog/thumb-market.png',
         paras=[
            '베트남의 틱톡 사용자는 약 6,700만 명, 광고 도달 가능 사용자만 약 4,000만 명입니다. 동남아시아에서 틱톡 사용률 2위에 해당하는 규모입니다.',
            '더 중요한 것은 연령 구성입니다. 사용자 10명 중 7명이 18~34세로, 트렌드에 가장 민감하고 소비 전환이 빠른 세대가 틱톡에 모여 있습니다. 베트남 인터넷 사용자의 약 70%가 틱톡을 사용합니다.',
            '베트남에서 트렌드를 이끄는 세대는 틱톡을 중심으로 움직입니다. 새로운 매장, 새로운 제품이 알려지는 경로도 검색이 아니라 피드입니다. 한국에서 네이버 검색이 하는 역할을, 베트남에서는 틱톡 추천 피드가 하고 있다고 보면 이해가 빠릅니다.',
            '그래서 베트남 진출 초기에 가장 효율이 높은 채널도 틱톡입니다. 검증된 인플루언서가 만든 콘텐츠 하나가 매장 방문과 제품 구매로 이어지는 속도는, 다른 어떤 채널보다 빠릅니다.',
         ]),
    dict(slug='blog-midtier', cat='인플루언서 부킹', title='팔로워 10만~50만, 왜 이 구간이 가장 효율적일까요?',
         date='2026.07.19', read='5분 분량', thumb='images/about-tiktok.png',
         paras=[
            '인플루언서 마케팅에서 가장 자주 받는 질문이 있습니다. "팔로워가 많을수록 좋은 것 아닌가요?" 결론부터 말씀드리면, 아닙니다.',
            '팔로워 1,000명대 계정에 제품을 뿌리는 시딩은 비용이 적게 드는 대신 판매로 이어지지 않습니다. 물류비, 인증, 관세까지 부담하며 들여온 제품을 영향력 없는 계정에 소진하기엔 너무 아깝습니다. 반대로 100만 팔로워급 셀럽은 비용이 기하급수적으로 올라가고, 광고 티가 나는 순간 반응이 식습니다.',
            '팔로워 10만~50만 구간은 그 사이에 있습니다. 콘텐츠 품질과 오디언스 신뢰가 검증되어 있으면서도, 아직 팬과의 거리가 가까워 추천이 실제 행동으로 이어지는 구간입니다.',
            '트래비티가 이 구간만 부킹하는 이유도 여기에 있습니다. 그리고 이 구간이라면 팔로워 수와 관계없이 1명당 20만원 균일가로 진행합니다. 규모가 아니라 제품과의 연관성으로 인플루언서를 고르셔야 하니까요.',
         ]),
    dict(slug='blog-diy', cat='틱톡 마케팅', title='직접 섭외해 보면 알게 되는 것들 — 인플루언서 마케팅 9단계',
         date='2026.07.16', read='4분 분량', thumb='images/blog/thumb-process.png',
         paras=[
            '인플루언서 마케팅을 직접 해보려고 하면, 생각보다 많은 단계를 만나게 됩니다. 인플루언서 찾기, 한 명씩 DM 보내기, 답장 기다리기, 협업 비용 문의까지가 시작입니다.',
            '겨우 답장을 받아도 끝이 아닙니다. 생각보다 높은 협업 비용에 놀라고, 결국 예산에 맞춰 영향력이 낮은 인플루언서를 선택하게 됩니다. 그 뒤로도 콘텐츠 조율, 촬영 일정 조율, 영상 업로드 확인, 성과 확인까지 전부 브랜드의 몫입니다.',
            '외국 브랜드라면 난이도가 한 단계 더 올라갑니다. 언어가 다르고, 현지 정서를 모르면 가이드 전달부터 어긋납니다. 단가도 현지 브랜드보다 높게 부르는 경우가 많습니다.',
            '트래비티는 이 아홉 단계를 의뢰서 한 장으로 줄였습니다. 베트남 현지 마케터가 섭외부터 가이드, 검수까지 직접 진행하기 때문에, 직접 하는 것보다 싸고 확실합니다.',
         ]),
    dict(slug='blog-hantown', cat='캠페인 사례', title='호치민 한식당 HAN TOWN, 현지 인플루언서 리뷰 캠페인 기록',
         date='2026.07.14', read='3분 분량', thumb='images/portfolio-hantown.png',
         paras=[
            '호치민 빈탄 지역의 한식당 HAN TOWN은 현지 고객 확보가 과제였습니다. 트래비티는 매장의 분위기와 메뉴에 맞는 현지 푸드 인플루언서를 선별해 리뷰 캠페인을 진행했습니다.',
            '인플루언서마다 같은 매장을 다른 각도로 소개했습니다. 학생 상권이라는 입지에 맞춰 가성비를 앞세운 콘텐츠, 메뉴 비주얼을 살린 먹방형 콘텐츠, 매장 분위기를 담은 브이로그형 콘텐츠가 동시에 퍼지며 피드를 채웠습니다.',
            '이런 캠페인들이 쌓여 트래비티의 누적 프로젝트 7,000건, 누적 콘텐츠 조회 280만, 누적 좋아요 100만이라는 기록이 되었습니다.',
            '매장에 맞는 전략과 체계적인 캠페인 관리가 틱톡 마케팅의 성과를 좌우합니다. 비슷한 고민을 하고 계시다면, 상담에서 매장 상황에 맞는 방향부터 함께 잡아드립니다.',
         ]),
]

cats = []
for p in POSTS:
    if p['cat'] not in cats:
        cats.append(p['cat'])

STYLE = '''<style id="blog-style">
html{scroll-behavior:smooth}
.tv-blog{max-width:1084px;margin:0 auto;padding:64px 20px 120px;display:flex;gap:48px;align-items:flex-start}
.tv-side{flex:0 0 232px;position:sticky;top:100px}
.tv-search{display:flex;border:1.5px solid #e5e7eb;border-radius:10px;overflow:hidden;background:#fff}
.tv-search input{flex:1;border:none;outline:none;padding:12px 14px;font-size:14.5px;font-family:inherit}
.tv-search button{border:none;background:none;padding:0 14px;cursor:pointer;color:#fa6781}
.tv-side h3{margin:32px 0 12px;font-size:16px;font-weight:700;color:#1f1f1f;letter-spacing:-0.32px}
.tv-cats{list-style:none;padding:0;margin:0}
.tv-cats li{margin-bottom:2px}
.tv-cats a{display:flex;justify-content:space-between;padding:10px 12px;border-radius:8px;text-decoration:none;color:#595959;font-size:14.5px;letter-spacing:-0.29px}
.tv-cats a:hover{background:#fff0f3}
.tv-cats li.on a{background:#fff0f3;color:#fa6781;font-weight:700}
.tv-grid{flex:1;display:grid;grid-template-columns:repeat(2,1fr);gap:28px}
.tv-card{border-radius:16px;overflow:hidden;background:#fff;border:1px solid #f0f0f0;box-shadow:0 2px 12px rgba(0,0,0,0.04);transition:transform .25s ease,box-shadow .25s ease}
.tv-card:hover{transform:translateY(-4px);box-shadow:0 12px 32px rgba(0,0,0,0.10)}
.tv-card a{text-decoration:none;color:inherit;display:block}
.tv-thumb{aspect-ratio:16/10;overflow:hidden;background:#fff5f7}
.tv-thumb img{width:100%;height:100%;object-fit:cover;display:block}
.tv-card-body{padding:20px 22px 24px}
.tv-chip{display:inline-block;font-size:12.5px;font-weight:700;color:#fa6781;background:#fff0f3;border-radius:999px;padding:4px 10px;margin-bottom:10px}
.tv-card h3{font-size:18px;font-weight:700;line-height:1.45;letter-spacing:-0.36px;color:#1f1f1f;margin:0 0 12px}
.tv-meta{font-size:13px;color:#8c8c8c;display:flex;gap:10px}
.tv-empty{padding:80px 0;text-align:center;color:#8c8c8c;font-size:15px}
.tv-bloghero{background:linear-gradient(180deg,#ffe9ee,#fff);padding:150px 20px 56px;text-align:center}
.tv-bloghero h1{font-size:40px;font-weight:800;letter-spacing:-0.8px;color:#1f1f1f;margin:0 0 14px}
.tv-bloghero p{font-size:17px;color:#595959;letter-spacing:-0.34px;line-height:1.7;margin:0}
.tv-article{max-width:760px;margin:0 auto;padding:140px 20px 100px}
.tv-article .tv-chip{margin-bottom:14px}
.tv-article h1{font-size:34px;font-weight:800;line-height:1.45;letter-spacing:-0.68px;color:#1f1f1f;margin:0 0 14px}
.tv-article .tv-meta{margin-bottom:32px}
.tv-article .tv-cover{border-radius:16px;overflow:hidden;margin-bottom:40px}
.tv-article .tv-cover img{width:100%;display:block}
.tv-article p{font-size:17px;line-height:1.85;letter-spacing:-0.34px;color:#434343;margin:0 0 24px}
.tv-back{display:inline-flex;align-items:center;gap:6px;margin-top:24px;color:#fa6781;font-weight:700;font-size:15px;text-decoration:none}
@media (max-width:767px){.tv-blog{flex-direction:column}.tv-side{position:static;flex:none;width:100%}.tv-grid{grid-template-columns:1fr}.tv-bloghero{padding-top:110px}.tv-bloghero h1{font-size:30px}.tv-article{padding-top:100px}.tv-article h1{font-size:26px}}
</style>'''

# ── 리스트 페이지 ──
cat_lis = ['<li class="on" data-cat="all"><a href="#"><span>전체</span><span>(%d)</span></a></li>' % len(POSTS)]
for c in cats:
    n = sum(1 for p in POSTS if p['cat'] == c)
    cat_lis.append('<li data-cat="%s"><a href="#"><span>%s</span><span>(%d)</span></a></li>' % (c, c, n))

cards = []
for p in POSTS:
    cards.append(
        '<article class="tv-card" data-cat="%s" data-title="%s"><a href="./%s.html">'
        '<div class="tv-thumb"><img src="./%s" alt="%s" loading="lazy"/></div>'
        '<div class="tv-card-body"><span class="tv-chip">%s</span><h3>%s</h3>'
        '<div class="tv-meta"><time>%s</time><span>%s</span></div></div></a></article>'
        % (p['cat'], p['title'], p['slug'], p['thumb'], p['title'], p['cat'], p['title'], p['date'], p['read']))

FILTER_JS = '''<script>
(function () {
  var items = document.querySelectorAll('.tv-card');
  var cats = document.querySelectorAll('.tv-cats li');
  var input = document.getElementById('tv-search-input');
  var empty = document.querySelector('.tv-empty');
  var cur = 'all';
  function apply() {
    var q = (input.value || '').trim().toLowerCase();
    var shown = 0;
    items.forEach(function (it) {
      var ok = (cur === 'all' || it.getAttribute('data-cat') === cur)
            && (!q || it.getAttribute('data-title').toLowerCase().indexOf(q) !== -1);
      it.style.display = ok ? '' : 'none';
      if (ok) shown++;
    });
    empty.style.display = shown ? 'none' : '';
  }
  cats.forEach(function (li) {
    li.querySelector('a').addEventListener('click', function (e) {
      e.preventDefault();
      cats.forEach(function (x) { x.classList.remove('on'); });
      li.classList.add('on');
      cur = li.getAttribute('data-cat');
      apply();
    });
  });
  input.addEventListener('input', apply);
})();
</script>'''

def make_head(title):
    h = re.sub(r'<title>[^<]*</title>', '<title>%s | 트래비티</title>' % title, head)
    return h + STYLE

blog_hdr = activate_blog(hdr)

list_page = (make_head('블로그')
    + '<body class="max-[767px]:min-w-[360px] min-[767px]:min-w-[1440px]">'
    + blog_hdr + mhdr
    + '<div class="tv-bloghero"><h1>블로그</h1><p>베트남 시장과 틱톡 인플루언서 마케팅,<br>진행하기 전에 알아두면 좋은 이야기를 모았습니다.</p></div>'
    + '<div class="tv-blog">'
    + '<aside class="tv-side">'
      '<div class="tv-search"><input id="tv-search-input" type="search" placeholder="검색어를 입력해 주세요" autocomplete="off"/>'
      '<button type="button" aria-label="검색"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></button></div>'
      '<h3>카테고리</h3><ul class="tv-cats">' + ''.join(cat_lis) + '</ul></aside>'
    + '<div style="flex:1"><div class="tv-grid">' + ''.join(cards) + '</div>'
    + '<div class="tv-empty" style="display:none">검색 결과가 없습니다.</div></div>'
    + '</div>' + footer + FILTER_JS
    + '<script src="./mirror.js?v=2"></script></body></html>')
open('blog.html', 'w', encoding='utf-8').write(list_page)
print('blog.html written:', len(list_page))

# ── 상세 페이지 ──
for p in POSTS:
    body = ''.join('<p>%s</p>' % t for t in p['paras'])
    art = (make_head(p['title'])
        + '<body class="max-[767px]:min-w-[360px] min-[767px]:min-w-[1440px]">'
        + blog_hdr + mhdr
        + '<article class="tv-article">'
        + '<span class="tv-chip">%s</span>' % p['cat']
        + '<h1>%s</h1>' % p['title']
        + '<div class="tv-meta"><time>%s</time><span>%s</span></div>' % (p['date'], p['read'])
        + '<div class="tv-cover"><img src="./%s" alt="%s"/></div>' % (p['thumb'], p['title'])
        + body
        + '<a class="tv-back" href="./blog.html">← 블로그 목록으로</a>'
        + '</article>' + footer
        + '<script src="./mirror.js?v=2"></script></body></html>')
    open(p['slug'] + '.html', 'w', encoding='utf-8').write(art)
    print(p['slug'] + '.html written')

# ── 기존 페이지 메뉴 연결: ./blog → ./blog.html ──
for f in ['index.html', 'about.html']:
    h = open(f, encoding='utf-8').read()
    n = h.count('href="./blog"')
    h = h.replace('href="./blog"', 'href="./blog.html"')
    # 푸터의 블로그/인사이트 링크도
    open(f, 'w', encoding='utf-8').write(h)
    print(f, 'blog links updated:', n)
