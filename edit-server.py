# -*- coding: utf-8 -*-
"""트래비티 편집 서버 — 사이트를 그대로 띄우고, 화면에서 클릭해 고친 텍스트를
HTML 파일에 바로 굽는다(정적 반영). 실행: python edit-server.py  → http://localhost:5723
- GET  : 정적 서빙. *.html 에는 편집 오버레이(assets/js/edit-mode.js) 자동 주입
- POST /api/bake : {page, replacements:[{old,new}]} → 해당 HTML 파일에서 문자열 치환 후 저장
"""
import base64
import hashlib
import http.server
import json
import io
import os
import re
import time
import urllib.parse

import seo_bake

PORT = 5723
ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(ROOT, "images", "uploads")

INJECT = '<script src="/assets/js/edit-mode.js?v=3"></script>'


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == '/api/seo':
            out = []
            for page, label, prio, freq, kw in seo_bake.PAGES:
                cur = seo_bake.read_meta(page)
                if cur is not None:
                    out.append({'page': page, 'label': label, 'defaultKeywords': kw, **cur})
            self._json(out)
            return
        if path == '/api/settings':
            self._json(seo_bake.settings())
            return
        if path == '/api/board':
            self._json(seo_bake.blog_posts())
            return
        if path == '/':
            path = '/index.html'
        fs_path = os.path.normpath(os.path.join(ROOT, path.lstrip('/')))
        if fs_path in (os.path.join(ROOT, 'seo.html'), os.path.join(ROOT, 'board.html')):
            return super().do_GET()   # 관리 UI에는 편집 오버레이 미주입
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

    def _json(self, obj, code=200):
        out = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    def _body(self):
        n = int(self.headers.get('Content-Length', 0))
        return json.loads(self.rfile.read(n).decode('utf-8')) if n else {}

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path

        # ---------- SEO: 페이지별 메타 저장+굽기 ----------
        if path == '/api/seo':
            try:
                d = self._body()
                seo_bake.bake_meta(d['page'], d.get('meta', {}))
                self._json({'ok': True})
            except Exception as e:
                self._json({'ok': False, 'error': str(e)}, 400)
            return

        # ---------- SEO: 기술 SEO 일괄 굽기 ----------
        if path == '/api/seo-tech':
            try:
                r = seo_bake.bake_technical()
                n = seo_bake.bake_settings()
                self._json({'ok': True, **r, 'settingsPages': n})
            except Exception as e:
                self._json({'ok': False, 'error': str(e)}, 400)
            return

        # ---------- 게시판: 글 저장(+정적 굽기) / 삭제 ----------
        if path == '/api/board':
            try:
                d = self._body()
                post = d.get('post') or {}
                slug = (post.get('slug') or '').strip()
                if not re.match(r'^[a-z0-9-]+$', slug):
                    raise ValueError('슬러그는 영문 소문자·숫자·하이픈만 가능합니다')
                posts = seo_bake.blog_posts()
                now = time.strftime('%Y-%m-%d')
                i = next((i for i, p in enumerate(posts) if p.get('slug') == slug), -1)
                if i >= 0:
                    posts[i].update(post)
                    posts[i]['updated_at'] = now
                else:
                    post.setdefault('created_at', now)
                    post['updated_at'] = now
                    post.setdefault('published', True)
                    post.setdefault('read_minutes', 4)
                    posts.insert(0, post)
                seo_bake.save_blog_posts(posts)
                files = seo_bake.bake_board()
                self._json({'ok': True, 'files': files})
            except Exception as e:
                self._json({'ok': False, 'error': str(e)}, 400)
            return
        if path == '/api/board-delete':
            try:
                d = self._body()
                slug = (d.get('slug') or '').strip()
                posts = [p for p in seo_bake.blog_posts() if p.get('slug') != slug]
                seo_bake.save_blog_posts(posts)
                f = os.path.join(ROOT, f'blog-{slug}.html')
                if re.match(r'^[a-z0-9-]+$', slug) and os.path.isfile(f):
                    os.remove(f)
                seo_bake.bake_board()
                self._json({'ok': True})
            except Exception as e:
                self._json({'ok': False, 'error': str(e)}, 400)
            return

        # ---------- 설정 저장+굽기 (headCode·파비콘·og·SNS) ----------
        if path == '/api/settings':
            try:
                d = self._body()
                st = seo_bake.settings()
                for k in ('domain', 'siteName', 'headCode',
                          'snsKakao', 'snsInstagram', 'snsBlog', 'snsPhone',
                          'snsNaverTalk', 'snsInquiry', 'channelTalkKey',
                          'mailEndpoint', 'mailTo'):
                    if k in d:
                        st[k] = d[k]
                # 파비콘/OG 이미지: base64 업로드
                for key, field in (('favicon', 'faviconData'), ('ogImage', 'ogImageData')):
                    item = d.get(field)
                    if item and item.get('data'):
                        os.makedirs(UPLOAD_DIR, exist_ok=True)
                        ext = os.path.splitext(item.get('name', ''))[1].lower() or '.png'
                        if ext not in ('.png', '.ico', '.jpg', '.jpeg', '.webp', '.svg'):
                            ext = '.png'
                        name = key + '_' + hashlib.md5(str(time.time()).encode()).hexdigest()[:8] + ext
                        raw = base64.b64decode(item['data'].split(',')[-1])
                        io.open(os.path.join(UPLOAD_DIR, name), 'wb').write(raw)
                        st[key] = 'images/uploads/' + name
                seo_bake.save_settings(st)
                seo_bake.bake_settings()
                seo_bake.bake_sns()
                self._json({'ok': True, 'settings': st})
            except Exception as e:
                self._json({'ok': False, 'error': str(e)}, 400)
            return

        # ---------- 이미지 교체 (편집모드에서 이미지 클릭) ----------
        if path == '/api/image-replace':
            try:
                d = self._body()
                page = (d.get('page') or 'index.html').lstrip('/').split('?')[0]
                if '/' in page or not page.endswith('.html'):
                    raise ValueError('bad page')
                old_src = d.get('oldSrc', '')
                item = d.get('image') or {}
                if not old_src or not item.get('data'):
                    raise ValueError('oldSrc/image 필요')
                upload_only = old_src == '__upload_only__'
                os.makedirs(UPLOAD_DIR, exist_ok=True)
                ext = os.path.splitext(item.get('name', ''))[1].lower() or '.jpg'
                if ext not in ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.mp4', '.webm'):
                    ext = '.jpg'
                name = 'rp_' + hashlib.md5((item.get('name', '') + str(time.time())).encode()).hexdigest()[:12] + ext
                dst = os.path.join(UPLOAD_DIR, name)
                io.open(dst, 'wb').write(base64.b64decode(item['data'].split(',')[-1]))
                try:  # 큰 이미지 최적화 (PIL 있으면)
                    from PIL import Image
                    im = Image.open(dst)
                    if max(im.size) > 1600:
                        im.thumbnail((1600, 1600), Image.LANCZOS)
                        im.save(dst)
                except Exception:
                    pass
                new_src = './images/uploads/' + name
                if upload_only:   # 업로드만 하고 치환은 안 함 (게시판 썸네일 등)
                    self._json({'ok': True, 'newSrc': new_src, 'files': []})
                    return
                # 같은 src 를 쓰는 모든 루트 페이지에서 교체
                changed = []
                for fn in sorted(os.listdir(ROOT)):
                    if not fn.endswith('.html') or fn.startswith('_') or '.bak' in fn or fn == 'rendered.html':
                        continue
                    fp = os.path.join(ROOT, fn)
                    s = io.open(fp, encoding='utf-8').read()
                    variants = [old_src]
                    if old_src.startswith('./'):
                        variants.append(old_src[2:])
                    hits = 0
                    for v in variants:
                        c = s.count(v)
                        if c:
                            s = s.replace(v, new_src)
                            hits += c
                    if hits:
                        io.open(fp, 'w', encoding='utf-8', newline='').write(s)
                        changed.append({'file': fn, 'n': hits})
                self._json({'ok': bool(changed), 'newSrc': new_src, 'files': changed})
            except Exception as e:
                self._json({'ok': False, 'error': str(e)}, 400)
            return

        if path != '/api/bake':
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
