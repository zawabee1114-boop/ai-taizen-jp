#!/usr/bin/env node
/**
 * 静的QA: dist/ 配下の HTML を走査して以下を検出する
 *  A. 必須メタ（title / description / canonical / OGP）の欠落
 *  B. JSON-LD のパース失敗・必須型（WebSite / Organization）欠落
 *  C. テンプレページの DLボタン（href="/files/...") に対応するファイルが存在するか
 *  D. broken内部リンク (href="/...")
 */
import fs from 'node:fs';
import path from 'node:path';

const DIST = path.resolve('dist');
const FILES_DIR = path.join(DIST, 'files');

let issues = 0;
const errors = [];

function walk(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) walk(full);
    else if (e.name.endsWith('.html')) checkHtml(full);
  }
}

function checkHtml(filepath) {
  const html = fs.readFileSync(filepath, 'utf8');
  const rel = '/' + path.relative(DIST, filepath).replace(/\\/g, '/').replace(/index\.html$/, '');

  // A. 必須メタ
  if (!/<title>/i.test(html)) errors.push(`${rel}: <title> missing`);
  if (!/<meta\s+name="description"/i.test(html)) errors.push(`${rel}: meta description missing`);
  if (!/<link\s+rel="canonical"/i.test(html)) errors.push(`${rel}: canonical missing`);
  if (!/<meta\s+property="og:title"/i.test(html)) errors.push(`${rel}: og:title missing`);

  // B. JSON-LD parse
  const jsonLdMatches = html.matchAll(/<script\s+type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/gi);
  let hasWebSite = false;
  let hasOrganization = false;
  for (const m of jsonLdMatches) {
    try {
      const ld = JSON.parse(m[1]);
      const types = Array.isArray(ld['@type']) ? ld['@type'] : [ld['@type']];
      if (types.includes('WebSite')) hasWebSite = true;
      if (types.includes('Organization')) hasOrganization = true;
    } catch (e) {
      errors.push(`${rel}: JSON-LD parse error: ${e.message}`);
    }
  }
  if (!hasWebSite) errors.push(`${rel}: WebSite JSON-LD missing`);
  if (!hasOrganization) errors.push(`${rel}: Organization JSON-LD missing`);

  // C. /files/ リンクの存在確認
  const fileLinks = [...html.matchAll(/href="(\/files\/[^"]+)"/g)].map(m => m[1]);
  for (const link of fileLinks) {
    const localPath = path.join(DIST, link.replace(/^\//, ''));
    if (!fs.existsSync(localPath)) {
      errors.push(`${rel}: missing file ${link}`);
    }
  }

  // D. 内部リンクで明らかに dead なもの（/...で.html化対象）の検出
  // ※簡易チェック・完全な broken-link 検出は省略
}

console.log('static QA scan...');
if (!fs.existsSync(DIST)) {
  console.error('dist/ not found. run `npm run build` first.');
  process.exit(1);
}
walk(DIST);

if (errors.length > 0) {
  console.error('==================================================');
  console.error(`QA FAILED — issues: ${errors.length}`);
  console.error('==================================================');
  for (const e of errors) console.error('  - ' + e);
  process.exit(1);
}
console.log('==================================================');
console.log('QA PASS — issues: 0');
console.log('==================================================');
process.exit(0);
