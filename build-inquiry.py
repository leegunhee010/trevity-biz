# -*- coding: utf-8 -*-
# 문의(CTA) 폼 페이지 inquiry.html 생성 + 전 페이지 링크 연결
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
head = re.sub(r'<title>[^<]*</title>', '<title>문의하기 | 트래비티</title>', head)
ds = idx.find('<div class="max-[767px]:hidden"><div class="fixed top-0 z-40 h-[72px]')
hdr = idx[ds:balanced(idx, ds)]
ms = idx.find('<div class="min-[768px]:hidden">')
mhdr = '<div>' + idx[ms:balanced(idx, ms)] + '</div>'
fs = idx.find('<footer')
footer = idx[fs:balanced(idx, fs, 'footer')]

STYLE = '''<style id="inquiry-style">
html{scroll-behavior:smooth}
.iq-hero{background:linear-gradient(180deg,#ffe9ee,#fff);padding:150px 20px 48px;text-align:center}
.iq-hero h1{font-size:40px;font-weight:800;letter-spacing:-0.8px;color:#1f1f1f;margin:0 0 14px}
.iq-hero p{font-size:17px;color:#595959;letter-spacing:-0.34px;line-height:1.7;margin:0}
.iq-wrap{max-width:680px;margin:0 auto;padding:40px 20px 140px}
.iq-card{background:#fff;border:1px solid #f0f0f0;border-radius:20px;box-shadow:0 8px 40px rgba(0,0,0,0.06);padding:44px 40px}
.iq-row{margin-bottom:24px}
.iq-row label{display:block;font-size:15px;font-weight:700;letter-spacing:-0.3px;color:#1f1f1f;margin-bottom:9px}
.iq-row label .req{color:#fa6781;margin-left:2px}
.iq-row input[type=text],.iq-row input[type=tel],.iq-row input[type=email],.iq-row select,.iq-row textarea{width:100%;border:1.5px solid #e5e7eb;border-radius:10px;padding:13px 14px;font-size:15.5px;font-family:inherit;letter-spacing:-0.31px;color:#1f1f1f;background:#fff;outline:none;transition:border-color .15s;box-sizing:border-box}
.iq-row input:focus,.iq-row select:focus,.iq-row textarea:focus{border-color:#fa6781}
.iq-row textarea{min-height:130px;resize:vertical;line-height:1.65}
.iq-grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.iq-pkg{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
.iq-pkg input{display:none}
.iq-pkg span{display:block;text-align:center;border:1.5px solid #e5e7eb;border-radius:10px;padding:13px 8px;font-size:14.5px;letter-spacing:-0.29px;color:#595959;cursor:pointer;transition:all .15s}
.iq-pkg input:checked+span{border-color:#fa6781;background:#fff0f3;color:#fa6781;font-weight:700}
.iq-agree{display:flex;align-items:flex-start;gap:10px;font-size:13.5px;color:#737373;line-height:1.6;letter-spacing:-0.27px}
.iq-agree input{margin-top:3px;accent-color:#fa6781;width:16px;height:16px}
.iq-submit{width:100%;height:58px;border:none;border-radius:12px;background:#fa6781;color:#fff;font-size:17px;font-weight:700;letter-spacing:-0.34px;font-family:inherit;cursor:pointer;transition:opacity .15s;margin-top:8px}
.iq-submit:hover{opacity:.85}
.iq-submit:disabled{background:#e5e7eb;color:#9ca3af;cursor:default}
.iq-done{display:none;text-align:center;padding:56px 12px}
.iq-done .ic{width:64px;height:64px;border-radius:50%;background:#fff0f3;display:flex;align-items:center;justify-content:center;margin:0 auto 20px}
.iq-done h3{font-size:24px;font-weight:800;letter-spacing:-0.48px;color:#1f1f1f;margin:0 0 10px}
.iq-done p{font-size:15.5px;color:#595959;line-height:1.7;letter-spacing:-0.31px;margin:0 0 28px}
.iq-done a{display:inline-block;border-radius:10px;background:#fa6781;color:#fff;font-weight:700;font-size:15px;padding:13px 26px;text-decoration:none}
.iq-note{margin-top:20px;text-align:center;font-size:13.5px;color:#8c8c8c;letter-spacing:-0.27px}
@media (max-width:767px){.iq-hero{padding-top:110px}.iq-hero h1{font-size:30px}.iq-card{padding:32px 22px}.iq-grid2{grid-template-columns:1fr}.iq-pkg{grid-template-columns:1fr 1fr}}
</style>'''

FORM = '''
<div class="iq-hero">
  <h1>문의하기</h1>
  <p>남겨주시면 베트남 담당 매니저가 하루 안에 연락드립니다.<br>패키지가 고민되시면 비워두셔도 괜찮습니다.</p>
</div>
<div class="iq-wrap">
  <div class="iq-card">
    <form id="iq-form" novalidate>
      <div class="iq-grid2">
        <div class="iq-row"><label>회사 / 브랜드명 <span class="req">*</span></label><input type="text" name="company" required placeholder="예) 트래비티 코스메틱"/></div>
        <div class="iq-row"><label>담당자 성함 <span class="req">*</span></label><input type="text" name="name" required placeholder="예) 김트래"/></div>
      </div>
      <div class="iq-grid2">
        <div class="iq-row"><label>연락처 <span class="req">*</span></label><input type="tel" name="phone" required placeholder="010-0000-0000"/></div>
        <div class="iq-row"><label>이메일</label><input type="email" name="email" placeholder="example@brand.com"/></div>
      </div>
      <div class="iq-row"><label>제품 카테고리</label>
        <select name="category">
          <option value="">선택해 주세요</option>
          <option>뷰티 · 스킨케어</option>
          <option>식품 · F&amp;B</option>
          <option>패션 · 잡화</option>
          <option>생활용품 · 리빙</option>
          <option>매장 (식당 · 카페 등)</option>
          <option>기타</option>
        </select>
      </div>
      <div class="iq-row"><label>관심 패키지</label>
        <div class="iq-pkg">
          <label><input type="radio" name="package" value="스타터 10명"/><span>스타터 · 10명</span></label>
          <label><input type="radio" name="package" value="그로스 20명"/><span>그로스 · 20명</span></label>
          <label><input type="radio" name="package" value="도미넌트 50명"/><span>도미넌트 · 50명</span></label>
          <label><input type="radio" name="package" value="상담 후 결정"/><span>상담 후 결정할게요</span></label>
        </div>
      </div>
      <div class="iq-row"><label>문의 내용</label><textarea name="message" placeholder="제품 소개, 캠페인 목표, 일정 등 편하게 남겨주세요."></textarea></div>
      <div class="iq-row"><label class="iq-agree"><input type="checkbox" id="iq-agree"/><span>개인정보 수집 및 이용에 동의합니다. 수집된 정보(회사명, 성함, 연락처, 이메일)는 상담 목적으로만 사용되며, 상담 완료 후 파기됩니다.</span></label></div>
      <button type="submit" class="iq-submit" id="iq-btn">문의 접수하기</button>
    </form>
    <div class="iq-done" id="iq-done">
      <div class="ic"><svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#fa6781" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></div>
      <h3>문의가 접수되었습니다</h3>
      <p>남겨주신 연락처로 하루 안에<br>베트남 담당 매니저가 연락드리겠습니다.</p>
      <a href="./">홈으로 돌아가기</a>
    </div>
  </div>
  <p class="iq-note">전화가 편하시면 상담 가능 시간에 연락 주세요 · (트래비티 연락처 기입)</p>
</div>
<script>
(function () {
  // 구글 Apps Script 웹앱 URL을 배포 후 여기에 넣으세요 (비어 있으면 접수 화면만 표시)
  var SHEET_ENDPOINT = '';
  var form = document.getElementById('iq-form');
  var btn = document.getElementById('iq-btn');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var must = [['company', '회사/브랜드명'], ['name', '담당자 성함'], ['phone', '연락처']];
    for (var i = 0; i < must.length; i++) {
      var el = form.elements[must[i][0]];
      if (!el.value.trim()) { alert(must[i][1] + '을(를) 입력해 주세요.'); el.focus(); return; }
    }
    if (!document.getElementById('iq-agree').checked) { alert('개인정보 수집 및 이용에 동의해 주세요.'); return; }
    btn.disabled = true;
    btn.textContent = '접수 중...';
    var data = new FormData(form);
    data.append('page', 'trevity-kol-booking');
    data.append('ts', new Date().toISOString());
    function done() {
      form.style.display = 'none';
      document.getElementById('iq-done').style.display = 'block';
      window.scrollTo(0, 0);
    }
    if (!SHEET_ENDPOINT) { console.warn('SHEET_ENDPOINT 미설정 — 접수 데이터가 저장되지 않습니다.'); done(); return; }
    fetch(SHEET_ENDPOINT, { method: 'POST', mode: 'no-cors', body: data })
      .then(done)
      .catch(function () { btn.disabled = false; btn.textContent = '문의 접수하기'; alert('접수 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.'); });
  });
})();
</script>
'''

page = (head + STYLE
        + '<body class="max-[767px]:min-w-[360px] min-[767px]:min-w-[1440px]">'
        + hdr + mhdr + FORM + footer
        + '<script src="./mirror.js?v=2"></script></body></html>')
open('inquiry.html', 'w', encoding='utf-8').write(page)
print('inquiry.html written:', len(page))

# 전 페이지 ./inquiry → ./inquiry.html
import glob
for f in ['index.html', 'about.html', 'blog.html', 'blog-market.html', 'blog-midtier.html', 'blog-diy.html', 'blog-hantown.html', 'inquiry.html']:
    h = open(f, encoding='utf-8').read()
    n = len(re.findall(r'href="\./inquiry"', h))
    h = h.replace('href="./inquiry"', 'href="./inquiry.html"')
    open(f, 'w', encoding='utf-8').write(h)
    print(f, 'links:', n)
