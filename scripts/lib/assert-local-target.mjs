/**
 * assert-local-target.mjs — 自動ブラウザの接続先をローカルに限る門（2026-09-29 新設）
 *
 * ■ なぜ必要か
 *   2026-09-04〜09-29、AdSense のアカウント全体に「広告配信の制限（無効なトラフィック）」が出ていた。
 *   自動ブラウザで本番を開くスクリプトが最有力容疑。CEO「同じこと二度とやらないようにしてね」。
 *
 * ■ 決まり
 *   - 許可リスト方式。http(s) で host が localhost / 127.0.0.1 / [::1] のときだけ通す。
 *     本番（ai-taizen.jp）も *.pages.dev（プレビュー・同じ広告コード入り）も LAN の IP も throw。
 *   - 抜け道の環境変数・引数は作らない。本番の確認は curl（JS 非実行）で行う。
 *   - 広告リクエストの遮断（block-ad-requests.mjs の blockAdRequests）は別途そのまま使う。
 *     ローカルでも HTML が広告スクリプトを外部から読むため、両方が要る。
 *   - ブラウザを起動するスクリプトはこれを import して goto の直前に通す。
 *     検査: scripts/check-browser-scripts-guarded.mjs（qa に結線）
 */
const ALLOWED_HOSTS = new Set(['localhost', '127.0.0.1', '[::1]']);

export function assertLocalTarget(url) {
  let u;
  try {
    u = new URL(String(url));
  } catch {
    throw new Error(`[assertLocalTarget] URL として読めない接続先は開かない: ${url}`);
  }
  if (!/^https?:$/.test(u.protocol) || !ALLOWED_HOSTS.has(u.hostname)) {
    throw new Error(
      `[assertLocalTarget] ローカル以外を自動ブラウザで開こうとした: ${u.href}\n` +
      '  本番・*.pages.dev・LAN は開かない（AdSense の無効トラフィック対策）。本番の確認は curl で。'
    );
  }
  return u.href;
}
