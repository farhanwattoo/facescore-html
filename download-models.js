const https = require('https');
const fs = require('fs');
const path = require('path');

const baseURL = 'https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/';
const modelsPath = path.join(__dirname, 'models');

if (!fs.existsSync(modelsPath)) {
    fs.mkdirSync(modelsPath);
}

const files = [
    'ssd_mobilenetv1_model-weights_manifest.json',
    'ssd_mobilenetv1_model-shard1',
    'ssd_mobilenetv1_model-shard2',
    'face_landmark_68_model-weights_manifest.json',
    'face_landmark_68_model-shard1',
    'face_expression_model-weights_manifest.json',
    'face_expression_model-shard1',
    'age_gender_model-weights_manifest.json',
    'age_gender_model-shard1'
];

const downloadFile = (file) => {
    return new Promise((resolve, reject) => {
        const filePath = path.join(modelsPath, file);
        if (fs.existsSync(filePath)) {
            console.log(`${file} already exists. Skipping.`);
            return resolve();
        }
        console.log(`Downloading ${file}...`);

        const request = (url) => {
            https.get(url, (response) => {
                if (response.statusCode === 301 || response.statusCode === 302) {
                    return request(response.headers.location);
                }
                if (response.statusCode !== 200) {
                    return reject(new Error(`Failed to get '${url}' (${response.statusCode})`));
                }
                const fileStream = fs.createWriteStream(filePath);
                response.pipe(fileStream);
                fileStream.on('finish', () => {
                    fileStream.close();
                    resolve();
                });
            }).on('error', (err) => {
                fs.unlink(filePath, () => { });
                reject(err);
            });
        };
        request(baseURL + file);
    });
};

(async () => {
    console.log('Starting face-api.js model downloads (this might take a minute)...');
    try {
        for (const file of files) {
            await downloadFile(file);
        }
        console.log('All models downloaded successfully!');
    } catch (e) {
        console.error('Error downloading files:', e.message);
    }
})();
