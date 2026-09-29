/**
 * block-ad-requests.mjs — 実ブラウザ検査から広告リクエストを出さないための共通遮断（2026-09-29 新設）
 *
 * ■ なぜ必要か（CEO 絶対ルール）
 *
 *   「ほかのサイトも広告が掲載されたら改修作業とか注意するように徹底しよう。
 *     収益にかかわるからこれは絶対に守るように」
 *
 *   自動ブラウザによる広告の読み込み・表示は、クリックしていなくても
 *   無効トラフィックとして数えられうる。
 *
 * ■ 「ローカルだから安全」は誤り
 *
 *   検査対象が 127.0.0.1 でも、その HTML が広告スクリプトを外部から読む可能性がある。
 *   ページの配信元がローカルであることと、広告リクエストが出ないことは別物である。
 *   ローカルかどうかではなく、遮断しているかどうかでしか判断してはいけない。
 *
 * ■ 使い方
 *
 *     import { blockAdRequests } from './lib/block-ad-requests.mjs';
 *     const blocked = await blockAdRequests(contextOrPage, { origin });
 *     ...
 *     console.log(blocked.summary());   // 何件止めたかを必ず出力する
 *
 *   `origin` を渡すと、その origin と data:/blob: だけを通し、他は全て止める
 *   （検査の安定・高速化にもなる）。`origin` を省くと広告ドメインだけを止める。
 *
 * ■ 注意
 *
 *   ・遮断は既定 ON。フラグで ON にする設計にしない（渡し忘れが事故になる）。
 *   ・止めた件数を必ず表示する。0件なら「安全」ではなく「遮断が効いていない」を疑う。
 */

/** 広告・計測系のホスト。ここに無いものを足すときは理由をコメントで残すこと。 */
export const AD_HOST_PATTERN =
  /googlesyndication\.com|doubleclick\.net|adtrafficquality\.google|googleadservices\.com|fundingchoicesmessages\.google\.com|adservice\.google\./;

/** アフィリエイト計測。踏むと成果計測を汚すので同様に止める。 */
export const AFFILIATE_HOST_PATTERN = /px\.a8\.net|amazon-adsystem\.com|amzn\.to/;

export function isAdRequest(url) {
  return AD_HOST_PATTERN.test(url) || AFFILIATE_HOST_PATTERN.test(url);
}

/**
 * Playwright の BrowserContext か Page に遮断を仕掛ける。
 *
 * @param {{route: Function}} target BrowserContext または Page
 * @param {{origin?: string, allowExternal?: boolean}} opts
 *        origin: これと data:/blob: 以外を全部止める（推奨）
 *        allowExternal: true なら広告以外の外部は通す（フォント等が要るとき）
 * @returns {{ blocked: string[], summary: () => string }}
 */
export async function blockAdRequests(target, opts = {}) {
  const { origin, allowExternal = false } = opts;
  const blocked = [];

  await target.route('**/*', (route) => {
    const url = route.request().url();

    if (url.startsWith('data:') || url.startsWith('blob:')) return route.continue();
    if (origin && url.startsWith(origin)) return route.continue();

    if (isAdRequest(url)) {
      blocked.push(url);
      return route.abort();
    }

    // origin 指定があるなら、広告以外の外部も既定で止める（安定・高速）
    if (origin && !allowExternal) return route.abort();

    return route.continue();
  });

  return {
    blocked,
    summary() {
      const hosts = [...new Set(blocked.map((u) => new URL(u).host))];
      return blocked.length
        ? `広告リクエストを ${blocked.length} 件遮断しました（${hosts.join(', ')}）`
        : '広告リクエストの発生は 0 件でした（遮断が効いていない可能性もあるので、' +
            'ページに広告スクリプトが含まれるかを確認すること）';
    },
  };
}
