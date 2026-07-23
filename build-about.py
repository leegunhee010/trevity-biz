# -*- coding: utf-8 -*-
# about.html 조립
head = open('_part_head.html', encoding='utf-8').read()
hdr = open('_part_hdr.html', encoding='utf-8').read()
mhdr = open('_part_mhdr.html', encoding='utf-8').read()
footer = open('_part_footer.html', encoding='utf-8').read()

REVEAL = 'opacity: 0; transform: translateY(40px); transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;'


def countup(target, label):
    suffix = ''.join(c for c in target if not c.isdigit() and c != ',')
    return ('<div style="text-align:center;min-width:170px">'
            '<p style="font-size:40px;font-weight:800;letter-spacing:-0.8px;color:#fa6781;line-height:1.2">'
            '<span class="inline-grid tabular-nums"><span class="invisible col-start-1 row-start-1" aria-hidden="true">%s</span>'
            '<span class="col-start-1 row-start-1 text-right">0%s</span></span></p>'
            '<p style="margin-top:8px;font-size:16px;letter-spacing:-0.32px;color:#595959">%s</p></div>'
            ) % (target, suffix, label)


def base_card(city, role, desc):
    return ('<div style="flex:1 1 230px;max-width:256px;background:#fff;border-radius:16px;padding:28px 24px;box-shadow:0 2px 14px rgba(0,0,0,0.06)">'
            '<p style="font-size:17px;font-weight:800;letter-spacing:0.5px;color:#fa6781;margin-bottom:4px">%s</p>'
            '<p style="font-size:15px;font-weight:700;letter-spacing:-0.3px;color:#1f1f1f;margin-bottom:10px">%s</p>'
            '<p style="font-size:14px;line-height:1.65;letter-spacing:-0.28px;color:#737373">%s</p></div>') % (city, role, desc)


def svc_card(num, title, desc):
    return ('<div style="flex:1 1 240px;max-width:256px;background:#fff;border-radius:16px;padding:32px 24px;border:1px solid #f0f0f0">'
            '<p style="color:#fa6781;font-size:14px;font-weight:800;margin-bottom:14px">%s</p>'
            '<h6 style="font-size:18px;font-weight:700;line-height:1.4;letter-spacing:-0.36px;color:#1f1f1f;margin-bottom:12px">%s</h6>'
            '<p style="font-size:14.5px;line-height:1.7;letter-spacing:-0.29px;color:#595959">%s</p></div>') % (num, title, desc)


def strength_card(num, title, desc):
    return ('<div style="flex:1 1 240px;max-width:256px;background:#fff5f7;border-radius:16px;padding:32px 24px">'
            '<p style="color:#fa6781;font-size:15px;font-weight:800;margin-bottom:12px">%s</p>'
            '<h6 style="font-size:18px;font-weight:700;line-height:1.45;letter-spacing:-0.36px;color:#1f1f1f;margin-bottom:14px">%s</h6>'
            '<p style="font-size:14.5px;line-height:1.65;letter-spacing:-0.29px;color:#595959">%s</p></div>') % (num, title, desc)


def sec_head(label, title, sub=''):
    s = ('<div style="text-align:center;margin-bottom:56px">'
         '<p style="color:#fa6781;font-size:18px;font-weight:700;letter-spacing:-0.36px;margin-bottom:12px">%s</p>'
         '<h2 style="font-size:36px;font-weight:700;line-height:1.5;letter-spacing:-0.72px;color:#1f1f1f">%s</h2>') % (label, title)
    if sub:
        s += '<p style="margin-top:20px;font-size:18px;line-height:1.7;letter-spacing:-0.36px;color:#595959">%s</p>' % sub
    return s + '</div>'


body = []

# 히어로
body.append(
    '<div style="background:linear-gradient(180deg,#ffe9ee 0%,#fff6f8 55%,#ffffff 100%);padding:172px 20px 96px;position:relative;overflow:hidden">'
    '<div style="position:absolute;top:-120px;right:-80px;width:420px;height:420px;border-radius:50%;background:radial-gradient(circle,#fa678133,#fa678100 70%)"></div>'
    '<div style="position:absolute;bottom:-160px;left:-100px;width:480px;height:480px;border-radius:50%;background:radial-gradient(circle,#ec489922,#ec489900 70%)"></div>'
    '<div style="max-width:1084px;margin:0 auto;position:relative">'
    '<div style="' + REVEAL + '">'
    '<div style="text-align:center">'
    '<p style="color:#fa6781;font-size:18px;font-weight:700;letter-spacing:-0.36px;margin-bottom:16px">회사소개</p>'
    '<h1 style="font-size:48px;font-weight:800;line-height:1.4;letter-spacing:-0.96px;color:#1f1f1f">'
    '베트남 마케팅의 기준을<br>만들어 온 회사, <span style="color:#fa6781">트래비티</span></h1>'
    '<p style="margin-top:24px;font-size:19px;line-height:1.75;letter-spacing:-0.38px;color:#595959">'
    '한국, 베트남, 중국 세 나라를 잇는 글로벌 마케팅 그룹입니다.<br>'
    '한국 관광객부터 현지 고객까지, 매장의 손님으로 만드는 캠페인을 만들어 왔습니다.</p>'
    '</div>'
    '<div style="display:flex;gap:24px;flex-wrap:wrap;justify-content:center;margin-top:64px">'
    + countup('10년+', '글로벌 마케팅 업력')
    + countup('3개국', '한국 · 베트남 · 중국 거점')
    + countup('6,000+', '수행한 캠페인')
    + countup('100,000+', '인플루언서 풀')
    + '</div></div></div></div>')

# 지도 / 네트워크
body.append(
    '<section><div style="padding:120px 20px;background:#fff"><div style="max-width:1084px;margin:0 auto">'
    '<div style="' + REVEAL + '">'
    + sec_head('글로벌 네트워크', '한국 · 베트남 · 중국을 잇는<br>현지 완결형 네트워크',
               '기획과 콘텐츠는 한국에서, 실행은 베트남 현지에서, 시스템은 자체 개발로.<br>캠페인의 모든 과정이 트래비티 안에서 완결됩니다.')
    + '<img src="./images/about-map.png" alt="트래비티 글로벌 거점 지도" style="width:100%;border-radius:24px;box-shadow:0 8px 40px rgba(0,0,0,0.08)"/>'
    '<div style="display:flex;gap:16px;flex-wrap:wrap;justify-content:center;margin-top:32px">'
    + base_card('SEOUL', '디자인 · 촬영 스튜디오', '브랜드 콘텐츠의 기획과 촬영을 책임집니다.')
    + base_card('DAEGU', '마케팅 센터', '국내 광고주와 가장 가까운 곳에서 소통합니다.')
    + base_card('HOCHIMINH', '마케팅 센터', '현지 마케터가 섭외부터 검수까지 직접 진행합니다.')
    + base_card('CHINA', '개발 센터', '캠페인을 뒷받침하는 시스템을 개발합니다.')
    + '</div></div></div></div></section>')

# 하는 일
body.append(
    '<section><div style="padding:120px 20px;background:#fafafa"><div style="max-width:1084px;margin:0 auto">'
    '<div style="' + REVEAL + '">'
    + sec_head('하는 일', '한국 관광객부터 현지 고객까지,<br>매장의 손님으로 만듭니다')
    + '<div style="display:flex;gap:20px;flex-wrap:wrap;justify-content:center">'
    + svc_card('01', '틱톡 인플루언서 마케팅', '현지 인플루언서가 만드는 영상으로 베트남 고객을 매장으로 부릅니다. 팔로워 10만~50만 인플루언서를 1명당 20만원에 대량 부킹합니다.')
    + svc_card('02', '네이버 블로그 마케팅', '한국인이 여행지를 검색하는 네이버에서, 블로거의 진짜 후기로 상위 노출을 만듭니다.')
    + svc_card('03', '네이버 카페 마케팅', '호치민 · 다낭 여행자 커뮤니티에서 자연스러운 입소문을 만듭니다.')
    + svc_card('04', '인스타그램 마케팅', '감각적인 피드와 릴스로, 한국 여행객의 저장 목록에 매장을 올립니다.')
    + '</div></div></div></div></section>')

# 강점
body.append(
    '<section><div style="padding:120px 20px;background:#fff"><div style="max-width:1084px;margin:0 auto">'
    '<div style="' + REVEAL + '">'
    + sec_head('우리의 강점', '10년의 경험이 만든<br>네 가지 확신')
    + '<div style="display:flex;gap:20px;flex-wrap:wrap;justify-content:center">'
    + strength_card('01', '풍부한 글로벌<br>마케팅 경험', '한국과 베트남을 중심으로 다양한 캠페인을 운영하며, 각 시장의 소비 패턴과 트렌드를 분석해 전략을 설계합니다.')
    + strength_card('02', '맞춤형 1:1<br>마케팅 전략 설계', '매장의 업종과 타겟 고객을 분석해, 비즈니스마다 맞춤형 캠페인으로 마케팅 효율을 끌어올립니다.')
    + strength_card('03', '차별화된<br>인플루언서 네트워크', '수만 명의 팔로워를 보유한 현지 인플루언서까지, 방대한 네트워크에서 캠페인에 맞는 사람만 선별해 관리합니다.')
    + strength_card('04', '성과 모니터링 및<br>보고 시스템', '캠페인 이후 노출, 방문, 반응 데이터를 분석한 리포트를 제공하고, 다음 캠페인의 전략을 함께 다듬습니다.')
    + '</div></div></div></div></section>')

# 슬로건 밴드
body.append(
    '<section><div style="padding:96px 20px;background:linear-gradient(135deg,#fa6781,#ec4899);text-align:center">'
    '<div style="' + REVEAL + '">'
    '<p style="font-size:32px;font-weight:700;line-height:1.55;letter-spacing:-0.64px;color:#fff">'
    '여러분의 매장을, 한국인과 현지인<br>모두가 찾는 공간으로 만듭니다.</p>'
    '</div></div></section>')

# CTA
body.append(
    '<section><div style="padding:120px 20px 140px;background:#fff;text-align:center">'
    '<div style="' + REVEAL + '">'
    '<h2 style="font-size:36px;font-weight:700;line-height:1.5;letter-spacing:-0.72px;color:#1f1f1f;margin-bottom:16px">트래비티와 함께 시작해 보세요</h2>'
    '<p style="font-size:18px;line-height:1.7;letter-spacing:-0.36px;color:#595959;margin-bottom:36px">베트남 틱톡 인플루언서 부킹부터 상담까지, 하루면 충분합니다.</p>'
    '<div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">'
    '<a href="./inquiry"><button type="button" style="height:56px;padding:0 32px;border-radius:8px;background:#fa6781;color:#fff;font-size:16px;font-weight:600;border:none;cursor:pointer">무료 상담 받기</button></a>'
    '<a href="./"><button type="button" style="height:56px;padding:0 32px;border-radius:8px;background:#fff;color:#595959;font-size:16px;font-weight:600;border:1px solid #d9d9d9;cursor:pointer">부킹 서비스 보기</button></a>'
    '</div></div></div></section>')

page = (head + '<body class="max-[767px]:min-w-[360px] min-[767px]:min-w-[1440px]">'
        + hdr + mhdr
        + ''.join(body) + footer
        + '<script src="./mirror.js"></script></body></html>')
open('about.html', 'w', encoding='utf-8').write(page)
print('about.html written:', len(page))
