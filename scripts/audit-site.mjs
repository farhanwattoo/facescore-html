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
  return (text.match(/[A-Za-z0-9\u3040-\u30ff\u3400-\u9fff]+/g) || []).length;
}

const files = (await readdir(publicDir))
  .filter((file) => /\.(html|php)$/i.test(file))
  .sort();
const sitemap = await readFile(path.join(publicDir, 'sitemap.xml'), 'utf8').catch(() => '');

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
  const inSitemap = file === 'index.php' || file === 'index.html' || sitemap.includes(`/${file}`);
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
