// Regenerates public/sitemap.xml from the HTML files actually present in public/.
// Priorities: homepage 1.0, main tool page 0.9, JP pillar guides 0.85, core docs 0.75,
// tool/test pages 0.7, article cluster 0.6, trust pages 0.5-0.4, html sitemap 0.3.
import { readdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const PUB = join(dirname(fileURLToPath(import.meta.url)), '..', 'public');
const BASE = 'https://face-score.net/';
const LASTMOD = process.argv[2] || new Date().toISOString().slice(0, 10);

const EXCLUDE = new Set([
  'index.html', // homepage is emitted as "/"
  'google8a2939e9b7d79b04.html', // Search Console verification file
]);

const PRIORITY = new Map(Object.entries({
  'ai-face-analysis.html': [0.9, 'weekly'],
  '顔-黄金比-美しさの科学.html': [0.85, 'monthly'],
  '顔-パーツ-ランドマーク-解説.html': [0.85, 'monthly'],
  '自撮り-顔診断-写真-完全ガイド.html': [0.85, 'monthly'],
  '顔面偏差値-上げる方法.html': [0.85, 'monthly'],
  '顔面偏差値-平均.html': [0.8, 'monthly'],
  '顔面偏差値-男女別ランキング.html': [0.8, 'monthly'],
  'how-face-score-works.html': [0.75, 'monthly'],
  'accuracy-limitations.html': [0.75, 'monthly'],
  'face-symmetry-guide.html': [0.75, 'monthly'],
  'golden-ratio-face-analysis.html': [0.75, 'monthly'],
  'facial-landmarks-explained.html': [0.75, 'monthly'],
  'selfie-photo-quality-guide.html': [0.75, 'monthly'],
  'face-attractiveness-test.html': [0.7, 'monthly'],
  'face-comparison-tool.html': [0.7, 'monthly'],
  'smile-expression-analysis.html': [0.7, 'monthly'],
  'age-estimation-ai.html': [0.7, 'monthly'],
  'photo-face-rating.html': [0.7, 'monthly'],
  'hotness-scale-test.html': [0.7, 'monthly'],
  'random-face-score-generator.html': [0.65, 'monthly'],
  'what-makes-you-attractive.html': [0.65, 'monthly'],
  'about.html': [0.5, 'yearly'],
  'team.html': [0.5, 'yearly'],
  'editorial-guidelines.html': [0.4, 'yearly'],
  'privacy.html': [0.4, 'yearly'],
  'terms.html': [0.4, 'yearly'],
  'contact.html': [0.4, 'yearly'],
  'sitemap.html': [0.3, 'monthly'],
}));

const files = readdirSync(PUB).filter(f => f.endsWith('.html') && !EXCLUDE.has(f)).sort();

const entry = (loc, [prio, freq]) =>
  `  <url><loc>${loc}</loc><lastmod>${LASTMOD}</lastmod><changefreq>${freq}</changefreq><priority>${prio}</priority></url>`;

const lines = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
  entry(BASE, [1.0, 'weekly']),
];

// Ordered: explicit priorities first (by priority desc), then the article cluster at 0.6.
const prioritized = files.filter(f => PRIORITY.has(f))
  .sort((a, b) => PRIORITY.get(b)[0] - PRIORITY.get(a)[0]);
const cluster = files.filter(f => !PRIORITY.has(f));

for (const f of prioritized) lines.push(entry(BASE + encodeURI(f), PRIORITY.get(f)));
for (const f of cluster) lines.push(entry(BASE + encodeURI(f), [0.6, 'monthly']));

lines.push('</urlset>', '');
writeFileSync(join(PUB, 'sitemap.xml'), lines.join('\n'));
console.log(`sitemap.xml written: ${files.length + 1} URLs (lastmod ${LASTMOD})`);
