const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const os = require('os');
const { Jimp } = require('jimp');
const faceapi = require('face-api.js');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 3000;

// Set up storage to system temp directory for Vercel Serverless compatibility
const upload = multer({ dest: os.tmpdir() });

app.use(cors());
app.use(express.static('public'));
app.use(express.json());

// Initialize models
let modelsLoaded = false;
async function loadModels() {
    const modelsPath = path.join(__dirname, 'models');
    console.log(`Loading Face API models from ${modelsPath}...`);
    try {
        // Load the 4 required models
        await faceapi.nets.ssdMobilenetv1.loadFromDisk(modelsPath);
        await faceapi.nets.faceLandmark68Net.loadFromDisk(modelsPath);
        await faceapi.nets.faceExpressionNet.loadFromDisk(modelsPath);
        await faceapi.nets.ageGenderNet.loadFromDisk(modelsPath);
        modelsLoaded = true;
        console.log('Face API Models loaded successfully.');
    } catch (err) {
        console.error('Error loading models. Make sure you ran download-models.js first:', err.message);
    }
}

// API Route for Analyzing Faces
app.post('/api/analyze', upload.single('image'), async (req, res) => {
    try {
        if (!modelsLoaded) {
            if (req.file) fs.unlinkSync(req.file.path);
            return res.status(503).json({ error: 'Server models are still loading. Please try again in a few seconds.' });
        }
        if (!req.file) {
            return res.status(400).json({ error: 'No image uploaded.' });
        }

        const imgPath = req.file.path;
        console.log(`Analyzing image: ${imgPath}`);

        let tensor;
        try {
            const image = await Jimp.read(imgPath);
            const { width, height, data } = image.bitmap;
            const values = new Int32Array(width * height * 3);
            for (let i = 0; i < width * height; i++) {
                values[i * 3 + 0] = data[i * 4 + 0]; // R
                values[i * 3 + 1] = data[i * 4 + 1]; // G
                values[i * 3 + 2] = data[i * 4 + 2]; // B
            }
            tensor = faceapi.tf.tensor3d(values, [height, width, 3], 'int32');
        } catch (e) {
            fs.unlinkSync(imgPath);
            return res.status(400).json({ error: 'Invalid or unsupported image file.' });
        }

        // Detect single face + landmarks + expressions + age/gender
        const detections = await faceapi.detectSingleFace(tensor)
            .withFaceLandmarks()
            .withFaceExpressions()
            .withAgeAndGender();

        if (tensor) {
            tensor.dispose();
        }

        if (!detections) {
            fs.unlinkSync(imgPath);
            return res.status(400).json({ error: 'No face detected in the image. 画像から顔を検出できませんでした。' });
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

        const result = {
            age: Math.round(age),
            gender,
            emotion: mainEmotion,
            symmetry: (symmetry * 100).toFixed(1),
            smileIntensity: (smileScore * 100).toFixed(1),
            faceScore,
            landmarks: positions // Return 68 landmarks for frontend overlay
        };

        // Clean up uploaded image
        fs.unlinkSync(imgPath);

        res.json(result);
    } catch (error) {
        console.error(error);
        if (req.file && fs.existsSync(req.file.path)) {
            fs.unlinkSync(req.file.path);
        }
        res.status(500).json({ error: 'Server error during facial analysis.' });
    }
});

loadModels();

if (process.env.NODE_ENV !== 'production') {
    app.listen(port, () => {
        console.log(`Face Score App listening at http://localhost:${port}`);
    });
}

// Export for Vercel Serverless Function
module.exports = app;
