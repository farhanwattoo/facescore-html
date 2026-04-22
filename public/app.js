const FACE_API_CDN = 'https://cdn.jsdelivr.net/npm/face-api.js@0.22.2/dist/face-api.min.js';

const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const loading = document.getElementById('loading');
const resultsArea = document.getElementById('results-area');
const errorMessage = document.getElementById('error-message');
const resultCanvas = document.getElementById('result-canvas');
const resetBtn = document.getElementById('reset-btn');
const downloadBtn = document.getElementById('download-btn');
const shareXBtn = document.getElementById('share-x-btn');

const progressBar = document.getElementById('progress-bar');
const loadingText = document.getElementById('loading-text');

const ctx = resultCanvas.getContext('2d');
let currentImage = null;
let currentScore = 0;

function getUiLanguage() {
    return document.documentElement.lang === 'ja' ? 'ja' : 'en';
}

const messages = {
    invalidImage: {
        en: 'Please upload an image file (JPEG/PNG/WEBP).',
        ja: '画像ファイル（JPEG/PNG/WEBP）をアップロードしてください。'
    },
    loadingImage: {
        en: 'Loading image...',
        ja: '画像を読み込み中...'
    },
    preparingModels: {
        en: 'Preparing AI models...',
        ja: 'AIモデルを準備中...'
    },
    readFailed: {
        en: 'Failed to read the image.',
        ja: '画像の読み込みに失敗しました。'
    },
    scriptFailed: {
        en: 'Failed to load the script',
        ja: 'スクリプトの読み込みに失敗しました'
    },
    loadingModels: {
        en: 'Loading AI models...',
        ja: 'AIモデルを読み込み中...'
    },
    modelFailed: {
        en: 'Failed to load AI models: ',
        ja: 'AIモデルの読み込みに失敗しました: '
    },
    detectingParts: {
        en: 'Detecting facial landmarks...',
        ja: '顔パーツを検出中...'
    },
    calculatingScore: {
        en: 'Calculating reference score...',
        ja: 'ルックス評価を計算中...'
    },
    noFace: {
        en: 'No face could be detected. Please upload another image.',
        ja: '画像から顔を検出できませんでした。別の画像をアップロードしてください。'
    },
    shareText: {
        en: 'My AI face reference score was ',
        ja: '私の顔面偏差値は'
    },
    shareSuffix: {
        en: ' points. Try the free AI face analysis tool here:',
        ja: '点でした！AIによる顔の参考スコアはこちらから無料で測定できます：'
    },
    canvasTitle: {
        en: 'AI Face Score',
        ja: 'AI 顔面偏差値診断'
    }
};

function t(key) {
    const value = messages[key];
    return value ? value[getUiLanguage()] : key;
}

// Event Listeners for Drag and Drop
uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('active');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('active');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('active');
    if (e.dataTransfer.files.length) {
        fileInput.files = e.dataTransfer.files;
        handleFileSelect(fileInput.files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length) {
        handleFileSelect(e.target.files[0]);
    }
});

resetBtn.addEventListener('click', () => {
    resultsArea.classList.add('hidden');
    uploadArea.classList.remove('hidden');
    errorMessage.classList.add('hidden');
    fileInput.value = '';
    updateProgress(0, '');
});

downloadBtn.addEventListener('click', () => {
    // Generate a downloadable URL from the rendered canvas
    const dataUrl = resultCanvas.toDataURL('image/jpeg', 0.9);
    const a = document.createElement('a');
    a.href = dataUrl;
    a.download = `FaceScore_${currentScore}_Results.jpg`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
});

shareXBtn.addEventListener('click', () => {
    const text = encodeURIComponent(getUiLanguage() === 'ja'
        ? `${t('shareText')}【${currentScore}】${t('shareSuffix')}`
        : `${t('shareText')}${currentScore}${t('shareSuffix')}`
    );
    const url = encodeURIComponent('https://face-score.net/');
    const twitterUrl = `https://twitter.com/intent/tweet?text=${text}&url=${url}`;
    window.open(twitterUrl, '_blank', 'noopener,noreferrer');
});

function handleFileSelect(file) {
    if (!file.type.startsWith('image/')) {
        showError(t('invalidImage'));
        return;
    }

    // Show loading state immediately to improve UX
    uploadArea.classList.add('hidden');
    errorMessage.classList.add('hidden');
    loading.classList.remove('hidden');
    updateProgress(10, t('loadingImage'));

    const reader = new FileReader();
    reader.onload = (e) => {
        currentImage = new Image();
        currentImage.onload = () => {
            updateProgress(30, t('preparingModels'));
            uploadImage();
        };
        currentImage.src = e.target.result;
    };
    reader.onerror = () => {
        showError(t('readFailed'));
    };
    reader.readAsDataURL(file);
}

function updateProgress(percent, text) {
    if (progressBar) progressBar.style.width = `${percent}%`;
    if (loadingText && text) loadingText.textContent = text;
}

function loadScript(src) {
    return new Promise((resolve, reject) => {
        const s = document.createElement('script');
        s.src = src;
        s.crossOrigin = 'anonymous';
        s.async = true;
        s.onload = () => resolve();
        s.onerror = () => reject(new Error(t('scriptFailed')));
        document.head.appendChild(s);
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
        ])).then(() => {
            console.log('Face API Models loaded successfully.');
        }).catch((err) => {
            console.error('Failed to load Face API models:', err);
            modelsPromise = null;
            throw err;
        });
    }
    return modelsPromise;
}

async function uploadImage() {
    uploadArea.classList.add('hidden');
    errorMessage.classList.add('hidden');
    loading.classList.remove('hidden');

    try {
        updateProgress(40, t('loadingModels'));
        try {
            await ensureFaceModels();
        } catch (err) {
            throw new Error(t('modelFailed') + (err.message || String(err)));
        }

        updateProgress(50, t('detectingParts'));

        // Run client-side face detection
        const detections = await faceapi.detectSingleFace(currentImage)
            .withFaceLandmarks()
            .withFaceExpressions()
            .withAgeAndGender();

        updateProgress(80, t('calculatingScore'));

        if (!detections) {
            throw new Error(t('noFace'));
        }

        // --- FACE SCORE LOGIC ---
        const { landmarks, expressions, age, gender } = detections;
        const positions = landmarks.positions;

        // Calculate Symmetry using nose tip against jawline width
        const noseTip = positions[30];
        const leftJaw = positions[0];
        const rightJaw = positions[16];

        const distLeft = Math.hypot(noseTip.x - leftJaw.x, noseTip.y - leftJaw.y);
        const distRight = Math.hypot(noseTip.x - rightJaw.x, noseTip.y - rightJaw.y);

        // Symmetry metric 0 to 1
        const symmetry = 1 - (Math.abs(distLeft - distRight) / Math.max(distLeft, distRight));

        // Emotion and Smile
        const smileScore = expressions.happy; // 0 to 1

        // Find dominant emotion
        let mainEmotion = Object.keys(expressions).reduce((a, b) => expressions[a] > expressions[b] ? a : b);

        // Final score out of 100 (Weighted: 70% symmetry, 30% smile)
        const faceScoreValue = (symmetry * 70) + (smileScore * 30);
        const faceScore = Math.min(100, Math.max(0, faceScoreValue)).toFixed(1);

        const data = {
            age: Math.round(age),
            gender,
            emotion: mainEmotion,
            symmetry: (symmetry * 100).toFixed(1),
            smileIntensity: (smileScore * 100).toFixed(1),
            faceScore,
            landmarks: positions
        };

        displayResults(data);
    } catch (error) {
        showError(error.message);
    } finally {
        loading.classList.add('hidden');
    }
}

function showError(msg) {
    loading.classList.add('hidden');
    uploadArea.classList.remove('hidden');
    errorMessage.textContent = msg;
    errorMessage.classList.remove('hidden');
}

function displayResults(data) {
    resultsArea.classList.remove('hidden');

    // Draw Image & Landmarks
    const MAX_WIDTH = 600;
    let scale = 1;
    if (currentImage.width > MAX_WIDTH) {
        scale = MAX_WIDTH / currentImage.width;
    }

    resultCanvas.width = currentImage.width * scale;
    resultCanvas.height = currentImage.height * scale;

    ctx.drawImage(currentImage, 0, 0, resultCanvas.width, resultCanvas.height);

    currentScore = data.faceScore;

    // Draw landmarks
    if (data.landmarks) {
        ctx.fillStyle = '#FF7EB3';
        ctx.strokeStyle = '#FF7EB3';
        ctx.lineWidth = 1.5;

        data.landmarks.forEach(point => {
            ctx.beginPath();
            ctx.arc(point.x * scale, point.y * scale, 2, 0, 2 * Math.PI);
            ctx.fill();
        });
    }

    // Draw Score directly on Canvas so downloaded image is cool!
    const padding = 20;
    ctx.fillStyle = 'rgba(0,0,0,0.6)';
    ctx.roundRect ? ctx.roundRect(padding, padding, 240, 90, 15) : ctx.fillRect(padding, padding, 240, 90);
    ctx.fill();

    ctx.fillStyle = '#FF7EB3';
    ctx.font = 'bold 22px system-ui, "Segoe UI", "Hiragino Sans", "Noto Sans JP", sans-serif';
    ctx.fillText(t('canvasTitle'), padding + 15, padding + 35);

    ctx.fillStyle = '#FFFFFF';
    ctx.font = 'bold 36px system-ui, "Segoe UI", sans-serif';
    ctx.fillText(`Score: ${currentScore}`, padding + 15, padding + 75);

    // Fill Stats
    document.getElementById('score-val').textContent = data.faceScore;
    document.getElementById('age-val').textContent = data.age;

    const genderIcons = getUiLanguage() === 'ja'
        ? { 'male': '♂ 男性', 'female': '♀ 女性' }
        : { 'male': '♂ Male', 'female': '♀ Female' };
    document.getElementById('gender-val').textContent = genderIcons[data.gender] || data.gender;

    const emojis = {
        'happy': '😊', 'sad': '😢', 'angry': '😠',
        'neutral': '😐', 'surprised': '😲', 'fearful': '😨', 'disgusted': '🤢'
    };
    const emotionLabels = getUiLanguage() === 'ja'
        ? {
            'happy': '笑顔', 'sad': '悲しみ', 'angry': '怒り',
            'neutral': '真顔', 'surprised': '驚き', 'fearful': '恐れ', 'disgusted': '嫌悪'
        }
        : {
            'happy': 'Happy', 'sad': 'Sad', 'angry': 'Angry',
            'neutral': 'Neutral', 'surprised': 'Surprised', 'fearful': 'Fearful', 'disgusted': 'Disgusted'
        };
    document.getElementById('emotion-val').textContent = `${emojis[data.emotion] || ''} ${emotionLabels[data.emotion] || data.emotion}`;

    document.getElementById('symmetry-val').textContent = `${data.symmetry}%`;
    document.getElementById('smile-val').textContent = `${data.smileIntensity}%`;

    // Fill Stars
    const starsDiv = document.getElementById('score-stars');
    starsDiv.innerHTML = '';
    const numStars = Math.round(data.faceScore / 20);
    for (let i = 0; i < 5; i++) {
        const star = document.createElement('span');
        star.textContent = i < numStars ? '★' : '☆';
        star.style.color = i < numStars ? '#FFD700' : '#E0E0E0';
        starsDiv.appendChild(star);
    }
}
