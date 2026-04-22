"""Apply performance-oriented head/media changes to all inner pages under public/."""
import json
import re
from pathlib import Path

public = Path(__file__).resolve().parent.parent / "public"

OLD_CSS = """  <link rel="stylesheet" href="style-core.min.css" media="print" onload="this.media='all'">
  <link rel="stylesheet" href="style-pages.min.css" media="print" onload="this.media='all'">"""

NEW_CSS = """  <link rel="preconnect" href="https://www.youtube.com" crossorigin>
  <link rel="preconnect" href="https://i.ytimg.com" crossorigin>
  <link rel="dns-prefetch" href="https://www.youtube.com">
  <link rel="dns-prefetch" href="https://i.ytimg.com">
  <link rel="preload" href="style-core.min.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <link rel="preload" href="style-pages.min.css" as="style" onload="this.onload=null;this.rel='stylesheet'">"""

PICTURE_BLOCK = """      <figure class="content-illustration">
        <picture>
          <source type="image/avif" srcset="ganmen-hensachi-keyword.avif 1200w" sizes="(max-width: 720px) 100vw, 820px">
          <source type="image/webp" srcset="ganmen-hensachi-keyword-800.webp 800w, ganmen-hensachi-keyword.webp 1200w" sizes="(max-width: 720px) 100vw, 820px">
          <img class="content-illustration__img" src="ganmen-hensachi-keyword.svg" width="1200" height="630" loading="lazy" decoding="async" alt="\u9854\u9762\u504f\u5dee\u5024 \u30ac\u30a4\u30c9\u753b\u50cf">
        </picture>
      </figure>"""

IFRAME_RE = re.compile(
    r'<div class="video-wrap">\s*'
    r'<iframe src="https://www\.youtube\.com/embed/([^"]+)" title="([^"]*)"[^>]*></iframe>\s*'
    r"</div>",
    re.DOTALL,
)


def merge_ld_json(html: str) -> str:
    scripts = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', html, flags=re.DOTALL
    )
    if len(scripts) != 2:
        return html
    g = [json.loads(scripts[0]), json.loads(scripts[1])]
    for node in g:
        node.pop("@context", None)
    merged = json.dumps(
        {"@context": "https://schema.org", "@graph": g}, ensure_ascii=False
    )
    return re.sub(
        r'<script type="application/ld\+json">.*?</script>\s*'
        r'<script type="application/ld\+json">.*?</script>',
        f'<script type="application/ld+json">{merged}</script>',
        html,
        count=1,
        flags=re.DOTALL,
    )


def replace_video_facade(html: str) -> str:
    def repl(m: re.Match) -> str:
        vid, title = m.group(1), m.group(2)
        return (
            f'<div class="video-wrap yt-facade" data-yt="{vid}" data-title="{title}">\n'
            f'        <button type="button" class="yt-facade__btn" aria-label="{title}を再生">\n'
            f'          <img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" width="480" height="360" loading="lazy" decoding="async" fetchpriority="low">\n'
            f'          <span class="yt-facade__play" aria-hidden="true"></span>\n'
            f"        </button>\n"
            f"      </div>"
        )

    return IFRAME_RE.sub(repl, html, count=1)


def replace_img_picture(html: str) -> str:
    old = re.compile(
        r"<p><img src=\"ganmen-hensachi-keyword\.svg\"[^>]*></p>",
        re.DOTALL,
    )
    return old.sub(PICTURE_BLOCK, html, count=1)


def patch_file(path: Path) -> None:
    t = path.read_text(encoding="utf-8")
    if OLD_CSS not in t:
        return
    t = merge_ld_json(t)
    t = t.replace(OLD_CSS, NEW_CSS, 1)
    t = replace_video_facade(t)
    t = replace_img_picture(t)
    path.write_text(t, encoding="utf-8")


def main() -> None:
    for p in sorted(public.glob("*.html")):
        if p.name == "index.html":
            continue
        patch_file(p)
        print("upgraded", p.name)


if __name__ == "__main__":
    main()
