/**
 * アフィリエイトリンク管理
 * Phase 0+1 では PLACEHOLDER で運用。CEO が ASP 承認後に実リンクに差し替え。
 */

export interface AffiliateProgram {
  id: string;
  name: string;
  category: 'taishoku-daiko' | 'tenshoku' | 'bengoshi' | 'denshi-keiyaku' | 'kaikei-saas' | 'shaIRSshi' | 'kintai-saas' | 'gijiroku-ai' | 'inbasinokito';
  cpa: string;
  href: string; // PLACEHOLDER URL
  catchCopy: string;
  approved: boolean;
}

export const affiliates: AffiliateProgram[] = [
  // 退職代行
  { id: 'momuri', name: '退職代行モームリ', category: 'taishoku-daiko', cpa: '¥10,000〜¥20,000', href: '#PLACEHOLDER_momuri', catchCopy: '即日対応・全額返金保証', approved: false },
  { id: 'jobs', name: '退職代行Jobs', category: 'taishoku-daiko', cpa: '¥10,000〜¥20,000', href: '#PLACEHOLDER_jobs', catchCopy: '弁護士監修・違法請求リスクゼロ', approved: false },
  { id: 'saraba', name: 'SARABA', category: 'taishoku-daiko', cpa: '¥10,000〜¥15,000', href: '#PLACEHOLDER_saraba', catchCopy: '24時間対応・最短即日退職', approved: false },

  // 転職
  { id: 'doda', name: 'doda', category: 'tenshoku', cpa: '¥5,000〜¥10,000', href: '#PLACEHOLDER_doda', catchCopy: '20万件以上の求人から選べる', approved: false },
  { id: 'recruit-agent', name: 'リクルートエージェント', category: 'tenshoku', cpa: '¥5,000〜¥10,000', href: '#PLACEHOLDER_recruit', catchCopy: '転職実績No.1', approved: false },
  { id: 'mynavi', name: 'マイナビ転職', category: 'tenshoku', cpa: '¥5,000〜¥8,000', href: '#PLACEHOLDER_mynavi', catchCopy: '20代・30代に強い', approved: false },

  // 弁護士
  { id: 'alg', name: '弁護士法人ALG', category: 'bengoshi', cpa: '¥30,000〜¥80,000', href: '#PLACEHOLDER_alg', catchCopy: '残業代請求の実績多数', approved: false },
  { id: 'adire', name: 'アディーレ法律事務所', category: 'bengoshi', cpa: '¥30,000〜¥80,000', href: '#PLACEHOLDER_adire', catchCopy: '完全成功報酬制', approved: false },
  { id: 'verybest', name: 'ベリーベスト法律事務所', category: 'bengoshi', cpa: '¥30,000〜¥80,000', href: '#PLACEHOLDER_verybest', catchCopy: '全国対応・初回相談無料', approved: false },

  // 電子契約
  { id: 'cloudsign', name: 'クラウドサイン', category: 'denshi-keiyaku', cpa: '¥5,000〜¥15,000', href: '#PLACEHOLDER_cloudsign', catchCopy: '契約締結を5分で完結', approved: false },
  { id: 'gmosign', name: 'GMOサイン', category: 'denshi-keiyaku', cpa: '¥5,000〜¥10,000', href: '#PLACEHOLDER_gmosign', catchCopy: '電子契約シェアNo.1', approved: false },
  { id: 'freeesign', name: 'freeeサイン', category: 'denshi-keiyaku', cpa: '¥5,000〜¥10,000', href: '#PLACEHOLDER_freeesign', catchCopy: 'freee会計と連携', approved: false },

  // 会計SaaS
  { id: 'freee', name: 'freee会計', category: 'kaikei-saas', cpa: '¥5,000', href: '#PLACEHOLDER_freee', catchCopy: '個人事業主・フリーランス向け', approved: false },
  { id: 'mfcloud', name: 'マネーフォワード クラウド', category: 'kaikei-saas', cpa: '¥3,000', href: '#PLACEHOLDER_mfcloud', catchCopy: '銀行・カードを自動連携', approved: false },
  { id: 'misoca', name: 'Misoca', category: 'kaikei-saas', cpa: '¥3,000〜¥5,000', href: '#PLACEHOLDER_misoca', catchCopy: '請求書作成に特化', approved: false },

  // 勤怠管理
  { id: 'kingoftime', name: 'KING OF TIME', category: 'kintai-saas', cpa: '¥3,000〜¥10,000', href: '#PLACEHOLDER_kingoftime', catchCopy: '勤怠管理シェアNo.1', approved: false },
  { id: 'jobcan-kintai', name: 'ジョブカン勤怠', category: 'kintai-saas', cpa: '¥3,000〜¥10,000', href: '#PLACEHOLDER_jobcan', catchCopy: '中小企業に強い', approved: false },

  // AI議事録
  { id: 'notta', name: 'Notta', category: 'gijiroku-ai', cpa: '¥3,000〜¥10,000', href: '#PLACEHOLDER_notta', catchCopy: 'AIが自動で議事録生成', approved: false },
  { id: 'otter', name: 'Otter', category: 'gijiroku-ai', cpa: '¥3,000〜¥8,000', href: '#PLACEHOLDER_otter', catchCopy: '英語議事録に強い', approved: false },
];

export function getAffiliatesByCategory(category: AffiliateProgram['category']): AffiliateProgram[] {
  return affiliates.filter(a => a.category === category);
}

export function getAffiliate(id: string): AffiliateProgram | undefined {
  return affiliates.find(a => a.id === id);
}
