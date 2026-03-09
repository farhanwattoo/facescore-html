const tf = require('@tensorflow/tfjs-node');
const faceapi = require('face-api.js');
const fs = require('fs');
async function r() {
    await faceapi.nets.ssdMobilenetv1.loadFromDisk('./models');
    const tensor = tf.node.decodeImage(fs.readFileSync('test.jpg'));
    const res = await faceapi.detectSingleFace(tensor);
    console.log('Result:', res);
}
r().catch(console.error);
