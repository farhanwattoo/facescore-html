import sharp from 'sharp';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const publicDir = join(__dirname, '..', 'public');
const base = join(publicDir, 'ganmen-hensachi-keyword');

await sharp(join(publicDir, 'ganmen-hensachi-keyword.svg'))
  .resize(1200, 630, { fit: 'cover' })
  .webp({ quality: 82 })
  .toFile(`${base}.webp`);

await sharp(join(publicDir, 'ganmen-hensachi-keyword.svg'))
  .resize(1200, 630, { fit: 'cover' })
  .avif({ quality: 55 })
  .toFile(`${base}.avif`);

await sharp(join(publicDir, 'ganmen-hensachi-keyword.svg'))
  .resize(800, 420, { fit: 'cover' })
  .webp({ quality: 80 })
  .toFile(`${base}-800.webp`);

console.log('Wrote ganmen-hensachi-keyword.webp, .avif, -800.webp');
