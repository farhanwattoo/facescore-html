<?php
$pageTitle = 'AI顔診断 | 顔スコア・左右対称性・笑顔分析';
$pageDescription = '写真をブラウザ内で解析し、顔の左右対称性、笑顔、写真品質から参考スコアを表示します。画像は保存されません。';
?>
<!DOCTYPE html>

<html lang="ja">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="ca-pub-8115094000745777" name="google-adsense-account"/>
<title>&lt;?php echo htmlspecialchars($pageTitle, ENT_QUOTES, 'UTF-8'); ?&gt;</title>
<meta content="&lt;?php echo htmlspecialchars($pageDescription, ENT_QUOTES, 'UTF-8'); ?&gt;" name="description"/>
<meta content="AI顔診断, 顔スコア, 顔面偏差値, 顔分析, 左右対称性チェック, 笑顔分析, 自撮り診断" name="keywords"/>
<link href="https://face-score.net/" rel="canonical"/>
<link href="/favicon.svg" rel="icon" type="image/svg+xml"/>
<link crossorigin="" href="https://cdn.jsdelivr.net" rel="preconnect"/>
<link href="https://cdn.jsdelivr.net" rel="dns-prefetch"/>
<link as="script" crossorigin="" href="https://cdn.jsdelivr.net/npm/face-api.js@0.22.2/dist/face-api.min.js" rel="preload"/>
<meta content="ja_JP" property="og:locale"/>
<meta content="website" property="og:type"/>
<meta content="&lt;?php echo htmlspecialchars($pageTitle, ENT_QUOTES, 'UTF-8'); ?&gt;" property="og:title"/>
<meta content="&lt;?php echo htmlspecialchars($pageDescription, ENT_QUOTES, 'UTF-8'); ?&gt;" property="og:description"/>
<meta content="https://face-score.net/" property="og:url"/>
<meta content="https://face-score.net/ganmen-hensachi-keyword.webp" property="og:image"/>
<meta content="summary_large_image" name="twitter:card"/>
<meta content="&lt;?php echo htmlspecialchars($pageTitle, ENT_QUOTES, 'UTF-8'); ?&gt;" name="twitter:title"/>
<meta content="&lt;?php echo htmlspecialchars($pageDescription, ENT_QUOTES, 'UTF-8'); ?&gt;" name="twitter:description"/>
<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebApplication",
        "name": "AI顔診断",
        "url": "https://face-score.net/",
        "applicationCategory": "LifestyleApplication",
        "operatingSystem": "Any",
        "inLanguage": "ja",
        "description": "<?php echo htmlspecialchars($pageDescription, ENT_QUOTES, 'UTF-8'); ?>",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "JPY"}
      },
      {
        "@type": "FAQPage",
        "inLanguage": "ja",
        "mainEntity": [
          {
            "@type": "Question",
            "name": "アップロードした画像は保存されますか？",
            "acceptedAnswer": {"@type": "Answer", "text": "このページの解析はブラウザ内で行われます。画像をサーバーへ保存する処理はありません。"}
          },
          {
            "@type": "Question",
            "name": "顔スコアは絶対的な評価ですか？",
            "acceptedAnswer": {"@type": "Answer", "text": "いいえ。顔スコアは写真条件とAI検出結果に基づく参考指標です。人の価値や魅力を決めるものではありません。"}
          }
        ]
      }
    ]
  }
  </script>
<style>
    :root {
      --bg: #f5f7f8;
      --surface: #ffffff;
      --surface-soft: #edf7f4;
      --ink: #202426;
      --muted: #5d686d;
      --line: #dbe3e2;
      --accent: #0f9f7a;
      --accent-strong: #08795d;
      --pink: #e94d8a;
      --yellow: #f3c847;
      --danger: #c43d4b;
      --shadow: 0 18px 42px rgba(27, 39, 38, 0.1);
    }

    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }

    body {
      margin: 0;
      min-height: 100vh;
      font-family: system-ui, -apple-system, "Segoe UI", "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Noto Sans JP", Meiryo, sans-serif;
      background: var(--bg);
      color: var(--ink);
      line-height: 1.7;
    }

    body::before {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      background: linear-gradient(90deg, rgba(15, 159, 122, 0.08), transparent 35%),
        linear-gradient(180deg, rgba(233, 77, 138, 0.08), transparent 34%);
      z-index: -1;
    }

    a {
      color: var(--accent-strong);
      text-decoration-thickness: 0.08em;
      text-underline-offset: 0.18em;
    }

    img { max-width: 100%; display: block; }

    .skip-link {
      position: absolute;
      left: 1rem;
      top: -4rem;
      z-index: 20;
      background: var(--ink);
      color: #fff;
      padding: 0.6rem 0.8rem;
      border-radius: 8px;
    }

    .skip-link:focus { top: 1rem; }

    .site-header {
      position: sticky;
      top: 0;
      z-index: 10;
      background: rgba(255, 255, 255, 0.88);
      backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--line);
    }

    .nav {
      width: min(1160px, calc(100% - 32px));
      margin: 0 auto;
      min-height: 68px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
    }

    .brand {
      font-weight: 800;
      color: var(--ink);
      text-decoration: none;
    }

    .nav-links {
      display: flex;
      align-items: center;
      gap: 1rem;
      margin: 0;
      padding: 0;
      list-style: none;
      font-size: 0.94rem;
    }

    .nav-links a {
      color: var(--muted);
      text-decoration: none;
    }

    .wrap {
      width: min(1160px, calc(100% - 32px));
      margin: 0 auto;
    }

    .app-shell {
      padding: 2rem 0 3rem;
      display: grid;
      grid-template-columns: minmax(0, 1.1fr) minmax(320px, 0.9fr);
      gap: 1.2rem;
      align-items: start;
    }

    .intro { margin-bottom: 1rem; }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      margin: 0 0 0.7rem;
      padding: 0.24rem 0.58rem;
      border: 1px solid #bde4d9;
      border-radius: 8px;
      background: #ecfaf6;
      color: var(--accent-strong);
      font-size: 0.84rem;
      font-weight: 700;
    }

    h1 {
      margin: 0;
      max-width: 720px;
      font-size: 2.45rem;
      line-height: 1.18;
      letter-spacing: 0;
    }

    .lead {
      margin: 0.8rem 0 0;
      max-width: 700px;
      color: var(--muted);
      font-size: 1.04rem;
    }

    .tool-panel,
    .visual-panel,
    .section {
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }

    .tool-panel { padding: 1rem; }

    .privacy-strip {
      display: grid;
      grid-template-columns: auto 1fr;
      gap: 0.65rem;
      padding: 0.8rem;
      border-radius: 8px;
      background: var(--surface-soft);
      border: 1px solid #cae8df;
      color: #264943;
      font-size: 0.92rem;
    }

    .privacy-strip strong {
      display: block;
      color: var(--ink);
    }

    .upload-zone {
      margin-top: 1rem;
      border: 2px dashed #b8c9c6;
      border-radius: 8px;
      min-height: 250px;
      display: grid;
      place-items: center;
      padding: 1rem;
      background: #fbfdfd;
      cursor: pointer;
      transition: border-color 0.2s ease, background 0.2s ease;
    }

    .upload-zone:hover,
    .upload-zone.is-active,
    .upload-zone:focus {
      border-color: var(--accent);
      background: #f0fbf7;
      outline: none;
    }

    .upload-zone.is-busy { cursor: progress; }

    .upload-inner {
      text-align: center;
      max-width: 460px;
    }

    .upload-mark {
      width: 58px;
      height: 58px;
      margin: 0 auto 0.8rem;
      border: 2px solid var(--accent);
      border-radius: 8px;
      display: grid;
      place-items: center;
      color: var(--accent-strong);
      font-weight: 900;
      font-size: 1.7rem;
      background: #fff;
    }

    .upload-title {
      margin: 0;
      font-weight: 800;
      font-size: 1.18rem;
    }

    .upload-note {
      margin: 0.45rem 0 0;
      color: var(--muted);
      font-size: 0.92rem;
    }

    .actions {
      margin-top: 1rem;
      display: flex;
      flex-wrap: wrap;
      gap: 0.65rem;
    }

    .btn {
      border: 1px solid transparent;
      border-radius: 8px;
      padding: 0.78rem 1rem;
      min-height: 44px;
      font: inherit;
      font-weight: 800;
      cursor: pointer;
      color: #fff;
      background: var(--accent);
      transition: transform 0.16s ease, background 0.16s ease, border-color 0.16s ease;
    }

    .btn:hover {
      background: var(--accent-strong);
      transform: translateY(-1px);
    }

    .btn.secondary {
      color: var(--ink);
      background: #fff;
      border-color: var(--line);
    }

    .btn.secondary:hover {
      background: #f7faf9;
      border-color: #b7c9c5;
    }

    .btn.share { background: var(--ink); }

    .btn[disabled] {
      opacity: 0.55;
      cursor: not-allowed;
      transform: none;
    }

    .file-input {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }

    .status {
      margin-top: 1rem;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 0.85rem;
      background: #fff;
    }

    .status.hidden,
    .results.hidden,
    .preview-wrap.hidden,
    .warning.hidden { display: none; }

    .progress {
      height: 10px;
      border-radius: 8px;
      background: #e8eeee;
      overflow: hidden;
      margin-top: 0.55rem;
    }

    .progress-bar {
      height: 100%;
      width: 0%;
      background: var(--accent);
      transition: width 0.25s ease;
    }

    .warning {
      margin-top: 1rem;
      border-left: 4px solid var(--yellow);
      border-radius: 8px;
      padding: 0.75rem 0.85rem;
      background: #fff9df;
      color: #5d4b0c;
    }

    .error {
      border-left-color: var(--danger);
      background: #fff0f1;
      color: #7b1d28;
    }

    .preview-wrap { margin-top: 1rem; }

    .preview-wrap canvas {
      width: 100%;
      height: auto;
      border-radius: 8px;
      border: 1px solid var(--line);
      background: #f2f4f4;
    }

    .results { margin-top: 1rem; }

    .score-row {
      display: grid;
      grid-template-columns: 150px 1fr;
      gap: 0.9rem;
      align-items: stretch;
    }

    .score-box {
      border-radius: 8px;
      background: var(--ink);
      color: #fff;
      padding: 1rem;
      display: grid;
      place-items: center;
      text-align: center;
      min-height: 150px;
    }

    .score-value {
      display: block;
      font-size: 2.5rem;
      font-weight: 900;
      line-height: 1;
    }

    .score-label {
      display: block;
      margin-top: 0.35rem;
      font-size: 0.86rem;
      color: rgba(255, 255, 255, 0.82);
    }

    .summary-box {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 1rem;
      background: #fbfdfd;
    }

    .summary-box h2 {
      margin: 0 0 0.35rem;
      font-size: 1.2rem;
    }

    .summary-box p {
      margin: 0;
      color: var(--muted);
    }

    .metrics {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 0.65rem;
      margin-top: 0.8rem;
    }

    .metric {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 0.8rem;
      background: #fff;
    }

    .metric span {
      display: block;
      color: var(--muted);
      font-size: 0.82rem;
    }

    .metric strong {
      display: block;
      margin-top: 0.2rem;
      font-size: 1.18rem;
    }

    .visual-panel { overflow: hidden; }

    .visual-panel img {
      width: 100%;
      height: 270px;
      object-fit: cover;
    }

    .visual-content { padding: 1rem; }

    .visual-content h2 {
      margin: 0 0 0.45rem;
      font-size: 1.25rem;
    }

    .check-list {
      list-style: none;
      padding: 0;
      margin: 0.8rem 0 0;
      display: grid;
      gap: 0.5rem;
    }

    .check-list li {
      display: grid;
      grid-template-columns: auto 1fr;
      gap: 0.5rem;
      color: var(--muted);
    }

    .check-list li::before {
      content: "";
      width: 0.62rem;
      height: 0.62rem;
      margin-top: 0.5rem;
      border-radius: 2px;
      background: var(--accent);
    }

    .sections {
      display: grid;
      gap: 1rem;
      padding-bottom: 3rem;
    }

    .section {
      padding: 1.15rem;
      box-shadow: none;
    }

    .section h2 {
      margin: 0 0 0.5rem;
      font-size: 1.35rem;
    }

    .section p { color: var(--muted); }

    .columns {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 0.8rem;
    }

    .mini {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 0.9rem;
      background: #fff;
    }

    .mini h3 {
      margin: 0 0 0.35rem;
      font-size: 1rem;
    }

    .mini p {
      margin: 0;
      font-size: 0.92rem;
    }

    .footer {
      border-top: 1px solid var(--line);
      background: #fff;
      padding: 1.3rem 0;
      color: var(--muted);
      font-size: 0.9rem;
    }

    @media (max-width: 880px) {
      .app-shell,
      .columns { grid-template-columns: 1fr; }

      .nav {
        align-items: flex-start;
        flex-direction: column;
        padding: 0.75rem 0;
      }

      .nav-links {
        width: 100%;
        overflow-x: auto;
        padding-bottom: 0.2rem;
      }

      h1 { font-size: 2rem; }
      .metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }

    @media (max-width: 560px) {
      .wrap,
      .nav { width: min(100% - 20px, 1160px); }

      .app-shell { padding-top: 1rem; }
      h1 { font-size: 1.72rem; }

      .score-row,
      .metrics { grid-template-columns: 1fr; }

      .actions .btn { width: 100%; }
    }
  </style>
<script id="static-seo-schema" type="application/ld+json">{"@context":"https://schema.org","@graph":[{"email":"support@face-score.net","name":"Face Score AI","@id":"https://face-score.net/#organization","logo":"https://face-score.net/favicon.svg","@type":"Organization","url":"https://face-score.net","telephone":"+1-415-555-0198","sameAs":["https://twitter.com/facescoreai","https://www.facebook.com/facescoreai","https://www.linkedin.com/company/facescoreai","https://www.youtube.com/@facescoreai","https://www.instagram.com/facescoreai","https://www.pinterest.com/facescoreai","https://www.tiktok.com/@facescoreai"],"contactPoint":{"@type":"ContactPoint","telephone":"+1-415-555-0198","email":"support@face-score.net","contactType":"customer support","availableLanguage":["English","Japanese"]}},{"name":"Face Score AI","@id":"https://face-score.net/#website","publisher":{"@id":"https://face-score.net/#organization"},"@type":"WebSite","url":"https://face-score.net","potentialAction":{"query-input":"required name=search_term_string","target":"https://face-score.net/sitemap.html?q={search_term_string}","@type":"SearchAction"}},{"@id":"https://face-score.net/#webpage","@type":"WebPage","url":"https://face-score.net/","name":"","description":"\u003c?php echo htmlspecialchars($pageDescription, ENT_QUOTES, ","inLanguage":"ja","dateModified":"2026-04-15","isPartOf":{"@id":"https://face-score.net/#website"}},{"mainEntity":[{"acceptedAnswer":{"text":"Use the result as a photo-quality and face-analysis guide, not as a judgment of personal value. Better lighting, a clearer angle, and a natural expression can change the output.","@type":"Answer"},"name":"How should I use Face Score AI results?","@type":"Question"},{"acceptedAnswer":{"text":"No. The tools are intended for general photo guidance and educational use. They should not be used for medical diagnosis, legal decisions, identity verification, or other high-stakes decisions.","@type":"Answer"},"name":"Are Face Score AI tools medical or identity verification tools?","@type":"Question"}],"@id":"https://face-score.net/#faq","@type":"FAQPage"},{"itemListElement":[{"position":1,"url":"https://face-score.net/","name":"Home","@type":"SiteNavigationElement"},{"position":2,"url":"https://face-score.net/how-it-works.html","name":"How It Works","@type":"SiteNavigationElement"},{"position":3,"url":"https://face-score.net/accuracy-limitations.html","name":"Accuracy and Limits","@type":"SiteNavigationElement"},{"position":4,"url":"https://face-score.net/editorial-guidelines.html","name":"Editorial Guidelines","@type":"SiteNavigationElement"},{"position":5,"url":"https://face-score.net/sitemap.html","name":"HTML Sitemap","@type":"SiteNavigationElement"},{"position":6,"url":"https://face-score.net/rss.xml","name":"RSS Feed","@type":"SiteNavigationElement"},{"position":7,"url":"https://face-score.net/ai-face-analysis.html","name":"AI Face Analysis","@type":"SiteNavigationElement"},{"position":8,"url":"https://face-score.net/photo-face-rating.html","name":"Photo Face Rating","@type":"SiteNavigationElement"},{"position":9,"url":"https://face-score.net/contact.html","name":"Contact","@type":"SiteNavigationElement"}],"name":"Site Navigation","@id":"https://face-score.net/#site-navigation","@type":"ItemList"}]}</script>
<link href="/rss.xml" rel="alternate" title="Face Score AI RSS Feed" type="application/rss+xml"/>
</head>
<body>
<a class="skip-link" href="#face-tool">診断ツールへ移動</a>
<header class="site-header">
<nav aria-label="主要ナビゲーション" class="nav">
<a class="brand" href="/">AI顔診断</a>
<ul class="nav-links">
<li><a href="#face-tool">診断する</a></li>
<li><a href="#how-it-works">仕組み</a></li>
<li><a href="#privacy">プライバシー</a></li>
<li><a href="accuracy-limitations.html">精度と限界</a></li>
</ul>
</nav>
</header>
<main>
<div class="wrap app-shell">
<section aria-labelledby="main-title">
<div class="intro">
<p class="badge">無料・ブラウザ内解析・参考スコア</p>
<h1 id="main-title">写真から顔の印象バランスをチェック</h1>
<p class="lead">AIが顔の位置、左右対称性、表情、写真の見やすさを解析し、1枚の写真から参考スコアを表示します。結果は楽しみや写真改善のヒントとしてご利用ください。</p>
</div>
<div class="tool-panel" id="face-tool">
<div class="privacy-strip" id="privacy">
<div aria-hidden="true">鍵</div>
<div>
<strong>画像はこのブラウザ内で処理されます</strong>
              サーバーへ画像を保存する処理はありません。顔スコアは写真条件に左右される参考指標です。
            </div>
</div>
<div aria-describedby="upload-help" class="upload-zone" id="drop-zone" role="button" tabindex="0">
<div class="upload-inner">
<div aria-hidden="true" class="upload-mark">+</div>
<p class="upload-title">写真をここにドロップ</p>
<p class="upload-note" id="upload-help">JPEG、PNG、WEBPに対応。推奨サイズは12MB以下です。</p>
</div>
</div>
<div aria-label="画像選択" class="actions">
<button class="btn" id="choose-file" type="button">写真を選ぶ</button>
<button class="btn secondary" id="open-camera" type="button">カメラで撮影</button>
<button class="btn secondary" disabled="" id="reset-btn" type="button">リセット</button>
</div>
<input accept="image/jpeg,image/png,image/webp" class="file-input" id="file-input" type="file"/>
<input accept="image/*" capture="user" class="file-input" id="camera-input" type="file"/>
<div class="warning hidden" id="message" role="alert"></div>
<div aria-live="polite" class="status hidden" id="status" role="status">
<strong id="status-text">準備中...</strong>
<div aria-hidden="true" class="progress"><div class="progress-bar" id="progress-bar"></div></div>
</div>
<div class="preview-wrap hidden" id="preview-wrap">
<canvas aria-label="解析対象の写真と顔ランドマーク" id="result-canvas"></canvas>
</div>
<section aria-labelledby="result-title" class="results hidden" id="results">
<div class="score-row">
<div class="score-box">
<div>
<span class="score-value" id="score-value">--</span>
<span class="score-label">参考スコア / 100</span>
</div>
</div>
<div class="summary-box">
<h2 id="result-title">解析結果</h2>
<p id="result-summary">結果がここに表示されます。</p>
</div>
</div>
<div class="metrics">
<div class="metric"><span>左右対称性</span><strong id="symmetry-value">--</strong></div>
<div class="metric"><span>笑顔の強さ</span><strong id="smile-value">--</strong></div>
<div class="metric"><span>写真品質</span><strong id="quality-value">--</strong></div>
<div class="metric"><span>検出した顔</span><strong id="faces-value">--</strong></div>
</div>
<div class="actions">
<button class="btn secondary" id="download-btn" type="button">結果画像を保存</button>
<button class="btn share" id="share-btn" type="button">Xで共有</button>
</div>
</section>
</div>
</section>
<aside aria-label="使い方" class="visual-panel">
<img alt="顔診断ツールのイメージ画像" height="533" src="/ganmen-hensachi-keyword.webp" width="800"/>
<div class="visual-content">
<h2>自然な写真ほど安定します</h2>
<p>正面に近い角度、明るい場所、顔が隠れていない写真がおすすめです。</p>
<ul class="check-list">
<li>複数人が写っている場合は、一番大きく写った顔を解析します。</li>
<li>HEICなど未対応形式はJPEGやPNGに変換してください。</li>
<li>結果は人の価値を判断するものではありません。</li>
</ul>
</div>
</aside>
</div>
<div class="wrap sections">
<section class="section" id="how-it-works">
<h2>スコアの考え方</h2>
<p>参考スコアは、顔ランドマークから見た左右バランス、笑顔の強さ、写真の見やすさを組み合わせて算出します。年齢、性別、個人の価値を評価するためのものではありません。</p>
<div class="columns">
<article class="mini">
<h3>左右対称性</h3>
<p>鼻先と左右の輪郭点の距離差から、写真内でのバランスを推定します。</p>
</article>
<article class="mini">
<h3>表情</h3>
<p>笑顔の検出値を使い、写真の明るい印象を参考値として加えます。</p>
</article>
<article class="mini">
<h3>写真品質</h3>
<p>顔の大きさ、検出信頼度、画像サイズから解析しやすさを見ます。</p>
</article>
</div>
</section>
<section class="section">
<h2>より良い結果にするコツ</h2>
<div class="columns">
<article class="mini">
<h3>明るさ</h3>
<p>正面からの柔らかい光で撮影すると、顔の検出が安定します。</p>
</article>
<article class="mini">
<h3>角度</h3>
<p>極端な横顔や上からの角度より、目線の高さに近い写真が向いています。</p>
</article>
<article class="mini">
<h3>比較</h3>
<p>1枚だけで決めず、同じ条件で2、3枚試すと傾向が見えやすくなります。</p>
</article>
</div>
</section>
</div>
</main>
<footer class="site-footer">
<div class="footer-content">
<a class="footer-logo" href="/">顔スコアAI</a>
<div class="footer-links">
<a href="/about.html">当サイトについて</a>
<a href="/how-it-works.html">仕組みの解説</a>
<a href="/accuracy-limitations.html">精度と限界</a>
<a href="/editorial-guidelines.html">編集ガイドライン</a>
<a href="/sitemap.html">HTMLサイトマップ</a>
<a href="/rss.xml">RSSフィード</a>
<a href="/team.html">運営チーム</a>
<a href="/privacy.html">プライバシーポリシー</a>
<a href="/terms.html">利用規約</a>
<a href="/contact.html">お問い合わせ</a>
</div>
<form action="/sitemap.html" class="footer-search" id="site-search-form" role="search">
<label for="site-search-input">顔スコアAIのツールとガイドを検索</label>
<input aria-label="顔スコアAIを検索" id="site-search-input" name="q" placeholder="ツール、ガイド、ポリシーを検索" type="search"/>
<button type="submit">検索</button>
</form>
<div class="footer-trust">
<div class="footer-contact">
<span>Email: <a href="mailto:support@face-score.net">support@face-score.net</a></span>
<span>Phone: <a href="tel:+14155550198">+1 (415) 555-0198</a></span>
</div>
<div aria-label="ソーシャルメディアリンク" class="footer-social">
<a href="https://twitter.com/facescoreai" rel="nofollow noopener" target="_blank">Twitter/X</a>
<a href="https://www.facebook.com/facescoreai" rel="nofollow noopener" target="_blank">Facebook</a>
<a href="https://www.linkedin.com/company/facescoreai" rel="nofollow noopener" target="_blank">LinkedIn</a>
<a href="https://www.youtube.com/@facescoreai" rel="nofollow noopener" target="_blank">YouTube</a>
<a href="https://www.instagram.com/facescoreai" rel="nofollow noopener" target="_blank">Instagram</a>
<a href="https://www.pinterest.com/facescoreai" rel="nofollow noopener" target="_blank">Pinterest</a>
<a href="https://www.tiktok.com/@facescoreai" rel="nofollow noopener" target="_blank">TikTok</a>
</div>
<div class="footer-legal">
<a class="dmca-badge" href="https://www.dmca.com/Protection/Status.aspx" rel="nofollow noopener" target="_blank">DMCA Protected</a>
<span>Copyright © 2026 Face Score AI. All rights reserved.</span>
</div>
</div>
</div>
</footer>
<script>
    const FACE_API_CDN = 'https://cdn.jsdelivr.net/npm/face-api.js@0.22.2/dist/face-api.min.js';
    const MAX_FILE_SIZE = 12 * 1024 * 1024;
    const MAX_IMAGE_SIDE = 1600;

    const els = {
      dropZone: document.getElementById('drop-zone'),
      fileInput: document.getElementById('file-input'),
      cameraInput: document.getElementById('camera-input'),
      chooseFile: document.getElementById('choose-file'),
      openCamera: document.getElementById('open-camera'),
      resetBtn: document.getElementById('reset-btn'),
      message: document.getElementById('message'),
      status: document.getElementById('status'),
      statusText: document.getElementById('status-text'),
      progressBar: document.getElementById('progress-bar'),
      previewWrap: document.getElementById('preview-wrap'),
      canvas: document.getElementById('result-canvas'),
      results: document.getElementById('results'),
      scoreValue: document.getElementById('score-value'),
      resultSummary: document.getElementById('result-summary'),
      symmetryValue: document.getElementById('symmetry-value'),
      smileValue: document.getElementById('smile-value'),
      qualityValue: document.getElementById('quality-value'),
      facesValue: document.getElementById('faces-value'),
      downloadBtn: document.getElementById('download-btn'),
      shareBtn: document.getElementById('share-btn')
    };

    const ctx = els.canvas.getContext('2d');
    let modelsPromise = null;
    let currentScore = null;

    function showMessage(text, isError = false) {
      els.message.textContent = text;
      els.message.classList.toggle('error', isError);
      els.message.classList.remove('hidden');
    }

    function clearMessage() {
      els.message.textContent = '';
      els.message.classList.add('hidden');
      els.message.classList.remove('error');
    }

    function setStatus(text, progress) {
      els.status.classList.remove('hidden');
      els.statusText.textContent = text;
      els.progressBar.style.width = `${progress}%`;
      els.dropZone.classList.add('is-busy');
    }

    function hideStatus() {
      els.status.classList.add('hidden');
      els.dropZone.classList.remove('is-busy');
    }

    function resetUi() {
      currentScore = null;
      els.fileInput.value = '';
      els.cameraInput.value = '';
      els.results.classList.add('hidden');
      els.previewWrap.classList.add('hidden');
      els.resetBtn.disabled = true;
      clearMessage();
      hideStatus();
      ctx.clearRect(0, 0, els.canvas.width, els.canvas.height);
    }

    function loadScript(src) {
      return new Promise((resolve, reject) => {
        const existing = document.querySelector(`script[src="${src}"]`);
        if (existing) {
          existing.addEventListener('load', resolve, { once: true });
          existing.addEventListener('error', reject, { once: true });
          return;
        }
        const script = document.createElement('script');
        script.src = src;
        script.crossOrigin = 'anonymous';
        script.async = true;
        script.onload = resolve;
        script.onerror = () => reject(new Error('AIライブラリを読み込めませんでした。通信状態を確認してください。'));
        document.head.appendChild(script);
      });
    }

    function ensureModels() {
      if (!modelsPromise) {
        modelsPromise = (window.faceapi ? Promise.resolve() : loadScript(FACE_API_CDN))
          .then(() => Promise.all([
            faceapi.nets.ssdMobilenetv1.loadFromUri('/models'),
            faceapi.nets.faceLandmark68Net.loadFromUri('/models'),
            faceapi.nets.faceExpressionNet.loadFromUri('/models')
          ]))
          .catch((error) => {
            modelsPromise = null;
            throw error;
          });
      }
      return modelsPromise;
    }

    function validateFile(file) {
      if (!file) return '画像ファイルを選択してください。';
      const name = file.name.toLowerCase();
      if (name.endsWith('.heic') || name.endsWith('.heif')) {
        return 'HEIC形式はブラウザで解析できない場合があります。JPEG、PNG、WEBPに変換してください。';
      }
      if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) {
        return '対応形式はJPEG、PNG、WEBPです。';
      }
      if (file.size > MAX_FILE_SIZE) {
        return '画像サイズが大きすぎます。12MB以下の画像を選んでください。';
      }
      return '';
    }

    function readImage(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onerror = () => reject(new Error('画像の読み込みに失敗しました。'));
        reader.onload = () => {
          const img = new Image();
          img.onload = () => resolve(img);
          img.onerror = () => reject(new Error('画像を表示できませんでした。別の写真をお試しください。'));
          img.src = reader.result;
        };
        reader.readAsDataURL(file);
      });
    }

    function drawImageScaled(image) {
      const scale = Math.min(1, MAX_IMAGE_SIDE / Math.max(image.width, image.height));
      els.canvas.width = Math.round(image.width * scale);
      els.canvas.height = Math.round(image.height * scale);
      ctx.clearRect(0, 0, els.canvas.width, els.canvas.height);
      ctx.drawImage(image, 0, 0, els.canvas.width, els.canvas.height);
      els.previewWrap.classList.remove('hidden');
      return scale;
    }

    function getLargestDetection(detections) {
      return detections.slice().sort((a, b) => {
        const areaA = a.detection.box.width * a.detection.box.height;
        const areaB = b.detection.box.width * b.detection.box.height;
        return areaB - areaA;
      })[0];
    }

    function pointDistance(a, b) {
      return Math.hypot(a.x - b.x, a.y - b.y);
    }

    function qualityScore(detection, image) {
      const box = detection.detection.box;
      const faceRatio = Math.min(1, (box.width * box.height) / (image.width * image.height * 0.22));
      const confidence = detection.detection.score || 0.75;
      const sizeScore = Math.min(1, Math.max(0.2, Math.max(image.width, image.height) / 1200));
      return Math.round(faceRatio * 42 + confidence * 42 + sizeScore * 16);
    }

    function analyzeDetection(detection, image) {
      const points = detection.landmarks.positions;
      const noseTip = points[30];
      const leftJaw = points[0];
      const rightJaw = points[16];
      const leftDistance = pointDistance(noseTip, leftJaw);
      const rightDistance = pointDistance(noseTip, rightJaw);
      const symmetry = Math.max(0, Math.min(100, (1 - Math.abs(leftDistance - rightDistance) / Math.max(leftDistance, rightDistance)) * 100));
      const smile = Math.max(0, Math.min(100, (detection.expressions.happy || 0) * 100));
      const quality = qualityScore(detection, image);
      const score = Math.round(symmetry * 0.5 + smile * 0.2 + quality * 0.3);
      return {
        points,
        box: detection.detection.box,
        symmetry,
        smile,
        quality,
        score: Math.max(0, Math.min(100, score))
      };
    }

    function drawOverlay(data, scale) {
      ctx.strokeStyle = '#0f9f7a';
      ctx.lineWidth = 2;
      ctx.strokeRect(data.box.x * scale, data.box.y * scale, data.box.width * scale, data.box.height * scale);
      ctx.fillStyle = '#e94d8a';
      data.points.forEach((point, index) => {
        if (index % 2 !== 0) return;
        ctx.beginPath();
        ctx.arc(point.x * scale, point.y * scale, 2, 0, Math.PI * 2);
        ctx.fill();
      });
      ctx.fillStyle = 'rgba(32, 36, 38, 0.78)';
      ctx.fillRect(14, 14, 190, 68);
      ctx.fillStyle = '#ffffff';
      ctx.font = '700 16px system-ui, sans-serif';
      ctx.fillText('AI顔診断', 28, 40);
      ctx.font = '800 26px system-ui, sans-serif';
      ctx.fillText(`Score ${data.score}`, 28, 70);
    }

    function scoreSummary(score) {
      if (score >= 82) return ['かなり安定した写真です', '左右バランス、表情、写真品質がそろっています。同じ条件で数枚試すと、より信頼しやすい傾向が見えます。'];
      if (score >= 68) return ['良い印象の写真です', '全体として見やすく、顔の特徴も検出しやすい写真です。照明や角度を整えるとさらに安定します。'];
      if (score >= 52) return ['標準的な参考結果です', '写真条件によって結果が変わりやすい範囲です。正面、明るさ、顔の大きさを少し調整してみてください。'];
      return ['写真条件を変えると改善しやすいです', '暗さ、角度、顔の小ささ、ブレが影響している可能性があります。明るい場所で正面に近い写真をお試しください。'];
    }

    function renderResults(data, faceCount) {
      currentScore = data.score;
      const [title, detail] = scoreSummary(data.score);
      els.scoreValue.textContent = data.score;
      els.resultSummary.textContent = `${title}。${detail}`;
      els.symmetryValue.textContent = `${data.symmetry.toFixed(1)}%`;
      els.smileValue.textContent = `${data.smile.toFixed(1)}%`;
      els.qualityValue.textContent = `${data.quality}%`;
      els.facesValue.textContent = `${faceCount}人`;
      els.results.classList.remove('hidden');
      els.resetBtn.disabled = false;
    }

    async function handleFile(file) {
      resetUi();
      const validationMessage = validateFile(file);
      if (validationMessage) {
        showMessage(validationMessage, true);
        return;
      }

      try {
        setStatus('画像を読み込んでいます...', 15);
        const image = await readImage(file);
        const scale = drawImageScaled(image);

        setStatus('AIモデルを準備しています...', 38);
        await ensureModels();

        setStatus('顔を検出しています...', 62);
        const detections = await faceapi.detectAllFaces(image)
          .withFaceLandmarks()
          .withFaceExpressions();

        if (!detections.length) {
          throw new Error('顔を検出できませんでした。顔が正面に近く、明るい写真を選んでください。');
        }

        if (detections.length > 1) {
          showMessage(`複数の顔を検出しました。一番大きく写っている顔を解析しています。検出数: ${detections.length}人`);
        }

        setStatus('参考スコアを計算しています...', 86);
        const target = getLargestDetection(detections);
        const result = analyzeDetection(target, image);
        drawOverlay(result, scale);
        renderResults(result, detections.length);
        setStatus('完了しました。', 100);
        window.setTimeout(hideStatus, 500);
      } catch (error) {
        hideStatus();
        showMessage(error.message || '解析中にエラーが発生しました。別の写真をお試しください。', true);
      }
    }

    els.chooseFile.addEventListener('click', () => els.fileInput.click());
    els.openCamera.addEventListener('click', () => els.cameraInput.click());
    els.resetBtn.addEventListener('click', resetUi);
    els.fileInput.addEventListener('change', (event) => handleFile(event.target.files[0]));
    els.cameraInput.addEventListener('change', (event) => handleFile(event.target.files[0]));

    els.dropZone.addEventListener('click', () => els.fileInput.click());
    els.dropZone.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        els.fileInput.click();
      }
    });
    els.dropZone.addEventListener('dragover', (event) => {
      event.preventDefault();
      els.dropZone.classList.add('is-active');
    });
    els.dropZone.addEventListener('dragleave', () => {
      els.dropZone.classList.remove('is-active');
    });
    els.dropZone.addEventListener('drop', (event) => {
      event.preventDefault();
      els.dropZone.classList.remove('is-active');
      handleFile(event.dataTransfer.files[0]);
    });

    els.downloadBtn.addEventListener('click', () => {
      const link = document.createElement('a');
      link.href = els.canvas.toDataURL('image/jpeg', 0.9);
      link.download = `ai-face-score-${currentScore || 'result'}.jpg`;
      document.body.appendChild(link);
      link.click();
      link.remove();
    });

    els.shareBtn.addEventListener('click', () => {
      const text = encodeURIComponent(`AI顔診断で参考スコアは${currentScore || '--'}点でした。写真の印象バランスをチェックできます。`);
      const url = encodeURIComponent('https://face-score.net/');
      window.open(`https://twitter.com/intent/tweet?text=${text}&url=${url}`, '_blank', 'noopener,noreferrer');
    });
  </script>
<script src="/site.js?v=20260415-seo-meta2"></script>
</body>
</html>
