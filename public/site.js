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
  try {
    localStorage.setItem('face-score-global-language', 'ja');
  } catch (error) {
    console.debug('Unable to persist language preference.', error);
  }

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
      p.textContent = '\u66f4\u65b0\u65e5: 2026\u5e744\u670815\u65e5';
      updated.appendChild(p);
    }

    document.querySelectorAll('.intent-tool, .analyzer-card, [data-guidance-tool], [data-simple-tool]').forEach((tool) => {
      if (tool.querySelector('.tool-privacy-note')) return;

      const note = document.createElement('p');
      note.className = 'tool-privacy-note';
      note.textContent = '\u30d7\u30e9\u30a4\u30d0\u30b7\u30fc\u30e1\u30e2: \u3054\u81ea\u8eab\u306e\u5199\u771f\u3001\u307e\u305f\u306f\u8a31\u53ef\u306e\u3042\u308b\u5199\u771f\u3060\u3051\u3092\u4f7f\u7528\u3057\u3066\u304f\u3060\u3055\u3044\u3002\u7d50\u679c\u306f\u5199\u771f\u6539\u5584\u306e\u76ee\u5b89\u3067\u3042\u308a\u3001\u533b\u7642\u30fb\u672c\u4eba\u78ba\u8a8d\u30fb\u6cd5\u7684\u5224\u65ad\u3067\u306f\u3042\u308a\u307e\u305b\u3093\u3002';

      const firstResult = tool.querySelector('.intent-tool__result, .tool-result, .results-area');
      if (firstResult && firstResult.parentNode === tool) {
        tool.insertBefore(note, firstResult);
      } else {
        tool.appendChild(note);
      }
    });
  });
})();
