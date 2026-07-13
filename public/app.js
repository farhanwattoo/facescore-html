const FACE_API_CDN = 'https://cdn.jsdelivr.net/npm/face-api.js@0.22.2/dist/face-api.min.js';

function getUiLanguage() {
  return document.documentElement.lang === 'ja' ? 'ja' : 'en';
}

const messages = {
  invalidImage: {
    en: 'Please upload an image file (JPEG/PNG/WEBP).',
    ja: '\u753b\u50cf\u30d5\u30a1\u30a4\u30eb\uff08JPEG/PNG/WEBP\uff09\u3092\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9\u3057\u3066\u304f\u3060\u3055\u3044\u3002'
  },
  loadingImage: {
    en: 'Loading image...',
    ja: '\u753b\u50cf\u3092\u8aad\u307f\u8fbc\u307f\u4e2d...'
  },
  preparingModels: {
    en: 'Preparing AI models...',
    ja: 'AI\u30e2\u30c7\u30eb\u3092\u6e96\u5099\u4e2d...'
  },
  readFailed: {
    en: 'Failed to read the image.',
    ja: '\u753b\u50cf\u306e\u8aad\u307f\u8fbc\u307f\u306b\u5931\u6557\u3057\u307e\u3057\u305f\u3002'
  },
  scriptFailed: {
    en: 'Failed to load the script.',
    ja: '\u30b9\u30af\u30ea\u30d7\u30c8\u306e\u8aad\u307f\u8fbc\u307f\u306b\u5931\u6557\u3057\u307e\u3057\u305f\u3002'
  },
  loadingModels: {
    en: 'Loading AI models...',
    ja: 'AI\u30e2\u30c7\u30eb\u3092\u8aad\u307f\u8fbc\u307f\u4e2d...'
  },
  modelFailed: {
    en: 'Failed to load AI models: ',
    ja: 'AI\u30e2\u30c7\u30eb\u306e\u8aad\u307f\u8fbc\u307f\u306b\u5931\u6557\u3057\u307e\u3057\u305f: '
  },
  detectingParts: {
    en: 'Detecting facial landmarks...',
    ja: '\u9854\u30d1\u30fc\u30c4\u3092\u691c\u51fa\u4e2d...'
  },
  calculatingScore: {
    en: 'Calculating reference score...',
    ja: '\u53c2\u8003\u30b9\u30b3\u30a2\u3092\u8a08\u7b97\u4e2d...'
  },
  noFace: {
    en: 'No face could be detected. Please upload another image.',
    ja: '\u753b\u50cf\u304b\u3089\u9854\u3092\u691c\u51fa\u3067\u304d\u307e\u305b\u3093\u3067\u3057\u305f\u3002\u5225\u306e\u753b\u50cf\u3092\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9\u3057\u3066\u304f\u3060\u3055\u3044\u3002'
  },
  shareText: {
    en: 'My AI face reference score was ',
    ja: '\u79c1\u306e\u9854\u9762\u504f\u5dee\u5024\u306f'
  },
  shareSuffix: {
    en: ' points. Try the free AI face analysis tool here:',
    ja: '\u70b9\u3067\u3057\u305f\uff01AI\u306b\u3088\u308b\u9854\u306e\u53c2\u8003\u30b9\u30b3\u30a2\u306f\u3053\u3061\u3089\u304b\u3089\u7121\u6599\u3067\u6e2c\u5b9a\u3067\u304d\u307e\u3059\uff1a'
  },
  canvasTitle: {
    en: 'AI Face Score',
    ja: 'AI \u9854\u9762\u504f\u5dee\u5024\u8a3a\u65ad'
  },
  genderMale: {
    en: '\u2642 Male',
    ja: '\u2642 \u7537\u6027'
  },
  genderFemale: {
    en: '\u2640 Female',
    ja: '\u2640 \u5973\u6027'
  }
};

function t(key) {
  const value = messages[key];
  return value ? value[getUiLanguage()] : key;
}

function loadScript(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = src;
    script.crossOrigin = 'anonymous';
    script.async = true;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error(t('scriptFailed')));
    document.head.appendChild(script);
  });
}

let modelsPromise = null;
function ensureFaceModels() {
  if (!modelsPromise) {
    modelsPromise = (typeof faceapi !== 'undefined'
      ? Promise.resolve()
      : loadScript(FACE_API_CDN)
    ).then(() => Promise.all([
      faceapi.nets.ssdMobilenetv1.loadFromUri('/models'),
      faceapi.nets.faceLandmark68Net.loadFromUri('/models'),
      faceapi.nets.faceExpressionNet.loadFromUri('/models'),
      faceapi.nets.ageGenderNet.loadFromUri('/models')
    ])).catch((error) => {
      console.error('Failed to load Face API models:', error);
      modelsPromise = null;
      throw error;
    });
  }
  return modelsPromise;
}

function drawRoundedRect(ctx, x, y, width, height, radius) {
  if (typeof ctx.roundRect === 'function') {
    ctx.beginPath();
    ctx.roundRect(x, y, width, height, radius);
    return;
  }

  const r = Math.min(radius, width / 2, height / 2);
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + width - r, y);
  ctx.quadraticCurveTo(x + width, y, x + width, y + r);
  ctx.lineTo(x + width, y + height - r);
  ctx.quadraticCurveTo(x + width, y + height, x + width - r, y + height);
  ctx.lineTo(x + r, y + height);
  ctx.quadraticCurveTo(x, y + height, x, y + height - r);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y, x + r, y);
}

function initAnalyzer(root) {
  const uploadArea = root.querySelector('[data-upload-area]');
  const fileInput = root.querySelector('[data-file-input]');
  const loading = root.querySelector('[data-loading]');
  const resultsArea = root.querySelector('[data-results-area]');
  const errorMessage = root.querySelector('[data-error-message]');
  const resultCanvas = root.querySelector('[data-result-canvas]');
  const resetBtn = root.querySelector('[data-reset-btn]');
  const downloadBtn = root.querySelector('[data-download-btn]');
  const shareXBtn = root.querySelector('[data-share-x-btn]');
  const progressBar = root.querySelector('[data-progress-bar]');
  const loadingText = root.querySelector('[data-loading-text]');
  const scoreVal = root.querySelector('[data-score-val]');
  const ageVal = root.querySelector('[data-age-val]');
  const genderVal = root.querySelector('[data-gender-val]');
  const emotionVal = root.querySelector('[data-emotion-val]');
  const symmetryVal = root.querySelector('[data-symmetry-val]');
  const smileVal = root.querySelector('[data-smile-val]');
  const scoreStars = root.querySelector('[data-score-stars]');

  if (!uploadArea || !fileInput || !loading || !resultsArea || !errorMessage || !resultCanvas) {
    return;
  }

  const ctx = resultCanvas.getContext('2d');
  let currentImage = null;
  let currentScore = 0;

  function updateProgress(percent, text) {
    if (progressBar) progressBar.style.width = `${percent}%`;
    if (loadingText && text) loadingText.textContent = text;
  }

  function showError(message) {
    loading.classList.add('hidden');
    uploadArea.classList.remove('hidden');
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
  }

  function resetState() {
    resultsArea.classList.add('hidden');
    loading.classList.add('hidden');
    errorMessage.classList.add('hidden');
    uploadArea.classList.remove('hidden');
    fileInput.value = '';
    updateProgress(0, '');
  }

  function populateStars(score) {
    scoreStars.innerHTML = '';
    const numericScore = Number(score);
    const numStars = Math.round(numericScore / 20);
    for (let i = 0; i < 5; i += 1) {
      const star = document.createElement('span');
      star.textContent = i < numStars ? '\u2605' : '\u2606';
      scoreStars.appendChild(star);
    }
  }

  function displayResults(data) {
    resultsArea.classList.remove('hidden');

    const maxWidth = 600;
    let scale = 1;
    if (currentImage.width > maxWidth) {
      scale = maxWidth / currentImage.width;
    }

    resultCanvas.width = currentImage.width * scale;
    resultCanvas.height = currentImage.height * scale;

    ctx.clearRect(0, 0, resultCanvas.width, resultCanvas.height);
    ctx.drawImage(currentImage, 0, 0, resultCanvas.width, resultCanvas.height);

    currentScore = data.faceScore;

    if (data.landmarks) {
      ctx.fillStyle = '#FF7EB3';
      ctx.strokeStyle = '#FF7EB3';
      ctx.lineWidth = 1.5;
      data.landmarks.forEach((point) => {
        ctx.beginPath();
        ctx.arc(point.x * scale, point.y * scale, 2, 0, 2 * Math.PI);
        ctx.fill();
      });
    }

    const padding = 20;
    ctx.fillStyle = 'rgba(0, 0, 0, 0.6)';
    drawRoundedRect(ctx, padding, padding, 250, 92, 15);
    ctx.fill();

    ctx.fillStyle = '#FF7EB3';
    ctx.font = 'bold 22px system-ui, "Segoe UI", "Hiragino Sans", "Noto Sans JP", sans-serif';
    ctx.fillText(t('canvasTitle'), padding + 15, padding + 35);

    ctx.fillStyle = '#FFFFFF';
    ctx.font = 'bold 36px system-ui, "Segoe UI", sans-serif';
    ctx.fillText(`Score: ${currentScore}`, padding + 15, padding + 75);

    scoreVal.textContent = data.faceScore;
    ageVal.textContent = data.age;
    genderVal.textContent = data.gender === 'male'
      ? t('genderMale')
      : data.gender === 'female'
        ? t('genderFemale')
        : data.gender;

    const emotionLabels = getUiLanguage() === 'ja'
      ? {
          happy: '\u7b11\u9854',
          sad: '\u60b2\u3057\u307f',
          angry: '\u6012\u308a',
          neutral: '\u771f\u9854',
          surprised: '\u9a5a\u304d',
          fearful: '\u6050\u308c',
          disgusted: '\u5acc\u60aa'
        }
      : {
          happy: 'Happy',
          sad: 'Sad',
          angry: 'Angry',
          neutral: 'Neutral',
          surprised: 'Surprised',
          fearful: 'Fearful',
          disgusted: 'Disgusted'
        };

    const emojis = {
      happy: '\ud83d\ude0a',
      sad: '\ud83d\ude22',
      angry: '\ud83d\ude20',
      neutral: '\ud83d\ude10',
      surprised: '\ud83d\ude32',
      fearful: '\ud83d\ude28',
      disgusted: '\ud83e\udd22'
    };

    emotionVal.textContent = `${emojis[data.emotion] || ''} ${emotionLabels[data.emotion] || data.emotion}`.trim();
    symmetryVal.textContent = `${data.symmetry}%`;
    smileVal.textContent = `${data.smileIntensity}%`;
    populateStars(data.faceScore);
    resultsArea.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  async function analyzeCurrentImage() {
    uploadArea.classList.add('hidden');
    errorMessage.classList.add('hidden');
    loading.classList.remove('hidden');

    try {
      updateProgress(40, t('loadingModels'));
      try {
        await ensureFaceModels();
      } catch (error) {
        throw new Error(t('modelFailed') + (error.message || String(error)));
      }

      updateProgress(55, t('detectingParts'));
      const detections = await faceapi.detectSingleFace(currentImage)
        .withFaceLandmarks()
        .withFaceExpressions()
        .withAgeAndGender();

      updateProgress(80, t('calculatingScore'));

      if (!detections) {
        throw new Error(t('noFace'));
      }

      const { landmarks, expressions, age, gender } = detections;
      const positions = landmarks.positions;
      const noseTip = positions[30];
      const leftJaw = positions[0];
      const rightJaw = positions[16];
      const distLeft = Math.hypot(noseTip.x - leftJaw.x, noseTip.y - leftJaw.y);
      const distRight = Math.hypot(noseTip.x - rightJaw.x, noseTip.y - rightJaw.y);
      const symmetry = 1 - (Math.abs(distLeft - distRight) / Math.max(distLeft, distRight));
      const smileScore = expressions.happy;
      const dominantEmotion = Object.keys(expressions).reduce((best, candidate) => (
        expressions[best] > expressions[candidate] ? best : candidate
      ));
      const faceScoreValue = (symmetry * 70) + (smileScore * 30);
      const faceScore = Math.min(100, Math.max(0, faceScoreValue)).toFixed(1);

      displayResults({
        age: Math.round(age),
        gender,
        emotion: dominantEmotion,
        symmetry: (symmetry * 100).toFixed(1),
        smileIntensity: (smileScore * 100).toFixed(1),
        faceScore,
        landmarks: positions
      });
    } catch (error) {
      showError(error.message);
    } finally {
      loading.classList.add('hidden');
    }
  }

  function handleFileSelect(file) {
    if (!file || !file.type.startsWith('image/')) {
      showError(t('invalidImage'));
      return;
    }

    uploadArea.classList.add('hidden');
    resultsArea.classList.add('hidden');
    errorMessage.classList.add('hidden');
    loading.classList.remove('hidden');
    updateProgress(10, t('loadingImage'));

    const reader = new FileReader();
    reader.onload = (event) => {
      currentImage = new Image();
      currentImage.onload = () => {
        updateProgress(25, t('preparingModels'));
        analyzeCurrentImage();
      };
      currentImage.src = event.target.result;
    };
    reader.onerror = () => {
      showError(t('readFailed'));
    };
    reader.readAsDataURL(file);
  }

  uploadArea.addEventListener('click', () => fileInput.click());
  uploadArea.addEventListener('dragover', (event) => {
    event.preventDefault();
    uploadArea.classList.add('active');
  });
  uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('active');
  });
  uploadArea.addEventListener('drop', (event) => {
    event.preventDefault();
    uploadArea.classList.remove('active');
    if (event.dataTransfer.files.length) {
      fileInput.files = event.dataTransfer.files;
      handleFileSelect(fileInput.files[0]);
    }
  });

  fileInput.addEventListener('change', (event) => {
    if (event.target.files.length) {
      handleFileSelect(event.target.files[0]);
    }
  });

  if (resetBtn) {
    resetBtn.addEventListener('click', resetState);
  }

  if (downloadBtn) {
    downloadBtn.addEventListener('click', () => {
      const dataUrl = resultCanvas.toDataURL('image/jpeg', 0.9);
      const anchor = document.createElement('a');
      anchor.href = dataUrl;
      anchor.download = `FaceScore_${currentScore}_Results.jpg`;
      document.body.appendChild(anchor);
      anchor.click();
      document.body.removeChild(anchor);
    });
  }

  if (shareXBtn) {
    shareXBtn.addEventListener('click', () => {
      const text = encodeURIComponent(
        getUiLanguage() === 'ja'
          ? `${t('shareText')}\u3010${currentScore}\u3011${t('shareSuffix')}`
          : `${t('shareText')}${currentScore}${t('shareSuffix')}`
      );
      const url = encodeURIComponent('https://facescore.net/');
      const twitterUrl = `https://twitter.com/intent/tweet?text=${text}&url=${url}`;
      window.open(twitterUrl, '_blank', 'noopener,noreferrer');
    });
  }

  resetState();
}

document.querySelectorAll('[data-analyzer]').forEach((root) => {
  initAnalyzer(root);
});
