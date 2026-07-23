// 정적 미러 보조 스크립트: 스크롤 리빌 + 카운트업 + 영상 자동재생 복원
(function () {
  // 1) 스크롤 리빌: opacity:0 + translateY 로 저장된 요소를 뷰포트 진입 시 표시
  var hidden = Array.prototype.slice.call(document.querySelectorAll('[style]')).filter(function (el) {
    var s = el.getAttribute('style') || '';
    return /opacity:\s*0(;|\s|$)/.test(s);
  });
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) {
        en.target.style.opacity = '1';
        en.target.style.transform = 'translateY(0)';
        io.unobserve(en.target);
      }
    });
  }, { threshold: 0.1 });
  hidden.forEach(function (el) { io.observe(el); });

  // 2) 카운트업: <span class="inline-grid tabular-nums"> 안의
  //    invisible 자리표시자("10,000+")가 목표값, 보이는 span("0+")을 카운트업
  document.querySelectorAll('span.inline-grid.tabular-nums').forEach(function (wrap) {
    var ghost = wrap.querySelector('span.invisible');
    var live = wrap.querySelector('span:not(.invisible)');
    if (!ghost || !live) return;
    var target = ghost.textContent;
    var num = parseInt(target.replace(/[^0-9]/g, ''), 10);
    if (isNaN(num)) return;
    var suffix = target.replace(/[0-9,]/g, '');
    var fired = false;
    function run() {
      if (fired) return;
      fired = true;
      var t0 = null, dur = 1500;
      function step(ts) {
        if (!t0) t0 = ts;
        var p = Math.min((ts - t0) / dur, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        live.textContent = Math.round(num * eased).toLocaleString() + suffix;
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        cio.unobserve(en.target);
        run();
      });
    }, { threshold: 0.5 });
    cio.observe(wrap);
    // 뷰포트가 좁아 가로로 잘린 경우 등 IO가 안 걸릴 때: 세로로 화면 근처에 오면 강제 실행
    function fallbackCheck() {
      if (fired) return;
      var r = wrap.getBoundingClientRect();
      if (r.top < window.innerHeight && r.bottom > 0) run();
      else setTimeout(fallbackCheck, 800);
    }
    setTimeout(fallbackCheck, 1200);
  });

  // 3) 영상 자동재생 (음소거 필수)
  function playAll() {
    document.querySelectorAll('video').forEach(function (v) {
      v.muted = true;
      v.loop = true;
      v.playsInline = true;
      var p = v.play();
      if (p && p.catch) p.catch(function () {});
    });
  }
  playAll();
  document.addEventListener('visibilitychange', playAll);
})();
