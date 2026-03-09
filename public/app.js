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
            uploadImage(file);
        };
        currentImage.src = e.target.result;
    };
    reader.readAsDataURL(file);
}

async function uploadImage(file) {
    uploadArea.classList.add('hidden');
    errorMessage.classList.add('hidden');
    loading.classList.remove('hidden');

    const formData = new FormData();
    formData.append('image', file);

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to analyze image.');
        }

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
