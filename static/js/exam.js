// 기출 근거 찾기 화면 동작 (사이트와 미리보기가 같이 쓴다)
// - 지문의 꼬리표(14-③)를 누르면 그 문제의 맨 위로 가고 해당 선지에 색 표시
// - 선지의 '지문 근거/정답 근거'를 누르면 지문의 해당 밑줄로 가서 강조
// - 색 표시는 다른 것을 누를 때까지 남긴다 (사용자 결정 2026-11-24)
(function () {
  function bar() {
    var t = document.querySelector('.topbar');
    return t ? t.getBoundingClientRect().height + 12 : 12;
  }
  function go(el, center) {
    if (!el) return;
    var r = el.getBoundingClientRect();
    var y = center ? r.top + window.pageYOffset - window.innerHeight / 2 + r.height / 2
                   : r.top + window.pageYOffset - bar();
    window.scrollTo({ top: Math.max(0, y), behavior: 'smooth' });
  }
  document.addEventListener('click', function (e) {
    var tag = e.target.closest('a.xm-tag');
    if (tag) {
      e.preventDefault();
      go(document.getElementById(tag.getAttribute('href').slice(1)), false);
      document.querySelectorAll('.xm-pick').forEach(function (x) { x.classList.remove('xm-pick'); });
      var li = document.getElementById(tag.dataset.pick);
      if (li) li.classList.add('xm-pick');
      return;
    }
    var src = e.target.closest('a.xm-src');
    if (src) {
      e.preventDefault();
      var pre = src.dataset.ev;
      document.querySelectorAll('.xm-hit').forEach(function (x) { x.classList.remove('xm-hit'); });
      var hits = Array.prototype.filter.call(document.querySelectorAll('[data-ev]'), function (x) {
        return x.dataset.ev.split(' ').some(function (id) { return id.indexOf(pre) === 0; });
      });
      hits.forEach(function (x) { x.classList.add('xm-hit'); });
      go(hits[0], true);
    }
  });
})();
