// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

const project = (label, slug) => ({
	label,
	collapsed: true,
	items: [{ autogenerate: { directory: `wiki/${slug}` } }],
});

export default defineConfig({
	site: 'https://spirtysprite.github.io',
	integrations: [
		starlight({
			title: 'KiruProject',
			description: 'Documentation for FoliaGUI, FoliaBoard, FoliaNPC and the Itemsmith, Puppeteer, Lootrift and Loadout plugins.',
			logo: { src: './src/assets/mark.svg', replacesTitle: false },
			favicon: '/favicon.svg',
			customCss: ['./src/styles/docs.css'],
			components: {
				PageTitle: './src/components/PageTitle.astro',
			},
			head: [
				{ tag: 'link', attrs: { rel: 'preconnect', href: 'https://fonts.googleapis.com' } },
				{ tag: 'link', attrs: { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: true } },
				{
					tag: 'link',
					attrs: {
						rel: 'stylesheet',
						href: 'https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500&display=swap',
					},
				},
			],
			social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/SpirtySprite' }],
			lastUpdated: false,
			pagination: true,
			tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },
			expressiveCode: {
				themes: ['github-dark-dimmed', 'github-light'],
				styleOverrides: { borderRadius: '6px', codeFontFamily: "'Geist Mono', ui-monospace, monospace" },
			},
			sidebar: [
				{ label: 'Overview', link: '/wiki/' },
				{
					label: 'Libraries',
					items: [
						project('FoliaGUI', 'foliagui'),
						project('FoliaBoard', 'foliaboard'),
						project('FoliaNPC', 'folianpc'),
					],
				},
				{
					label: 'Plugins',
					items: [
						project('Itemsmith', 'itemsmith'),
						project('Puppeteer', 'puppeteer'),
						project('Lootrift', 'lootrift'),
						project('Loadout', 'loadout'),
					],
				},
			],
		}),
	],
});
