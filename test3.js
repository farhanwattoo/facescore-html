const faceapi = require('face-api.js');
const fs = require('fs');
const jpeg = require('jpeg-js');
const { tf } = faceapi; // faceapi bundles its own tfjs-core

async function run() {
    await faceapi.nets.ssdMobilenetv1.loadFromDisk('./models');

    const buffer = fs.readFileSync('test.jpg');
    const jpegData = jpeg.decode(buffer, { useTArray: true });

    // jpegData.data is RGBA (4 channels) Int8Array
    // face-api expects 3 channels (RGB)
    const numChannels = 3;
    const numPixels = jpegData.width * jpegData.height;
    const values = new Int32Array(numPixels * numChannels);

    for (let i = 0; i < numPixels; i++) {
        for (let c = 0; c < numChannels; c++) {
            values[i * numChannels + c] = jpegData.data[i * 4 + c];
        }
    }

    const tensor = tf.tensor3d(values, [jpegData.height, jpegData.width, numChannels], 'int32');

    console.log('Detecting face with tensor...');
    const res = await faceapi.detectSingleFace(tensor);
    console.log('Result:', res);
    tensor.dispose();
}

run().catch(console.error);
