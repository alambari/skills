---
name: beauty-readme
description: Write or redesign a repository README so a first-time visitor understands the project in ten seconds and can try it in one minute, and so the page looks deliberate on GitHub and on GitLab, in light and dark mode. Use when the user asks to beautify, redesign, polish, restructure or audit a README, to make a README "like" another project's, or to add a logo, hero, badges or a diagram to one. Works in any coding agent; needs only file access, a shell and python3.
---

# beauty-readme

A good README is a short, honest page that answers three questions in order: what is this, why would I want it, how do I try it. Looks come second and serve that order. The pages people admire (a centred mark, one sentence, a few badges, a real screenshot, a table of real numbers) are restrained: nearly all of their effect is structure and true content.

Follow the steps in order. Do not skip step 1 and do not start with visuals.

## 1. Read the project before writing a word

Collect facts from the repository, not from the old README alone:

- the manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, a plugin manifest): name, version, license, entry points, supported runtimes;
- how it is really installed and run: scripts, CLI `--help`, a `Makefile`, CI files;
- tests, benchmarks or result files that hold real numbers;
- existing docs, screenshots, logos, brand colours;
- the git remote: the host (GitHub, GitLab, or both), the owner and repository name for badges and links, and whether there are releases or tags.

Write down, for yourself, one line each: what it is, who it is for, the one thing it does better than the alternative, the shortest command that shows it working, and what it does not do. If you cannot fill a line from the repository, ask the user that one question; do not invent it.

## 2. Decide the scope

- **Full**: structure, text and visuals. The default when the user says "beautify" or "redesign".
- **Polish**: keep the text, fix the order, the first screen and the formatting.
- **Assets only**: a logo, hero or diagram for a README that is otherwise staying.

Pick from the request. Ask only when the request truly fits two of these.

## 3. Build the structure

Read `references/structure.md` and choose the section order for the project type (CLI, library, plugin or skill, app, framework). The first screen is fixed for every type:

1. the mark: a logo or the project name, centred;
2. **one sentence** that says what it is and for whom, in plain words;
3. three to five links to the places a visitor goes next;
4. at most five badges that each state a fact a visitor would check;
5. one visual that proves the claim (a screenshot, a short terminal capture, a diagram), or none at all if there is nothing real to show.

Then: why (three to six bullets, each a concrete outcome, numbers where the project has them), install, quick start, the evidence (numbers, comparison), how it works, reference links, limits, contributing, license.

## 4. Write the text

- Lead every section with its answer. No "Welcome to", no "This project aims to".
- A claim needs a number, an example or a link. Cut the ones that have none.
- Every command is copied from something you ran or read in the repository, with the output it really gives.
- State the limits where they change a visitor's decision ("not for small jobs", "macOS only"). An honest limit makes the rest believable.
- Explain a term the first time it appears, or use a plainer word.
- Long reference material (every flag, every config key) moves to `docs/` or under `<details>`; the README links to it.
- Keep what was true and useful in the old README. Never drop install steps, license or security notes while restyling.

## 5. Add the visual layer

Read `references/visuals.md`, and `references/hosts.md` for what GitHub and GitLab each render. Rules that always hold:

- Everything a visitor must copy, search or translate stays as text. Images carry identity, shape and proof only.
- Each image works on a light and on a dark page. On GitHub alone: two files switched with `<picture>`. On GitLab, or when the repository lives on both: one file that carries its own background, because GitLab does not document a theme switch for images.
- A project with no mark gets a simple wordmark from `templates/`, not a mascot or a stock illustration.
- One accent colour, taken from the project's existing brand if it has one, used in the mark, the badges and the diagram.
- Diagrams show the real mechanism with the project's real names. An ASCII diagram in a code block is often the better choice.
- Assets live in `assets/readme/` (or the repository's existing asset folder) with lowercase hyphenated names. No external image hosts except badge services.

## 6. Never invent

No made-up stars, users, testimonials, benchmark figures, "trusted by" logos, download counts or version numbers. No badge for a service the repository does not use. No screenshot of something that does not exist. If the project has no numbers, the README has no numbers section.

## 7. Check before handing over

Run the audit and fix everything it reports:

```
python3 <this skill's directory>/scripts/audit_readme.py <path to README.md> --host github|gitlab|both
```

It checks that local links, images and heading anchors resolve, that images have alt text and a width, that light and dark variants come in pairs, that SVG files are safe to show as images, that no syntax is used that only the other host understands, that code blocks name their language, that no placeholder text is left, and that the first screen is short enough. Then look at the result yourself: render the SVG files (or open the page) and read the first screen as a stranger would. If the one sentence does not make sense without the rest of the page, rewrite it.

## 8. Hand over

Say what changed in three or four lines, list the new asset files, name anything you could not verify (a badge that needs a published package, a screenshot the user must take), and stop. Committing and pushing are the user's decision unless they already asked for them.
