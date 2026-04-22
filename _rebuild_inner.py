from pathlib import Path

base = Path(r"C:\Users\farhan.atif\Desktop\tools website\ai-face-detection-system\facescore-html\public")

pages = {
    "how-it-works.html": ("顔面偏差値診断の仕組み", "AI顔診断の処理フローと指標の見方を解説", "アップロード画像から顔ランドマークを抽出し、左右対称性・表情・推定年齢などを参考値として表示します。結果は比較用途の指標です。"),
    "accuracy-limitations.html": ("精度と限界", "AI顔診断の精度条件と誤差要因", "照明・角度・画質・フィルターで結果は変動します。単一スコアではなく、同条件での複数比較で傾向を確認してください。"),
    "about.html": ("当サイトについて", "運営方針・編集体制・信頼性情報", "当サイトはFace Score Media Labが運営し、一次情報確認と公開前レビューを行った上でコンテンツを提供します。"),
    "contact.html": ("お問い合わせ", "連絡先とサポート窓口", "ご質問や修正依頼はメールで受け付けています。内容確認後、順次返信いたします。"),
    "face-symmetry-guide.html": ("左右対称性ガイド", "顔面偏差値における左右対称性の見方", "左右対称性は顔ランドマークの距離差から推定されます。撮影条件を揃えると比較精度が上がります。"),
    "golden-ratio-face.html": ("黄金比と顔分析", "黄金比の考え方とAI診断での扱い", "黄金比は参考概念のひとつであり、単独で魅力を決めるものではありません。複数指標を合わせて解釈してください。"),
    "facial-landmarks-explained.html": ("顔ランドマーク解説", "AI顔認識で使われる基準点", "目・鼻・口・輪郭の座標点を使って幾何特徴を分析します。ランドマーク品質が推定結果の安定性に直結します。"),
    "smile-expression-analysis.html": ("笑顔・表情分析", "笑顔強度と感情ラベルの見方", "笑顔強度は視覚特徴に基づく推定値です。感情の真実を断定するものではなく、比較目的で活用してください。"),
    "age-estimation-ai.html": ("AI年齢推定", "年齢推定の誤差と正しい解釈", "AI年齢推定は近似値です。メイク・照明・画質で変動するため、重要判断への利用は推奨されません。"),
    "selfie-photo-quality-guide.html": ("自撮り品質ガイド", "顔面偏差値診断に適した撮影条件", "正面・均一光・高解像度・無加工に近い写真ほど、ランドマークが安定して比較しやすい結果が得られます。"),
    "team.html": ("運営チーム", "編集・開発・品質レビュー体制", "運営チームは編集担当、開発担当、品質レビュー担当で構成され、継続的な改善と安全運用を行っています。"),
    "editorial-guidelines.html": ("編集ガイドライン", "公開品質と更新ルール", "一次情報確認、誇張表現の抑制、公開前レビュー、修正反映のフローを明文化しています。"),
    "sitemap.html": ("HTMLサイトマップ", "サイト内ページの一覧", "主要ページへの導線を一覧化し、ユーザーと検索エンジンの回遊性を高めています。"),
    "privacy.html": ("プライバシーポリシー", "データ取り扱い方針", "画像・アクセス情報の取り扱い方針を公開し、利用者が安心して確認できるようにしています。"),
    "terms.html": ("利用規約", "サービス利用条件", "本サービスの利用条件、禁止事項、免責事項を定め、透明な運用基準を示しています。"),
}

for file, (h1, subtitle, intro) in pages.items():
    title = f"{h1} | 顔面偏差値診断"
    desc = f"{h1}ページ。{subtitle}を分かりやすくまとめたガイド。"
    url = f"https://face-score.net/{file}"

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <link rel="stylesheet" href="style-core.min.css" media="print" onload="this.media='all'">
  <link rel="stylesheet" href="style-pages.min.css" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="style-core.min.css"><link rel="stylesheet" href="style-pages.min.css"></noscript>
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{url}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"ホーム","item":"https://face-score.net/"}},{{"@type":"ListItem","position":2,"name":"{h1}","item":"{url}"}}]}}</script>
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"顔面偏差値とは何ですか？","acceptedAnswer":{{"@type":"Answer","text":"顔面偏差値は、AIが顔特徴量を分析して表示する参考指標です。"}}}},{{"@type":"Question","name":"結果はどのように解釈すべきですか？","acceptedAnswer":{{"@type":"Answer","text":"単一結果ではなく同条件の複数画像で比較し、傾向を確認してください。"}}}}]}}</script>
</head>
<body class="inner-page">
  <nav class="navbar">
    <div class="nav-container">
      <a href="/" class="nav-logo">顔面偏差値診断</a>
      <ul class="nav-links">
        <li><a href="/">ホーム</a></li>
        <li><a href="how-it-works.html">仕組み</a></li>
        <li><a href="accuracy-limitations.html">精度と限界</a></li>
        <li><a href="about.html">運営情報</a></li>
      </ul>
    </div>
  </nav>

  <main class="container page-content professional-inner">
    <h1>{h1} - 顔面偏差値ガイド</h1>
    <p class="lead">{intro}</p>

    <section class="trust-section">
      <h2>目次</h2>
      <ul>
        <li><a href="#definition">定義</a></li>
        <li><a href="#tips">活用ポイント</a></li>
        <li><a href="#table">比較表</a></li>
        <li><a href="#video">解説動画</a></li>
      </ul>
    </section>

    <section class="trust-section" id="definition">
      <h2>顔面偏差値とは</h2>
      <p><strong>顔面偏差値</strong>は、顔の幾何特徴や表情の傾向をAIで分析し、比較可能な参考値として表示するための指標です。絶対評価ではなく、同条件での比較に適しています。</p>
    </section>

    <section class="trust-section" id="tips">
      <h2>活用ポイント</h2>
      <h3>1. 撮影条件を揃える</h3>
      <p>照明、角度、距離を揃えることで、再現性の高い比較ができます。</p>
      <h3>2. 加工を抑える</h3>
      <p>強いフィルター加工はランドマーク検出の安定性を下げることがあります。</p>
    </section>

    <section class="trust-section" id="table">
      <h2>比較表</h2>
      <table>
        <thead><tr><th>項目</th><th>推奨</th><th>注意</th></tr></thead>
        <tbody>
          <tr><td>照明</td><td>均一な光</td><td>逆光</td></tr>
          <tr><td>角度</td><td>正面</td><td>極端な横向き</td></tr>
          <tr><td>画質</td><td>高解像度</td><td>強圧縮</td></tr>
        </tbody>
      </table>
    </section>

    <section class="trust-section" id="video">
      <h2>解説動画</h2>
      <div class="video-wrap">
        <iframe src="https://www.youtube.com/embed/2Vv-BfVoq4g" title="{h1} 解説動画" loading="lazy" allowfullscreen></iframe>
      </div>
      <p><img src="ganmen-hensachi-keyword.svg" width="1200" height="630" loading="lazy" decoding="async" style="max-width:100%;height:auto" alt="顔面偏差値 ガイド画像"></p>
    </section>

    <section class="trust-section">
      <h2>関連内部リンク</h2>
      <ul>
        <li><a href="/">ホーム</a></li>
        <li><a href="how-it-works.html">仕組みの解説</a></li>
        <li><a href="accuracy-limitations.html">精度と限界</a></li>
        <li><a href="contact.html">お問い合わせ</a></li>
      </ul>
    </section>
  </main>

  <footer class="site-footer">
    <div class="footer-content">
      <div class="footer-links">
        <a href="about.html">当サイトについて</a>
        <a href="team.html">運営チーム</a>
        <a href="editorial-guidelines.html">編集ガイドライン</a>
        <a href="privacy.html">プライバシーポリシー</a>
        <a href="terms.html">利用規約</a>
      </div>
      <p>連絡先: support@face-score.net</p>
    </div>
  </footer>

  <button id="back-to-top" class="back-to-top" aria-label="ページ上部へ戻る">Top</button>
  <script src="site.js" defer></script>
</body>
</html>
'''
    (base / file).write_text(html, encoding="utf-8")
    print("rebuilt", file)
