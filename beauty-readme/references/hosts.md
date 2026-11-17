# GitHub and GitLab

Find the host from the git remote (`git remote -v`): `github.com`, `gitlab.com`, or a self-managed GitLab. A repository mirrored to both, or one whose host you cannot tell, gets the portable form.

Everything in this file about GitLab is taken from GitLab's own documentation (GitLab Flavored Markdown and Project badges). Where that documentation is silent, this file says so: treat those points as unknown and check them in GitLab's Markdown preview before relying on them. GitLab's docs also warn that the only exact check is the preview inside GitLab itself.

## What both render the same way

Headings, paragraphs, lists, tables, fenced code blocks with a language, links, relative links to files in the repository, relative image paths, `<details>` and `<summary>`, `<kbd>`, `<sub>`, `<sup>`, `<br>`, `<img>` with `width` and `height`, emoji shortcodes, task lists, footnotes, math, Mermaid diagrams in a `mermaid` code block, and alerts written as `> [!NOTE]` (GitLab since 17.10).

Heading anchors follow the same rule on both: lower case, everything except letters, digits, hyphens and underscores removed, spaces to hyphens, a number appended to a repeated heading. So `[Install](#install)` and `[Quick start](#quick-start)` work on both.

## Where they differ

| Need | GitHub | GitLab | Portable choice |
|---|---|---|---|
| A different image in light and dark mode | `<picture>` with `<source media="(prefers-color-scheme: dark)">` | not documented | one image that paints its own background |
| Image size | `<img width="…">` | `<img width="…">`, or `![alt](path){width=75%}` | `<img width="…">` |
| Centred block | `<p align="center">` | the `align` attribute is not documented | `<p align="center">`, then check in the GitLab preview; the page must still read well left-aligned |
| Table of contents | none (the page has an outline button) | `[[_TOC_]]` or `[TOC]` on its own line | none; keep the README short |
| Other diagram languages | Mermaid only | Mermaid, PlantUML (on GitLab.com), Kroki when an administrator enabled it | Mermaid, or an SVG, or ASCII |
| Video | drag-and-drop upload only | an image link to `.mp4`, `.webm`, `.mov` becomes a player | a GIF, or a link |
| Issue and merge request references | `#123` | `#123` also links; write `\#123` to stop it | — |
| Multi-line quote | `>` on each line | `>` on each line, or a block fenced by `>>>` | `>` on each line |
| Pulling another file in | no | `::include{file=path.md}` | no |

GitLab-only syntax (`{width=…}`, `[[_TOC_]]`, `>>>`, `::include`, `[- removed -]`/`{+ added +}`) shows as literal text on GitHub. GitHub-only features (`<picture>` theme switching, `#gh-dark-mode-only` image fragments) are not promised by GitLab. `scripts/audit_readme.py --host both` (the default) flags each of them.

## Light and dark on GitLab

Because GitLab does not document a theme switch for images, an image there must look right on a white page and on a dark page at once:

- give the SVG its own background: a rounded rectangle in a surface colour with a thin border, and put the content on it (`templates/card.svg`); or
- for a small mark, use colours that hold on both pages: a filled accent shape with white inside it, and no bare dark or bare light text outside the shape.

The same single file works on GitHub too, so it is the portable form. Use the `-light` / `-dark` pair with `<picture>` only for a repository that lives on GitHub alone.

## Badges

GitHub repositories usually use shields.io: `https://img.shields.io/github/v/release/OWNER/REPO`, `…/github/license/OWNER/REPO`, `…/github/actions/workflow/status/OWNER/REPO/FILE.yml`.

GitLab serves its own badge images:

```text
https://gitlab.example.com/<namespace>/<project>/badges/<branch>/pipeline.svg
https://gitlab.example.com/<namespace>/<project>/badges/<branch>/coverage.svg
https://gitlab.example.com/<namespace>/<project>/-/badges/release.svg
```

Useful parameters: `style=flat-square`, `key_text=<text>`, `key_width=<n>`, `value_width=<n>`, `ignore_skipped=true` (pipeline), `job=<name>` (coverage). Link the pipeline badge to `https://gitlab.example.com/<namespace>/<project>/-/commits/<branch>`.

In a README, write them as ordinary images: `[![pipeline](…/badges/main/pipeline.svg)](…/-/commits/main)`. GitLab can also show badges under the project description (Settings > General > Badges); those are separate from the README, so do not repeat the same ones in both places. A private project's badge images are not visible to people who cannot see the project.

## Links between files

Use relative paths on both hosts (`docs/usage.md`, `LICENSE`, `assets/readme/flow.svg`). An absolute path that starts with `/`, or a full URL to the repository's own files, breaks in forks and on mirrors. A wiki cannot be reached from a repository file with a relative link on GitLab.

## Checking

- GitHub: push to a branch and open the README there, in light and dark theme, and narrow the window.
- GitLab: paste the README into any Markdown preview in the project, or view the branch. Switch the theme under Preferences to check both.
- Before either, run the audit with the right `--host`.
