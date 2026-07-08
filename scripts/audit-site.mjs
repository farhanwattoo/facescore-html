import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';

const root = process.cwd();
const publicDir = path.join(root, 'public');
const guideMinWords = 750;
const supportMinWords = 300;
const placeholderPatterns = [
  /lorem ipsum/i,
  /this section gives practical guidance/i,
  /use it as a repeatable checklist/i,
  /japanese version/i,
  /home jp/i,
  /dummy/i
];
const toolNamePattern = /(face|photo|score|symmetry|attractiveness|golden|hotness|selfie|smile|age|landmark|comparison|analysis|rating)/i;
const nonToolPages = new Set([
  'accuracy-limitations.html',
  'editorial-guidelines.html',
  'privacy.html',
  'terms.html',
  'contact.html',
  'about.html',
  'team.html',
  'sitemap.html'
]);
const supportPages = new Set([
  'about.html',
  'contact.html',
  'privacy.html',
  'terms.html',
  'team.html',
  'sitemap.html',
  'how-it-works.html'
]);
const pillarPages = {
  pillar1: [
    'index.html',
    'how-face-score-works.html',
    'selfie-photo-quality-guide.html',
    'golden-ratio-face-analysis.html',
    'face-symmetry-guide.html',
    'accuracy-limitations.html',
    '顔面偏差値-平均.html',
    '顔面偏差値-上げる方法.html',
    '顔面偏差値-男女別ランキング.html'
  ],
  pillar2: [
    'ai-face-analysis.html',
    'photo-face-rating.html',
    'face-attractiveness-test.html',
    'face-comparison-tool.html',
    'hotness-scale-test.html',
    'age-estimation-ai.html',
    'smile-expression-analysis.html',
    'facial-landmarks-explained.html'
  ],
  pillar3: [
    '顔-黄金比-美しさの科学.html',
    'golden-ratio-face-analysis.html',
    'face-symmetry-guide.html',
    'attractiveness-psychology.html',
    'beauty-standards-by-culture.html',
    'averageness-face-attractiveness.html',
    'evolutionary-psychology-beauty.html',
    'smile-attractiveness-science.html',
    'skin-quality-attractiveness.html'
  ],
  pillar4: [
    '顔-パーツ-ランドマーク-解説.html',
    'eye-shape-types-guide.html',
    'face-shape-types.html',
    'nose-shape-attractiveness.html',
    'lip-ratio-guide.html',
    'jawline-face-shape-guide.html',
    'eyebrow-shape-attractiveness.html',
    'facial-landmarks-explained.html',
    'face-thirds-proportions.html'
  ],
  pillar5: [
    '自撮り-顔写真-完全ガイド.html',
    'selfie-lighting-guide.html',
    'best-camera-angle-face.html',
    'natural-smile-guide.html',
    'filter-effect-face-score.html',
    'smartphone-selfie-setup.html',
    'professional-vs-selfie-score.html',
    'face-analysis-bad-photos.html',
    'makeup-effect-face-score.html'
  ]
};

function stripTags(html) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function count(pattern, html) {
  return (html.match(pattern) || []).length;
}

function wordCount(html) {
  const text = stripTags(html);

  if (typeof Intl?.Segmenter === 'function') {
    const segmenter = new Intl.Segmenter('ja', { granularity: 'word' });
    let total = 0;

    for (const segment of segmenter.segment(text)) {
      if (segment.isWordLike) total += 1;
    }

    return total;
  }

  return (text.match(/[A-Za-z0-9\u3040-\u30ff\u3400-\u9fff]+/g) || []).length;
}

function collectSitemapPaths(xml) {
  const locMatches = xml.match(/<loc>([^<]+)<\/loc>/gi) || [];
  const paths = new Set();

  for (const entry of locMatches) {
    const loc = entry.replace(/<\/?loc>/gi, '').trim();

    try {
      const pathname = new URL(loc).pathname;
      paths.add(pathname);
      paths.add(decodeURIComponent(pathname));
    } catch {
      paths.add(loc);

      try {
        paths.add(decodeURIComponent(loc));
      } catch {
        // Ignore malformed percent-encoding and keep the raw value.
      }
    }
  }

  return paths;
}

const args = process.argv.slice(2);
const explicitFiles = [];

for (const arg of args) {
  if (!arg.startsWith('--')) explicitFiles.push(arg);
}

const presetArg = args.find((arg) => arg.startsWith('--pillar='));
const presetName = presetArg ? presetArg.split('=')[1] : '';
const presetFiles = presetArg ? pillarPages[presetName] || [] : [];
const selectedFiles = new Set([...presetFiles, ...explicitFiles]);
const verificationFiles = new Set(['google8a2939e9b7d79b04.html']);
const allFiles = (await readdir(publicDir))
  .filter((file) => /\.(html|php)$/i.test(file))
  .filter((file) => !verificationFiles.has(file))
  .sort();
const files = selectedFiles.size ? allFiles.filter((file) => selectedFiles.has(file)) : allFiles;
const sitemap = await readFile(path.join(publicDir, 'sitemap.xml'), 'utf8').catch(() => '');
const sitemapPaths = collectSitemapPaths(sitemap);

const findings = [];
const rows = [];

for (const file of files) {
  const html = await readFile(path.join(publicDir, file), 'utf8');
  const h1 = count(/<h1[\s>]/gi, html);
  const h2 = count(/<h2[\s>]/gi, html);
  const words = wordCount(html);
  const hasSiteJs = /site\.js/i.test(html);
  const hasToolMarkup = /(intent-tool|data-guidance-tool|data-simple-tool|upload-area|tool-)/i.test(html);
  const hasToolScript = /intent-tools\.js/i.test(html) || /upload-area/i.test(html) || /data-simple-tool/i.test(html) || /querySelector\(['"]\.tool-result['"]\)/i.test(html);
  const shouldHaveTool = toolNamePattern.test(file) && !nonToolPages.has(file);
  const placeholders = placeholderPatterns.filter((pattern) => pattern.test(html)).map(String);
  const inSitemap = file === 'index.php' || file === 'index.html' || sitemapPaths.has(`/${file}`) || sitemapPaths.has(file);
  const requiredWords = supportPages.has(file) ? supportMinWords : guideMinWords;

  rows.push({ file, words, h1, h2, hasToolMarkup, hasSiteJs, inSitemap });

  if (h1 !== 1) findings.push(`${file}: expected exactly one H1, found ${h1}.`);
  if (h2 < 4) findings.push(`${file}: weak heading structure, found only ${h2} H2 headings.`);
  if (file !== 'index.php' && words < requiredWords) findings.push(`${file}: thin content, about ${words} words.`);
  if (!hasSiteJs) findings.push(`${file}: missing site.js language/SEO helper.`);
  if (shouldHaveTool && (!hasToolMarkup || !hasToolScript)) findings.push(`${file}: page title suggests a tool, but tool markup/script is missing.`);
  if (placeholders.length) findings.push(`${file}: placeholder-like phrase found (${placeholders.join(', ')}).`);
  if (!inSitemap) findings.push(`${file}: not found in sitemap.xml.`);
}

console.table(rows);

if (findings.length) {
  console.log('\nSite audit findings:');
  findings.forEach((finding) => console.log(`- ${finding}`));
  process.exitCode = 1;
} else {
  console.log('\nSite audit passed: headings, content depth, tool presence, sitemap coverage, and language helper checks look good.');
}
