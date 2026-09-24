export type Project = {
	slug: string;
	name: string;
	kind: 'Library' | 'Plugin';
	repo: string;
	version: string;
	summary: string;
	requires: string;
	highlights: string[];
	install: string;
};

export const PROJECTS: Project[] = [
	{
		slug: 'foliagui',
		name: 'FoliaGUI',
		kind: 'Library',
		repo: 'FoliaGUI-API',
		version: '1.1.1',
		summary: 'Inventory menus you can open, update and animate from any thread.',
		requires: 'Paper or Folia 1.21, Java 21',
		highlights: ['Paginated, scrolling and storage menus', 'Anvil, sign and chat input', 'Dialogs, themes and animation'],
		install: 'com.github.SpirtySprite:FoliaGUI-API:1.1.1',
	},
	{
		slug: 'foliaboard',
		name: 'FoliaBoard',
		kind: 'Library',
		repo: 'FoliaBoard-API',
		version: '1.1.0',
		summary: 'Packet-level sidebars, nametags, tab lists and boss bars.',
		requires: 'Paper or Folia 1.20.6+, Java 21',
		highlights: ['Per-player sidebars and layouts', 'Per-viewer nametags and tab names', 'No ProtocolLib, no locks'],
		install: 'com.github.SpirtySprite:FoliaBoard-API:1.1.0',
	},
	{
		slug: 'folianpc',
		name: 'FoliaNPC',
		kind: 'Library',
		repo: 'FoliaNPC-API',
		version: '1.2.1',
		summary: 'NPCs made only of packets, with skins, nametags and pathfinding.',
		requires: 'Paper or Folia 1.20.6 to 26.x, Java 21',
		highlights: ['Any living entity, skins and variants', 'Pathfinding with navigateTo', 'Clean reloads, no dependencies'],
		install: 'com.github.SpirtySprite:FoliaNPC-API:1.2.1',
	},
	{
		slug: 'itemsmith',
		name: 'Itemsmith',
		kind: 'Plugin',
		repo: 'Itemsmith',
		version: '1.0.0',
		summary: 'Edit any item in hand from a menu, with a full undo history.',
		requires: 'Paper or Folia 1.21 and 26.x',
		highlights: ['Names, lore, enchantments, attributes', 'Saved item library and /item give', 'Undo, redo and /give export'],
		install: '/item',
	},
	{
		slug: 'puppeteer',
		name: 'Puppeteer',
		kind: 'Plugin',
		repo: 'Puppeteer',
		version: '1.0.0',
		summary: 'Packet NPCs described in one YAML file, with click actions.',
		requires: 'Paper or Folia 1.21 and 26.x',
		highlights: ['Patrols, dialogues, one-time actions', 'Sixteen click action types', 'Imports Citizens, FancyNpcs, ZNPCsPlus'],
		install: '/npc',
	},
	{
		slug: 'lootrift',
		name: 'Lootrift',
		kind: 'Plugin',
		repo: 'Lootrift',
		version: '1.0.0',
		summary: 'Animated crates with keys, pity, milestones and an in-game editor.',
		requires: 'Paper or Folia 1.21 and 26.x',
		highlights: ['Twelve opening animations, pity', 'Seasons, key drops, ItemsAdder and Nexo rewards', 'Imports CrazyCrates, ExcellentCrates'],
		install: '/crate',
	},
	{
		slug: 'loadout',
		name: 'Loadout',
		kind: 'Plugin',
		repo: 'Loadout',
		version: '1.0.0',
		summary: 'Kits with cooldowns, mastery tiers, streaks and vouchers.',
		requires: 'Paper or Folia 1.21 and 26.x',
		highlights: ['Placeholder conditions, team kits, points', 'Mastery, streaks and collection', 'Imports EssentialsX, UltimateKits'],
		install: '/kit',
	},
];
