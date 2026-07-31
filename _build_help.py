# -*- coding: utf-8 -*-
"""
종합 헬프센터 (help.html) 재구축
- 헤더 / 푸터 / 컴파일된 Tailwind CSS 는 원본 그대로 보존, 그 사이 본문만 교체
- 주제(채널)별 8블록 구조 + 공통 블록(이용흐름/상담확정사항/용어사전/공식대행사/문의)
- 디자인 원칙: 프레임리스(카드 남발 금지) / 라인아이콘 SVG / 이모지 금지 / 좌측정렬
- Tailwind 는 컴파일본이라 새 클래스를 못 씀 -> 자체 프리픽스 .tvhc-* + 전용 <style>
재실행 가능. 원본은 help.html.bak_prehc 로 백업됨.
"""
import io, os, re, shutil

os.chdir(r"C:\Users\이건희\creplanet-clone")
SRC = 'help.html'
PINK = '#fa6781'

# ─────────────────────────────────────────────────────────────
# 주제(채널) 데이터
#   cost / period 에 None 을 주면 "상담 시 안내" 로 렌더됨
#   TODO(사장님 확인): period 전 항목, cost 중 None 항목
# ─────────────────────────────────────────────────────────────
TOPICS = [
    dict(
        key='tiktok', name='틱톡', en='TikTok', market='베트남',
        lead='베트남 현지 인플루언서가 제품을 직접 사용하고 세로 숏폼으로 올리는 방식입니다. '
             '베트남에서 가장 빠르게 확산되는 채널이고, 트래비티의 주력 상품입니다.',
        fit=['뷰티·화장품', 'F&B·건강식품', '생활가전', '패션·잡화'],
        content='세로 숏폼 15~60초<br/>인플루언서 1명당 1편',
        reach='추천 피드(FYP)<br/>+ 팔로워 피드',
        cost='1명당 20만원 균일가<br/>부가세 별도',
        period=None,
        link='./vietnam-tiktok.html',
        faq=[
            ('팔로워가 많은 인플루언서는 더 비싼가요?',
             '아닙니다. 팔로워 10만부터 50만까지 <b>1명당 20만원 균일가</b>입니다(부가세 별도). '
             '패키지는 10명 200만원, 20명 400만원, 50명 1,000만원으로 구성됩니다.'),
            ('인플루언서는 어떤 기준으로 고르나요?',
             '팔로워 수가 아니라 <b>제품과의 연관성</b>을 먼저 봅니다. 평소 어떤 제품을 다뤄 왔는지, '
             '시청자층이 제품의 구매층과 겹치는지를 분석해 매칭합니다.'),
            ('직접 섭외하는 것보다 유리한가요?',
             '컨택, 가이드라인 작성, 일정과 결과물 컨트롤을 전부 대행합니다. '
             '베트남 현지 마케터가 직접 진행하기 때문에 그 수고를 전부 더하면 균일가보다 비싸집니다.'),
            ('아직 베트남에 진출하지 않았는데 가능한가요?',
             '틱톡 인플루언서 부킹은 쇼피·틱톡샵에 제품이 이미 올라가 있는 상태를 전제로 설계된 상품입니다. '
             '진출 준비 단계라면 상담에서 단계에 맞는 방법을 먼저 안내드립니다.'),
        ],
    ),
    dict(
        key='tiktokshop', name='틱톡샵 · 어필리에이트', en='TikTok Shop', market='베트남',
        lead='인플루언서 콘텐츠에 상품 링크를 붙여, 영상을 본 사람이 그 자리에서 구매하도록 연결하는 구조입니다. '
             '조회수가 판매로 이어지는 경로를 만드는 단계입니다.',
        fit=['틱톡샵 입점 완료 브랜드', '쇼피 입점 브랜드', '재구매가 일어나는 소비재'],
        content='숏폼 + 상품 링크<br/>라이브 커머스 연계 가능',
        reach='추천 피드 + 틱톡샵 내부 노출',
        cost=None,
        period=None,
        link='./vietnam-tiktok.html',
        faq=[
            ('어필리에이트가 뭔가요?',
             '인플루언서가 콘텐츠에 상품 링크를 걸고, 그 링크로 발생한 판매에 대해 수수료를 받는 구조입니다. '
             '인플루언서에게 판매를 늘릴 동기가 생기는 것이 장점입니다.'),
            ('틱톡샵에 어필리에이트 신청자가 아예 없습니다.',
             '제품이 올라가 있어도 신청이 들어오지 않는 경우가 많습니다. '
             '기다리는 구조가 아니라 트래비티가 인플루언서를 직접 섭외해 연결하는 방식으로 진행합니다.'),
            ('판매량까지 추적되나요?',
             '어필리에이트 링크를 사용하면 콘텐츠별 유입과 판매를 확인할 수 있습니다. '
             '측정 범위는 계정 설정에 따라 달라져 상담에서 안내드립니다.'),
        ],
    ),
    dict(
        key='xiaohongshu', name='샤오홍슈', en='RED / 小红书', market='중국',
        lead='중국에서 검색처럼 쓰이는 리뷰 기반 SNS입니다. 구매나 방문 전에 이곳에서 후기를 찾아보기 때문에, '
             '후기가 없으면 선택지에서 빠집니다.',
        fit=['한국 매장·병원·클리닉', '뷰티·화장품', '관광 상권 매장'],
        content='사진 + 장문 후기<br/>위치·매장 태그',
        reach='앱 내 검색 · 해시태그<br/>추천 피드',
        cost=None,
        period=None,
        link='./tourist-cn.html',
        faq=[
            ('왜 샤오홍슈부터 해야 하나요?',
             '방한 중국인은 방문 전에 샤오홍슈에서 검색합니다. 광고는 끄면 사라지지만 후기는 검색 결과에 남기 때문에, '
             '한 번 쌓인 후기가 계속 손님을 데려옵니다.'),
            ('중국인 관광객이 실제로 그렇게 많나요?',
             '2025년 기준 방한 중국인은 548만 명으로 방한 국적 1위이고, 국내 체류 외국인 중에서도 '
             '중국이 35.2%로 가장 많습니다. 외국인 환자 국적도 중국이 1위입니다.'),
            ('중국어를 못 하는데 진행이 되나요?',
             '섭외부터 콘텐츠 검수까지 트래비티가 진행합니다. 사장님은 체험 제공과 확인만 하시면 됩니다.'),
        ],
    ),
    dict(
        key='douyin', name='더우인', en='Douyin / 抖音', market='중국',
        lead='중국의 숏폼 채널입니다. 샤오홍슈가 검색이라면 더우인은 확산에 가깝습니다. '
             '짧은 시간에 많은 사람에게 매장이나 제품을 보여줄 때 씁니다.',
        fit=['시각적으로 보여줄 게 있는 매장', 'F&B·체험 업종', '뷰티·시술'],
        content='세로 숏폼<br/>현장 촬영 위주',
        reach='추천 알고리즘',
        cost=None,
        period=None,
        link='./tourist-cn.html',
        faq=[
            ('샤오홍슈와 같이 해야 하나요?',
             '목적이 다릅니다. 더우인으로 넓게 알리고 샤오홍슈에 후기를 남겨 검색에서 받는 조합이 일반적입니다. '
             '예산에 맞춰 상담에서 구성해 드립니다.'),
            ('왕홍이 인플루언서와 같은 말인가요?',
             '중국에서 인플루언서를 부르는 말입니다. 채널과 팔로워 규모에 따라 섭외 조건이 달라집니다.'),
        ],
    ),
    dict(
        key='dianping', name='다중디엔핑', en='Dianping / 大众点评', market='중국',
        lead='중국의 맛집·상점 리뷰 플랫폼입니다. 방한 중국인이 식당이나 매장을 고를 때 확인하는 곳으로, '
             '평점과 후기 수가 그대로 방문에 영향을 줍니다.',
        fit=['음식점·카페', '관광 상권 매장', '체험형 업종'],
        content='매장 리뷰 · 사진<br/>평점 등록',
        reach='지역·업종 검색',
        cost=None,
        period=None,
        link='./tourist-cn.html',
        faq=[
            ('우리 매장이 등록되어 있는지 모르겠습니다.',
             '등록 여부와 현재 노출 상태를 먼저 확인한 뒤 진행 방향을 안내드립니다. 상담에서 함께 점검합니다.'),
        ],
    ),
    dict(
        key='naver', name='네이버 블로그', en='Naver Blog', market='한국',
        lead='한국 손님이 예약이나 방문 전에 검색하는 곳입니다. 숙박 체험단의 기본 채널이고, '
             '\'지역 + 후기\' 검색에 우리 가게가 걸리게 만드는 것이 목적입니다.',
        fit=['호텔·펜션·풀빌라', '음식점·카페', '지역 상권 매장'],
        content='사진 + 장문 후기<br/>필요 시 네이버 카페 확산',
        reach='네이버 검색<br/>블로그·카페 유입',
        cost='숙박 체험단은 사장님 비용 0원<br/>객실 1박만 제공',
        period=None,
        link='./stay.html',
        faq=[
            ('정말 사장님 비용이 0원인가요?',
             '숙박 체험단은 그렇습니다. 광고비도 대행비도 원고료도 없고, '
             '비어 있던 객실 <b>하루</b>만 제공하시면 됩니다. 트래비티는 체험단 운영에서 수익을 얻습니다.'),
            ('후기는 얼마나 남아 있나요?',
             '블로그 글은 삭제하지 않는 한 검색에 계속 남습니다. 광고와 달리 중단해도 사라지지 않는 것이 차이입니다.'),
            ('원고료를 요구하는 블로거는 없나요?',
             '트래비티가 섭외와 조건 조율을 대신 진행합니다. 사장님이 개별 협상하실 일은 없습니다.'),
        ],
    ),
    dict(
        key='instagram', name='인스타그램', en='Instagram', market='한국 · 현지',
        lead='매장 분위기나 제품을 이미지로 보여주는 채널입니다. 검색보다 발견에 가깝고, '
             '한국과 현지 양쪽에서 진행할 수 있습니다.',
        fit=['분위기가 중요한 매장', '패션·잡화', '뷰티·시술'],
        content='사진 · 릴스<br/>스토리 태그',
        reach='해시태그 · 탐색 탭<br/>팔로워 피드',
        cost=None,
        period=None,
        link='./local-vn.html',
        faq=[
            ('한국 인플루언서와 현지 인플루언서 중 어느 쪽인가요?',
             '타겟 손님이 누구인지에 따라 다릅니다. 한국 손님을 늘리려면 한국 계정, '
             '현지 손님을 늘리려면 현지 계정으로 진행합니다. 두 쪽을 같이 쓰는 경우도 있습니다.'),
            ('팔로워가 적은 계정 여러 개에 뿌리는 방식인가요?',
             '트래비티는 영향력이 없는 소규모 계정에 제품을 뿌리는 시딩 방식을 권하지 않습니다. '
             '물류비와 관세를 들여 보낸 제품이라면 도달이 나오는 계정에 쓰는 것이 맞습니다.'),
        ],
    ),
]

# ─────────────────────────────────────────────────────────────
# 상담에서 확정하는 항목  (TODO: 사장님 답변 오면 공통 FAQ 로 승격)
# ─────────────────────────────────────────────────────────────
CONSULT = [
    ('콘텐츠 2차 활용 범위', '만들어진 콘텐츠를 광고 소재나 자사 채널에 다시 쓸 수 있는 범위와 기간'),
    ('제품값 · 배송비 부담', '체험 제품의 값과 현지까지의 배송비를 누가 부담하는지'),
    ('결제 조건', '선결제 여부와 계약금 비율'),
    ('취소 · 환불 규정', '진행 중 취소가 발생했을 때의 처리 기준'),
    ('성과 관련 기준', '업로드 지연이나 도달 미달이 생겼을 때의 처리 방식'),
    ('인플루언서 사전 공유', '섭외 예정 계정을 진행 전에 어디까지 공유하는지'),
]

# ─────────────────────────────────────────────────────────────
# 이용 흐름
# ─────────────────────────────────────────────────────────────
STEPS = [
    ('문의', '브랜드 또는 매장의 상황과 목표를 남겨주세요. 어떤 채널이 맞는지 모르셔도 됩니다.'),
    ('상담 · 견적', '하루 안에 담당 매니저가 연락드리고, 목적에 맞는 구성과 견적을 제안드립니다.'),
    ('진행', '인플루언서 섭외, 가이드라인 전달, 촬영과 업로드까지 현지 마케터가 직접 컨트롤합니다.'),
    ('리포트', '업로드된 콘텐츠 링크와 성과를 정리해 전달드립니다.'),
]

# ─────────────────────────────────────────────────────────────
# 공통 FAQ
# ─────────────────────────────────────────────────────────────
COMMON_FAQ = [
    ('어떤 채널을 선택해야 할지 모르겠어요.',
     '고르지 않으셔도 됩니다. 제품인지 매장인지, 손님이 어느 나라 사람인지만 알려주시면 '
     '맞는 채널과 구성을 제안드립니다.'),
    ('문의하면 언제 연락이 오나요?',
     '평일 기준 하루 안에 담당 매니저가 연락드립니다. 상담 운영 시간은 평일 10:00~18:00입니다.'),
    ('견적은 어떻게 받을 수 있나요?',
     '문의하기에서 브랜드·매장 상황과 목표를 남겨주시면, 상담 후 목적에 맞는 구성과 견적을 제안드립니다.'),
    ('표기된 금액에 부가세가 포함되어 있나요?',
     '별도입니다. 사이트에 표기된 금액에 부가세 10%가 추가됩니다.'),
    ('세금계산서 발행이 되나요?',
     '됩니다. 주식회사 퍼스트마케팅컴퍼니(사업자등록번호 884-88-01123) 명의로 발행됩니다.'),
    ('결과는 어떻게 확인하나요?',
     '업로드된 콘텐츠 링크와 성과를 정리한 리포트를 전달드립니다. '
     '어필리에이트를 연계한 경우 콘텐츠별 유입도 확인할 수 있습니다.'),
    ('가이드라인이나 대본은 누가 만드나요?',
     '트래비티가 작성해 인플루언서에게 전달합니다. 강조하고 싶은 내용이 있으면 상담에서 반영합니다.'),
    ('지방에 있는 매장도 가능한가요?',
     '가능합니다. 다만 방한 관광객 체험단은 상권에 따라 방문 일정 조율이 필요해 상담에서 확인합니다.'),
]

# ─────────────────────────────────────────────────────────────
# 용어 사전
# ─────────────────────────────────────────────────────────────
GLOSSARY = [
    ('KOL', '팔로워가 많은 영향력 계정. Key Opinion Leader. 트래비티 부킹 기준은 팔로워 10만~50만입니다.'),
    ('KOC', '팔로워 1,000~1만 규모의 소비자형 계정. Key Opinion Consumer. 도달이 작아 단독으로는 판매에 영향이 적습니다.'),
    ('시딩', '다수의 소규모 계정에 제품을 무상 배포해 후기를 만드는 방식. 도달이 확보되지 않으면 제품만 소모됩니다.'),
    ('어필리에이트', '콘텐츠에 상품 링크를 붙이고 그 링크로 발생한 판매에 수수료를 지급하는 구조.'),
    ('FYP', '틱톡 추천 피드. For You Page. 팔로워가 아닌 사람에게 콘텐츠가 노출되는 경로입니다.'),
    ('틱톡샵', '틱톡 앱 안에서 상품을 판매하는 커머스 기능.'),
    ('샤오홍슈', '중국의 리뷰·검색 기반 SNS. 구매나 방문 전에 후기를 찾아보는 용도로 쓰입니다.'),
    ('더우인', '중국의 숏폼 영상 플랫폼. 중국판 틱톡으로 불립니다.'),
    ('다중디엔핑', '중국의 맛집·상점 리뷰 플랫폼. 평점과 후기 수가 방문 결정에 영향을 줍니다.'),
    ('왕홍', '중국에서 인플루언서를 부르는 말.'),
    ('체험단', '제품이나 서비스를 무상 제공하고 후기 콘텐츠를 받는 방식.'),
    ('도달', '콘텐츠를 실제로 본 사람의 수. 조회수와 달리 중복을 제외합니다.'),
]

# ─────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────
CSS = """
.tvhc{background:#fff;word-break:keep-all;color:#1f1f1f}
.tvhc-w{max-width:1084px;margin:0 auto;padding:0 20px}
.tvhc-label{display:inline-block;font-size:14px;font-weight:800;letter-spacing:2.5px;color:%(pink)s;margin:0 0 18px}
.tvhc-h1{font-size:44px;font-weight:800;line-height:1.35;letter-spacing:-0.9px;margin:0}
.tvhc-h2{font-size:34px;font-weight:800;line-height:1.45;letter-spacing:-0.68px;margin:0}
.tvhc-h3{font-size:22px;font-weight:700;line-height:1.5;letter-spacing:-0.44px;margin:0}
.tvhc-sub{font-size:16px;line-height:1.8;letter-spacing:-0.32px;color:#595959;margin:18px 0 0;max-width:620px}
.tvhc-sec{padding:96px 0 0}
.tvhc-sec:last-child{padding-bottom:110px}
.tvhc-eyebrow{font-size:13px;font-weight:800;letter-spacing:1.6px;color:#8c8c8c;margin:0 0 14px}

/* 히어로 + 검색 : 밑줄형 (프레임리스) */
.tvhc-hero{padding:96px 0 0}
.tvhc-search{position:relative;max-width:560px;margin:38px 0 0;border-bottom:2px solid #1f1f1f}
.tvhc-search input{width:100%%;border:0;outline:0;background:transparent;font-size:20px;font-weight:600;
  letter-spacing:-0.4px;color:#1f1f1f;padding:0 34px 14px 0;font-family:inherit}
.tvhc-search input::placeholder{color:#b0b0b0;font-weight:500}
.tvhc-search svg{position:absolute;right:2px;bottom:14px;width:22px;height:22px;stroke:#1f1f1f;
  stroke-width:1.8;fill:none;pointer-events:none}
.tvhc-res{font-size:15px;font-weight:600;color:%(pink)s;margin:16px 0 0;min-height:22px}

/* 주제 탭 : 텍스트 + 활성 밑줄, 카드 아님 */
.tvhc-tabs{display:flex;gap:30px;margin:44px 0 0;border-bottom:1px solid #e5e5e5;
  overflow-x:auto;scrollbar-width:none;-ms-overflow-style:none}
.tvhc-tabs::-webkit-scrollbar{display:none}
.tvhc-tab{flex:none;background:none;border:0;padding:0 0 15px;cursor:pointer;font-family:inherit;
  font-size:17px;font-weight:700;letter-spacing:-0.34px;color:#a6a6a6;position:relative;white-space:nowrap;
  transition:color .2s}
.tvhc-tab:hover{color:#595959}
.tvhc-tab.on{color:#1f1f1f}
.tvhc-tab.on::after{content:'';position:absolute;left:0;right:0;bottom:-1px;height:2px;background:%(pink)s}
.tvhc-tab i{display:block;font-style:normal;font-size:12px;font-weight:600;color:#b0b0b0;
  letter-spacing:0;margin-top:5px}

/* 주제 패널 */
.tvhc-panel{padding:52px 0 0}
.tvhc-mkt{display:inline-flex;align-items:center;gap:7px;font-size:13px;font-weight:700;color:%(pink)s;
  letter-spacing:-0.26px;margin:0 0 16px}
.tvhc-mkt::before{content:'';width:6px;height:6px;border-radius:50%%;background:%(pink)s}
.tvhc-lead{font-size:20px;font-weight:600;line-height:1.75;letter-spacing:-0.4px;color:#1f1f1f;
  margin:0;max-width:760px}
.tvhc-fit{font-size:16px;line-height:1.8;letter-spacing:-0.32px;color:#595959;margin:22px 0 0}
.tvhc-fit b{color:#1f1f1f;font-weight:700}

/* 헤어라인 위 가로 4칸 (지도 v3 승인 패턴) */
.tvhc-facts{display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin:44px 0 0;
  border-top:1px solid #1f1f1f}
.tvhc-fact{padding:22px 22px 0 0}
.tvhc-fact dt{font-size:13px;font-weight:800;letter-spacing:0.4px;color:#8c8c8c;margin:0 0 10px}
.tvhc-fact dd{font-size:16px;font-weight:700;line-height:1.65;letter-spacing:-0.32px;color:#1f1f1f;margin:0}
.tvhc-fact dd.q{color:#a6a6a6;font-weight:600}

/* 아코디언 */
.tvhc-acc{margin:46px 0 0;border-top:1px solid #e5e5e5}
.tvhc-item{border-bottom:1px solid #e5e5e5}
.tvhc-item>summary{list-style:none;cursor:pointer;padding:22px 40px 22px 0;position:relative;
  font-size:17px;font-weight:700;line-height:1.6;letter-spacing:-0.34px;color:#1f1f1f}
.tvhc-item>summary::-webkit-details-marker{display:none}
.tvhc-item>summary::after{content:'';position:absolute;right:6px;top:31px;width:9px;height:9px;
  border-right:2px solid #a6a6a6;border-bottom:2px solid #a6a6a6;transform:rotate(45deg);
  transition:transform .2s}
.tvhc-item[open]>summary{color:%(pink)s}
.tvhc-item[open]>summary::after{transform:rotate(-135deg);border-color:%(pink)s}
.tvhc-item>div{font-size:16px;line-height:1.85;letter-spacing:-0.32px;color:#595959;
  padding:0 40px 26px 0;margin:-4px 0 0}
.tvhc-item>div b{color:#1f1f1f;font-weight:700}

.tvhc-more{display:inline-flex;align-items:center;gap:8px;margin:34px 0 0;font-size:16px;
  font-weight:700;letter-spacing:-0.32px;color:%(pink)s;text-decoration:none;
  border-bottom:1px solid %(pink)s;padding-bottom:3px}
.tvhc-more svg{width:15px;height:15px;stroke:%(pink)s;stroke-width:2;fill:none}

/* 이용 흐름 : 헤어라인 위 가로 4칸 */
.tvhc-steps{display:grid;grid-template-columns:repeat(4,1fr);margin:42px 0 0;border-top:1px solid #1f1f1f}
.tvhc-step{padding:22px 24px 0 0}
.tvhc-step em{display:block;font-style:normal;font-size:13px;font-weight:800;color:%(pink)s;
  letter-spacing:1px;margin:0 0 12px}
.tvhc-step strong{display:block;font-size:18px;font-weight:800;letter-spacing:-0.36px;margin:0 0 10px}
.tvhc-step span{display:block;font-size:15px;line-height:1.75;letter-spacing:-0.3px;color:#595959}

/* 상담 확정 항목 : 2열 리스트 */
.tvhc-consult{display:grid;grid-template-columns:1fr 1fr;gap:0 48px;margin:38px 0 0}
.tvhc-crow{border-top:1px solid #e5e5e5;padding:20px 0}
.tvhc-crow strong{display:block;font-size:16px;font-weight:800;letter-spacing:-0.32px;margin:0 0 7px}
.tvhc-crow span{display:block;font-size:15px;line-height:1.7;letter-spacing:-0.3px;color:#8c8c8c}

/* 용어 사전 */
.tvhc-gl{margin:38px 0 0}
.tvhc-glrow{display:grid;grid-template-columns:190px 1fr;gap:0 32px;border-top:1px solid #e5e5e5;
  padding:20px 0}
.tvhc-glrow dt{font-size:17px;font-weight:800;letter-spacing:-0.34px;color:#1f1f1f;margin:0}
.tvhc-glrow dd{font-size:16px;line-height:1.8;letter-spacing:-0.32px;color:#595959;margin:0}

/* 문의 채널 : 헤어라인 위 가로 3칸 */
.tvhc-ch{display:grid;grid-template-columns:repeat(3,1fr);margin:42px 0 0;border-top:1px solid #1f1f1f}
.tvhc-chi{padding:24px 24px 0 0}
.tvhc-chi dt{font-size:13px;font-weight:800;letter-spacing:0.4px;color:#8c8c8c;margin:0 0 11px}
.tvhc-chi dd{font-size:20px;font-weight:800;letter-spacing:-0.4px;color:#1f1f1f;margin:0}
.tvhc-chi dd small{display:block;font-size:15px;font-weight:600;color:#8c8c8c;margin-top:8px;
  letter-spacing:-0.3px}
.tvhc-cta{display:inline-block;margin:40px 0 0;background:%(pink)s;color:#fff;text-decoration:none;
  font-size:17px;font-weight:800;letter-spacing:-0.34px;padding:18px 42px;border-radius:100px}

@media (max-width:1023px){
  .tvhc-facts,.tvhc-steps{grid-template-columns:1fr 1fr}
  .tvhc-fact,.tvhc-step{padding-bottom:22px}
}
@media (max-width:767px){
  .tvhc-sec{padding-top:62px}
  .tvhc-sec:last-child{padding-bottom:68px}
  .tvhc-hero{padding-top:52px}
  .tvhc-h1{font-size:30px;letter-spacing:-0.6px}
  .tvhc-h2{font-size:25px}
  .tvhc-h3{font-size:19px}
  .tvhc-search input{font-size:17px}
  .tvhc-tabs{gap:22px;margin-top:34px}
  .tvhc-tab{font-size:16px}
  .tvhc-panel{padding-top:38px}
  .tvhc-lead{font-size:17px}
  .tvhc-facts,.tvhc-steps,.tvhc-ch{grid-template-columns:1fr}
  .tvhc-fact,.tvhc-step,.tvhc-chi{padding:20px 0 0}
  .tvhc-consult{grid-template-columns:1fr;gap:0}
  .tvhc-glrow{grid-template-columns:1fr;gap:8px}
  .tvhc-item>summary{font-size:16px;padding-right:32px}
  .tvhc-item>summary::after{top:29px}
  .tvhc-cta{display:block;text-align:center;padding:17px 0}
}
""" % dict(pink=PINK)

ARROW = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M12 5l7 7-7 7" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')
GLASS = ('<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/>'
         '<path d="M20 20l-4.2-4.2" stroke-linecap="round"/></svg>')


def acc_item(q, a):
    return ('<details class="tvhc-item"><summary>%s</summary><div>%s</div></details>' % (q, a))


def build_body():
    o = []
    o.append('<div class="tvhc">')
    o.append('<style>%s</style>' % CSS)

    # ── 히어로 + 검색
    o.append('<section class="tvhc-hero"><div class="tvhc-w">')
    o.append('<span class="tvhc-label">HELP CENTER</span>')
    o.append('<h1 class="tvhc-h1">무엇을 도와드릴까요?</h1>')
    o.append('<p class="tvhc-sub">채널별로 어떤 마케팅인지, 비용이 어떻게 되는지 정리해 두었습니다. '
             '찾는 내용이 없으면 아래 문의 채널로 바로 남겨주세요.</p>')
    o.append('<div class="tvhc-search"><input id="tvhc-q" type="search" autocomplete="off" '
             'placeholder="궁금한 내용을 검색해 보세요" aria-label="헬프센터 검색"/>%s</div>' % GLASS)
    o.append('<p class="tvhc-res" id="tvhc-res" role="status"></p>')
    o.append('</div></section>')

    # ── 주제 탭
    o.append('<section class="tvhc-sec" id="channel" style="scroll-margin-top:76px"><div class="tvhc-w">')
    o.append('<span class="tvhc-label">CHANNEL GUIDE</span>')
    o.append('<h2 class="tvhc-h2">채널별로 무엇이 다른가요?</h2>')
    o.append('<p class="tvhc-sub">같은 인플루언서 마케팅이라도 채널마다 노출되는 방식과 비용 구조가 다릅니다. '
             '주제를 골라 확인해 보세요.</p>')
    o.append('<div class="tvhc-tabs" id="tvhc-tabs" role="tablist">')
    for t in TOPICS:
        o.append('<button class="tvhc-tab" type="button" data-k="%s" role="tab">%s<i>%s</i></button>'
                 % (t['key'], t['name'], t['en']))
    o.append('</div>')

    for t in TOPICS:
        o.append('<div class="tvhc-panel" data-k="%s" role="tabpanel">' % t['key'])
        o.append('<span class="tvhc-mkt">%s</span>' % t['market'])
        o.append('<p class="tvhc-lead">%s</p>' % t['lead'])
        o.append('<p class="tvhc-fit"><b>이런 업종에 맞습니다</b><br/>%s</p>'
                 % ' · '.join(t['fit']))
        o.append('<dl class="tvhc-facts">')
        for lab, val in (('콘텐츠', t['content']), ('노출 방식', t['reach']),
                         ('비용', t['cost']), ('기간', t['period'])):
            if val:
                o.append('<div class="tvhc-fact"><dt>%s</dt><dd>%s</dd></div>' % (lab, val))
            else:
                o.append('<div class="tvhc-fact"><dt>%s</dt><dd class="q">상담 시 안내</dd></div>' % lab)
        o.append('</dl>')
        o.append('<div class="tvhc-acc">')
        for q, a in t['faq']:
            o.append(acc_item(q, a))
        o.append('</div>')
        o.append('<a class="tvhc-more" href="%s">%s 서비스 자세히 보기%s</a>'
                 % (t['link'], t['name'], ARROW))
        o.append('</div>')
    o.append('</div></section>')

    # ── 이용 흐름
    o.append('<section class="tvhc-sec" id="guide" style="scroll-margin-top:76px"><div class="tvhc-w">')
    o.append('<span class="tvhc-label">HOW IT WORKS</span>')
    o.append('<h2 class="tvhc-h2">문의부터 리포트까지</h2>')
    o.append('<div class="tvhc-steps">')
    for i, (name, desc) in enumerate(STEPS, 1):
        o.append('<div class="tvhc-step"><em>STEP %d</em><strong>%s</strong><span>%s</span></div>'
                 % (i, name, desc))
    o.append('</div></div></section>')

    # ── 공통 FAQ
    o.append('<section class="tvhc-sec" id="faq" style="scroll-margin-top:76px"><div class="tvhc-w">')
    o.append('<span class="tvhc-label">FAQ</span>')
    o.append('<h2 class="tvhc-h2">채널과 무관하게 자주 묻는 것</h2>')
    o.append('<div class="tvhc-acc">')
    for q, a in COMMON_FAQ:
        o.append(acc_item(q, a))
    o.append('</div></div></section>')

    # ── 상담에서 확정하는 항목
    o.append('<section class="tvhc-sec"><div class="tvhc-w">')
    o.append('<span class="tvhc-label">CONSULTING</span>')
    o.append('<h2 class="tvhc-h2">상담에서 확정하는 항목</h2>')
    o.append('<p class="tvhc-sub">아래 항목은 채널과 진행 규모에 따라 조건이 달라집니다. '
             '일괄로 안내드리기보다 상담에서 정확한 기준을 드리는 편이 맞다고 판단해 따로 정리했습니다.</p>')
    o.append('<div class="tvhc-consult">')
    for name, desc in CONSULT:
        o.append('<div class="tvhc-crow"><strong>%s</strong><span>%s</span></div>' % (name, desc))
    o.append('</div></div></section>')

    # ── 용어 사전
    o.append('<section class="tvhc-sec" id="glossary" style="scroll-margin-top:76px"><div class="tvhc-w">')
    o.append('<span class="tvhc-label">GLOSSARY</span>')
    o.append('<h2 class="tvhc-h2">알아두면 편한 용어</h2>')
    o.append('<dl class="tvhc-gl">')
    for term, desc in GLOSSARY:
        o.append('<div class="tvhc-glrow tvhc-item" style="border-bottom:0">'
                 '<dt>%s</dt><dd>%s</dd></div>' % (term, desc))
    o.append('</dl></div></section>')

    o.append('</div>')
    return '\n'.join(o)


CONTACT = """
<div class="tvhc"><section class="tvhc-sec" id="contact" style="scroll-margin-top:76px;padding-bottom:110px">
<div class="tvhc-w">
<span class="tvhc-label">CONTACT</span>
<h2 class="tvhc-h2">해결되지 않았다면 바로 남겨주세요</h2>
<p class="tvhc-sub">상황만 알려주시면 어떤 채널이 맞는지부터 함께 정리해 드립니다.</p>
<dl class="tvhc-ch">
<div class="tvhc-chi"><dt>전화</dt><dd>070-4212-8266<small>평일 10:00 ~ 18:00</small></dd></div>
<div class="tvhc-chi"><dt>이메일</dt><dd>notice@trevity.com<small>주말·공휴일 제외</small></dd></div>
<div class="tvhc-chi"><dt>온라인 문의</dt><dd>문의 폼<small>하루 안에 담당 매니저가 연락드립니다</small></dd></div>
</dl>
<a class="tvhc-cta" href="./inquiry.html">무료 상담 받기</a>
</div></section></div>
"""

JS = """
<script>
(function(){
  var tabs   = [].slice.call(document.querySelectorAll('.tvhc-tab'));
  var panels = [].slice.call(document.querySelectorAll('.tvhc-panel'));
  var items  = [].slice.call(document.querySelectorAll('.tvhc-item'));
  var nav    = document.getElementById('tvhc-tabs');
  var q      = document.getElementById('tvhc-q');
  var res    = document.getElementById('tvhc-res');
  if(!tabs.length) return;

  var current = tabs[0].getAttribute('data-k');
  function activate(k){
    current = k;
    tabs.forEach(function(t){
      var on = t.getAttribute('data-k') === k;
      t.classList.toggle('on', on);
      t.setAttribute('aria-selected', on ? 'true' : 'false');
    });
    panels.forEach(function(p){
      p.style.display = (p.getAttribute('data-k') === k) ? '' : 'none';
    });
  }
  tabs.forEach(function(t){
    t.addEventListener('click', function(){ activate(t.getAttribute('data-k')); });
  });
  activate(current);

  if(!q) return;
  function reset(){
    nav.style.display = '';
    res.textContent = '';
    items.forEach(function(i){ i.style.display=''; if(i.tagName==='DETAILS') i.open=false; });
    activate(current);
  }
  q.addEventListener('input', function(){
    var v = q.value.trim().toLowerCase();
    if(!v){ reset(); return; }
    nav.style.display = 'none';
    var n = 0;
    items.forEach(function(i){
      var hit = i.textContent.toLowerCase().indexOf(v) >= 0;
      i.style.display = hit ? '' : 'none';
      if(hit){ n++; if(i.tagName==='DETAILS') i.open = true; }
    });
    // 결과가 없는 주제 패널은 접어둔다
    panels.forEach(function(p){
      var any = [].slice.call(p.querySelectorAll('.tvhc-item'))
                  .some(function(i){ return i.style.display !== 'none'; });
      p.style.display = any ? '' : 'none';
    });
    res.textContent = n ? ('검색 결과 ' + n + '건')
                        : '검색 결과가 없습니다. 아래 문의 채널로 남겨주세요.';
  });
})();
</script>
"""


def main():
    s = io.open(SRC, encoding='utf-8').read()
    shutil.copy2(SRC, SRC + '.bak_prehc')

    # 경계: </header> 직후 ~ <footer 직전
    m_head = re.search(r'</header>', s)
    m_foot = re.search(r'<footer\b', s)
    if not m_head or not m_foot:
        print('ABORT: 헤더/푸터 경계를 못 찾음'); return 1

    pre  = s[:m_head.end()]
    post = s[m_foot.start():]
    old  = s[m_head.end():m_foot.start()]

    # 공식대행사는 별도 서브페이지(agency.html)로 분리 — 헬프센터에서는 제외
    if '<section id="agency"' in old:
        print('제거: #agency 섹션 -> agency.html 로 분리됨')

    new = build_body() + '\n' + CONTACT + '\n' + JS
    out = pre + '\n' + new + '\n' + post

    io.open(SRC, 'w', encoding='utf-8').write(out)
    print('교체: %d -> %d chars' % (len(old), len(new)))
    print('주제 %d개 / 주제FAQ %d / 공통FAQ %d / 용어 %d'
          % (len(TOPICS), sum(len(t['faq']) for t in TOPICS), len(COMMON_FAQ), len(GLOSSARY)))
    print('written:', SRC)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
