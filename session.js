// NeedsOcean 세션 스텁 스크립트
// 실제 로그인/세션 로직이 준비되기 전까지 index.html의 인라인 스크립트가
// 에러 없이 동작하도록 최소 기능만 제공합니다.
window.NeedsOceanSession = {
  renderHeaderCta: function () {
    var cta = document.getElementById('headerCta');
    if (!cta) return;
    // 필요 시 로그인 상태에 따라 버튼 텍스트/링크를 바꾸는 로직을 여기에 추가하세요.
    // 예: cta.textContent = '마이페이지'; cta.href = 'mypage.html';
  }
};
