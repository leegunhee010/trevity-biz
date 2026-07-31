# -*- coding: utf-8 -*-
"""
헤더 '고객센터' 드롭다운에서 '제휴 문의' 항목 삭제 (전 페이지)
- href 에 ?svc=... 쿼리가 붙은 페이지가 있어 정규식으로 매칭
- 공식대행사(#agency) 섹션 본문의 '제휴 문의' 언급은 건드리지 않음
재실행 안전. 백업: *.bak_delpartner
"""
import io, os, re, glob, shutil

os.chdir(r"C:\Users\이건희\creplanet-clone")

# 드롭다운 항목만 정확히 겨냥: inquiry.html(+쿼리) 로 가는 <b>제휴 문의</b> 항목
PAT = re.compile(
    r'<a href="\./inquiry\.html[^"]*"><b>제휴 문의</b><small>함께할 파트너를 찾습니다</small></a>'
)

files = sorted(f for f in glob.glob('*.html') if not f.startswith('_'))
stat = {}

for f in files:
    s = io.open(f, encoding='utf-8').read()
    if '<header class="tvh">' not in s:
        r = 'no header'
    else:
        n = len(PAT.findall(s))
        if n == 0:
            r = 'already / 없음'
        else:
            if n != 1:
                r = 'SKIP: %d개 발견(예상 1개)' % n
            else:
                # 삭제 후 형제 항목이 남아있는지 검증
                new = PAT.sub('', s, count=1)
                if new.count('<b>종합 헬프센터</b>') != s.count('<b>종합 헬프센터</b>') or \
                   new.count('<b>공식대행사</b>') != s.count('<b>공식대행사</b>'):
                    r = 'SKIP: 형제 항목 손상 감지'
                else:
                    shutil.copy2(f, f + '.bak_delpartner')
                    io.open(f, 'w', encoding='utf-8').write(new)
                    r = 'OK'
    stat[r] = stat.get(r, 0) + 1
    print('%-24s %s' % (f, r))

print()
for k, v in sorted(stat.items()):
    print('%-28s %d' % (k, v))

# 남은 '제휴 문의' 언급 리포트 (공식대행사 섹션 등)
print()
print('=== 삭제 후 남은 "제휴 문의" 언급 ===')
for f in files:
    s = io.open(f, encoding='utf-8').read()
    n = s.count('제휴 문의')
    if n:
        print('  %-22s %d개' % (f, n))
