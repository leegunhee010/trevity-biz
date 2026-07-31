# -*- coding: utf-8 -*-
"""
헤더 '인플루언서라면?' 을 카테고리 <ul> 밖으로 꺼내 '문의하기' 바로 왼쪽에 배치.
- 데스크톱: 핑크 아웃라인 버튼(.tvh-inf) — 솔리드 핑크 문의하기 옆, 카테고리와 분리
- 모바일  : 바가 좁으니 버튼은 숨기고, 기존 <li>(.tvh-inf-m)를 드로어에 그대로 남김
- 드롭다운(kr/vn/cn/mm)은 그대로 유지. hover 셀렉터만 .tvh-inf 용으로 추가
전 페이지 적용. 재실행 안전(이미 적용된 파일은 skip). 백업: *.bak_inf
"""
import io, os, re, glob, shutil

os.chdir(r"C:\Users\이건희\creplanet-clone")

LI_START = '<li><a href="https://kr.trevity.com" target="_blank">인플루언서라면?</a>'
LI_END = '</li></ul>'

CSS_MARK = '/* tvh-inf */'
CSS_ADD = """
/* tvh-inf */
.tvh-inf{position:relative;flex:none;margin-left:14px}
.tvh-inf>a{display:inline-block;box-sizing:border-box;height:40px;line-height:38px;padding:0 16px;
  border:1px solid #fa6781;border-radius:8px;background:#fff;color:#fa6781;font-size:14px;
  font-weight:700;letter-spacing:-0.28px;text-decoration:none;white-space:nowrap;transition:background .2s}
.tvh-inf>a:hover{background:#fff0f3}
.tvh-inf .tvh-dd{left:auto;right:0;transform:none}
.tvh-inf:hover .tvh-dd{display:block}
.tvh-inf-m{display:none}
@media (max-width:767px){
.tvh-inf{display:none}
.tvh-inf-m{display:block}
.tvh-inf-m>a{color:#fa6781!important;font-weight:700}
}
"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    if '<header class="tvh">' not in s:
        return 'no header'
    if 'tvh-inf' in s:
        return 'already'

    i = s.find(LI_START)
    if i < 0:
        return 'SKIP: 인플루언서라면? li 없음'
    j = s.find(LI_END, i)
    if j < 0:
        return 'SKIP: </li></ul> 못 찾음'

    li_full = s[i: j + len('</li>')]           # <li>...</li>
    inner = li_full[len('<li>'): -len('</li>')]  # <a>...</a><div class="tvh-dd">...</div>

    # 다른 li 가 끼어들지 않았는지 확인 (마지막 li 여야 함)
    if '<li>' in inner or '</li>' in inner:
        return 'SKIP: li 경계 이상'

    # 1) 원본 li -> 모바일 전용으로 클래스만 부여
    s = s.replace(li_full, '<li class="tvh-inf-m">' + inner + '</li>', 1)

    # 2) 문의하기 버튼 바로 왼쪽에 데스크톱 버튼 삽입
    cta = '<a class="tvh-cta" href="./inquiry.html">문의하기</a>'
    if cta not in s:
        m = re.search(r'<a class="tvh-cta"[^>]*>.*?</a>', s, re.S)
        if not m:
            return 'SKIP: tvh-cta 못 찾음'
        cta = m.group(0)
    s = s.replace(cta, '<div class="tvh-inf">' + inner + '</div>' + cta, 1)

    # 3) CSS 추가
    m = re.search(r'(<style id="tvnav-style">)(.*?)(</style>)', s, re.S)
    if not m:
        return 'SKIP: tvnav-style 없음'
    if CSS_MARK not in m.group(2):
        s = s[:m.start(3)] + CSS_ADD + s[m.start(3):]

    shutil.copy2(path, path + '.bak_inf')
    io.open(path, 'w', encoding='utf-8').write(s)
    return 'OK'


files = sorted(f for f in glob.glob('*.html') if not f.startswith('_'))
stat = {}
for f in files:
    r = patch(f)
    stat[r] = stat.get(r, 0) + 1
    print('%-24s %s' % (f, r))

print()
for k, v in sorted(stat.items()):
    print('%-28s %d' % (k, v))
