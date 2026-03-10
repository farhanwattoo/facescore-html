const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const loading = document.getElementById('loading');
const resultsArea = document.getElementById('results-area');
const errorMessage = document.getElementById('error-message');
const resultCanvas = document.getElementById('result-canvas');
const resetBtn = document.getElementById('reset-btn');
const downloadBtn = document.getElementById('download-btn');
const shareXBtn = document.getElementById('share-x-btn');

const ctx = resultCanvas.getContext('2d');
let currentImage = null;
let currentScore = 0;

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
    const text = encodeURIComponent(`私の顔面偏差値は【${currentScore}点】でした！AIによる高精度なルックス評価と顔の黄金比診断はこちらから無料で測定できます：`);
    const url = encodeURIComponent('https://face-score.net/');
    const twitterUrl = `https://twitter.com/intent/tweet?text=${text}&url=${url}`;
    window.open(twitterUrl, '_blank', 'noopener,noreferrer');
});

function handleFileSelect(file) {
    if (!file.type.startsWith('image/')) {
        showError('画像ファイル（JPEG/PNG/WEBP）をアップロードしてください。');
        return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
        currentImage = new Image();
        currentImage.onload = () => {
            uploadImage();
        };
        currentImage.src = e.target.result;
    };
    reader.readAsDataURL(file);
}

let modelsLoaded = false;
Promise.all([
    faceapi.nets.ssdMobilenetv1.loadFromUri('./models'),
    faceapi.nets.faceLandmark68Net.loadFromUri('./models'),
    faceapi.nets.faceExpressionNet.loadFromUri('./models'),
    faceapi.nets.ageGenderNet.loadFromUri('./models')
]).then(() => {
    modelsLoaded = true;
    console.log('Face API Models loaded successfully.');
}).catch((err) => {
    console.error('Failed to load Face API models:', err);
    setTimeout(() => showError('AIモデルの読み込みに失敗しました: ' + err.message), 1000);
});

async function uploadImage() {
    uploadArea.classList.add('hidden');
    errorMessage.classList.add('hidden');
    loading.classList.remove('hidden');

    try {
        if (!modelsLoaded) {
            throw new Error('AIモデルを読み込み中です。数秒後にもう一度お試しください。');
        }

        // Run client-side face detection
        const detections = await faceapi.detectSingleFace(currentImage)
            .withFaceLandmarks()
            .withFaceExpressions()
            .withAgeAndGender();

        if (!detections) {
            throw new Error('画像から顔を検出できませんでした。別の画像をアップロードしてください。');
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
    ctx.font = 'bold 22px "Noto Sans JP", Poppins, sans-serif';
    ctx.fillText('AI 顔面偏差値診断', padding + 15, padding + 35);

    ctx.fillStyle = '#FFFFFF';
    ctx.font = 'bold 36px Poppins, sans-serif';
    ctx.fillText(`Score: ${currentScore}`, padding + 15, padding + 75);

    // Fill Stats
    document.getElementById('score-val').textContent = data.faceScore;
    document.getElementById('age-val').textContent = data.age;

    const genderIcons = { 'male': '♂ 男性', 'female': '♀ 女性' };
    document.getElementById('gender-val').textContent = genderIcons[data.gender] || data.gender;

    const emojis = {
        'happy': '😊', 'sad': '😢', 'angry': '😠',
        'neutral': '😐', 'surprised': '😲', 'fearful': '😨', 'disgusted': '🤢'
    };
    const emotionJa = {
        'happy': '笑顔', 'sad': '悲しみ', 'angry': '怒り',
        'neutral': '真顔', 'surprised': '驚き', 'fearful': '恐れ', 'disgusted': '嫌悪'
    };
    document.getElementById('emotion-val').textContent = `${emojis[data.emotion] || ''} ${emotionJa[data.emotion] || data.emotion}`;

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
