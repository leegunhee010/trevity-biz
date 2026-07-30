insert into blog_posts (slug, title, category, thumbnail_url, excerpt, body_html, read_minutes, published, created_at) values
('market', '동남아 틱톡 사용률 2위, 베트남 시장이 특별한 이유', '베트남 시장',
 './images/blog/thumb-market.png', '동남아에서 틱톡 사용률 2위인 베트남 시장이 왜 특별한지 살펴봅니다.',
 '<p>동남아에서 틱톡 사용률 2위인 베트남 시장이 왜 특별한지 살펴봅니다.</p>', 4, true, '2026-07-21'),
('midtier', '팔로워 10만~50만, 왜 이 구간이 가장 효율적일까요?', '인플루언서 부킹',
 './images/about-tiktok.png', '팔로워 10만~50만 구간 인플루언서가 캠페인에 가장 효율적인 이유입니다.',
 '<p>팔로워 10만~50만 구간 인플루언서가 캠페인에 가장 효율적인 이유입니다.</p>', 4, true, '2026-07-20'),
('diy', 'DIY 인플루언서 섭외, 왜 오히려 더 비쌀까요?', '인플루언서 부킹',
 './images/blog/thumb-diy.png', '직접 섭외가 대행보다 왜 더 비용이 드는지 비교합니다.',
 '<p>직접 섭외가 대행보다 왜 더 비용이 드는지 비교합니다.</p>', 4, true, '2026-07-19'),
('hantown', '베트남 한인타운, 왜 로컬 마케팅의 시작점일까요?', '캠페인 사례',
 './images/blog/thumb-hantown.png', '베트남 한인타운 상권의 로컬 마케팅 사례를 소개합니다.',
 '<p>베트남 한인타운 상권의 로컬 마케팅 사례를 소개합니다.</p>', 4, true, '2026-07-18');

insert into packages (slug, name, influencer_count, price_krw, description, sort_order) values
('starter', '스타터', 10, 2000000, '인플루언서 10명 부킹, 부가세 별도', 1),
('growth', '그로스', 20, 4000000, '인플루언서 20명 부킹, 부가세 별도', 2),
('dominant', '도미넌트', 50, 10000000, '인플루언서 50명 부킹, 부가세 별도', 3);

insert into portfolio_items (placement, media_type, url, poster_url, alt, sort_order, active) values
('home-roll', 'image', './assets/roll/1.jpg', '', '', 1, true),
('hero-wall', 'video', './assets/pfv/s01.mp4', './assets/pfv/s01.jpg', '트래비티 인플루언서 콘텐츠', 1, true);
