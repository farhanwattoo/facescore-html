import os, re

translations = {
    # sitemap.html
    r'Before uploading sensitive images, read Privacy, Terms, and Editorial[\s\S]*?claims about faces\.': '機密性の高い画像をアップロードする前に、プライバシー、利用規約、編集ガイドラインをお読みください。これらのページでは、同意、制限事項、そして顔に関する主張をサイトがどのように処理すべきかについて説明しています。',
    r'Use this sitemap to find the right face-analysis tool, learn how[\s\S]*?privacy and support pages\.': 'このサイトマップを使用して、適切な顔分析ツールを見つけたり、スコアの仕組みを学んだり、プライバシーやサポートのページを確認したりしてください。',
    r'If you want a score, start with the 顔面偏差値チェッカー or Photo Face[\s\S]*?before testing multiple photos\.': 'スコアが必要な場合は、顔面偏差値チェッカーまたは写真の顔評価ページから開始してください。数値を理解したい場合は、複数の写真をテストする前に「顔スコアの仕組み」と「精度と限界」をお読みください。',
    r'The language selector creates SEO-friendly language paths and[\s\S]*?selected language path where possible\.': '言語セレクターは、1つのコードベースを維持しながら、SEOにフレンドリーな言語パスを作成し、ページコンテンツを翻訳します。内部リンクは、可能な限り選択した言語パス内に留まります。',
    r'Start with the tool that matches your immediate goal, then read the[\s\S]*?privacy and accuracy pages first\.': '当座の目的に合ったツールから始め、結果を信頼する前に関連ガイドをお読みください。顔画像をアップロードする場合は、まずプライバシーと精度のページをお読みください。',
    r'Use the 自撮り写真の品質ガイド when your main goal is a better image\.[\s\S]*?judging the face itself\.': 'より良い画像が主な目的の場合は、自撮り写真の品質ガイドを使用してください。顔そのものを評価するのではなく、照明、カメラの距離、ポーズ、編集の選択に焦点を当てています。',
    r'Privacy Policy': 'プライバシーポリシー',
    
    # facial-landmarks-explained.html
    r'Facial Landmarks Explained: AI Facial Landmark Detection, Human Face[\s\S]*?and Face Landmark Uses': '顔のランドマーク解説：AI顔のランドマーク検出、人間の顔のポイント、および顔のランドマークの用途',
    r'Facial landmarks are key points on a face that help ai systems detect[\s\S]*?orientation, and movement\.': '顔のランドマークは、AIシステムが構造、表情、向き、動きを検出するのに役立つ、顔の重要なポイントです。',

    # common missed strings across multiple files
    r'This section explains what the tool can reasonably read from one[\s\S]*?not as a permanent judgment\.': 'このセクションでは、ツールが1枚の画像から合理的に読み取れるものと、人物について知ることができないことを説明します。永続的な判断としてではなく、実用的な写真のガイダンスとして使用してください。',
    r'The score should be read as an estimate based on visible signals\. It[\s\S]*?culture, or real-world chemistry\.': 'スコアは、目に見える兆候に基づく推定値として読み取ってください。性格、自信、優しさ、声、動き、文化、または現実世界の相性を測定することはできません。',
    r'A better result usually starts with a clearer input: soft light, a[\s\S]*?drawing[\s\S]*?conclusions\.': '通常、より良い結果は明瞭な入力から始まります。柔らかい光、正面からの角度、はっきりと見える顔の特徴、最小限の編集です。結果に驚いた場合は、結論を出す前に写真を撮り直してください。',
    r'Use the feedback to choose a stronger photo, understand why one image[\s\S]*?overthinking a single number\.': 'フィードバックを使用して、より強力な写真を選択し、ある画像が別の画像よりもうまく機能する理由を理解し、1つの数値について考えすぎないようにしてください。',
    r'Photo quality changes most face-analysis results more than users[\s\S]*?can all make a model less stable\.': '写真の品質は、ユーザーが予想する以上にほとんどの顔分析結果を変化させます。ぼかし、圧縮、影、フィルター、極端なカメラの角度はすべて、顔のモデルを不安定にする可能性があります。',
    r'This article is worth reading because it gives practical steps,[\s\S]*?the score\.': 'この記事は、実践的な手順を提供し、限界を説明し、スコアについて考えすぎずに機能を使用するのに役立つため、読む価値があります。',
    r'Privacy matters because face images are personal\. Users should know[\s\S]*?stored, or deleted after analysis\.': '顔画像は個人的なものであるため、プライバシーは重要です。ユーザーは、写真がブラウザで処理されるか、サーバーにアップロードされるか、保存されるか、または分析後に削除されるかを知っておく必要があります。',
    r'A useful result gives context, not only a number\. It should explain[\s\S]*?improving light or reducing 強いフィルターs\.': '有用な結果は、数値だけでなく文脈を提供します。信頼度、可能性のある入力の問題、および照明の改善や強いフィルターの削減などの簡単な次のステップを説明する必要があります。',
    r'A useful result gives context, not only a number\. It should explain[\s\S]*?improving light or reducing heavy filters\.': '有用な結果は、数値だけでなく文脈を提供します。信頼度、可能性のある入力の問題、および照明の改善や強いフィルターの削減などの簡単な次のステップを説明する必要があります。',
    r'The goal is to make the page helpful even when the score is imperfect\.[\s\S]*?Clear limitations build more trust than exaggerated claims\.': '目標は、スコアが不完全であってもページを役立つものにすることです。明確な制限は、誇張された主張よりも多くの信頼を築きます。',
    r'Use this quick checker to see whether your photo setup is likely to[\s\S]*?produce a stable estimate\.': 'このクイックチェッカーを使用して、写真のセットアップが安定した推定を生成する可能性が高いかどうかを確認してください。',
    r'Do not upload someone else without consent\. For sensitive use cases[\s\S]*?qualified service rather than a casual web tool\.': '同意なしに他人の顔をアップロードしないでください。身元確認、年齢確認、医療判断などの機密性の高いユースケースについては、カジュアルなウェブツールではなく、適格なサービスを使用してください。',
    r'The safest way to compare results is to use similar conditions each[\s\S]*?consistent so the tool is reading the face rather than the setup\.': '結果を比較する最も安全な方法は、毎回同等の条件を使用することです。カメラの距離、照明、表情、トリミングを一定に保つことで、ツールはセットアップのノイズではなく安定して顔を読み取ります。',

    # face-symmetry-guide.html missed translations
    r'Aging can change facial balance too\. Skin elasticity, collagen, fat[\s\S]*?"wrong"; it means the face has a history\.': '加齢は顔のバランスも変化させる可能性があります。皮膚の弾力性、コラーゲン、脂肪パッド、骨のサポートは時間の経過とともに変化します。特に片側で寝る、噛む癖、または日光への露出が何年も不均等である場合、片側がもう一方よりもたるむ可能性があります。れらのどれも「間違っている」という意味ではありません。それは顔に歴史があることを意味します。',
    r'To improve facial confidence, focus on repeatable conditions: clean[\s\S]*?without changing your features\.': '顔への自信を高めるには、再現可能な条件に焦点を当ててください。きれいな光、リラックスした表情、良い姿勢、自然なカメラの距離です。これらのステップにより、写真上の全体的な顔の外観が向上し、影の厳しい印象が減少し、顔の造作を変えることなく顔の対称性が向上する可能性があります。',
    r'This guide is for the person who wants a clear answer without panic or[\s\S]*?calmer eye\.': 'このガイドは、焦りや営業のプレッシャーなしに明確な答えを求める人のためのものです。何が正常か、何をチェックする価値があるか、どの非外科的な習慣や治療が役立つか、そしていつ外科的な手法を検討すべきかを学びます。完全に鏡写しの顔を追求することが目的ではありません。より冷静な目で自分にある選択肢を理解することが目的です。',
    r'外科的治療 are usually considered when the concern is structural,[\s\S]*?paralysis, trauma-related changes, or excess skin from aging\.': '外科的治療は、通常、懸念事項が構造的、機能的であるか、あるいは一時的な方法では目的を達成できないほど重大である場合に検討されます。例としては、顎の不均衡、顎の位置、顔面麻痺、外傷による変化、または加齢による余分な皮膚などがあります。',
    r'Photos lie in tiny ways\. A slightly turned head can make one cheek[\s\S]*?the camera at eye level\.': '写真は小さな嘘をつきます。頭をわずかに向けるだけで片頬が広く見えます。頭上の照明は片側の影を深くする可能性があります。数度傾いたカメラは、通常の特徴を不均等な顔の悩みに変えてしまう可能性があります。何か大きな決断をする前に、必ず同じ照明、距離でカメラを目の高さに置き、正面からの写真を数枚撮ってください。',
    r'Before seeking treatment, try to improve facial photos\. Stand near a[\s\S]*?awkward frame that looks like it belongs to a stranger\.': '治療を検討する前に、顔写真の写りを改善してみてください。窓の近くに立ち、光を顔に浴び、カメラを目の高さに置き、レンズが顔の中心を引き伸ばさないように十分離れます。顎の力を抜いてリラックスしてください。1枚ではなく、10枚の写真を撮りましょう。誰でも一枚くらい、他人の顔に見えるような気まずいショットが撮れるものだからです。',
    r'These 非外科的選択肢 usually involve less downtime than surgery, but[\s\S]*?photo\.': 'これら非外科的選択肢は通常、手術よりもダウンタイムが短いですが、リスクがないわけではありません。注射の部位、製品の選択、投与量、解剖学、そして美的目標のすべてが重要です。静止写真だけでなく、動いているあなたの顔を研究してくれる経験豊富な医療専門家を選んでください。',
    r'Non-surgical methods can help when the concern is mild, photo-related,[\s\S]*?presentation enough that the issue feels less loud\.': '非外科的手法は、懸念事項が軽度であるか、写真関連、姿勢関連、または皮膚の質や筋肉の緊張に関連している場合に役立ちます。骨を動かしたり構造を再構築したりすることはできませんが、懸念事項がそれほど目立たなくなるくらい顔の印象を改善する可能性があります。',
    r'This quick tool does not diagnose anything\. Use it like a small note[\s\S]*?often exactly what helps\.': 'このクイックツールはいかなる診断も行いません。写真を比較したり、習慣を変えたり、あるいは相談の予約を入れたりする前の小さなメモ帳として使用してください。少しプロセスを減速させることを目的としていますが、それが多くの場合最も役に立つことなのです。',
    r'Signs of aging can make asymmetry more visible\. Sagging and wrinkles[\s\S]*?one eyelid appearing heavier\.': '加齢の兆しは顔の非対称性をより目立たせる可能性があります。顔のたるみやシワは、特に顔の中央部、口の周り、顎の輪郭などで、片側により多く現れることがあります。顔の上部も変化し、片方の眉が下がったり、片方のまぶたが重く見えたりする場合があります。',
    r'7\. When Are 外科的治療 or Surgical Methods Considered\?': '7. 外科的治療や手術はいつ検討されますか？',
    r'If the difference is old, mild, and mostly photo-related, start with[\s\S]*?it alone\.': 'その違いが昔からのもので、軽度であり、主に写真に関連している場合は、より良い写真と穏やかな習慣から始めてください。それが新しいものであったり、変化していたり、痛みを伴ったり、動きに関連している場合は、自分一人で解決しようとせずに専門家のアドバイスを求めてください。',
    r'For example, a clinician may add cheek support, refine the chin, or[\s\S]*?balance, and a balanced appearance\.': '例えば、医師は両側に光がより均等に当たるように、頬のサポートを追加したり、顎の形を整えたり、顔の特徴のバランスを取ることができるかもしれません。計画では、すべての不均等な詳細を同じ問題として扱うのではなく、サポートが必要な顔の特定の領域を明記する必要があります。目的は新しい顔を作ることではなく、顔の調和、顔のバランス、そして均衡の取れた外見をサポートすることです。',
    r'Botulinum toxin can relax overactive muscles in selected cases\. For[\s\S]*?coordinate more evenly\.': 'ボツリヌストキシンは、特定の症例において過活動な筋肉を弛緩させることができます。例えば、片側の筋肉がより強く引っ張る場合、慎重に行う治療によって表情をより均等に見せることができる可能性があります。神経に関連する懸念については、顔の再訓練療法により、下層の筋肉をより均等に調整するのに役立つ場合があります。',
    r'Facial Asymmetry and Facial Symmetry: What You Can Actually Do Before[\s\S]*?You Worry': '顔の非対称性と対称性：悩む前に実際にできること',
    r'Volume-based treatments can adjust facial contours when one area is[\s\S]*?people\.': 'ボリュームベースの治療法は、ある領域が平坦になったりサポートが減っていたりする場合に、顔の輪郭を調整できます。ヒアルロン酸注入は不均等な特徴を和らげることができ、一方で脂肪移植は適切な人へより長持ちするボリュームの選択肢を提供できます。',
    r'A better question than "am I perfectly symmetrical\?" is this: has the[\s\S]*?and light can carve shadows into one side\.': '「私は完全に対称ですか？」という質問よりも優れた質問は、「その違いは以前からそこにありましたか？ そして、それは快適さ、動き、または自信に影響しますか？」ということです。軽度の非対称性は自撮りで顕著になりがちです。スマートフォンのレンズが近づき、無意識のうちに頭が傾き、光が片側に深い影を刻むからです。',
    r'Facial asymmetry simply means the left and right sides of the face are[\s\S]*?part of how real faces look\.': '顔の非対称性とは、顔の左側と右側が完全にコピーされたものではないことを意味します。左右が完全に一致している人はほとんどいません。笑うと片方の目が少し高くなったり、片方の頬が少しふっくらしていたり、口角の片方が先に上がったりします。これらの小さな違いこそが、本物の顔の自然なあり方なのです。',
    r'There is rarely one single cause\. Facial asymmetry may be due to[\s\S]*?brow, cheek, or chin at rest\.': '原因が1つだけであることは稀です。顔の非対称性の原因は、遺伝、成長過程、噛み合わせ、顎の発達、外傷、加齢、紫外線、筋肉の癖、また神経にかかわる変化による場合があります。笑顔の時に最も顕著に現れると言う人もいれば、安静時に眉、頬、または顎の周りに気付く人もいます。',
    r'If asymmetry appears suddenly, or comes with weakness, drooping,[\s\S]*?needs medical attention first\.': '非対称性が突然に現れたり、脱力感、垂れ下がり、発声の変化、目を閉じることの困難、激しい頭痛、痛み、または痺れを伴う場合は、美容上の問題として捉えるのはやめてください。そのような状況は、まず医師の診察を必要とします。',
    r'Methods to enhance a harmonious appearance should be personalized\. The[\s\S]*?you, not just what is popular this month\.': '調和のとれた外見を高める方法は、個人に合わせてカスタマイズされるべきです。最良の計画では、顔の非対称性の程度、サポートが必要な領域、皮膚の状態、噛み合わせ、顔の動き、そして美的目標を考慮します。優れた医師は、今月何が流行っているかだけでなく、なぜその方法があなたに適しているのかを説明するはずです。',
    r'New or rapidly changing asymmetry deserves extra care\. If there is[\s\S]*?as a health question first and a cosmetic question later\.': '新発の、または急激に変化する非対称性に関しては、特別な注意が必要です。脱力感、痛み、しびれがあったり、顔の筋肉を動かすのに問題がある場合は、まずそれを健康上のご相談として扱い、美容上に関する事は後回しにしてください。',
    r'5\. Which Non-外科的治療 Can Address Facial Asymmetry\?': '5. どのような非外科的治療で非対称性に対処できますか？',
    r'Depending on the case, surgical methods may include orthognathic jaw[\s\S]*?face and body and placing it where support is needed\.': 'ケースに応じて様々ですが、外科的方法には、顎矯正手術、顎のインプラント、脂肪移植、額のリフト、フェイスリフト、頬のリフト、または顔面神経や眼瞼機能のための外科的処置が含まれる場合があります。脂肪の移植には、顔や体のある領域から脂肪を採取し、それらをサポートが必要な場所に配置することが含まれる場合があります。',
    r'A lot of people notice facial asymmetry in the least forgiving place[\s\S]*?annoying, but it is also a very ordinary human thing\.': '多くの人は、最も許容されない場所である非常にカメラを近づけた「フロントカメラの写真」で非対称性に気づきます。突然、片側の眉が高く見えたり、顎のラインが片側に強調されて見えたり、鏡で普段行っていた笑顔がわずかに不均衡に見えたりします。厄介なことかもしれませんが、これは非常にありふれた人間の出来事でもあります。',
    r'Facial muscles matter too\. If one side is tighter, weaker, or more[\s\S]*?therapy for underlying muscles rather than using one solution for[\s\S]*?everything\.': '顔の筋肉も重要です。片側が緊張していたり、弱かったり、より活動的だったりすると、笑顔や表情が非対称にみえる可能性があります。これが、一部の治療プランにおいて、全てに一つの解決策を用いるのではなく、スキンケア、注射治療、及び基礎となる筋肉の治療を組み合わせる理由です。',
    r'Good care should support overall well-being as much as appearance and[\s\S]*?every concern is answered with the same product, slow down and get[\s\S]*?another opinion\.': '良い医療的ケアは、見た目や自信と同じくらい、全体的な健康をサポートするものであるべきです。治療計画によって急かされていると感じたり、すべての懸念事項に対して同じ商品や方法で答えられたりした場合は、一度立ち止まり、可能なら別の意見を求めてください。',
    r'Non-invasive methods such as facial massage, lymphatic drainage, and[\s\S]*?facial asymmetry caused by bone, bite, or nerve issues\.': 'フェイシャルマッサージ、リンパの排出、穏やかなモビリティワークなどの非侵襲的な方法は、むくみを軽減することで、見た目を一時的にさわやかにする可能性があります。ネット上では「ミューイング」の姿勢について話し合う人もいますが、成人における大きな美容的変化についてのエビデンスは限定的です。これらの習慣はより強化された顔の表現をサポートするかもしれませんが、骨格、噛み合わせ、あるいは神経の問題による顔の非対称性を矯正する方法ではありません。',
    r'For mild concerns, start with 非外科的選択肢, 写真の習慣s, and[\s\S]*?is likely to achieve your desired outcome\.': '軽度の問題の場合は、非外科的選択肢、写真習慣の見直し、および専門家への相談から始めましょう。骨格や運動に関連するより大きな問題の場合は、外科的選択肢について、非対称性の矯正によって望む結果が得られる可能性が高いかどうかを尋ねてください。',
    r'The goal is not to erase personality\. A symmetrical and balanced[\s\S]*?quality as much as bone structure\.': '目標は個性を消すことではありません。対称的でバランスの取れた印象は、骨格と同じくらい、姿勢、リラックスした表情、そして写真の品質からもたらされるものです。',
    r'Non-外科的治療 may include injectable filler, botulinum toxin[\s\S]*?or the chin, to soften visible imbalance and create a more refreshed[\s\S]*?look\.': '非外科的治療には、皮膚充填剤の注射、ボツリヌストキシン注射、疲れた肌を若返らせるためのスキンケアベースの治療、または動きが関与する場合の顔の再訓練療法などがあります。医師は、片側の頬や顎などの特定の領域にボリュームを追加するためにヒアルロン酸充填剤を使用し、目に見える不均衡を和らげてよりさわやかな外見を作り出すことがあります。',
    r'For injections, surgery, jaw concerns, or nerve-related movement[\s\S]*?orthodontist, neurologist, or facial nerve specialist depending on[\s\S]*?what is happening\.': '注射、手術、あごの懸念、または神経関連の動きの変化については、何が起こっているかに応じて適切な資格を持つ専門家に相談してください：皮膚科医、形成外科医、口腔外科医、歯科矯正医、神経科医、または顔面神経の専門医。',
    r'If one side of the face always looks different, take front-facing[\s\S]*?concern is much smaller than it looked in casual selfies\.': '常に顔の片側が違って見える場合は、同じ距離と照明で正面の写真を撮ってください。明らかなカメラの問題を取り除いた後に顔の側面のみを比較してください。普段の自撮り写真で見るよりも懸念事項がはるかに小さいことに気付くかもしれません。',
    r'Start with the boring things, because they are easy to test\. Try back[\s\S]*?as gentle movement, not a guaranteed correction\.': 'ありきたりなことから始めましょう。試すのは簡単だからです。枕による圧迫が常に顔の片側に起こっているなら、仰向けで寝ることを試してみてください。頭と首の機能向上の姿勢に取り組み、着実な水分補給を保ち、また、5つの製品を一度に変更するのではなく、一貫したスキンケアを使用してください。顔ヨガを試す人もいますが、結果は様々です。なので確実な矯正としてではなく、穏やかな運動として扱ってください。',
    r'Surgery can create more lasting or permanent results and, in selected[\s\S]*?and limits\.': '手術は、より長続きするか永久的な結果を生み出すことができ、特定された加齢に関連したケースでは、より若々しい外観を作ることもできます。しかし、費用、回復時間、およびリスクがより高くなります。診断、写真、病歴、代替案、予想されるダウンタイム、そして利点と限界についての現実的な議論を含むような、入念で急かされない優れたカウンセリングを受けるべきです。',
    r'Choosing the right approach starts with your unique needs\. Are you[\s\S]*?answer changes the decision-making process\.': '正しいアプローチの選択は、あなた独自のニーズから始まります。写真の写りを良くしたい、顔の動きのバランスを取りたい、顔のバランスを改善したい、顔の緊張を和らげたい、あるいは機能的な懸念に対処したいですか？その答えによって意思決定プロセスは変わります。',
    r'These choices are highly anatomy-dependent\. Too much filler can make[\s\S]*?how a face looks while talking, smiling, and resting\.': 'これらの選択は解剖学に大きく依存しています。多すぎるフィラー処置は、顔を腫れぼったくしたり、アンバランスに見せたりする可能性があります。最良の結果は通常、保守的な計画、優れた抑制、そして会話中、笑顔、休息中の顔の見え方を理解している医師またはプロバイダーからもたらされます。',
    r'Facial symmetry matters in photos because the eye likes order\. When[\s\S]*?fair judge of your overall facial appearance\.': '顔の対称性は写真において重要です。なぜなら目は秩序を好むからです。目、口、頬、顎のラインが揃っていると感じられる時、画像全体は非常に落ち着いて見えます。しかし、写真は医学的なスキャンではありませんので、顔全体の外観を公平に判断できるものではありません。',

}

for filename in ['sitemap.html', 'face-symmetry-guide.html', 'facial-landmarks-explained.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    for eng, jp in translations.items():
        pattern = re.compile(eng, re.IGNORECASE)
        content = re.sub(pattern, jp, content)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
