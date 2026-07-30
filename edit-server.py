# -*- coding: utf-8 -*-
"""트래비티 편집 서버 — 사이트를 그대로 띄우고, 화면에서 클릭해 고친 텍스트를
HTML 파일에 바로 굽는다(정적 반영). 실행: python edit-server.py  → http://localhost:5723
- GET  : 정적 서빙. *.html 에는 편집 오버레이(assets/js/edit-mode.js) 자동 주입
- POST /api/bake : {page, replacements:[{old,new}]} → 해당 HTML 파일에서 문자열 치환 후 저장
"""
import http.server
import json
import io
import os
import re
import urllib.parse

PORT = 5723
ROOT = os.path.dirname(os.path.abspath(__file__))

INJECT = '<script src="/assets/js/edit-mode.js?v=1"></script>'


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == '/':
            path = '/index.html'
        fs_path = os.path.normpath(os.path.join(ROOT, path.lstrip('/')))
        if fs_path.startswith(ROOT) and fs_path.endswith('.html') and os.path.isfile(fs_path):
            data = io.open(fs_path, encoding='utf-8').read()
            # </body> 마지막 위치에 편집 스크립트 주입
            i = data.rfind('</body>')
            if i >= 0 and 'edit-mode.js' not in data:
                data = data[:i] + INJECT + data[i:]
            body = data.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def do_POST(self):
        if urllib.parse.urlparse(self.path).path != '/api/bake':
            self.send_error(404)
            return
        try:
            n = int(self.headers.get('Content-Length', 0))
            req = json.loads(self.rfile.read(n).decode('utf-8'))
            page = req.get('page', '')
            reps = req.get('replacements', [])
            # 페이지 경로 검증: 루트의 .html 만
            page = page.lstrip('/').split('?')[0] or 'index.html'
            if '/' in page or '\\' in page or not page.endswith('.html'):
                raise ValueError('bad page: ' + page)
            fs_path = os.path.join(ROOT, page)
            if not os.path.isfile(fs_path):
                raise ValueError('no such page: ' + page)

            # 같은 문구(헤더·푸터 등)가 다른 페이지에도 있으면 함께 굽는다.
            # 우선순위: 현재 페이지 먼저, 이후 나머지 루트 .html (작업 파일 _*, *.bak* 제외)
            targets = [page]
            for fn in sorted(os.listdir(ROOT)):
                if not fn.endswith('.html') or fn == page:
                    continue
                if fn.startswith('_') or '.bak' in fn or fn == 'rendered.html':
                    continue
                targets.append(fn)

            results = []
            files_changed = []
            cur_page_hit = False
            for fn in targets:
                fp = os.path.join(ROOT, fn)
                if not os.path.isfile(fp):
                    continue
                data = io.open(fp, encoding='utf-8').read()
                changed = False
                hits = 0
                for r in reps:
                    old, new = r.get('old', ''), r.get('new', '')
                    if not old or old == new:
                        continue
                    cnt = data.count(old)
                    if cnt == 0:
                        # 폴백: <br> vs <br/> 표기 차이 흡수
                        old2 = old.replace('<br>', '<br/>')
                        cnt = data.count(old2)
                        if cnt:
                            data = data.replace(old2, new)
                            changed = True
                            hits += cnt
                        continue
                    data = data.replace(old, new)
                    changed = True
                    hits += cnt
                if changed:
                    io.open(fp, 'w', encoding='utf-8', newline='').write(data)
                    files_changed.append({'file': fn, 'n': hits})
                    if fn == page:
                        cur_page_hit = True
            results = files_changed
            out = json.dumps({'ok': cur_page_hit or bool(files_changed),
                              'results': results, 'files': files_changed},
                             ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(out)))
            self.end_headers()
            self.wfile.write(out)
        except Exception as e:
            out = json.dumps({'ok': False, 'error': str(e)}, ensure_ascii=False).encode('utf-8')
            self.send_response(400)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(out)))
            self.end_headers()
            self.wfile.write(out)

    def log_message(self, fmt, *args):
        pass  # 조용히


if __name__ == '__main__':
    with http.server.ThreadingHTTPServer(('127.0.0.1', PORT), Handler) as srv:
        print(f'트래비티 편집 서버: http://localhost:{PORT}  (파일에 바로 저장됩니다)')
        srv.serve_forever()
