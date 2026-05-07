/**
 * template-free.jp 全ページ巡回スクリプト
 *
 * 各ページを PC（1280x800）・モバイル（375x812）の2サイズでキャプチャし、
 * コンソールエラー / 横スクロール / 画面崩れの基本検査を実施する。
 *
 * 使い方:
 *   cd sites/template-free-jp/web
 *   npm run dev      # 別ターミナルで dev server を 4323 ポートで起動
 *   node scripts/audit.mjs
 */
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

const BASE = process.env.BASE_URL || 'http://localhost:4323';
const OUT = path.resolve('./audit-screenshots');
fs.mkdirSync(OUT, { recursive: true });

const PAGES = [
  // TOP / カテゴリ
  { url: '/',                                  name: 'home' },
  { url: '/rodo/',                             name: 'cat-rodo' },
  { url: '/kaikei/',                           name: 'cat-kaikei' },
  { url: '/business/',                         name: 'cat-business' },
  { url: '/gyoshu/',                           name: 'cat-gyoshu' },
  // 静的ページ
  { url: '/about/',                            name: 'about' },
  { url: '/contact/',                          name: 'contact' },
  { url: '/privacy/',                          name: 'privacy' },
  { url: '/disclaimer/',                       name: 'disclaimer' },
  // T001〜T040 全テンプレ
  { url: '/rodo/taishokutodoke/',                  name: 'T001-taishoku' },
  { url: '/rodo/shimatsusho/',                     name: 'T007-shimatsu' },
  { url: '/rodo/roudoujouken-tsuuchisho/',         name: 'T011-roudoujouken' },
  { url: '/rodo/koyou-keiyakusho/',                name: 'T012-koyou' },
  { url: '/rodo/koyou-keiyakusho-kensetsu/',       name: 'T015-koyou-kensetsu' },
  { url: '/rodo/gyoumu-itaku-keiyaku/',            name: 'T016-gyoumu' },
  { url: '/rodo/nda/',                             name: 'T019-nda' },
  { url: '/rodo/himitsuhoji-seiyakusho/',          name: 'T020-himitsuhoji' },
  { url: '/kaikei/seikyu-kojin-jigyonushi/',       name: 'T023-seikyu-kojin' },
  { url: '/kaikei/mitsumori-iraisho/',             name: 'T028-mits-iraisho' },
  { url: '/kaikei/mitsumori-tourokufuyou/',        name: 'T029-mits-touroku' },
  { url: '/business/gijiroku/',                    name: 'T035-gijiroku' },
  { url: '/business/ai-gijiroku-tool/',            name: 'T038-ai-tool' },
  { url: '/gyoshu/freelance/',                     name: 'T039-freelance' },
  { url: '/gyoshu/kojin-jigyonushi/',              name: 'T040-kojin' },
  // Vol.2 カテゴリ
  { url: '/houritsu/',                             name: 'cat-houritsu' },
  { url: '/kaikei2/',                              name: 'cat-kaikei2' },
  { url: '/business2/',                            name: 'cat-business2' },
  { url: '/houritsu/nensho/',                      name: 'T041-nensho' },
  { url: '/business2/nippo/',                      name: 'T054-nippo' },
  { url: '/business2/oreijo/',                     name: 'T057-oreijo' },
  // サイクル2
  { url: '/business2/tenmatsusho/',                name: 'T060-tenmatsu' },
  // サイクル3
  // サイクル4
  { url: '/houritsu/ininjo-sokai/',                name: 'T047-sokai' },
  // サイクル5
  { url: '/kaikei2/ryoshusho-oshare/',             name: 'T050-oshare' },
  // サイクル6
  // サイクル7（最終）
  { url: '/business2/shanai-tsutatsu/',            name: 'T061-tsutatsu' },
  { url: '/business2/zaiko-kanri-spreadsheet/',    name: 'T062-zaiko' },
  // Vol.3 法律深堀
  { url: '/houritsu2/',                            name: 'cat-houritsu2' },
  { url: '/houritsu2/naiyo-shomei/',               name: 'T063-naiyo' },
  { url: '/houritsu2/shakuyosho/',                 name: 'T067-shakuyo' },
  { url: '/houritsu2/kaiko-tsuchisho/',            name: 'T074-kaiko' },
  { url: '/houritsu2/taishoku-shomeisho/',         name: 'T077-taishoku-shomei' },
  { url: '/houritsu2/jidan-sho/',                  name: 'T080-jidan' },
  { url: '/houritsu2/yuigon-sho/',                 name: 'T082-yuigon' },
  { url: '/houritsu2/rikon-kyogisho/',             name: 'T083-rikon' },
];

const VIEWPORTS = [
  { name: 'pc',     width: 1280, height: 800,  deviceScaleFactor: 1 },
  { name: 'mobile', width: 375,  height: 812,  deviceScaleFactor: 2 },
];

const issues = [];

(async () => {
  const browser = await chromium.launch();

  for (const vp of VIEWPORTS) {
    const ctx = await browser.newContext({
      viewport: { width: vp.width, height: vp.height },
      deviceScaleFactor: vp.deviceScaleFactor,
      isMobile: vp.name === 'mobile',
      hasTouch:  vp.name === 'mobile',
      userAgent: vp.name === 'mobile'
        ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
        : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    });
    const page = await ctx.newPage();

    page.on('pageerror', (err) => {
      issues.push({ vp: vp.name, type: 'jserror', msg: err.message });
    });
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        issues.push({ vp: vp.name, type: 'console', msg: msg.text() });
      }
    });

    for (const p of PAGES) {
      try {
        const url = BASE + p.url;
        await page.goto(url, { waitUntil: 'networkidle', timeout: 15000 });
        await page.waitForTimeout(300);

        // fade-up を全て可視化（IntersectionObserver の代わり）
        await page.evaluate(() => {
          document.querySelectorAll('.fade-up').forEach(el => el.classList.add('visible'));
        });
        // 全体スクロールで lazy-load 系も発火させる
        await page.evaluate(async () => {
          await new Promise(r => {
            let y = 0;
            const step = 200;
            const i = setInterval(() => {
              window.scrollTo(0, y);
              y += step;
              if (y > document.body.scrollHeight) { clearInterval(i); window.scrollTo(0,0); r(); }
            }, 30);
          });
        });
        await page.waitForTimeout(400);

        // 横スクロール検出
        const overflow = await page.evaluate(() => {
          const html = document.documentElement;
          return { sw: html.scrollWidth, cw: html.clientWidth, has: html.scrollWidth > html.clientWidth + 2 };
        });
        if (overflow.has) {
          issues.push({ vp: vp.name, page: p.name, type: 'overflow-x', msg: `scrollWidth=${overflow.sw} > clientWidth=${overflow.cw}` });
        }

        // sticky header 動作確認（スクロールしてヘッダーが top:0 に居続けるか）
        if (vp.name === 'pc') {
          const headerSticky = await page.evaluate(() => {
            const h = document.querySelector('.site-header');
            if (!h) return null;
            const cs = window.getComputedStyle(h);
            return { position: cs.position, top: cs.top, zIndex: cs.zIndex };
          });
          if (headerSticky && headerSticky.position !== 'sticky' && headerSticky.position !== 'fixed') {
            issues.push({ vp: vp.name, page: p.name, type: 'header-not-sticky', msg: `position=${headerSticky.position}` });
          }
        }

        // 絵文字 / テキスト矢印検出
        const arrowText = await page.evaluate(() => {
          const arrows = ['←','→','↑','↓','⇐','⇒'];
          let found = '';
          (function walk(node) {
            if (node.nodeType === 3) {
              for (const a of arrows) {
                if (node.textContent.includes(a)) { found = a + ' in: ' + node.textContent.slice(0, 50); return; }
              }
            } else if (node.nodeType === 1 && node.tagName !== 'SCRIPT' && node.tagName !== 'STYLE') {
              for (const c of node.childNodes) walk(c);
            }
          })(document.body);
          return found;
        });
        if (arrowText) {
          issues.push({ vp: vp.name, page: p.name, type: 'arrow-found', msg: arrowText });
        }

        const filename = `${p.name}-${vp.name}.png`;
        await page.screenshot({ path: path.join(OUT, filename), fullPage: true });
        console.log(`  [${vp.name}] ${p.name} -> ${filename}`);
      } catch (e) {
        issues.push({ vp: vp.name, page: p.name, type: 'navigation-error', msg: String(e.message || e) });
      }
    }
    await ctx.close();
  }
  await browser.close();

  console.log('\n==================================================');
  if (issues.length === 0) {
    console.log('Audit PASS — issues: 0');
  } else {
    console.log(`Audit FAIL — issues: ${issues.length}`);
    for (const i of issues) {
      console.log(`  [${i.vp}] ${i.page || ''} ${i.type}: ${i.msg}`);
    }
  }
  console.log('==================================================');
  console.log(`Screenshots saved to: ${OUT}`);
  process.exit(issues.filter(i => i.type !== 'console').length > 0 ? 1 : 0);
})();
