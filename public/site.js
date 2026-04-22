const backToTop = document.getElementById('back-to-top');
if (backToTop) {
  window.addEventListener('scroll', () => {
    backToTop.style.display = window.scrollY > 280 ? 'block' : 'none';
  });
  backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

document.querySelectorAll('.yt-facade').forEach((wrap) => {
  const id = wrap.dataset.yt;
  const title = wrap.dataset.title || 'YouTube video';
  if (!id) return;
  const btn = wrap.querySelector('.yt-facade__btn');
  const load = () => {
    const host = document.createElement('div');
    host.className = 'video-wrap';
    const iframe = document.createElement('iframe');
    iframe.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1`;
    iframe.title = title;
    iframe.setAttribute('allow', 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share');
    iframe.allowFullscreen = true;
    iframe.loading = 'lazy';
    iframe.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;border:0';
    host.appendChild(iframe);
    wrap.replaceWith(host);
  };
  if (btn) btn.addEventListener('click', load, { once: true });
});

const searchForm = document.getElementById('site-search-form');
const searchInput = document.getElementById('site-search-input');
if (searchForm && searchInput) {
  searchForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const query = searchInput.value.trim();
    if (!query) return;
    if (!window.find || !window.find(query)) {
      window.location.href = `sitemap.html?q=${encodeURIComponent(query)}`;
    }
  });
}
(() => {
  document.documentElement.lang = 'ja';
  try { localStorage.setItem('face-score-global-language', 'ja'); } catch (e) {}
  
  (function setOgLocale() {
    let meta = document.querySelector('meta[property="og:locale"]');
    if (!meta) {
      meta = document.createElement('meta');
      meta.setAttribute('property', 'og:locale');
      document.head.appendChild(meta);
    }
    meta.setAttribute('content', 'ja_JP');
  })();
  
  document.addEventListener('DOMContentLoaded', () => {
    const updated = document.querySelector('.article-hero');
    if (updated && !document.querySelector('.page-updated')) {
      const p = document.createElement('p');
      p.className = 'page-updated';
      p.textContent = '更新日: 2026年4月15日';
      updated.appendChild(p);
    }
    document.querySelectorAll('.intent-tool, .analyzer-card, [data-guidance-tool], [data-simple-tool]').forEach((tool) => {
      if (tool.querySelector('.tool-privacy-note')) return;
      const note = document.createElement('p');
      note.className = 'tool-privacy-note';
      note.textContent = 'プライバシーメモ: ご自身の写真、または許可のある写真だけを使用してください。結果は写真改善の目安であり、医療・本人確認・法的判断ではありません。';
      const firstResult = tool.querySelector('.intent-tool__result, .tool-result, #results-area');
      if (firstResult && firstResult.parentNode === tool) tool.insertBefore(note, firstResult);
      else tool.appendChild(note);
    });
  });
})();
