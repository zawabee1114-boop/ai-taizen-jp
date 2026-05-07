// AIガイドサイト用の記事メタデータ（旧 templates.ts を articles 用に再定義）
// 既存コンポーネントとの互換性のためファイル名・関数名は維持

export type CategorySlug = 'video' | 'image' | 'chat' | 'agent' | 'business' | 'lifestyle';

export interface ArticleSource {
  url: string;
  label: string;
  verifiedAt: string;
}

export interface ArticleMeta {
  id: string;
  category: CategorySlug;
  subcategory?: string;
  slug: string;
  url: string;
  title: string;
  shortTitle: string;
  description: string;
  metaDescription: string;
  mainKw: string;
  searchVolume: number;
  cpc: number;
  seoDifficulty: number;
  featured: boolean;
  priority: 'top' | 'high' | 'mid' | 'low';
  affiliateGroup: string;
  sources: ArticleSource[];
  crossSiteLinks?: { title: string; url: string; reason: string }[];
  lastUpdated: string;
  publishedAt: string;
  published: boolean;
}

// 既存コンポーネントから参照されるエイリアス
export type TemplateMeta = ArticleMeta;

export const templates: ArticleMeta[] = [
  // パイプライン試走後にここへ追加していく
];

export const articles = templates;

export function getTemplatesByCategory(category: CategorySlug): ArticleMeta[] {
  return templates.filter(t => t.category === category && t.published);
}

export function getArticlesByCategory(category: CategorySlug): ArticleMeta[] {
  return getTemplatesByCategory(category);
}

export function getFeaturedTemplates(): ArticleMeta[] {
  return templates.filter(t => t.featured && t.published);
}

export function getCategoryNavItems(category: CategorySlug): {
  published: ArticleMeta[];
  upcoming: { title: string; expectedAt?: string }[];
} {
  return {
    published: getTemplatesByCategory(category),
    upcoming: upcomingByCategory[category] ?? [],
  };
}

export const upcomingByCategory: Record<CategorySlug, { title: string; expectedAt?: string }[]> = {
  video: [],
  image: [],
  chat: [],
  agent: [],
  business: [],
  lifestyle: [],
};
