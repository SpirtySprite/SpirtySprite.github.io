# KiruProject

The home page and wiki for my Paper and Folia libraries and plugins, live at
[spirtysprite.github.io](https://spirtysprite.github.io).

- `/` is the home page, `src/pages/index.astro`.
- `/wiki/` is the documentation, built with [Starlight](https://starlight.astro.build): search with
  <kbd>Ctrl</kbd> <kbd>K</kbd>, a sidebar per project and the sections of each page on the right.

Every push to `main` is built and published by `.github/workflows/deploy.yml`.

## Local development

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # static site in dist/
```

## Updating the wiki from the READMEs

The wiki pages under `src/content/docs/wiki/` are generated from each project's README. The maps in
`tools/wiki/*.json` decide which README sections go on which page:

```bash
python tools/split_readme.py tools/wiki/foliagui.json
```

The script refuses to run if a README section is not placed on any page, pins the install snippets
to the version in the map, and turns links between sections into links between wiki pages.

Project names, versions and summaries for the home page live in `src/data/projects.ts`.
