// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://ai-taizen.jp',
  integrations: [
    sitemap({
      changefreq: 'weekly',
      lastmod: new Date(),
      serialize(item) {
        const url = item.url;
        if (url === 'https://ai-taizen.jp/') {
          item.priority = 1.0;
          item.changefreq = 'weekly';
        } else if (url.match(/^https:\/\/ai-taizen\.jp\/(video|image|chat|agent|business|lifestyle)\/$/)) {
          item.priority = 0.9;
          item.changefreq = 'weekly';
        } else if (url.match(/^https:\/\/ai-taizen\.jp\/(video|image|chat|agent|business|lifestyle)\/[a-z][a-z0-9-]+\/$/)) {
          item.priority = 0.85;
          item.changefreq = 'weekly';
        } else if (url.match(/^https:\/\/ai-taizen\.jp\/(video|image|chat|agent|business|lifestyle)\/[a-z][a-z0-9-]+\/[a-z][a-z0-9-]+\/$/)) {
          item.priority = 0.8;
          item.changefreq = 'monthly';
        } else if (url.includes('/about/') || url.includes('/contact/')) {
          item.priority = 0.5;
          item.changefreq = 'yearly';
        } else if (url.includes('/privacy/') || url.includes('/disclaimer/')) {
          item.priority = 0.3;
          item.changefreq = 'yearly';
        }
        return item;
      },
    }),
  ],
  output: 'static',
  build: {
    inlineStylesheets: 'auto',
  },
  vite: {
    plugins: [tailwindcss()],
    build: {
      cssMinify: true,
    },
  },
});
