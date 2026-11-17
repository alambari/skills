# Visuals

GitHub and GitLab show a README on a white page and on a near-black page, on a desktop about 900 px wide and on a phone about 360 px wide. Every image has to survive all four. This file describes GitHub's behaviour in detail; `hosts.md` lists what GitLab does differently.

## What GitHub renders

Reliable: Markdown, tables, code blocks, `<details>`, `<p align="center">`, `<img>` with `width`, `<picture>` with `prefers-color-scheme`, `<kbd>`, `<sub>`, `<br>`, local images, GIF animation.

Stripped or ignored: `<style>`, `class`, inline `style`, `<script>`, iframes, CSS in Markdown. Animation inside an SVG does not play. An SVG is shown as an image, so links inside it do nothing.

## Light and dark

Preferred: two files and `<picture>`. GitHub switches them with the visitor's theme.

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/flow-dark.svg">
  <img src="assets/readme/flow-light.svg" alt="What the picture shows, in one sentence" width="760">
</picture>
```

Name the pair `<name>-light.svg` and `<name>-dark.svg`. Keep geometry identical; change only colours.

The portable form, and the one to use on GitLab: one file that paints its own background, so the page colour never shows through (`templates/card.svg`, `templates/wordmark.svg`). Check it on both pages anyway: a white card on a black page needs a border.

Never ship one transparent image with dark text only (it vanishes in dark mode) or light text only.

## Colours

- One accent, from the project's brand if it has one. Otherwise pick one hue and keep it everywhere.
- Light page: text `#1f2328`, muted `#59636e`, lines `#d1d9e0`, surfaces `#f6f8fa`.
- Dark page: text `#f0f6fc`, muted `#9198a1`, lines `#3d444d`, surfaces `#151b23`.
- The accent usually needs a lighter tint on the dark page to keep contrast (for example `#2f6feb` light, `#4493f8` dark).
- Text on a filled shape needs a contrast of at least 4.5 to 1.

## SVG rules

- `viewBox` always; `width`/`height` on the `<svg>` are optional because the README sets the display width.
- `<title>` and `<desc>` as the first children.
- Fonts: a system stack, `font-family="ui-sans-serif, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"` (or `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`). No web fonts: they do not load.
- Text is real `<text>`, large enough to read when the image is scaled down: at a 760-unit-wide viewBox shown 760 px wide, labels at 14 or more, titles at 18 or more. On a phone the image is about half that width, so keep labels short and few.
- Only shapes, paths, text, gradients, clip paths, simple transforms. No `<script>`, `<foreignObject>`, external images, external stylesheets, heavy filters.
- Round coordinates to whole or half units; one corner radius (`rx`) throughout; one line weight.
- Keep each file under about 20 KB. A logo is usually under 2 KB.

## The mark

Use the project's own logo if it has one. If it has none, do not design a mascot: start from `templates/wordmark-light.svg` and `templates/wordmark-dark.svg` (GitHub), or `templates/wordmark.svg` (portable): a small geometric glyph in the accent colour plus the name in a heavy system font. Display width 180 to 260 px.

## Hero

Optional. A hero earns its place only when it shows the product: a real screenshot, a real terminal session, or the one diagram that explains the idea. Display it at `width="900"` at most (GitHub will scale it down). A decorative banner with a tagline is not a hero; the centred mark and the sentence already do that job.

Screenshots: take them from the real product, crop the noise, keep them under about 500 KB (PNG for UI, JPEG or WebP for photos). Give light and dark versions when the product has both. Never fake one.

Terminal captures: a code block with the real output is searchable and copyable, and usually better than an image.

## Badges

- At most five. Each one states a fact a visitor checks: latest release, license, CI status, package version, supported platforms.
- One style for all of them (the default flat style, or `for-the-badge` when the mark is large), one label colour.
- Only for services the repository really uses. A CI badge needs a workflow; a version badge needs a published package or a release.
- Useful shields.io endpoints: `github/v/release/OWNER/REPO`, `github/license/OWNER/REPO`, `github/actions/workflow/status/OWNER/REPO/FILE.yml`, `npm/v/NAME`, `pypi/v/NAME`, `crates/v/NAME`. A static one: `badge/LABEL-MESSAGE-COLOR`.
- Every badge is a link to the thing it reports, and has alt text.

## Diagrams

Start from `templates/flow-light.svg` and `templates/flow-dark.svg` (GitHub), or `templates/card.svg` (portable), for a left-to-right flow of three to six steps. A Mermaid block renders on both hosts and follows the page theme by itself: use it when the default look is acceptable.

- The boxes carry the project's real names (commands, components, files), not generic words.
- One reading direction. Arrows mean one thing.
- The accent marks the one box that matters most; everything else is neutral.
- If the mechanism needs more than about seven boxes, it is two diagrams or a paragraph.
- An ASCII diagram in a code block is fully legitimate: it is text, it works in every theme, and it diffs. Prefer it for call paths and pipelines.

## Layout in Markdown

```html
<p align="center">
  <picture>…</picture>
</p>
```

- Set `width` on every `<img>` so the layout does not jump while loading and large images do not blow up.
- Put a blank line before and after every HTML block, or the Markdown after it is not parsed.
- A horizontal rule (`---`) once, between the first screen and the body.

## Checking the result

- Run `scripts/audit_readme.py` on the README.
- Render each SVG to a bitmap and look at it (macOS: `qlmanage -t -s 1200 -o <out dir> file.svg`; elsewhere `rsvg-convert`, Inkscape or a browser screenshot). Check both theme variants, and imagine it at half width. A dark variant is transparent, so to see it as the dark page shows it, render a temporary copy with `<rect width="100%" height="100%" fill="#0d1117"/>` as its first shape; delete the copy afterwards.
- Read the alt texts in a row: together they should tell the story the images tell.
