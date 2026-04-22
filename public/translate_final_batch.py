import os, re
import glob

# For all files
common_translations = {
    '"inLanguage": "en"': '"inLanguage": "ja"',
    '"availableLanguage": ["English", "Japanese"]': '"availableLanguage": ["Japanese"]',
    '<html': '<html lang="ja"',
    '<a class="nav-logo" href="/">Face Score AI</a>': '<a class="nav-logo" href="/">顔スコアAI</a>',
    '<li><a href="/">Home</a></li>': '<li><a href="/">ホーム</a></li>',
    '<li><a href="how-it-works.html">How It Works</a></li>': '<li><a href="how-it-works.html">仕組み</a></li>',
    '<li><a href="accuracy-limitations.html">Accuracy</a></li>': '<li><a href="accuracy-limitations.html">精度</a></li>',
    '<li><a href="about.html">About</a></li>': '<li><a href="about.html">概要</a></li>',
    'Trust and usability guide': '信頼性と操作性のガイド',
    'Practical guide and tool': '実践ガイドとツール',
    'Quick quality checker': 'クイック品質チェッカー',
    'Check readiness': '準備状況を確認する',
    'Camera angle': 'カメラの角度',
    'Lighting quality': '照明の品質',
    'Light filter': '軽いフィルター',
    'Heavy filter': '強いフィルター',
    'Editing level': '編集レベル',
    'Upload image': '画像をアップロード',
    'Start analysis': '分析を開始',
    'Generate random score': 'ランダムスコアを生成',
    'Calculate harmony score': '調和スコアを計算',

    'Article Outline: What Will This Guide Cover?': '記事の流れ：このガイドで扱う内容',
    '3. Why does photo quality matter?': '3. なぜ写真の品質が重要なのか？',
    '4. Which settings improve results?': '4. どの設定が結果を改善するか？',
    '7. How should privacy be handled?': '7. プライバシーはどう扱うべきか？',
    '8. Can AI give useful recommendations?': '8. AIは役立つ推奨事項を提供できるか？',
    '9. How should results be interpreted?': '9. 結果はどう解釈されるべきか？',
    'Most Important Things to Remember': '覚えておくべき最も重要なこと',

    'This article is worth reading because it gives practical steps, explains limits, and helps you use the feature without overthinking the score.': 'この記事は、実践的な手順を提供し、限界を説明し、スコアについて考えすぎずに機能を使用するのに役立つため、読む価値があります。',
    'This section explains what the tool can reasonably read from one image and what it cannot know about a person. Use it as practical photo guidance, not as a permanent judgment.': 'このセクションでは、ツールが1枚の画像から合理的に読み取れることと、人について知ることができないことについて説明します。永続的な判断基準としてではなく、実用的な写真のガイダンスとして使用してください。',
    'A better result usually starts with a clearer input: soft light, a front-facing angle, visible facial features, and minimal editing. If the result feels surprising, retake the photo before drawing conclusions.': 'より良い結果は通常、より明確な入力から始まります：柔らかな光、正面からの角度、目に見える顔の特徴、そして最小限の編集。結果に驚いた場合は、結論を出す前に写真を撮り直してください。',
    'Photo quality changes most face-analysis results more than users expect. Blur, compression, shadows, filters, and extreme camera angles can all make a model less stable.': '写真の品質は、ユーザーが期待する以上にほとんどの顔分析結果を変化させます。ぼかし、圧縮、影、フィルター、極端なカメラの角度はすべて、モデルの安定性を低下させる可能性があります。',
    'The safest way to compare results is to use similar conditions each time. Keep the camera distance, lighting, expression, and crop consistent so the tool is reading the face rather than the setup.': '結果を比較する最も安全な方法は、毎回同じような条件を使用することです。カメラの距離、照明、表情、トリミングを一定に保ち、ツールがセットアップではなく顔を読み取るようにします。',
    'The score should be read as an estimate based on visible signals. It cannot measure personality, confidence, kindness, voice, movement, culture, or real-world chemistry.': 'スコアは、目に見えるシグナルに基づく推定値として読み取る必要があります。性格、自信、優しさ、声、動き、文化、現実世界の相性を測定することはできません。',
    'Use the feedback to choose a stronger photo, understand why one image works better than another, and avoid overthinking a single number.': 'フィードバックを使用して、より強力な写真を選択し、ある画像が別の画像よりもうまく機能する理由を理解し、1つの数字について考えすぎないようにします。',
    'Privacy matters because face images are personal. Users should know whether a photo is processed in the browser, uploaded to a server, stored, or deleted after analysis.': '顔画像は個人的なものであるため、プライバシーは重要です。ユーザーは、写真がブラウザで処理されるか、サーバーにアップロードされるか、保存されるか、または分析後に削除されるかを知っておく必要があります。',
    'Do not upload someone else without consent. For sensitive use cases such as identity, age verification, or medical decisions, use a qualified service rather than a casual web tool.': '同意なしに他の人をアップロードしないでください。身元確認、年齢確認、または医学的決定などの機密性の高いユースケースでは、カジュアルなウェブツールではなく、資格のあるサービスを使用してください。',
    'A useful result gives context, not only a number. It should explain confidence, likely input problems, and simple next steps such as improving light or reducing heavy filters.': '有用な結果は、単なる数値だけでなくコンテキストを提供します。信頼性、可能性のある入力の問題、および光の改善や強力なフィルターの削減などの簡単な次のステップを説明する必要があります。',
    'The goal is to make the page helpful even when the score is imperfect. Clear limitations build more trust than exaggerated claims.': '目標は、スコアが不完全な場合でもページを役立つものにすることです。明確な制限は、誇張された主張よりも多くの信頼を築きます。',
    
    'AI results are estimates, not final judgments.': 'AIの結果は推定値であり、最終的な判断ではありません。',
    'Keep privacy in mind before uploading images.': '画像をアップロードする前にプライバシーを念頭に置いてください。',
    'Compare results under similar conditions.': '類似の条件下で結果を比較します。',
    'Use the advice to improve photos, not to judge your worth.': '自分の価値を判断するためではなく、写真を改善するためにアドバイスを使用してください。',
    'Copyright © 2026 Face Score AI. All rights reserved.': 'Copyright © 2026 顔スコアAI. All rights reserved.',
    'Copyright © 2026 Face Score AI. All rights reserved.': 'Copyright © 2026 顔スコアAI. All rights reserved.',

    # Specific H1 Titles & Tool text templates
    'Age Estimation Using Artificial Intelligence: Estimate Facial Age, Face Age, and Legal Age Limits': '人工知能を使用した年齢推定：顔年齢、見た目年齢、および法的年齢制限の推定',
    'Age Estimation Photo Readiness Checker': '年齢推定の写真準備状況チェッカー',
    'Use this quick checker to see whether your photo setup is likely to produce a stable estimate.': 'このクイックチェッカーを使用して、写真のセットアップが安定した推定値を作成する可能性が高いかどうかを確認してください。',

    'AI Face Analyzer: Free AI Face Analysis App for Face Shape, Symmetry, Facial Features, and Looksmax Tips': 'AI顔分析アプリ：顔の形、左右対称性、顔の特徴、およびルックス向上のヒントのための無料AIツール',
    'An ai face analyzer can help you understand face shape, symmetry, facial features, and photo quality in a practical way.': 'AI顔分析アプリは、顔の形、左右対称性、顔の特徴、写真の品質を実践的な方法で理解するのに役立ちます。',
    'Upload and choose options to analyze your face.': '顔を分析するためのオプションをアップロードして選択します。',

    'This ai attractiveness test online free guide explains how a beauty score, face rating, and attractiveness scale should be understood.': 'この無料のオンラインAI魅力度テストガイドでは、美しさのスコア、顔の評価、魅力の尺度がどのように理解されるべきかを説明します。',

    'Facial Landmark Photo Readiness Checker': '顔のランドマーク写真準備状況チェッカー',
    'Facial Landmarks Explained: AI Facial Landmark Detection, Human Face Points, and Face Landmark Uses': '顔のランドマークの解説：AIの顔ランドマーク検出、人間の顔のポイント、顔ランドマークの用途',
    'Facial landmarks are key points on a face that help ai systems detect structure, expression, orientation, and movement.': '顔のランドマークは、AIシステムが構造、表情、向き、または動きを検出するのに役立つ顔の重要なポイントです。',

    'Golden Ratio Face Analyzer: AI Golden Ratio Face Calculator for Facial Features, Symmetry, and Ratio Score': '黄金比顔分析：顔の特徴、左右対称性、比率スコアのためのAI黄金比顔面計算ツール',
    'A golden ratio face calculator can make facial proportion easier to understand, but it should be used as a guide rather than a final beauty judgment.': '黄金比の顔計算ツールは、顔のプロポーションを理解しやすくしますが、最終的な美の判断ではなくガイドとして使用する必要があります。',
    'Upload a photo and calculate the sample harmony score.': '写真をアップロードし、サンプルの調和スコアを計算します。',
    'Golden Ratio Photo Readiness Checker': '黄金比写真準備状況チェッカー',

    'Random AI Face Score Generator: Free Online Pretty Scale AI, Beauty Score, and Face Rating Result': 'ランダムAI顔スコアジェネレーター：無料オンラインのプレティスケールAI、美容スコア、および顔評価結果',
    'Random Face Score Generator': 'ランダム顔スコアジェネレーター',
    'A random face score generator is for fun, not identity or worth. It can make a beauty score feel playful instead of serious.': 'ランダム顔スコアジェネレーターは、アイデンティティや自己価値のためではなく、楽しみのためのものです。美のスコアを深刻なものではなく遊び心のあるものに感じさせることができます。',
    'Upload a photo and generate a playful result.': '写真をアップロードして、遊び心のある結果を生成します。',

    'Selfie Tips Ultimate Guide: Take a Good Selfie with Lighting, Edit Choices, Front Camera Angles, and Flattering Selfie Poses': '自撮りのコツ究極ガイド：照明、編集の選択、フロントカメラの角度、魅力的な自撮りのポーズで良い自撮りを撮る',
    'Selfie Quality Checker': '自撮り品質チェッカー',
    'A good selfie is not luck. It comes from lighting, camera distance, a relaxed expression, selfie poses, camera settings, and small choices that flatter your face without making the photo feel fake.': '良い自撮り写真は運ではありません。それは、照明、カメラ距離、リラックスした表情、自撮りのポーズ、カメラ設定、および写真を不自然に感じさせることなく顔を美しく見せる小さな選択から生まれます。',

    'Smile Expression Analysis: Facial Movements, Genuine Smile, Posed Smile, Facial Feedback, and Attractiveness': '笑顔の表情分析：顔の動き、本物の笑顔、作られた笑顔、顔のフィードバック、および魅力',
    'Smile Photo Readiness Checker': '笑顔写真準備状況チェッカー',
    'A smile is a facial expression, a social signal, and sometimes an emotional expression. This guide explains what a smile may reveal and what it cannot prove.': '笑顔は、顔の表情であり、社会的シグナルであり、時には感情の表現でもあります。このガイドでは、笑顔が明らかにする可能性のあることと、証明できないことについて説明します。',
}

face_symmetry_translations = {
    'Facial Asymmetry and Facial Symmetry: What You Can Actually Do Before You Worry': '顔の非対称性と左右対称性：心配する前に実際にできること',
    'This guide is for the person who wants a clear answer without panic or sales pressure. You will learn what is normal, what is worth checking, which non-surgical habits and treatments may help, and when surgical methods belong in the conversation. The point is not to chase a perfectly mirrored face. It is to understand your options with a calmer eye.': 'このガイドは、パニックや販売圧力なしで明確な答えを求める人のためのものです。何が正常であるか、何をチェックする価値があるか、どの非外科的習慣や治療が役立つか、そして、どの段階で外科的な方法が会話に上るべきかを学びます。要点は、完全に鏡像のような顔を追いかけることではありません。より落ち着いた目で自分の選択肢を理解することです。',
    'Facial Asymmetry Self-Check Tool': '顔の非対称性セルフチェックツール',
    'Safety First': '安全第一',
    'If asymmetry appears suddenly, or comes with weakness, drooping, speech changes, eye-closing difficulty, severe headache, pain, or numbness, stop treating it like a beauty question. That situation needs medical attention first.': '非対称性が突然現れたり、脱力感、垂れ下がり、発話の変化、目を閉じることの困難、激しい頭痛、痛み、またはしびれを伴う場合は、美容上の問題として扱うのをやめてください。その状況は、まず医師の診察を必要とします。',
    'Function or movement concern': '機能または動きの懸念',
    'Surgical treatments': '外科的治療',
    'Non-surgical options': '非外科的選択肢',
    'Photo habit': '写真の習慣',
    'Mixed angles': 'さまざまな角度',
    'Mostly front-facing': 'ほとんど正面',
    'Subtle cosmetic improvement': '微妙な美容の改善',
    'Choose the options above, then get a practical next-step suggestion.': '上記のオプションを選択して、実践的な次のステップの提案を取得します。',
    '1. What Is Facial Asymmetry, and When Is Asymmetry Normal?': '1. 顔の非対称性とは何ですか？非対称性が正常なのはどんな時ですか？',
    'Facial asymmetry simply means the left and right sides of the face are not exact copies. Almost nobody has two perfectly matched sides. One eye may sit a little higher, one cheek may be fuller, or one corner of the mouth may lift first when you smile. Those small differences are part of how real faces look.': '顔の非対称性とは、顔の左右が正確なコピーではないことを意味します。完全に一致する2つの面を持っている人はほとんどいません。片方の目が少し高い位置にあったり、片方の頬がふっくらしていたり、笑うと口の片方の端が先に上がったりすることがあります。これらの小さな違いは、実際の顔がどのように見えるかの一部です。',
    'A better question than "am I perfectly symmetrical?" is this: has the difference always been there, and does it affect comfort, movement, or confidence? Mild facial asymmetry often becomes obvious in selfies because a phone lens sits close, the head tilts without you noticing, and light can carve shadows into one side.': '「私は完全に対称ですか？」という質問よりも良い質問は、「違いは常にありましたか？それは快適さ、動き、または自信に影響しますか？」ということです。軽度の顔の非対称性は、スマートフォンのレンズが近づき、気づかないうちに頭が傾き、光が片側に影を作るため、自撮りで顕著になることがよくあります。',
    'If one side of the face always looks different, take front-facing photos with the same distance and lighting. Compare the sides of the face only after removing obvious camera issues. You may find the concern is much smaller than it looked in casual selfies.': '顔の片側が常に違って見える場合は、同じ距離と照明で正面の写真を撮ります。明らかなカメラの問題を取り除いた後にのみ、顔の側面を比較してください。カジュアルな自撮り写真で見ていたよりもはるかに懸念が小さいことに気付くかもしれません。',
    '2. Why Does Facial Symmetry Matter in Photos?': '2. 写真において左右対称性が重要な理由',
    'Facial symmetry matters in photos because the eye likes order. When the eyes, mouth, cheeks, and jawline feel lined up, the whole image often looks calmer. But a photo is not a medical scan, and it is not a fair judge of your overall facial appearance.': '目の錯覚は規則性を好むため、写真では顔の対称性が重要になります。目、口、頬、さらには顎のラインがまっすぐ並んでいると感じられるときは、画像全体に落ち着いた印象を与えることがよくあります。しかし、写真は医学的なスキャンではなく、顔全体の見た目に対する公平な判断材料にはなりません。',
    'A lot of people notice facial asymmetry in the least forgiving place possible: a front camera photo taken too close to the face. Suddenly one brow looks higher, the jawline seems stronger on one side, or a smile that felt normal in the mirror looks slightly uneven. It can be annoying, but it is also a very ordinary human thing.': '多くの人は、最も許容されない場所、つまり顔に近づきすぎたフロントカメラの写真で顔のゆがみに気づきます。突然、片方の眉が高く見えたり、顎のラインが片方だけ強く見えたり、また、鏡では普通だと感じていた笑顔がわずかに不均衡に見えたりします。いらいらするかもしれませんが、これは人間なら誰にでもあるごく普通のことです。',
    'Photos lie in tiny ways. A slightly turned head can make one cheek look wider. Overhead light can deepen shadows on one side. A camera tilted by a few degrees can turn a normal feature into an uneven facial concern. Before you make any big decision, take several front-facing photos in the same light, from the same distance, with the camera at eye level.': '写真は私たちを小さな方法で騙します。頭を少し回すだけで、頬の片側が広く見えることがあります。頭上からの光は片側の影を深くする可能性があります。数度傾いたカメラは、普通の特徴を不均衡な顔の懸念に変える可能性があります。大きな決定を下す前に、目の高さでカメラを使用し、同じ光の下、同じ距離からいくつかの正面の写真を撮ってください。',
    '3. What Causes Facial Asymmetry or an Imbalance?': '3. 顔のゆがみ、バランスの崩れの原因とは？',
    'There is rarely one single cause. Facial asymmetry may be due to genetics, growth patterns, dental bite, jaw development, injury, aging, sun exposure, muscle habits, or nerve-related movement changes. Some people see it most when smiling. Others notice it around the brow, cheek, or chin at rest.': '単一の理由であることはまれです。顔の非対称性は、遺伝、成長パターン、噛み合わせ、顎の発達、怪我、加齢、日光への露出、筋肉の癖、または神経関連の動きの変化によって生じる可能性があります。笑ったときに最も顕著になるとおっしゃる方もいれば、安静時に眉、頬、または顎の周りに気付く方もいます。',
    'Aging can change facial balance too. Skin elasticity, collagen, fat pads, and bone support shift over time. One side may sag more than the other, especially if sleeping on one side, chewing habits, or sun exposure have been uneven for years. None of that means something is "wrong"; it means the face has a history.': '加齢もまた、顔のバランスを変化させます。皮膚の弾力性、コラーゲン、脂肪パッド、そして骨のサポートは時間の経過とともに変化します。特に、片方の側で寝る、咀嚼の習慣、または日光への露出が何年も不均一であった場合、一方が他方よりもたるむ可能性があります。これらのうちどれも「間違っている」という意味ではなく、顔には歴史があるということを意味します。',
    'Facial muscles matter too. If one side is tighter, weaker, or more active, the smile or expression may look asymmetrical. This is why some plans combine skin care, injectable treatment, and muscle-focused therapy for underlying muscles rather than using one solution for everything.': '表情筋も重要です。片側が引き締まっている、弱い、または活動的である場合、笑顔や表情が非対称に見える可能性があります。これが一部のプランが、全てに一つの解決策を用いるのではなく、スキンケア、注射治療、および深部の筋肉に対する筋肉を対象とした療法を組み合わせる理由です。',
    '4. Can Non-Surgical Methods Improve Facial Symmetry?': '4. 切らない施術で顔の対称性は改善できる？',
    'Non-surgical methods can help when the concern is mild, photo-related, posture-related, or connected to skin quality and muscle tension. They cannot move bone or rebuild structure, but they may improve facial presentation enough that the issue feels less loud.': '非外科的方法は、その懸念が軽度であるか、写真に関連している場合や姿勢に関連していたり、また、肌の質と筋肉の緊張に関連している場合に役立つことがあります。これらは骨を移動させたり構造を再構築したりすることはできませんが、顔の見え方を改善し、問題があまり目立たなくなる可能性があります。',
    'Start with the boring things, because they are easy to test. Try back sleeping or sleeping on your back if pillow pressure always hits one side of the face. Work on posture through the head and neck, keep hydration steady, and use consistent skincare instead of changing five products at once. Some people try face yoga; results vary, so treat it as gentle movement, not a guaranteed correction.': '当たり前のことから始めましょう。試すのは簡単だからです。枕の圧力が常に顔の片側に当たっている場合は、仰向けで寝ることを試してください。頭と首の姿勢に気を付け、水分補給を怠らず、また、一度に5つの製品を変えるのではなく一貫したスキンケアを使用してください。顔ヨガを試す人もいますが、結果はさまざまであるため、確実な矯正としてではなく優しい運動として取り扱ってください。',
    'Non-invasive methods such as facial massage, lymphatic drainage, and gentle mobility work may refresh the look temporarily by reducing puffiness. Some people discuss mew posture online, but evidence for major adult cosmetic change is limited. These habits may support a more enhanced facial presentation, but they are not a way to correct facial asymmetry caused by bone, bite, or nerve issues.': '顔のフェイシャルマッサージ、リンパドレナージ、または優しいモビリティワークなどの非侵襲的な方法なら、むくみを減らすことによって一時的に見た目をリフレッシュできるかもしれません。ミューイングの姿勢について議論する人もネット上にはいますが、成人で大規模な美容上の変化を起こす証拠は限られています。これらの習慣はより充実した顔の表現をサポートするかもしれませんが、骨、噛み合わせ、または神経の問題によって引き起こされる顔の非対称性を矯正する方法ではありません。',
    '5. Which Non-Surgical Treatments Can Address Facial Asymmetry?': '5. 顔の非対称性に対処できる非外科的治療法は？',
    'Non-surgical treatments may include injectable filler, botulinum toxin injections, skincare-based treatment to rejuvenate tired skin, or facial retraining when movement is involved. A clinician may use hyaluronic filler to add volume to specific areas, such as one cheek or the chin, to soften visible imbalance and create a more refreshed look.': '非外科的治療法には、しわ取り注射、ボツリヌス毒素注射、疲れた肌を若返らせるスキンケアベースの治療、または動きが関与する場合の顔の再トレーニングなどがあります。医師は、片側の頬や顎などの特定の領域にヒアルロン酸注射を使用してボリュームを追加し、目に見える顔のアンバランスを和らげたり、よりリフレッシュした顔立ちを作ったりすることができます。',
    'Botulinum toxin can relax overactive muscles in selected cases. For example, if muscles on one side pull more strongly, carefully placed treatment may help the expression look more even. For nerve-related concerns, facial retraining therapy may help underlying muscles coordinate more evenly.': 'ボツリヌス毒素は一部の症例において過剰に活動している筋肉をリラックスさせることができます。たとえば、もし片方の筋肉がより強く引っ張る場合、慎重に配置された治療法は、表情をより均等に見せるのに役立つかもしれません。神経に関連する懸念については、顔の再トレーニング療法を用いることで基礎となる筋肉がより均等に調整されるよう役立つかもしれません。',
    'These choices are highly anatomy-dependent. Too much filler can make the face look puffy or imbalanced. The best result usually comes from conservative planning, good restraint, and a provider who understands how a face looks while talking, smiling, and resting.': 'これらの選択は解剖学的な特徴に大きく依存します。フィラーを多用しすぎると、顔が腫れぼったく見えたり、バランスが悪くなったりすることがあります。最良の結果は通常、控えめな計画、適切な抑制、そして話しているとき、笑っているとき、休んでいるときの顔がどのように見えるかを理解しているプロバイダーからもたらされます。',
    '6. How Can You Improve Facial Symmetry in Photos First?': '6. 写真撮影の際にできる顔の左右対称性を良くする方法は？',
    'Before seeking treatment, try to improve facial photos. Stand near a window, face the light, keep the camera at eye level, and step back far enough that the lens is not stretching the center of the face. Relax your jaw. Take ten photos, not one, because everyone has one awkward frame that looks like it belongs to a stranger.': '治療をお求めになる前に、顔の写真を改善してみてください。窓の近くに立ち、光に顔を向けます。カメラを目の高さに保ち、レンズが顔の半分を引き伸ばさないように十分後退してください。顎の力をリラックスさせます。誰でも一枚は見知らぬ人のように見える気まずい写真があるものなので、1枚ではなく、10枚の写真を撮ってください。',
    'To improve facial confidence, focus on repeatable conditions: clean light, relaxed expression, good posture, and a natural camera distance. These steps can improve overall facial appearance in photos, reduce facial harshness from shadows, and enhance facial symmetry without changing your features.': '顔に自信を持つためには、きれいな光、リラックスした表情、良い姿勢、そしてカメラの自然な距離といった再現可能な条件に焦点を当ててください。これらの手順により、写真での全体的な顔の外観を改善し、影による顔の厳しさを軽減し、顔の特徴を変えることなく顔の左右対称性を高めることができます。',
    'The goal is not to erase personality. A symmetrical and balanced impression often comes from posture, relaxed expression, and photo quality as much as bone structure.': '目標は個性を消すことではありません。対称的でバランスの取れた印象は、骨格と同じくらい、姿勢、リラックスした表情、そして写真の品質からもたらされることがよくあります。',
    '7. When Are Surgical Treatments or Surgical Methods Considered?': '7. 外科治療や手術はいつ検討すべき？',
    'Surgical treatments are usually considered when the concern is structural, functional, or significant enough that temporary methods will not meet the goal. Examples include jaw imbalance, chin position, facial paralysis, trauma-related changes, or excess skin from aging.': '外科治療は、通常、問題が構造的、機能的であり、一時的な方法では目的を達成できないほど重大な場合に検討されます。例としては、顎の非対称、顎の位置の問題、顔面麻痺、外傷に関連する変化、または加齢による皮膚の余剰などが挙げられます。',
    'Depending on the case, surgical methods may include orthognathic jaw surgery, chin implants, fat grafting, brow lift, facelift, cheek lifts, or a surgical procedure for facial nerve or eyelid function. Fat grafting sometimes involves harvesting fat from one area of the face and body and placing it where support is needed.': 'ケースに応じて、外科的方法には顎矯正手術、顎インプラント、脂肪移植、額の引き上げ手術、フェイスリフト、あるいは顔面神経や眼瞼機能のための外科処置が含まれる場合があります。脂肪移植は、顔や体のある部位から脂肪を採取し、それが必要な部位に移植することがあります。',
    'Surgery can create more lasting or permanent results and, in selected aging-related cases, a more youthful appearance. It also carries higher cost, recovery time, and risk. A good consultation should feel careful and unhurried, with diagnosis, photos, medical history, alternatives, likely downtime, and a realistic discussion of benefits and limits.': '手術はより持続的または永久的な結果を生み出すことができ、選択された加齢関連のケースでは、より若々しい外観を作ることもできます。これにはより多くの費用と回復時間、さらにリスクが伴うため、良い相談というものは診断、写真、病歴、代替案、予想されるダウンタイム、そして利点と限界についての現実的な議論が含まれているような、慎重で急かされないものになるべきです。',
    '8. How Do Fillers, Fat Grafting, and Facial Contours Work?': '8. ヒアルロン酸注射・脂肪注入・輪郭形成のしくみ',
    'Volume-based treatments can adjust facial contours when one area is flatter or less supported. Fillers may soften uneven features, while fat grafting can provide a longer-lasting volume option for selected people.': 'ボリュームを補う治療は、ある領域が平坦になったりサポートが減っていたりする場合に、顔の輪郭を調整できます。ヒアルロン酸注射は不均等な特徴を和らげることができ、一方で脂肪移植は適切な人にはより長持ちするボリュームの選択肢を提供できます。',
    'For example, a clinician may add cheek support, refine the chin, or balance facial features so light falls more evenly on both sides. Planning should name the specific areas of the face that need support instead of treating every uneven detail as the same problem. The aim is not to create a new face, but to support facial harmony, facial balance, and a balanced appearance.': '例えば、医師は頬のサポートを追加したり、顎を整えたり、あるいは顔の特徴の両側に光がより均等に当たるように顔のバランスを取ることがあります。すべての不均一な詳細を同じ問題として扱うのではなく、サポートが必要な顔の特定の領域の計画で指定する必要があります。目的は新しい顔を作ることではなく、顔の調和、顔のバランス、およびバランスの取れた外観をサポートすることです。',
    'These non-surgical options usually involve less downtime than surgery, but they are not risk-free. Injection placement, product choice, dosage, anatomy, and aesthetic goals all matter. Choose an experienced medical professional who studies your face in motion, not just in one still photo.': 'これらの非外科的選択肢は通常、手術よりもダウンタイムが短いですが、リスクがないわけではありません。注射の配置、製品の選択、用量、解剖学、そして美的目標のすべてが重要です。一枚の静止画だけでなく、動いているあなたの顔を研究してくれる経験豊富な医療専門家を選んでください。',
    '9. How Do Aging, Muscles, and Skin Affect Symmetry?': '9. 加齢、筋肉、皮膚は対称性にどう影響する？',
    'Signs of aging can make asymmetry more visible. Sagging and wrinkles may appear more on one side, especially around the midface, mouth, and jawline. The upper face can also shift, with one brow sitting lower or one eyelid appearing heavier.': '加齢の兆候により、非対称性がより目立つようになることがあります。特に中顔面、口周り、顎のラインでは、たるみやしわが片側により多く現れることがあります。顔の上部も変化し、片方の眉が低くなったり、片方のまぶたが重く見えたりすることがあります。',
    'Methods to enhance a harmonious appearance should be personalized. The best plan considers the degree of facial asymmetry, areas needing support, the condition of the skin, the bite, facial movement, and your aesthetic goals. A good provider will explain why a method fits you, not just what is popular this month.': '調和のとれた外観を向上させる方法は個別化されるべきです。最良の計画は、顔の非対称性の程度、サポートが必要な領域、皮膚の状態、噛み合わせ、顔の動き、そしてあなたの美的目標を考慮します。優れたプロバイダーは、今月何が人気があるかだけでなく、なぜその方法があなたに合っているのかを説明してくれます。',
    'Good care should support overall well-being as much as appearance and self-confidence. If a treatment plan makes you feel rushed, or if every concern is answered with the same product, slow down and get another opinion.': '良いケアは、外観や自信と同じくらい全体の幸福をサポートするべきです。治療計画によって急かされているように感じたり、すべての懸念に対して同じ製品または治療法で答える場合は、落ち着いて別の意見を求めてください。',
    '10. Choosing the Right Way to Correct Facial Asymmetry': '10. 顔の左右対称性を高める方法の選び方',
    'New or rapidly changing asymmetry deserves extra care. If there is weakness, pain, numbness, or trouble moving facial muscles, treat that as a health question first and a cosmetic question later.': '新しく急速に変化する非対称性については、特別な注意が必要です。脱力感、痛み、しびれ、または顔の筋肉を動かす際の問題がある場合は、まず健康上の問題として扱い、後で美容上の問題としてアプローチしてください。',
    'Choosing the right approach starts with your unique needs. Are you looking to enhance photos, balance facial movement, improve facial balance, reduce facial tension, or address a functional concern? The answer changes the decision-making process.': 'どのアプローチを選ぶかは、まずあなたが何を求めているのかという明確なニーズから始まります。写真を強化したいですか？顔の動きのバランスを取りたいですか？顔のバランスを改善したいですか？顔の緊張を和らげたいですか？それとも機能的な懸念に対処したいですか？答えによって意思決定プロセスが変わります。',
    'For mild concerns, start with non-surgical options, photo habits, and professional assessment. For larger skeletal or movement-related concerns, ask about surgical options and whether asymmetry correction is likely to achieve your desired outcome.': '軽度の心当たりがある場合は、非外科的選択肢、写真習慣、専門家による評価から始めてください。骨格や運動に関連するより大きな懸念がある場合は、外科的な選択肢と、非対称性の矯正により希望する結果が得られる可能性が高いかどうかを尋ねてください。',
    'If the difference is old, mild, and mostly photo-related, start with better photos and gentle habits. If it is new, changing, painful, or tied to movement, get professional advice rather than trying to solve it alone.': 'その違いが古く、軽度であり、主に写真に関連している場合は、より良い写真と優しい習慣から始めてください。それが新しい内容であったり、痛みを伴ったり、または動きに関係する場合は、自分で解決しようとせずに専門家のアドバイスを受けてください。',
    'For injections, surgery, jaw concerns, or nerve-related movement changes, speak with the right qualified professional: a dermatologist, plastic surgeon, oral and maxillofacial surgeon, orthodontist, neurologist, or facial nerve specialist depending on what is happening.': '注射、手術、顎の懸念、または神経に関連する運動の変化については、その発生状況に応じて、皮膚科医、形成外科医、口腔顎顔面外科医、歯科矯正医、神経科医、顔面神経の専門医など、適切な資格を持つ専門家に相談してください。',
    'Quick summary': '簡単なまとめ',
    'Facial symmetry guide': '顔の左右対称性ガイド',
}

how_it_works_translations = {
    'How Face Score Works: AI Face Analysis Process, Photo Quality, and Safe Interpretation': '顔スコアの仕組み：AI顔分析プロセス、写真の品質、安全な解釈',
    'Face score tools can be useful when you understand the process behind them. This guide explains detection, landmarks, scoring, and the limits of photo-based analysis.': '顔スコアツールは、その背後にあるプロセスを理解していれば役立つ場合があります。このガイドでは、検出、ランドマーク、スコアリング、および写真ベースの分析の限界について説明します。',
    'Process checker': 'プロセスチェッカー',
    'Face Analysis Input Readiness Tool': '顔分析入力準備状況ツール',
    'Soft front light': '柔らかなフロントライト',
    'Slight angle': 'わずかな角度',
    'Extreme angle': '極端な角度',
    'Use this before uploading a face photo to any scoring page.': 'スコーリングページに顔写真をアップロードする前に、これを使用してください。',
    'The first step is finding whether a face is present in the image. If the face is too small, hidden, blurred, or strongly angled, later analysis becomes less stable. Good tools should tell users when the input is weak instead of pretending every photo is equally reliable.': '最初のステップは、画像に顔が存在するかどうかを見つけることです。顔が小さすぎる、隠れている、ぼやけている、または極端に角度がついている場合、その後の分析は不安定になります。良いツールは、すべての写真が等しく信頼できるふりをするのではなく、入力が弱いときにユーザーに伝えるべきです。',
    'Step 2: Landmark and Feature Reading': 'ステップ2：ランドマークと特徴の読み取り',
    'After detection, software estimates facial landmarks around the eyes, nose, mouth, chin, eyebrows, and outline. These points support face shape, symmetry, golden ratio, expression, and comparison features.': '検出後、ソフトウェアは、目、鼻、口、顎、眉毛、および輪郭の周りの顔のランドマークを推定します。これらのポイントは、顔の形、左右対称性、黄金比、表情、および比較機能をサポートします。',
    'Landmarks are geometry, not identity. They describe where visible points appear in one photo. They cannot fully understand personality, emotion, or real-world attractiveness.': 'ランドマークは幾何学であり、アイデンティティではありません。それらは、1枚の写真に目に見えるポイントがどこに表示されるかを説明します。性格、感情、現実世界の魅力を完全に理解することはできません。',
    'A score combines signals such as clarity, symmetry, proportions, expression, and lighting. Different tools use different weights, so two websites may produce different numbers for the same image.': 'スコアは、明瞭さ、対称性、プロポーション、表情、照明などの信号を組み合わせます。ツールによって異なる重みが使用されるため、2つのWebサイトで同じ画像に対して異なる数値が生成される場合があります。',
    'The useful part is not the number alone. It is the explanation: what improved the score, what made it unstable, and what to try next.': '役に立つ部分は数字だけではありません。説明が重要です：何がスコアを改善したか、何が不安定にしたか、そして次に何を試すべきか。',
    'Step 4: Reading the Result Safely': 'ステップ4：結果を安全に読み取る',
    'Results should be read as estimates. Use them to compare photos under similar conditions or to improve camera setup. Do not use them to rank people, diagnose health, verify legal identity, or judge self-worth.': '結果は推定値として読み取る必要があります。それらを使用して、類似した条件で写真を比較したり、カメラのセットアップを改善したりします。人をランク付けしたり、健康状態を診断したり、法的な身元を確認したり、自己価値を判断したりするために使用しないでください。',
    'Best Photo Setup': '最適な写真設定',
    'Use soft front-facing light.': '柔らかな正面からの光を使用します。',
    'Avoid heavy filters and face reshaping.': '重いフィルターや顔の整形は避けてください。',
    'Use a clear, current photo.': '鮮明で最新の写真を使用してください。',
    'Compare more than one image before trusting a pattern.': 'パターンを信頼する前に、複数の画像を比較してください。',
    'Why Two Tools Can Give Different Scores': '2つのツールが異なるスコアを出す理由',
    'Different systems choose different signals. One tool may weight facial symmetry heavily, another may emphasize image clarity, and another may include expression or style. This is why a number should never be read without knowing the method behind it.': '異なるシステムは異なる信号を選択します。あるツールは顔の左右対称性を重く評価し、別のツールは画像の鮮明さを強調し、また別のツールは表情やスタイルを考慮する場合があります。これが、その手法を知らずして数値を読み取ってはならない理由です。',
    'Even the same tool can change its output when the image changes. A closer camera can distort proportions, while a softer light can make landmarks easier to detect. The process is technical, but the user lesson is simple: make the input consistent.': '画像が変化すると、同じツールでも出力が変化する可能性があります。カメラが近いと比率が歪む可能性があり、光が柔らかいとランドマークが検出しやすくなります。プロセスは技術的ですが、ユーザーの教訓は単純です。入力を一貫して行うことです。',
    'What Happens To Uploaded Images?': 'アップロードされた画像はどうなりますか？',
    'Every upload-based page should tell users what the tool does with the image. Some features only preview the file in the browser. Other features may need server processing. The user experience is stronger when that distinction is written near the upload button.': 'アップロードベースのすべてのページは、ツールが画像をどう処理するかをユーザーに伝える必要があります。一部の機能はブラウザでのみファイルをプレビューします。他の機能はサーバー処理を必要とする場合があります。この違いがアップロードボタンの近くに書かれていると、ユーザーエクスペリエンスが強くなります。',
    'How To Retest Fairly': '公平に再テストする方法',
    'Take three photos in the same place: neutral expression, slight smile, and the angle you normally use online. Compare those instead of mixing old photos, filters, and different lighting. Fair testing makes the result more useful and less emotional.': '同じ場所で3枚の写真を撮ります：ニュートラルな表情、わずかな笑顔、そしてオンラインで通常使用する角度。古い写真、フィルター、異なる照明を混在させるのではなく、それらを比較してください。公平なテストは、結果をより有益に、そして感情的な影響を少なくします。',
}

files = glob.glob('*.html')

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    combined_map = dict(common_translations)
    if 'face-symmetry-guide.html' in filepath:
        combined_map.update(face_symmetry_translations)
    if 'how-it-works.html' in filepath:
        combined_map.update(how_it_works_translations)

    for en, jp in combined_map.items():
        pattern = re.compile(en.replace(r'\ ', r'\s+'), re.MULTILINE|re.IGNORECASE)
        html = re.sub(pattern, jp, html)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Processed {filepath}')
