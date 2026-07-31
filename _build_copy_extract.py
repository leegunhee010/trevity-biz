# -*- coding: utf-8 -*-
"""카피 기본값 재추출 → assets/js/copy-data.js 재생성.
페이지 텍스트를 직접 수정했을 때 실행하면 기본값이 갱신된다 (오버라이드 키는 원문 해시라, 원문이 바뀐 항목의 오버라이드는 무효화됨에 주의)."""
from bs4 import BeautifulSoup, NavigableString, Tag
import io, re, json

PAGES = ['index','vietnam-tiktok','local-vn','stay','tourist-vn','tourist-cn',
         'help','agency','inquiry','blog']
SKIP_TAGS = {'script','style','title','noscript','svg','option','time'}
TEXT_TAGS = {'h1','h2','h3','h4','h5','h6','p','span','a','b','strong','em','small','li','td','th','button','div','label','summary','figcaption','blockquote','i','u'}

def leaf_text(el):
    parts = []
    for c in el.children:
        if isinstance(c, NavigableString):
            parts.append(str(c))
        elif isinstance(c, Tag) and c.name == 'br':
            parts.append('\n')
        else:
            return None
    t = ''.join(parts)
    lines = [re.sub(r'\s+', ' ', ln).strip() for ln in t.split('\n')]
    return '\n'.join(lines).strip() or None

def djb2(s):
    h = 5381
    for ch in s:
        h = ((h << 5) + h + ord(ch)) & 0xFFFFFFFF
    return 'c' + format(h, 'x')

entries, order = {}, 0
for pg in PAGES:
    soup = BeautifulSoup(io.open(pg + '.html', encoding='utf-8').read(), 'html.parser')
    for s in soup.find_all(SKIP_TAGS): s.decompose()
    for el in soup.find_all(TEXT_TAGS):
        t = leaf_text(el)
        if not t or len(t) < 2 or len(t) > 600: continue
        if not re.search(r'[가-힣A-Za-z]', t): continue
        k = djb2(t)
        if k not in entries:
            entries[k] = {'t': t, 'pg': [], 'o': order}; order += 1
        if pg not in entries[k]['pg']:
            entries[k]['pg'].append(pg)

rows = [dict(k=k, t=v['t'], pg=v['pg']) for k, v in sorted(entries.items(), key=lambda kv: kv[1]['o'])]
out = ('/* 트래비티 카피 기본값 — 자동 추출(공백 정규화·<br>→\n). 오버라이드는 TV_COPY_OVR에 로드된다.\n'
       '   재생성: python _build_copy_extract.py */\n'
       'const TV_COPY_DEFAULTS = ' + json.dumps(rows, ensure_ascii=False) + ';\n'
       'const TV_COPY_OVR = {};\n')
io.open('assets/js/copy-data.js', 'w', encoding='utf-8').write(out)
print('entries:', len(rows))
