import os
import re

replacements_contact = {
    'Contact Face Score AI | Support, Corrections, Privacy, and Tool Bugs': '顔スコアAI お問い合わせ | サポート、修正、プライバシー、バグ報告',
    'Contact Face Score AI for support, page corrections, privacy questions, bug reports, and responsible tool feedback.': 'サポート、ページの修正、プライバシーに関する質問、バグ報告、および責任あるツールへのフィードバックについては、顔スコアAIにお問い合わせください。',
    'Trust and usability guide': '信頼性と操作性のガイド',
    'Contact Face Score AI: Support, Corrections, Privacy, and Tool Bugs': '顔スコアAI お問い合わせ：サポート、修正、プライバシー、およびツールのバグ',
    'Use this page to contact us about tool issues, content corrections, privacy questions, or feedback about safer face-analysis experiences.': 'ツールの問題、コンテンツの修正、プライバシーに関する質問、またはより安全な顔分析体験に関するフィードバックについては、このページからお問い合わせください。',
    'Contact helper': 'お問い合わせヘルパー',
    'Choose the Right Contact Topic': '適切なお問い合わせトピックの選択',
    'Topic': 'トピック',
    'Tool bug': 'ツールのバグ',
    'Privacy question': 'プライバシーに関する質問',
    'Content correction': 'コンテンツの修正',
    'Business or media': 'ビジネスまたはメディア',
    'Message summary': 'メッセージの要約',
    'Write the short version of your request': 'リクエストの短い要約を書いてください',
    'Prepare message': 'メッセージを準備',
    'Select a topic and write a short summary before contacting support.': 'サポートに連絡する前に、トピックを選択し、短い要約を書いてください。',
    'How To Contact Us': 'お問い合わせ方法',
    'For support, corrections, privacy questions, or tool issues, email support@face-score.net. Clear messages help us respond faster, especially when the issue involves a specific page, browser, upload step, or result screen.': 'サポート、修正、プライバシーに関する質問、またはツールの問題については、support@face-score.net までメールでお問い合わせください。特に問題が特定のページ、ブラウザ、アップロード手順、または結果画面に関連している場合は、明確なメッセージをいただくと迅速に対応できます。',
    'What To Include': '含めるべき内容',
    'Please include the page URL, what you expected, what happened, and whether the issue appears on desktop, mobile, or both. Do not send sensitive face images unless we specifically request a safe example.': 'ページのURL、期待したこと、実際に起こったこと、および問題がデスクトップ、モバイル、またはその両方で発生するかどうかを記載してください。安全な例を特にリクエストしない限り、個人的な顔画像を送信しないでください。',
    'Content Corrections': 'コンテンツの修正',
    'If a guide is unclear or overstates what AI can do, tell us which sentence needs review. We prioritize corrections involving privacy, safety, medical/legal interpretation, and misleading accuracy claims.': 'ガイドが不明確であったり、AIができることを誇張している場合は、どの文を見直す必要があるかをお知らせください。プライバシー、安全性、医学的/法的解釈、および誤解を招く精度の主張を含む修正を優先します。',
    'Privacy Requests': 'プライバシーに関するリクエスト',
    'For privacy questions, describe the tool used and the approximate date. Avoid sending identity documents through normal email.': 'プライバシーに関する質問については、使用したツールとだいたいのユーザーご利用日を説明してください。通常の電子メールで身分証明書を送信することは避けてください。',
    'Bug Reports': 'バグ報告',
    'If a tool button does not work, a preview image does not appear, or a language URL behaves strangely, send the page URL and the browser you used. A screenshot can help, but please avoid sending sensitive face images unless absolutely necessary.': 'ツールのボタンが機能しない、プレビュー画像が表示されない、またはURLが異常に動作する場合は、ページのURLと使用したブラウザを送信してください。スクリーンショットは役に立ちますが、絶対に必要でない限り、個人的な顔画像を送信しないでください。',
    'Content Feedback': 'コンテンツフィードバック',
    'We welcome feedback when a page feels unclear, too robotic, too repetitive, or too confident about AI. Good face-analysis content should explain uncertainty in plain language.': 'ページが不明確、機械的すぎる、反復的すぎる、またはAIについて自信を持ちすぎていると感じた場合のフィードバックを歓迎します。優れた顔分析コンテンツは、不確実性をわかりやすい言葉で説明するべきです。',
    'If you notice a page where the tool does not match the title, mention that. We prioritize mismatches because they hurt both trust and SEO.': 'ツールがタイトルと一致しないページに気付いた場合は、それについて言及してください。不一致は信頼とSEOの両方を損なうため、優先的に対応します。',
    'Privacy and Safety Questions': 'プライバシーと安全に関する質問',
    'If your question involves privacy, include the page name and the action you took. Do not include government IDs, private photos, or another person\\\'s personal information in the first email.': 'プライバシーに関する質問の場合は、ページ名と実行したアクションを含めてください。最初のメールに、政府発行の身分証明書、プライベートな写真、または他人の個人情報を含めないでください。',
}

replacements_about = {
    'About Face Score AI | Purpose, Privacy, and Responsible Face Analysis': '顔スコアAIの概要 | 目的、プライバシー、および責任ある顔分析',
    'Learn what Face Score AI is for, how face analysis tools should be interpreted, privacy expectations, and responsible use.': '顔スコアAIの目的、顔分析ツールの解釈方法、プライバシーの期待事項、および責任ある使用について学びます。',
    'Trust and usability guide': '信頼性と操作性のガイド',
    'About Face Score AI: Purpose, Privacy, and Responsible Face Analysis': '顔スコアAIについて：目的、プライバシー、および責任ある顔分析',
    'Face Score AI helps people understand photo-based face analysis without turning a number into a judgment. This page explains what the site does, how to read scores, and where the limits are.': '顔スコアAIは、数値を判断基準にすることなく、写真ベースの顔分析を理解するのに役立ちます。このページでは、サイトの機能、スコアの読み方、および限界について説明します。',
    'Trust checker': '信頼チェッカー',
    'Can You Trust This Face Score Page?': 'この顔スコアページを信頼できますか？',
    'What are you checking?': '何をチェックしていますか？',
    'How the tool works': 'ツールの仕組みについて',
    'Privacy and upload safety': 'プライバシーとアップロードの安全性',
    'Accuracy limits': '精度の限界について',
    'Who writes the content': 'コンテンツの執筆者について',
    'Your concern': 'ご関心事項',
    'Example: Does the score judge my real attractiveness?': '例：スコアは私の本当の魅力を判断しますか？',
    'Get guidance': 'ガイダンスを取得する',
    'Choose a concern to get a practical trust reminder.': '実際的な信頼性のアドバイスを得るために、ご関心事項を選択してください。',
    'What Face Score AI Is For': '顔スコアAIの利用目的',
    'Face Score AI is a collection of face-analysis, photo-quality, attractiveness-estimate, facial symmetry, golden ratio, and comparison tools. The goal is practical feedback: better lighting, clearer selfies, more consistent inputs, and a calmer way to understand scores.': '顔スコアAIは、顔分析、写真品質、魅力度推定、顔の左右対称性、黄金比、および比較ツールのコレクションです。その目的は、より良い照明、より鮮明な自撮り写真、より一貫性のある入力など、スコアをより落ち着いて理解するための実用的なフィードバックを提供することです。',
    'The site should not be used to decide a person\\\'s worth. A face score is a model output from one image, shaped by light, angle, expression, image clarity, and tool design. It can help you choose a better profile photo, but it cannot measure personality, confidence, kindness, voice, movement, or real-world chemistry.': 'このサイトを人の価値を決めるために使用するべきではありません。顔スコアは、光、角度、表情、画像の鮮明さ、そしてツールの設計によって形成される、1枚の画像からのモデル出力です。より良いプロフィール写真を選ぶのには役立ちますが、性格、自信、優しさ、声、動き、または現実世界の相性を測定することはできません。',
    'How We Keep the Site Useful': 'サイトを有用に保つための取り組み',
    'Every serious page should explain what the tool reads, what changes the result, and what the result cannot know. We avoid language that turns a photo estimate into a personal verdict. The healthiest use is comparison under similar conditions, not obsessive retesting.': 'すべての専門的なページでは、ツールが何を読み取るか、何が結果を変えるか、そして結果が知ることができないことを説明するべきです。私たちは、写真の推定値を個人的な判断に変えるような表現を避けます。最も健康的な使用法は、強迫的に再テストすることではなく、類似した条件下での比較です。',
    'Our guides also separate entertainment tools from practical tools. A random score generator is playful; a photo rating tool is a structured estimate; an accuracy guide explains why neither should be treated as final truth.': 'ガイドでは、エンターテインメントツールと実用的なツールも区別しています。ランダムなスコアジェネレーターは遊び心があります。写真評価ツールは構造化された推定です。精度ガイドは、どちらも最終的な真実として扱われるべきではない理由を説明しています。',
    'Our Story': '私たちのストーリー',
    'Face Score AI started as a small browser-based experiment for explaining why the same person can look different across two photos. Early users were not only asking for a score; they wanted to know why lighting, camera distance, expression, and image clarity changed the result.': '顔スコアAIは、同じ人が2枚の写真で異なるように見える理由を説明するための小さなブラウザベースの実験として始まりました。初期のユーザーはスコアを求めているだけでなく、照明、カメラの距離、表情、画像の鮮明さが結果を変える理由を知りたがっていました。',
    'That history still shapes the site. We publish tools and guides together because a number without context can be confusing. The goal is to help people make better photo choices while keeping the experience calm, transparent, and realistic.': 'その歴史は今でもサイトを形成しています。コンテキストのない数値は混乱を招く可能性があるため、ツールとガイドを一緒に公開しています。私たちの目標は、落ち着いた、透明性があり、現実的な体験を保ちながら、人々がより良い写真の選択をするのを助けることです。',
    'Who We Are': '私たちについて',
    'We are a small editorial and engineering team focused on practical face-analysis education. Our work combines frontend development, image-quality testing, accessibility checks, SEO review, and plain-language writing.': '私たちは、実用的な顔分析教育に焦点を当てた、小規模な編集およびエンジニアリングチームです。私たちの仕事は、フロントエンド開発、画像品質のテスト、アクセシビリティのチェック、SEOレビュー、そしてわかりやすい文章の執筆を兼ね備えています。',
    'The team does not present face scores as personal judgments. We review pages for privacy language, consent reminders, photo-quality guidance, and clear limits before treating a tool page as complete.': 'チームは顔スコアを個人的な判断として提示しません。ツールページを完了したものとして扱う前に、プライバシーに関する文言、同意の通知、写真品質のガイダンス、および明確な制限についてページをレビューします。',
    'What We Do': '私たちの活動',
    'We build lightweight face-related tools, maintain guides about accuracy and limitations, and update content when users ask better questions. The site covers topics such as facial symmetry, photo face rating, AI face analysis, golden ratio analysis, age estimation, and selfie quality.': '軽量な顔関連ツールを構築し、精度と制限に関するガイドを維持し、ユーザーからより良い質問が寄せられたときにコンテンツを更新します。このサイトでは、顔の左右対称性、写真の顔評価、AI顔分析、黄金比の分析、年齢推定、自撮りの品質などのトピックを取り上げています。',
    'We also maintain editorial guidelines, an HTML sitemap, RSS updates, and contact channels so users and reviewers can understand how the site is organized and how to reach us.': 'また、ユーザーやレビュアーがサイトの構成と連絡方法を理解できるように、編集ガイドライン、HTMLサイトマップ、RSS更新、および連絡先チャネルを維持および管理しています。',
    'Team Photos in Workspace': 'ワークスペースのチーム写真',
    'Our workspace materials focus on product screenshots, tool previews, and visual examples rather than personal staff portraits. This keeps the site centered on user education and avoids turning team images into unnecessary trust decoration.': '私たちのワークスペースの資料は、個人のスタッフの肖像画ではなく、製品のスクリーンショット、ツールのプレビュー、および視覚的な例に焦点を当てています。これにより、サイトはユーザー教育を中心とし、チームの画像を不必要な信頼の飾りに変えることを防ぎます。',
    'Workspace tool preview': 'ワークスペースツールのプレビュー',
    'Photo rating workspace': '写真評価ワークスペース',
    'AI analysis workspace': 'AI分析ワークスペース',
    'Team review process': 'チームレビュープロセス',
    'Featured Websites Linked': '注目のウェブサイトのリンク',
    'For transparency, we link to our own core resources from the footer and sitemap rather than hiding important pages deep in the site. Useful starting points include the editorial guidelines, privacy policy, accuracy guide, HTML sitemap, and RSS feed.': '透明性を確保するため、重要なページをサイトの奥深くに隠すのではなく、フッターとサイトマップから自社のコアリソースにリンクしています。有用な出発点として、編集ガイドライン、プライバシーポリシー、精度ガイド、HTMLサイトマップ、RSSフィードなどがあります。',
    'Editorial Guidelines': '編集ガイドライン',
    'HTML Sitemap': 'HTMLサイトマップ',
    'RSS Feed': 'RSSフィード',
    'Contact Page': 'お問い合わせページ',
    'Privacy and Upload Expectations': 'プライバシーとアップロードの期待',
    'Face images are sensitive. Pages with upload tools should explain whether the image is used for preview, browser-side analysis, or server-side processing. Users should avoid uploading someone else\\\'s face without consent, especially children, identity documents, or private images.': '顔画像は機密性が高いものです。アップロードツールのあるページでは、画像がプレビューに使用されるのか、ブラウザ側での分析に使用されるのか、それともサーバー側での処理に使用されるのかを説明する必要があります。ユーザーは、同意なしに他人の顔、特に子供、身分証明書、または個人的な画像をアップロードすることを避けるべきです。',
    'What To Read Next': '次に読むべき記事',
    'How Face Score Works': '顔スコアの仕組み',
    'Accuracy and Limitations': '精度と限界',
    'Privacy Policy': 'プライバシーポリシー',
    'What Makes Our Tools Different': '私たちのツールの違い',
    'Many face-score pages on the web show a number and leave users to guess what it means. We try to pair each score with interpretation: what the image quality was like, what visible factors may have influenced the result, and what should not be inferred from it.': 'ウェブ上の多くの顔スコアページは、数値を表示し、その意味をユーザーに推測させます。私たちは、各スコアに解釈を付け加えるように努めています：写真の品質がどうであったか、結果に影響を与えた目に見える要因は何か、そして数値から推測すべきではないことは何か。',
    'The strongest pages on this site are built around user intent. Someone searching for a selfie guide needs practical camera advice. Someone using a face comparison tool needs consent and accuracy warnings. Someone reading about attractiveness needs humane language, not pressure.': 'このサイトで最も強力なページは、ユーザーの意図に基づいて構築されています。自撮りガイドを探している人には、実用的なカメラのアドバイスが必要です。顔比較ツールを使用している人には、同意と精度の警告が必要です。魅力について読んでいる人には、プレッシャーではなく、人間味のある言葉が必要です。',
    'How To Use Results Without Overthinking': '考えすぎずに結果を使用する方法',
    'Use one result as a clue and multiple results as a pattern. If a score changes when lighting improves, the lesson is about the photo setup, not your face changing. The most useful action is usually retaking the image with better light, distance, and expression.': '1つの結果をヒントとして使用し、複数の結果をパターンとして使用してください。照明が改善したときにスコアが変わる場合、その教訓はあなたの顔が変わることではなく、写真のセットアップに関するものです。最も役立つアクションは通常、より良い光、距離、表情で画像を取り直すことです。',
    'If a result feels upsetting, stop testing. The tool is not worth more than your confidence. Read the accuracy guide before treating any number as meaningful.': '結果に動揺を感じた場合は、テストを中止してください。あなたの自信を損なうツールであれば利用する価値はありません。数字を意味のあるものとして扱う前に、精度ガイドをご一読ください。',
    'Site Improvement Priorities': 'サイト改善の優先事項',
    'Keep tool labels honest.': 'ツールのラベルを正直に保つ。',
    'Add privacy notes near upload areas.': 'アップロード領域の近くにプライバシーに関するメモを追加する。',
    'Explain limits before showing strong claims.': '強い主張を示す前に限界を説明する。',
    'Use human copy instead of keyword stuffing.': 'キーワードの詰め込みの代わりに、自然な人間の文章を使用する。',
    'Improve weak pages based on user questions.': 'ユーザーの質問に基づいて弱いページを改善する。',
}

replacements_common = {
    '"Strong setup. This page gives enough context for a confident next step."': '"強力なセットアップです。このページは、自信を持って次のステップに進むための十分なコンテキストを提供します。"',
    '"Good starting point. Add one more detail or read the related guide before acting."': '"良い出発点です。行動する前にもう1つ詳細を追加するか、関連するガイドを読んでください。"',
    '"Needs more context. Use the checklist above and avoid relying on a single score or short answer."': '"より多くのコンテキストが必要です。上記のチェックリストを使用し、単一のスコアや短い回答に頼らないようにしてください。"'
}

for filename, specific_dict in [("contact.html", replacements_contact), ("about.html", replacements_about)]:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # We rebuild the target mapping using regex to replace regardless of line breaks.
    # Replace all newlines with spaces temporarily to easily run regex.
    # actually, using a regex with \s+ is cleaner.
    for k, v in {**replacements_common, **specific_dict}.items():
        # Escape k for regex but allow variable whitespaces
        pattern = re.escape(k).replace(r'\ ', r'\s+')
        html = re.sub(pattern, v, html, flags=re.MULTILINE|re.IGNORECASE)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
