export interface Category {
  slug: 'video' | 'image' | 'chat' | 'agent' | 'business' | 'lifestyle';
  name: string;
  shortName: string;
  description: string;
  longDescription: string;
  icon: string;
  color: string;
  order: number;
}

export const categories: Category[] = [
  {
    slug: 'video',
    name: 'AI動画生成',
    shortName: 'AI動画',
    description: 'Sora・Runway・Pika・Veo・Kling・Hailuo・Luma等のAI動画生成ツールの使い方・料金・無料枠を網羅',
    longDescription: 'AI動画生成は2026年に入り急速に進化中。Sora（OpenAI）・Runway Gen-4・Pika・Veo（Google）・Kling・Hailuo・Lumaなど主要9ツールを実機検証で比較。料金・無料枠・商用利用可否・出力品質を最新情報で網羅し、用途別の最適ツール選定ガイドを提供。',
    icon: 'video',
    color: '#8B5CF6',
    order: 1,
  },
  {
    slug: 'image',
    name: 'AI画像生成',
    shortName: 'AI画像',
    description: 'Midjourney・Stable Diffusion・DALL-E・無料登録不要ツールの実機ガイド',
    longDescription: 'AI画像生成の主要ツール（Midjourney v7・Stable Diffusion・DALL-E 3・Imagen等）と、登録不要・無料で使える日本語対応サイトを実機検証で網羅。プロンプト集・商用利用ライセンス・著作権の最新情報まで。',
    icon: 'image',
    color: '#EC4899',
    order: 2,
  },
  {
    slug: 'chat',
    name: 'AIチャット',
    shortName: 'AIチャット',
    description: 'ChatGPT・Gemini・Claude・Perplexity・Copilot等のAIチャットボット完全ガイド',
    longDescription: 'ChatGPT・Gemini・Claude・Perplexity・Microsoft Copilotなど主要AIチャットの使い方・料金・無料枠の比較。各ツール固有のプロンプト技法・モデル選択・API活用まで実機検証で網羅。',
    icon: 'chat',
    color: '#06B6D4',
    order: 3,
  },
  {
    slug: 'agent',
    name: 'AIエージェント',
    shortName: 'AIエージェント',
    description: '自律型AIエージェント・Claude Code・Devin・Manus等の使い方と業務自動化',
    longDescription: 'AIが自律的にタスクを実行する「AIエージェント」が2026年の大注目領域。Claude Code・Devin・Manus・AutoGPT等の主要エージェントの使い方・料金・実用例を実機検証で詳解。業務自動化のリアルな効果まで。',
    icon: 'robot',
    color: '#10B981',
    order: 4,
  },
  {
    slug: 'business',
    name: 'AI業務効率化',
    shortName: 'AI業務',
    description: 'AI議事録・スライド作成・メール返信・資料作成等の業務系AIツール',
    longDescription: 'AI議事録（tl;dv・Notta・Otter）・スライド作成（Gamma・Tome）・メール返信・資料作成など業務効率化系のAIツールを実機検証。料金・連携・セキュリティ要件まで法人利用視点で解説。',
    icon: 'briefcase',
    color: '#F59E0B',
    order: 5,
  },
  {
    slug: 'lifestyle',
    name: 'AI暮らし',
    shortName: 'AI暮らし',
    description: 'AI英会話・AI占い・AI料理・AI学習等の生活系AIサービス',
    longDescription: 'AI英会話（スピーク・ELSA）・AI占い・AI料理・AI学習など、暮らしに根付いたAIサービスを実機検証で紹介。料金・効果・無料枠で試す方法まで。',
    icon: 'home',
    color: '#EF4444',
    order: 6,
  },
];

export function getCategory(slug: Category['slug']): Category | undefined {
  return categories.find(c => c.slug === slug);
}

export function getCategoriesSorted(): Category[] {
  return [...categories].sort((a, b) => a.order - b.order);
}
