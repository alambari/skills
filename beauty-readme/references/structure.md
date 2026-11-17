# Structure

## The first screen

A visitor decides in about ten seconds. Above the first horizontal rule they should see, and nothing else:

```html
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/readme/logo-dark.svg">
    <img src="assets/readme/logo-light.svg" alt="PROJECT" width="220">
  </picture>
</p>

<p align="center">
  <b>One sentence: what it is and for whom.</b><br>
  One more line only if it removes a doubt (what it works with, what it replaces).
</p>

<p align="center">
  <a href="#install">Install</a> ·
  <a href="#quick-start">Quick start</a> ·
  <a href="#how-it-works">How it works</a> ·
  <a href="docs/">Docs</a>
</p>

<p align="center">
  <!-- at most five badges -->
</p>
```

On GitLab, replace the `<picture>` block with one `<img>` that carries its own background (`hosts.md`).

A plain `# name` heading followed by the sentence and the badges is just as good for a small tool. Centre the block only when there is a mark or a hero to centre it around.

The one sentence: name the thing by its category ("a container runtime", "a skill for coding agents"), say the outcome, and stop. Test it by reading it alone: a stranger must be able to tell whether the project is for them.

## Section order by project type

Use the order; drop a section that has nothing true to say.

**Command-line tool**
Why · Install · Quick start (three commands and the real output) · Commands (a table, or a link) · Numbers · How it works · Configuration · Platform support · Documentation · Contributing · License

**Library or SDK**
Why · Install · Usage (the smallest program that works) · API at a glance (link to the full reference) · Compatibility · How it works · Documentation · Contributing · License

**Plugin, extension or agent skill**
What it does · When it helps and when it does not · Install (one block per host, with a tested / untested column) · How it works · Configuration · Measured results · Safety (what it touches, what it never does) · Changelog pointer · License

**Application**
A screenshot · Why · Download or install · First run · Features (short, grouped) · Numbers · How it works · Roadmap · Contributing · License

**Framework or large project**
Why · Getting started (link out early) · A table of contents (only here, only when the page is long) · Concepts · Ecosystem · Community · Contributing · License

## Sections

- **Why**: three to six bullets. Bold lead word, then a concrete fact. "**Fast**: starts in 2.5 ms, about 80 times faster than X" beats "blazingly fast".
- **Install**: the shortest path that works, in one code block. Alternatives after it, in a sentence or a small table. Requirements in one line.
- **Quick start**: commands in the order a person types them, with a short comment per line and the output of the last one.
- **Numbers**: a table with the alternative next to the project, the unit in the header, right-aligned figures, and one line below saying how they were measured and where the raw data is. Also say what the numbers do not show.
- **How it works**: a diagram plus one short paragraph. The mechanism in the project's own terms, not a list of technologies.
- **Limits**: either their own short section or one honest bullet in "When it helps". Never hidden.
- **Documentation**: a list of links with half a line each.
- **License**: one line with a link.

## Length and layout

- The whole README fits in roughly 150 to 250 lines of Markdown. Past that, move reference material to `docs/`.
- No table of contents under about 300 lines; GitHub already shows an outline.
- One idea per paragraph, at most four lines. Bullets for parallel facts, tables for comparisons, code blocks for anything typed.
- Use `<details>` for long optional material (every platform's install variant, a full config reference).
- Headings are plain words in sentence case. No emoji as headings; an emoji is never the only carrier of meaning.
- Tables with long prose break on phones: keep cells short.

## Words

- Plain, specific, present tense. "Runs your Docker images" not "A solution enabling containerised workloads".
- "You" for the reader. No "we are excited", "simply", "just", "blazingly", "seamless", "powerful".
- A term the reader may not know is explained once, in passing.
- Numbers carry their unit and their condition ("median of 30 runs").
