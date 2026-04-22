(function () {
  function clamp(n, min, max) {
    return Math.max(min, Math.min(max, n));
  }

  function byId(id) {
    return document.getElementById(id);
  }

  function isJapaneseUi() {
    return document.documentElement.lang === "ja" || document.documentElement.classList.contains("lang-ja");
  }

  function setText(id, text) {
    var el = byId(id);
    if (el) {
      el.textContent = text;
    }
  }

  function setHtml(id, html) {
    var el = byId(id);
    if (el) {
      el.innerHTML = html;
    }
  }

  function bindRangeValue(rangeId, valueId) {
    var range = byId(rangeId);
    var value = byId(valueId);
    if (!range || !value) return;
    var update = function () {
      value.textContent = range.value;
    };
    update();
    range.addEventListener("input", update);
  }

  function ensureLoadingUi(resultId) {
    var resultEl = byId(resultId);
    if (!resultEl || byId(resultId + "-loading")) return;
    var loading = document.createElement("div");
    loading.id = resultId + "-loading";
    loading.className = "intent-tool__loading hidden";
    loading.innerHTML =
      '<div class="spinner"></div>' +
      '<p class="intent-tool__loading-text">' + (isJapaneseUi() ? "画像を解析中..." : "Analyzing image...") + '</p>' +
      '<div class="progress-container"><div class="progress-bar" id="' + resultId + '-bar"></div></div>';
    resultEl.parentNode.insertBefore(loading, resultEl);
  }

  function runWithLoading(resultId, computeResult) {
    ensureLoadingUi(resultId);
    var loadingEl = byId(resultId + "-loading");
    var resultEl = byId(resultId);
    var bar = byId(resultId + "-bar");
    if (!loadingEl || !resultEl || !bar) {
      setText(resultId, computeResult());
      return;
    }
    loadingEl.classList.remove("hidden");
    resultEl.classList.add("hidden");
    bar.style.width = "0%";
    var progress = 0;
    var timer = setInterval(function () {
      progress += 14;
      if (progress > 100) progress = 100;
      bar.style.width = progress + "%";
      if (progress >= 100) {
        clearInterval(timer);
        loadingEl.classList.add("hidden");
        resultEl.classList.remove("hidden");
        var output = computeResult();
        if (typeof output === "string" && output.trim().charAt(0) === "<") {
          setHtml(resultId, output);
        } else {
          setText(resultId, output);
        }
      }
    }, 120);
  }

  function getUploadedSeed(fileInputId, resultId) {
    var input = byId(fileInputId);
    if (!input || !input.files || !input.files[0]) {
      setText(resultId, isJapaneseUi() ? "先に画像をアップロードしてください。" : "Please upload an image first.");
      return null;
    }
    var file = input.files[0];
    var seed = (file.size % 997) + file.name.length * 13;
    return seed;
  }

  function getQualityAdvice(fileInputId) {
    var input = byId(fileInputId);
    if (!input || !input.dataset.qualityNote) {
      return isJapaneseUi()
        ? "写真品質メモ: 明るい正面写真を使うと結果が安定します。"
        : "Photo quality note: a clear, front-facing image gives the most stable result.";
    }
    return input.dataset.qualityNote;
  }

  function updatePreviewQuality(input, preview, file, url) {
    var qualityEl = preview.nextElementSibling;
    if (!qualityEl || !qualityEl.classList || !qualityEl.classList.contains("intent-tool__quality")) {
      qualityEl = document.createElement("div");
      qualityEl.className = "intent-tool__quality";
      preview.parentNode.insertBefore(qualityEl, preview.nextSibling);
    }
    qualityEl.textContent = isJapaneseUi() ? "写真の読みやすさを確認しています..." : "Checking photo readability...";
    input.dataset.qualityNote = "";

    var image = new Image();
    image.onload = function () {
      var width = image.naturalWidth || image.width || 0;
      var height = image.naturalHeight || image.height || 0;
      var canvas = document.createElement("canvas");
      var sampleSize = 80;
      canvas.width = sampleSize;
      canvas.height = sampleSize;
      var ctx = canvas.getContext("2d", { willReadFrequently: true });
      if (!ctx) return;
      ctx.drawImage(image, 0, 0, sampleSize, sampleSize);
      var data = ctx.getImageData(0, 0, sampleSize, sampleSize).data;
      var total = 0;
      var values = [];
      for (var i = 0; i < data.length; i += 4) {
        var value = Math.round(data[i] * 0.299 + data[i + 1] * 0.587 + data[i + 2] * 0.114);
        total += value;
        values.push(value);
      }
      var average = total / values.length;
      var contrast = values.reduce(function (sum, value) {
        return sum + Math.abs(value - average);
      }, 0) / values.length;
      var issues = [];
      if (Math.min(width, height) < 700) issues.push(isJapaneseUi() ? "解像度が低め" : "low resolution");
      if (average < 70) issues.push(isJapaneseUi() ? "暗め" : "dark lighting");
      if (average > 215) issues.push(isJapaneseUi() ? "明るすぎ" : "overexposed lighting");
      if (contrast < 24) issues.push(isJapaneseUi() ? "コントラスト不足" : "low contrast");
      var megapixels = width && height ? (width * height / 1000000).toFixed(1) : "?";
      var message = issues.length
        ? (isJapaneseUi()
          ? "写真品質メモ: " + issues.join("、") + "。窓際のやわらかい光で撮り直すと安定します。"
          : "Photo quality note: " + issues.join(", ") + ". Retake near soft window light for a steadier result.")
        : (isJapaneseUi()
          ? "写真品質メモ: 読み取りやすい画像です。光、顔の大きさ、解像度のバランスが良好です。"
          : "Photo quality note: this image is readable, with a good balance of light, face size, and resolution.");
      input.dataset.qualityNote = message + " (" + width + "x" + height + ", " + megapixels + "MP)";
      input.dataset.qualityScore = String(clamp(Math.round(100 - issues.length * 18 + Math.min(contrast, 40) / 4), 0, 100));
      qualityEl.textContent = input.dataset.qualityNote;
      window.setTimeout(function () {
        URL.revokeObjectURL(url);
      }, 1000);
    };
    image.onerror = function () {
      input.dataset.qualityNote = isJapaneseUi()
        ? "写真品質メモ: 画像を読み取れませんでした。別のJPEG、PNG、WEBPを試してください。"
        : "Photo quality note: this image could not be checked. Try another JPEG, PNG, or WEBP file.";
      qualityEl.textContent = input.dataset.qualityNote;
      URL.revokeObjectURL(url);
    };
    image.src = url;
  }

  function bindPreview(fileInputId, previewId) {
    var input = byId(fileInputId);
    var preview = byId(previewId);
    if (!input || !preview) return;
    input.addEventListener("change", function (e) {
      var file = e.target.files && e.target.files[0];
      if (!file) return;
      var url = URL.createObjectURL(file);
      preview.src = url;
      preview.style.display = "block";
      updatePreviewQuality(input, preview, file, url);
    });
  }

  function initAttractivenessTool() {
    var run = byId("tool-attractiveness-run");
    if (!run) return;
    bindPreview("tool-attractiveness-file", "tool-attractiveness-preview");
    run.addEventListener("click", function () {
      var seed = getUploadedSeed("tool-attractiveness-file", "tool-attractiveness-result");
      if (seed === null) return;
      runWithLoading("tool-attractiveness-result", function () {
        var symmetry = Number(byId("attr-symmetry").value || 50);
        var smile = Number(byId("attr-smile").value || 50);
        var clarity = Number(byId("attr-clarity").value || 50);
        var style = Number(byId("attr-style").value || 50);
        var score = Math.round(symmetry * 0.35 + smile * 0.2 + clarity * 0.25 + style * 0.2 + (seed % 8));
        var level = score >= 85 ? "Excellent" : score >= 72 ? "Strong" : score >= 58 ? "Average" : "Needs Better Input";
        var summary = score >= 85 ? "Very balanced, clear, and camera-friendly result." :
          score >= 72 ? "Above-average result with strong presentation signals." :
          score >= 58 ? "Solid baseline result with room to improve the photo setup." :
          "This image likely needs better 照明, framing, or clarity.";
        var tip = score >= 72 ? "Try 2-3 photos with the same angle to confirm consistency." : "Use brighter front lighting and keep the camera straight at eye level.";
        var qualityAdvice = getQualityAdvice("tool-attractiveness-file");
        return (
          '<div class="score-card">' +
            '<div class="score-card__hero">' +
              '<div>' +
                '<p class="score-card__eyebrow">AI魅力度結果</p>' +
                '<h3 class="score-card__title">' + level + '</h3>' +
                '<p class="score-card__summary">' + summary + '</p>' +
              '</div>' +
              '<div class="score-orb">' +
                '<span class="score-orb__value">' + score + '</span>' +
                '<span class="score-orb__label">/100</span>' +
              '</div>' +
            '</div>' +
            '<div class="score-card__metrics">' +
              '<div class="metric-chip"><span>Symmetry</span><strong>' + symmetry + '</strong></div>' +
              '<div class="metric-chip"><span>Smile</span><strong>' + smile + '</strong></div>' +
              '<div class="metric-chip"><span>Clarity</span><strong>' + clarity + '</strong></div>' +
              '<div class="metric-chip"><span>Style</span><strong>' + style + '</strong></div>' +
            '</div>' +
            '<div class="score-card__note">' +
              '<strong>Recommendation:</strong> ' + tip + '<br>' + qualityAdvice +
            '</div>' +
          '</div>'
        );
      });
    });
  }

  function initFaceAnalysisTool() {
    var run = byId("tool-analysis-run");
    if (!run) return;
    bindPreview("tool-analysis-file", "tool-analysis-preview");
    run.addEventListener("click", function () {
      var seed = getUploadedSeed("tool-analysis-file", "tool-analysis-result");
      if (seed === null) return;
      runWithLoading("tool-analysis-result", function () {
        var faceShape = (byId("analysis-shape") || {}).value || "balanced";
        var lighting = ((byId("analysis-lighting") || byId("analysis-light")) || {}).value || "good";
        var expression = (byId("analysis-expression") || {}).value || "natural";
        var confidence = 62 + (seed % 33);
        var result = isJapaneseUi()
          ? "分析結果: " + faceShape + " 顔型, " + lighting + " 照明, " + expression + " 表情。信頼度: " + confidence + "%."
          : "Analysis result: " + faceShape + " face shape, " + lighting + " lighting, " + expression + " expression. Confidence: " + confidence + "%.";
        if (lighting === "low") result += isJapaneseUi() ? " 信頼度向上のため照明を改善してください。" : " Improve lighting for a more stable result.";
        if (expression === "extreme") result += isJapaneseUi() ? " 自然な表情または軽い笑顔の方が安定します。" : " A natural expression or light smile is usually more stable.";
        return result + " " + getQualityAdvice("tool-analysis-file");
      });
    });
  }

  function initPhotoRatingTool() {
    var run = byId("tool-photo-run");
    bindPreview("tool-photo-file", "tool-photo-preview");
    if (!run) return;
    run.addEventListener("click", function () {
      var seed = getUploadedSeed("tool-photo-file", "tool-photo-result");
      if (seed === null) return;
      runWithLoading("tool-photo-result", function () {
        var light = Number(byId("photo-light").value || 50);
        var angle = Number(byId("photo-angle").value || 50);
        var quality = Number(byId("photo-quality").value || 50);
        var score = Math.round((light + angle + quality) / 3 + (seed % 6));
        return isJapaneseUi()
          ? "写真評価: " + score + "/100 (" + Math.round(score / 10) + "/10)。" + getQualityAdvice("tool-photo-file")
          : "Photo rating: " + score + "/100 (" + Math.round(score / 10) + "/10). " + getQualityAdvice("tool-photo-file");
      });
    });
  }

  function initGoldenRatioTool() {
    var run = byId("tool-golden-run");
    if (!run) return;
    bindPreview("tool-golden-file", "tool-golden-preview");
    run.addEventListener("click", function () {
      var seed = getUploadedSeed("tool-golden-file", "tool-golden-result");
      if (seed === null) return;
      runWithLoading("tool-golden-result", function () {
        var top = Number(byId("golden-top").value || 1);
        var mid = Number(byId("golden-mid").value || 1);
        var low = Number(byId("golden-low").value || 1);
        var avg = (top + mid + low) / 3;
        var dev = (Math.abs(top - avg) + Math.abs(mid - avg) + Math.abs(low - avg)) / 3;
        var harmony = clamp(Math.round(100 - dev * 30 + (seed % 5)), 0, 100);
        return (isJapaneseUi() ? "顔調和スコア: " : "Face harmony score: ") + harmony + "/100. " + getQualityAdvice("tool-golden-file");
      });
    });
  }

  function initHotnessTool() {
    var run = byId("tool-hotness-run");
    if (!run) return;
    bindPreview("tool-hotness-file", "tool-hotness-preview");
    run.addEventListener("click", function () {
      var seed = getUploadedSeed("tool-hotness-file", "tool-hotness-result");
      if (seed === null) return;
      runWithLoading("tool-hotness-result", function () {
        var confidence = Number(byId("hot-confidence").value || 50);
        var smile = Number(byId("hot-smile").value || 50);
        var style = Number(byId("hot-style").value || 50);
        var score10 = clamp(Math.round((confidence * 0.4 + smile * 0.25 + style * 0.35) / 10 + (seed % 2)), 1, 10);
        return (isJapaneseUi() ? "魅力度メーター: " : "Hotness meter: ") + score10 + "/10. " + getQualityAdvice("tool-hotness-file");
      });
    });
  }

  function initAttractiveTraitsTool() {
    var run = byId("tool-traits-run");
    if (!run) return;
    bindPreview("tool-traits-file", "tool-traits-preview");
    run.addEventListener("click", function () {
      var seed = getUploadedSeed("tool-traits-file", "tool-traits-result");
      if (seed === null) return;
      runWithLoading("tool-traits-result", function () {
        var confidence = Number(byId("trait-confidence").value || 50);
        var grooming = Number(byId("trait-grooming").value || 50);
        var warmth = Number(byId("trait-warmth").value || 50);
        var presence = Math.round((confidence + grooming + warmth) / 3 + (seed % 7));
        var band = presence >= 80 ? "High" : presence >= 60 ? "Good" : "Growing";
        return isJapaneseUi()
          ? "魅力プロフィール: " + band + " presence (" + presence + "/100)。" + getQualityAdvice("tool-traits-file")
          : "Attractiveness profile: " + band + " presence (" + presence + "/100). " + getQualityAdvice("tool-traits-file");
      });
    });
  }

  function initComparisonTool() {
    var run = byId("tool-compare-run");
    if (!run) return;
    bindPreview("tool-compare-file-a", "tool-compare-preview-a");
    bindPreview("tool-compare-file-b", "tool-compare-preview-b");
    run.addEventListener("click", function () {
      var seedA = getUploadedSeed("tool-compare-file-a", "tool-compare-result");
      if (seedA === null) return;
      var seedB = getUploadedSeed("tool-compare-file-b", "tool-compare-result");
      if (seedB === null) return;
      runWithLoading("tool-compare-result", function () {
        var a = Number(byId("compare-a").value || 0);
        var b = Number(byId("compare-b").value || 0);
        var scoreA = clamp(a + (seedA % 6), 0, 100);
        var scoreB = clamp(b + (seedB % 6), 0, 100);
        var diff = Math.abs(scoreA - scoreB);
        var winner = "同点";
        if (scoreA !== scoreB) winner = scoreA > scoreB ? "写真A" : "写真B";
        return "結果: " + winner + " (A: " + scoreA + ", B: " + scoreB + ", 差分: " + diff + "). " + getQualityAdvice("tool-compare-file-a") + " " + getQualityAdvice("tool-compare-file-b");
      });
    });
  }

  function initRandomTool() {
    var run = byId("tool-random-run");
    if (!run) return;
    bindPreview("tool-random-file", "tool-random-preview");
    var roast = [
      "主役級のオーラです。",
      "左右対称は良好、撮影条件は要調整。",
      "ミーム向けの映えスコアです。",
      "ローストモード: 写真映えしすぎています。"
    ];
    run.addEventListener("click", function () {
      var seed = getUploadedSeed("tool-random-file", "tool-random-result");
      if (seed === null) return;
      runWithLoading("tool-random-result", function () {
        var score = (seed * 17) % 101;
        var msg = roast[Math.floor(Math.random() * roast.length)];
        return "ランダムスコア: " + score + "/100 - " + msg + " " + getQualityAdvice("tool-random-file");
      });
    });
  }

  function initMethodTool() {
    var run = byId("tool-method-run");
    if (!run) return;
    bindPreview("tool-method-file", "tool-method-preview");
    run.addEventListener("click", function () {
      var seed = getUploadedSeed("tool-method-file", "tool-method-result");
      if (seed === null) return;
      runWithLoading("tool-method-result", function () {
        var symmetry = Number(byId("method-symmetry").value || 50);
        var proportions = Number(byId("method-proportions").value || 50);
        var expression = Number(byId("method-expression").value || 50);
        var quality = Number(byId("method-quality").value || 50);
        var finalScore = Math.round(symmetry * 0.35 + proportions * 0.3 + expression * 0.15 + quality * 0.2 + (seed % 5));
        return (isJapaneseUi() ? "算出スコア: " : "Calculated score: ") + finalScore + "/100. " + getQualityAdvice("tool-method-file");
      });
    });
  }

  function initGuidanceTools() {
    document.querySelectorAll("[data-guidance-tool]").forEach(function (tool) {
      var button = tool.querySelector("[data-guidance-run]");
      var result = tool.querySelector("[data-guidance-result]");
      if (!button || !result) return;
      button.addEventListener("click", function () {
        var inputs = Array.prototype.slice.call(tool.querySelectorAll("input[type='range'], select"));
        var total = 0;
        var count = 0;
        inputs.forEach(function (input) {
          if (input.tagName.toLowerCase() === "select") {
            total += Number(input.options[input.selectedIndex].dataset.score || 70);
          } else {
            total += Number(input.value || 0);
          }
          count += 1;
        });
        var score = count ? clamp(Math.round(total / count), 0, 100) : 70;
        var title = score >= 82 ? "Strong setup" : score >= 64 ? "Good starting point" : "Needs a cleaner input";
        var advice = score >= 82
          ? "Your setup is likely clear enough for a useful estimate. Try a second photo under similar conditions to confirm consistency."
          : score >= 64
            ? "This is usable, but one or two details could change the result. Improve lighting, camera distance, or expression before trusting the number."
            : "The result may be unstable. Use softer front light, keep the face visible, avoid heavy filters, and try again.";
        result.innerHTML =
          '<div class="score-card">' +
            '<div class="score-card__hero">' +
              '<div><p class="score-card__eyebrow">Quality check</p><h3 class="score-card__title">' + title + '</h3><p class="score-card__summary">' + advice + '</p></div>' +
              '<div class="score-orb"><span class="score-orb__value">' + score + '</span><span class="score-orb__label">/100</span></div>' +
            '</div>' +
            '<div class="score-card__note"><strong>Reminder:</strong> This helper estimates input quality and interpretation risk. It is not a medical, identity, or attractiveness judgment.</div>' +
          '</div>';
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    bindRangeValue("attr-symmetry", "attr-symmetry-val");
    bindRangeValue("attr-smile", "attr-smile-val");
    bindRangeValue("attr-clarity", "attr-clarity-val");
    bindRangeValue("attr-style", "attr-style-val");
    initAttractivenessTool();
    initFaceAnalysisTool();
    initPhotoRatingTool();
    initGoldenRatioTool();
    initHotnessTool();
    initAttractiveTraitsTool();
    initComparisonTool();
    initRandomTool();
    initMethodTool();
    initGuidanceTools();
  });
})();

