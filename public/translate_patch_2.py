import re

translations = {
    'sitemap.html': [
        ('Face Attractiveness Test', '顔の魅力度テスト'),
        ('Photo Face Rating', '写真顔評価'),
        ('AI Face Analysis', 'AI顔分析'),
        ('Face Comparison Tool', '顔比較ツール'),
        # To fix the 'Attractiveness TestPhoto' joined string caused by Prettier parsing html with missing spaces:
        # Actually it's probably just these 4 anchor texts in sitemap.html
    ],
    'face-symmetry-guide.html': [
        ('Cleveland Clinic', 'クリーブランド・クリニック'),
        ('American Association of Orthodontists', '米国矯正歯科学会'),
    ]
}

for filename, fixes in translations.items():
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    for eng, jp in fixes:
        pattern = re.compile(re.escape(eng), re.IGNORECASE)
        content = re.sub(pattern, jp, content)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
