import re

about_fixes = [
    (r"The site should not be used to decide a person's worth\. A face score[\s\S]*?real-world chemistry\.", "このサイトを人の価値を決めるために使用するべきではありません。顔スコアは、光、角度、表情、画像の鮮明さ、そしてツールの設計によって形成される、1枚の画像からのモデル出力です。より良いプロフィール写真を選ぶのには役立ちますが、性格、自信、優しさ、声、動き、または現実世界の相性を測定することはできません。"),
    (r"Face images are sensitive\. Pages with upload tools should explain[\s\S]*?private images\.", "顔画像は機密性が高いものです。アップロードツールのあるページでは、画像がプレビューに使用されるのか、ブラウザ側での分析に使用されるのか、それともサーバー側での処理に使用されるのかを説明する必要があります。ユーザーは、同意なしに他人の顔、特に子供、身分証明書、または個人的な画像をアップロードすることを避けるべきです。"),
    (r"Copyright © 2026 Face Score AI\. All rights reserved\.", "Copyright © 2026 顔スコアAI. All rights reserved.")
]

contact_fixes = [
    (r"For support, corrections, プライバシーに関する質問s, or tool issues, email[\s\S]*?result screen\.", "サポート、修正、プライバシーに関する質問、またはツールの問題については、support@face-score.net までメールでお問い合わせください。特に問題が特定のページ、ブラウザ、アップロード手順、または結果画面に関連している場合は、明確なメッセージをいただくと迅速に対応できます。"),
    (r"For プライバシーに関する質問s, describe the tool used and the approximate[\s\S]*?normal email\.", "プライバシーに関する質問については、使用したツールとだいたいのユーザーご利用日を説明してください。通常の電子メールで身分証明書を送信することは避けてください。"),
    (r"If your question involves privacy, include the page name and the[\s\S]*?first email\.", "プライバシーに関する質問の場合は、ページ名と実行したアクションを含めてください。最初のメールに、政府発行の身分証明書、プライベートな写真、または他人の個人情報を含めないでください。"),
    (r"Copyright © 2026 Face Score AI\. All rights reserved\.", "Copyright © 2026 顔スコアAI. All rights reserved.")
]

for filename, fixes in [('about.html', about_fixes), ('contact.html', contact_fixes)]:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    for pattern, replacement in fixes:
        html = re.sub(pattern, replacement, html)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
