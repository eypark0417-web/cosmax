/* 니즈오션 로그인 세션 관리 — localStorage 기반 (데모용, 실제 인증 서버 없음) */
(function () {
  const SESSION_KEY = 'needsoceanSession';
  const DISPLAY_NAME = '박서윤';
  const ENTRY_PAGE = 'needs.html'; // 로그인한 이용자가 CTA 배너로 바로 진입할 서비스 페이지

  function getSession() {
    try {
      return JSON.parse(localStorage.getItem(SESSION_KEY));
    } catch (e) {
      return null;
    }
  }

  function isLoggedIn() {
    const s = getSession();
    return !!(s && s.loggedIn);
  }

  function login(email) {
    const session = { loggedIn: true, name: DISPLAY_NAME, email: email, loginAt: new Date().toISOString() };
    localStorage.setItem(SESSION_KEY, JSON.stringify(session));
    return session;
  }

  function logout() {
    localStorage.removeItem(SESSION_KEY);
  }

  // 헤더의 "무료로 시작하기" 버튼을 로그인 상태에 따라 사용자 이름으로 교체
  function renderHeaderCta(elId) {
    const el = document.getElementById(elId || 'headerCta');
    if (!el) return;
    const session = getSession();
    if (session && session.loggedIn) {
      el.textContent = session.name;
      el.setAttribute('href', '#');
      el.title = '로그아웃';
      el.addEventListener('click', (e) => {
        e.preventDefault();
        if (confirm('로그아웃 하시겠어요?')) {
          logout();
          location.reload();
        }
      });
    }
    // 로그인 상태면 "시작하기" 계열 CTA 배너를 로그인 페이지 대신 서비스로 연결
    rewriteStartCtas();
  }

  // 로그인한 이용자가 CTA 배너로 진입할 서비스 페이지를 결정 (안전한 redirect 파라미터 우선)
  function enterServicePage() {
    try {
      const target = new URLSearchParams(location.search).get('redirect');
      if (target && target !== 'login.html' && /^[A-Za-z0-9_-]+\.html$/.test(target)) return target;
    } catch (e) { /* noop */ }
    return ENTRY_PAGE;
  }

  // login.html로 향하는 CTA 배너/버튼을, 로그인 상태에서는 서비스 페이지로 바꿔줌
  function rewriteStartCtas(root) {
    if (!isLoggedIn()) return;
    const dest = enterServicePage();
    (root || document).querySelectorAll('a[href="login.html"]').forEach((a) => {
      if (a.id === 'headerCta') return; // 헤더 버튼은 로그아웃 용도로 별도 처리됨
      a.setAttribute('href', dest);
    });
  }

  function gateHtml(message) {
    const msg = message || '코스맥스 회사 계정으로 로그인하면 모든 고객사 데이터를 이용할 수 있어요.';
    return `
      <div style="text-align:center;padding:64px 24px;background:var(--white);border-radius:32px;box-shadow:0 10px 30px rgba(43,43,61,0.06);">
        <div style="width:64px;height:64px;border-radius:50%;background:var(--rose-soft);display:flex;align-items:center;justify-content:center;margin:0 auto 20px;">
          <svg viewBox="0 0 24 24" fill="none" stroke="var(--rose-deep)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="width:28px;height:28px;display:block;"><rect x="5" y="10.5" width="14" height="9" rx="2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/></svg>
        </div>
        <h2 style="font-size:20px;margin-bottom:10px;font-family:'Malgun Gothic','Noto Sans KR',sans-serif;font-weight:700;color:var(--ink);">로그인이 필요합니다</h2>
        <p style="font-size:14px;color:var(--ink-soft);line-height:1.7;margin-bottom:26px;max-width:400px;margin-left:auto;margin-right:auto;">${message ? message : msg}</p>
        <a href="login.html" style="display:inline-block;padding:13px 30px;border-radius:999px;font-weight:700;font-size:14.5px;background:linear-gradient(135deg,var(--rose-deep),var(--gold-deep));color:var(--white);box-shadow:0 10px 24px rgba(201,122,147,0.28);text-decoration:none;">회사 계정으로 로그인하기</a>
      </div>
    `;
  }

  // containerEl에 로그인 여부를 확인해 필요시 게이트 화면을 그려줌. 로그인 상태면 true 반환.
  function requireLoginOrGate(containerEl, message) {
    if (isLoggedIn()) return true;
    if (containerEl) containerEl.innerHTML = gateHtml(message);
    return false;
  }

  window.NeedsOceanSession = {
    getSession, isLoggedIn, login, logout, renderHeaderCta, gateHtml, requireLoginOrGate,
    enterServicePage, rewriteStartCtas, SESSION_KEY
  };
})();
