#!/usr/bin/env node
/**
 * check-browser-scripts-guarded.mjs
 *
 * 実ブラウザを起動する全スクリプトが、接続先の門 `assertLocalTarget`
 * （scripts/lib/assert-local-target.mjs）を import しているかを検査する（2026-09-29 新設）。
 *
 * ■ なぜ必要か
 *   2026-09-04〜09-29、AdSense アカウント全体に「広告配信の制限（無効なトラフィック）」が発生。
 *   自動ブラウザで本番を開くスクリプトが最有力容疑。CEO「同じこと二度とやらないようにしてね」。
 *   本検査は「ローカル以外を開けない」ことを機械的に保証する。
 *
 * ■ 何を検出するか
 *   chromium/firefox/webkit/puppeteer の launch や launchPersistentContext を含む
 *   .mjs/.js/.cjs/.ts のうち、assert-local-target.mjs を import していないもの。
 *   除外は EXEMPT に「パスと理由」を書く方式（理由なしの除外は検出を黙らせるのと同じ）。
 *
 * 使い方:
 *   node scripts/check-browser-scripts-guarded.mjs
 * 終了コード: 違反1件以上 / 走査が空回り → 1
 */
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { resolve, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SCRIPTS = resolve(ROOT, 'scripts');
const SELF_REL = 'check-browser-scripts-guarded.mjs';
const SCAN_EXT = new Set(['.mjs', '.js', '.cjs', '.ts']);
const SKIP_DIRS = new Set(['node_modules', 'dist', '.git', '.astro']);

/** 検査自身と scripts/lib/ の2ファイルは常に除外。それ以外の例外はここに「パスと理由」で書く。 */
const EXEMPT = new Map([
  [SELF_REL, '本検査自身。ブラウザを起動せず、文字列として launch パターンを含むだけ'],
]);

export function launchesBrowser(text) {
  return /(chromium|firefox|webkit)\s*\.\s*launch\b|puppeteer\s*\.\s*launch\b|launchPersistentContext\s*\(/.test(text);
}
export function importsGate(text) {
  return /import\s*\{[^}]*\bassertLocalTarget\b[^}]*\}\s*from\s*['"][^'"]*assert-local-target\.mjs['"]/.test(text);
}

function listScripts(dir, out = [], prefix = '') {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    const rel = prefix ? `${prefix}/${name}` : name;
    if (statSync(p).isDirectory()) {
      if (SKIP_DIRS.has(name)) continue;
      listScripts(p, out, rel);
      continue;
    }
    const ext = name.slice(name.lastIndexOf('.'));
    if (SCAN_EXT.has(ext)) out.push({ rel: rel.replace(/\\/g, '/'), path: p });
  }
  return out;
}

function scan() {
  const files = listScripts(SCRIPTS);
  const launchers = [];
  const violations = [];
  for (const f of files) {
    // scripts/lib/ 配下（門そのもの・遮断ライブラリ）は常に除外対象
    const isLib = f.rel.startsWith('lib/');
    const text = readFileSync(f.path, 'utf8');
    if (!launchesBrowser(text)) continue;
    launchers.push(f.rel);
    if (EXEMPT.has(f.rel) || isLib) continue;
    if (!importsGate(text)) violations.push(f.rel);
  }
  return { files, launchers, violations };
}

const { files, launchers, violations } = scan();
console.log(`検査したスクリプト ${files.length} 本・うちブラウザ起動ファイル ${launchers.length} 本`);
if (launchers.length) {
  for (const l of launchers) {
    const tag = EXEMPT.has(l) ? '（除外）' : violations.includes(l) ? '（違反）' : '（OK）';
    console.log(`   scripts/${l} ${tag}`);
  }
}
if (files.length === 0) {
  console.log('❌ 走査が空回りしている（scripts/ 配下でファイルが見つからない）');
  process.exit(1);
}
if (violations.length) {
  console.log('❌ assertLocalTarget を import していないブラウザ起動スクリプト:');
  for (const v of violations) console.log(`   scripts/${v}`);
  console.log("   → import { assertLocalTarget } from './lib/assert-local-target.mjs' を足し、goto の直前に通すこと");
  process.exit(1);
}
console.log('✅ PASS — ブラウザを起動する全スクリプトが接続先の門を通している');
