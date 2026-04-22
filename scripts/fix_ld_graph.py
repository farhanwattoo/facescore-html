"""Normalize @graph JSON-LD: single @context, strip nested @context."""
import json
import re
from pathlib import Path

public = Path(__file__).resolve().parent.parent / "public"


def fix_html(t: str) -> str:
    m = re.search(
        r'<script type="application/ld\+json">(\{"@context": "https://schema.org", "@graph":.*?\})</script>',
        t,
        flags=re.DOTALL,
    )
    if not m:
        return t
    data = json.loads(m.group(1))
    if "@graph" not in data:
        return t
    for node in data["@graph"]:
        node.pop("@context", None)
    out = json.dumps(data, ensure_ascii=False)
    return t[: m.start(1)] + out + t[m.end(1) :]


def main() -> None:
    for p in public.glob("*.html"):
        if p.name == "index.html":
            continue
        t = p.read_text(encoding="utf-8")
        t2 = fix_html(t)
        if t2 != t:
            p.write_text(t2, encoding="utf-8")
            print("fixed ld+json", p.name)


if __name__ == "__main__":
    main()
