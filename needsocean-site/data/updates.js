/* 니즈오션 실무자 제보(고객사 업데이트) 저장/조회 헬퍼 — localStorage 기반 */
(function () {
  const STORAGE_KEY = 'needsoceanUpdates';

  function getUpdates() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    } catch (e) {
      return [];
    }
  }

  function saveUpdate(entry) {
    const list = getUpdates();
    list.push(entry);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
    return list;
  }

  function deleteUpdate(id) {
    const list = getUpdates().filter(u => u.id !== id);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
    return list;
  }

  function escapeHtml(str) {
    return String(str == null ? '' : str).replace(/[&<>"']/g, (c) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
  }

  function slugify(name) {
    return String(name).trim().replace(/\s+/g, '').replace(/[^\p{L}\p{N}_-]/gu, '');
  }

  function clientElementId(matchedId, clientName) {
    return matchedId ? matchedId : 'custom-' + slugify(clientName);
  }

  function findClientMatch(name) {
    if (!window.CLIENT_DATA) return null;
    const norm = String(name).trim().toLowerCase();
    if (!norm) return null;
    return window.CLIENT_DATA.find(c => c.name.toLowerCase() === norm || c.englishName.toLowerCase() === norm)
      || window.CLIENT_DATA.find(c => c.name.toLowerCase().includes(norm) || norm.includes(c.name.toLowerCase()));
  }

  // 캐주얼한 구어체 메모를 "제목 + 설명" 형태의 정리된 포인트로 변환 (간단한 규칙 기반 정리기)
  const LEADING_FILLER = /^(오늘|어제|아까|방금|지난주|이번주)?\s*[가-힣A-Za-z0-9&]{0,12}\s*(랑|와|과|이랑)?\s*(회의|통화|미팅|콜)\s*(했는데|했음|함|하면서|해서)[,]?\s*/;

  const TRAILING_RULES = [
    [/하고\s*싶대(요)?$/, ''],
    [/하고\s*싶다고\s*함$/, ''],
    [/(라고|다고)\s*들었(음|다)$/, ''],
    [/(라고|다고)\s*함$/, ''],
    [/것\s*같(음|아요|다)$/, ''],
    [/(계획|예정)이래(요)?$/, '$1'],
    [/(계획|예정)래(요)?$/, '$1']
  ];

  function polishClause(s) {
    let out = s.trim();
    for (let pass = 0; pass < 2; pass++) {
      for (const [re, rep] of TRAILING_RULES) out = out.replace(re, rep).trim();
    }
    return out;
  }

  const HEADLINE_KEYWORDS = ['진출', '전략', '채널', '캠페인', '계획', '확대', '개발', '협업', '리뉴얼', '패키지', '인증', '예산', '마케팅', '제품', '시장', '기술', '제형', '런칭', '디자인'];

  function makeTitle(clause) {
    for (const kw of HEADLINE_KEYWORDS) {
      const idx = clause.indexOf(kw);
      if (idx !== -1) {
        const end = idx + kw.length;
        const start = Math.max(0, end - 14);
        let head = clause.slice(start, end);
        const sp = head.indexOf(' ');
        if (sp !== -1 && sp < head.length - kw.length) head = head.slice(sp + 1);
        return head.trim();
      }
    }
    let head = clause.length > 14 ? clause.slice(0, 14) : clause;
    const lastSpace = head.lastIndexOf(' ');
    if (clause.length > 14 && lastSpace > 5) head = head.slice(0, lastSpace);
    return head.trim();
  }

  function summarizePoints(text) {
    let cleaned = String(text).replace(/\s+/g, ' ').trim().replace(LEADING_FILLER, '').trim();

    const clauses = cleaned.split(/[.!?]\s*/).map(s => s.trim()).filter(Boolean);
    const points = clauses
      .map(polishClause)
      .filter(s => s.length > 3)
      .slice(0, 4)
      .map(s => ({ title: makeTitle(s), desc: s }));

    return points.length ? points : [{ title: '제보 내용', desc: cleaned.slice(0, 80) }];
  }

  // 이전 버전(단순 문자열 배열)으로 저장된 제보도 깨지지 않게 title/desc 형태로 보정
  function toPoints(summary, fallbackContent) {
    if (Array.isArray(summary) && summary.length) {
      if (typeof summary[0] === 'string') {
        return summary.map(s => ({ title: s.length > 16 ? s.slice(0, 16) : s, desc: s }));
      }
      return summary;
    }
    return [{ title: '제보 내용', desc: String(fallbackContent || '').slice(0, 80) }];
  }

  function formatFileSize(bytes) {
    if (!bytes) return '';
    if (bytes < 1024 * 1024) return Math.round(bytes / 1024) + 'KB';
    return (bytes / (1024 * 1024)).toFixed(1) + 'MB';
  }

  function fileChipHtml(file) {
    if (!file || !file.name) return '';
    const safeName = escapeHtml(file.name);
    const size = formatFileSize(file.size);
    return `<div class="report-file">📎 ${safeName}${size ? ` (${size})` : ''}</div>`;
  }

  function formatDate(iso) {
    try {
      const d = new Date(iso);
      return `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, '0')}.${String(d.getDate()).padStart(2, '0')}`;
    } catch (e) {
      return '';
    }
  }

  window.NeedsOceanUpdates = {
    getUpdates, saveUpdate, deleteUpdate, escapeHtml, slugify, clientElementId,
    findClientMatch, summarizePoints, toPoints, formatDate, formatFileSize, fileChipHtml, STORAGE_KEY
  };
})();
