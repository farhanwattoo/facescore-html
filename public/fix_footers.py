import os
import re
from bs4 import BeautifulSoup

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    changed = False

    # Replace footer with Japanese only footer
    footer = soup.find('footer', class_='site-footer')
    if footer:
        jp_footer = """<footer class="site-footer">
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
    <form id="site-search-form" class="footer-search" role="search" action="/sitemap.html">
      <label for="site-search-input">顔スコアAIのツールとガイドを検索</label>
      <input id="site-search-input" name="q" type="search" placeholder="ツール、ガイド、ポリシーを検索" aria-label="顔スコアAIを検索">
      <button type="submit">検索</button>
    </form>
    <div class="footer-trust">
      <div class="footer-contact">
        <span>Email: <a href="mailto:support@face-score.net">support@face-score.net</a></span>
        <span>Phone: <a href="tel:+14155550198">+1 (415) 555-0198</a></span>
      </div>
      <div class="footer-social" aria-label="ソーシャルメディアリンク">
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
</footer>"""
        new_footer = BeautifulSoup(jp_footer, 'html.parser').footer
        # Let's replace only if it differs significantly
        if str(footer) != str(new_footer):
            footer.replace_with(new_footer)
            changed = True

    if changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Footer fixed: {file_path}")

directory = '.'
for root, dirs, files in os.walk(directory):
    for name in files:
        if name.endswith('.html') or name.endswith('.php'):
            process_file(os.path.join(root, name))
print("Footer fix done")
