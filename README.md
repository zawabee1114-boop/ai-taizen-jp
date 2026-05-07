# template-free.jp

無料・会員登録不要の業務テンプレート配布サイト。

- ドメイン: <https://template-free.jp>
- スタック: Astro 6 + Tailwind CSS 4（PCファースト・SSG）
- デプロイ: Cloudflare Pages
- グループサイト: [keisan-navi.jp](https://keisan-navi.jp) / [pet-hotel-japan.com](https://pet-hotel-japan.com)

## 開発

```bash
npm install
npm run dev    # http://localhost:4323
npm run build
```

## QA

```bash
node scripts/qa-static.mjs    # 静的検査（push前に必ず実行）
node scripts/audit.mjs        # Playwright 巡回（要 dev server）
```

## ファイル生成

```bash
python scripts/gen-templates.py   # Word/Excel
python scripts/gen-pdf.py         # PDF（記入例含む）
```

## 構成

```
src/
├── data/
│   ├── templates.ts       # T001〜T040 メタデータ
│   ├── categories.ts
│   └── site-meta.json
├── components/            # Header / Footer / DownloadButtons など
├── layouts/               # BaseLayout / CategoryLayout / TemplateLayout
└── pages/
    ├── rodo/              # 労働HR系（22本）
    ├── kaikei/            # 会計書類系（12本）
    ├── business/          # ビジネス文書系（4本）
    ├── gyoshu/            # 業種別ハブ（2本）
    └── about/contact/privacy/disclaimer
```
