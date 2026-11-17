#!/usr/bin/env python3
"""Audit a README for the things that break on GitHub and GitLab.

usage: audit_readme.py <README.md> [--host github|gitlab|both] [--strict]

Standard library only, Python 3.8 or later. Exits 1 when it finds an ERROR (or a
WARNING with --strict), 0 otherwise. It reads files; it never changes them and never
uses the network.
"""
import os
import re
import sys
import xml.etree.ElementTree as ET
from urllib.parse import unquote

FIRST_SCREEN_MAX_LINES = 45
MAX_BADGES = 5
MAX_README_LINES = 400
SVG_MAX_BYTES = 60 * 1024
RASTER_MAX_BYTES = 1024 * 1024
BADGE_HOSTS = ("img.shields.io", "badgen.net", "badge.fury.io", "/badges/", "/-/badges/", "/actions/workflows/")
PLACEHOLDERS = re.compile(r"\b(TODO|FIXME|TBD|lorem ipsum|OWNER/REPO|PROJECT_NAME|your-username|example\.com/your)\b", re.I)
HYPE = re.compile(r"\b(blazing(ly)?|seamless(ly)?|revolutionary|game[- ]chang\w+|cutting[- ]edge|world[- ]class|supercharge\w*|effortless(ly)?)\b", re.I)

MD_IMAGE = re.compile(r"!\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
MD_LINK = re.compile(r"(?<!!)\[([^\]]+)\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
HTML_TAG = re.compile(r"<(img|source|a)\b([^>]*)>", re.I)
ATTR = re.compile(r"([a-zA-Z-]+)\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+)")
FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
UNSAFE_SVG = {"script", "foreignObject", "iframe", "object", "embed", "animate", "animateTransform", "animateMotion", "set"}


def attrs(text):
    return {k.lower(): v.strip("\"'") for k, v in ATTR.findall(text)}


def is_remote(url):
    return url.startswith(("http://", "https://", "//", "mailto:", "data:", "tel:"))


def github_slug(text):
    """The anchor GitHub and GitLab give a heading (they agree for ordinary headings)."""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = text.replace("`", "").replace("*", "")
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    return text.replace(" ", "-")


def split_blocks(lines):
    """Yields (index, line, in_code) and collects fenced blocks as (start index, info string)."""
    out, fences, open_fence = [], [], None
    for i, line in enumerate(lines):
        m = FENCE.match(line)
        if m and open_fence is None:
            open_fence = (m.group(2)[0], len(m.group(2)))
            fences.append((i, m.group(3).strip()))
            out.append((i, line, True))
            continue
        if m and open_fence and m.group(2)[0] == open_fence[0] and len(m.group(2)) >= open_fence[1] and m.group(3).strip() == "":
            open_fence = None
            out.append((i, line, True))
            continue
        out.append((i, line, open_fence is not None))
    return out, fences, open_fence is not None


def audit_svg(path, report, base):
    name = os.path.relpath(path, base)
    size = os.path.getsize(path)
    if size > SVG_MAX_BYTES:
        report("WARNING", f"{name}: {size // 1024} KB is large for an SVG (aim under {SVG_MAX_BYTES // 1024} KB)")
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        report("ERROR", f"{name}: not valid XML ({exc})")
        return
    if "viewBox" not in root.attrib:
        report("ERROR", f"{name}: no viewBox, so it cannot scale")
    tags = [n.tag.rsplit("}", 1)[-1] for n in root.iter()]
    if "title" not in tags:
        report("WARNING", f"{name}: no <title> (screen readers and search get nothing)")
    for bad in sorted(UNSAFE_SVG.intersection(tags)):
        kind = "ERROR" if bad in ("script", "foreignObject", "iframe", "object", "embed") else "WARNING"
        why = "is removed or blocked by the host" if kind == "ERROR" else "does not play when the SVG is shown as an image"
        report(kind, f"{name}: <{bad}> {why}")
    for node in root.iter():
        for key, value in node.attrib.items():
            local = key.rsplit("}", 1)[-1]
            if local == "href" and value.startswith(("http://", "https://")) and node.tag.rsplit("}", 1)[-1] in ("image", "use"):
                report("ERROR", f"{name}: loads {value} from another site; hosts block that")
            if local.startswith("on"):
                report("ERROR", f"{name}: event handler attribute {local}")
        if node.tag.rsplit("}", 1)[-1] == "style" and node.text and ("@import" in node.text or "url(http" in node.text):
            report("ERROR", f"{name}: <style> loads an external resource (web fonts do not load)")
        if node.tag.rsplit("}", 1)[-1] == "text":
            size_attr = node.attrib.get("font-size")
            try:
                if size_attr and float(re.sub(r"[^\d.]", "", size_attr)) < 11:
                    report("WARNING", f"{name}: text at font-size {size_attr} will be unreadable when scaled down")
            except ValueError:
                pass


def main(argv):
    host, args, flags, rest = "both", [], [], list(argv[1:])
    while rest:
        a = rest.pop(0)
        if a == "--host" and rest:
            host = rest.pop(0)
        elif a.startswith("--host="):
            host = a.split("=", 1)[1]
        elif a.startswith("--"):
            flags.append(a)
        else:
            args.append(a)
    if len(args) != 1 or "--help" in flags:
        print(__doc__.strip())
        return 2
    if host not in ("github", "gitlab", "both"):
        print("--host must be github, gitlab or both")
        return 2
    readme = os.path.abspath(os.path.expanduser(args[0]))
    if not os.path.isfile(readme):
        print(f"ERROR: no such file: {readme}")
        return 2
    base = os.path.dirname(readme)
    found = []

    def report(level, message):
        if (level, message) not in found:
            found.append((level, message))

    text = open(readme, encoding="utf-8").read()
    lines = text.split("\n")
    marked, fences, unclosed = split_blocks(lines)
    prose = "\n".join(line for _, line, code in marked if not code)

    if unclosed:
        report("ERROR", "a code block is opened and never closed")
    for start, info in fences:
        if not info:
            report("WARNING", f"line {start + 1}: code block without a language (use text, sh, json, ...)")

    # headings and anchors
    slugs, counts, levels = set(), {}, []
    for i, line, code in marked:
        if code:
            continue
        m = HEADING.match(line)
        if not m:
            continue
        levels.append((i + 1, len(m.group(1))))
        slug = github_slug(m.group(2))
        n = counts.get(slug, 0)
        counts[slug] = n + 1
        slugs.add(slug if n == 0 else f"{slug}-{n}")
    for m in re.finditer(r"<(?:a|h[1-6]|p|div|span)\b[^>]*\b(?:id|name)\s*=\s*[\"']([^\"']+)[\"']", prose, re.I):
        slugs.add(m.group(1).lower())
    h1 = [n for n, level in levels if level == 1]
    if len(h1) > 1:
        report("WARNING", f"{len(h1)} top-level headings (lines {', '.join(map(str, h1))}); a README has one title")
    previous = 0
    for n, level in levels:
        if previous and level > previous + 1:
            report("WARNING", f"line {n}: heading jumps from level {previous} to {level}")
        previous = level

    # links and images
    images, links, tag_images = [], [], []
    for m in MD_IMAGE.finditer(prose):
        images.append((m.group(2), m.group(1), None, "markdown"))
    for m in MD_LINK.finditer(prose):
        links.append(m.group(2))
    for m in HTML_TAG.finditer(prose):
        tag, a = m.group(1).lower(), attrs(m.group(2))
        if tag == "img" and "src" in a:
            images.append((a["src"], a.get("alt"), a.get("width"), "html"))
            tag_images.append(a["src"])
        elif tag == "source" and "srcset" in a:
            for part in a["srcset"].split(","):
                images.append((part.strip().split(" ")[0], "(source)", "(source)", "source"))
        elif tag == "a" and "href" in a:
            links.append(a["href"])

    def check_target(url, what):
        if is_remote(url):
            if url.startswith("http://") and "localhost" not in url and "127.0.0.1" not in url:
                report("WARNING", f"{what} uses http://: {url}")
            return None
        path, _, fragment = url.partition("#")
        path = unquote(path.split("?", 1)[0])
        if not path:
            if fragment and fragment.lower() not in slugs:
                report("ERROR", f"{what} points at #{fragment}, and no heading has that anchor")
            return None
        if path.startswith("/"):
            report("WARNING", f"{what} uses an absolute path ({url}); a relative path works on every host and in forks")
            return None
        target = os.path.normpath(os.path.join(base, path))
        if not os.path.exists(target):
            report("ERROR", f"{what} points at {path}, which does not exist")
            return None
        return target

    for url in dict.fromkeys(links):
        check_target(url, "link")

    badges = 0
    seen_svgs = set()
    for src, alt, width, kind in images:
        if is_remote(src):
            if any(h in src for h in BADGE_HOSTS):
                badges += 1 if kind != "source" else 0
                if kind != "source" and not (alt or "").strip():
                    report("WARNING", f"badge without alt text: {src[:70]}")
            elif kind != "source":
                report("WARNING", f"image loaded from another site (it can vanish or be blocked): {src[:80]}")
            continue
        target = check_target(src, "image")
        if kind != "source":
            if alt is None or not alt.strip():
                report("ERROR", f"image without alt text: {src}")
            elif re.match(r"^(image|picture|screenshot|logo|banner|img)\d*$", alt.strip(), re.I):
                report("WARNING", f"alt text \"{alt}\" says nothing; describe what the image shows ({src})")
            if kind == "html" and not width:
                report("WARNING", f"<img> without a width: {src}")
        if not target:
            continue
        ext = os.path.splitext(target)[1].lower()
        if ext == ".svg" and target not in seen_svgs:
            seen_svgs.add(target)
            audit_svg(target, report, base)
        elif ext in (".png", ".jpg", ".jpeg", ".gif", ".webp") and os.path.getsize(target) > RASTER_MAX_BYTES:
            report("WARNING", f"{src}: {os.path.getsize(target) // 1024} KB is heavy for a README image")

    # light and dark variants
    local = [s for s, _, _, _ in images if not is_remote(s)]
    names = {os.path.normpath(os.path.join(base, unquote(s.split("#")[0]))) for s in local}
    for path in sorted(names):
        stem, ext = os.path.splitext(path)
        for a, b in (("-light", "-dark"), ("-dark", "-light")):
            if stem.endswith(a):
                partner = stem[: -len(a)] + b + ext
                if not os.path.exists(partner):
                    report("ERROR", f"{os.path.relpath(path, base)} has no {b[1:]} partner ({os.path.basename(partner)})")
                elif partner not in names:
                    report("WARNING", f"{os.path.basename(partner)} exists but the README never uses it")
    has_picture = "<picture" in prose.lower()
    if host in ("gitlab", "both") and has_picture:
        report("WARNING" if host == "both" else "ERROR",
               "<picture> with prefers-color-scheme is a GitHub feature; GitLab's documentation does not promise it. "
               "For GitLab use one image that carries its own background (see references/hosts.md)")
    if host in ("github", "both") and re.search(r"\)\{\s*(width|height)\s*=", prose):
        report("WARNING" if host == "both" else "ERROR",
               "the {width=...} image attribute is GitLab syntax and shows as plain text on GitHub; use <img width=...>")
    if host in ("github", "both") and re.search(r"^\s*(\[\[_TOC_\]\]|\[TOC\])\s*$", prose, re.M):
        report("WARNING" if host == "both" else "ERROR", "[[_TOC_]] / [TOC] is GitLab syntax and shows as plain text on GitHub")
    if host in ("gitlab", "both") and re.search(r"#gh-(dark|light)-mode-only", prose):
        report("WARNING" if host == "both" else "ERROR", "#gh-dark-mode-only / #gh-light-mode-only works on GitHub only")
    if badges > MAX_BADGES:
        report("WARNING", f"{badges} badges; more than {MAX_BADGES} reads as noise")

    # forbidden or useless markup
    if re.search(r"<(script|style|iframe)\b", prose, re.I):
        report("ERROR", "<script>, <style> and <iframe> are removed by the host")
    if re.search(r"<[a-z][^>]*\sstyle\s*=", prose, re.I):
        report("WARNING", "inline style attributes are removed by the host; use align and width instead")
    for i, line, code in marked:
        if code or not line.strip().startswith("<"):
            continue
        if re.match(r"^\s*</(p|div|picture|details|table)>\s*$", line, re.I) and i + 1 < len(lines) and lines[i + 1].strip() \
                and not lines[i + 1].lstrip().startswith("<"):
            report("WARNING", f"line {i + 2}: Markdown directly after an HTML block is not parsed; leave a blank line")

    # content
    for m in PLACEHOLDERS.finditer(prose):
        line_no = prose.count("\n", 0, m.start()) + 1
        report("ERROR", f"placeholder text left in the README: \"{m.group(0)}\" (near line {line_no} of the prose)")
    for word in sorted({m.group(0).lower() for m in HYPE.finditer(prose)}):
        report("WARNING", f"\"{word}\" is a claim without content; say what it does instead")
    if len(lines) > MAX_README_LINES:
        report("WARNING", f"{len(lines)} lines; move reference material to docs/ and link to it")

    first_heading_after = None
    title_seen = False
    for n, level in levels:
        if level == 1 and not title_seen:
            title_seen = True
            continue
        first_heading_after = n
        break
    if first_heading_after and first_heading_after - 1 > FIRST_SCREEN_MAX_LINES:
        report("WARNING", f"the first section starts at line {first_heading_after}; a visitor scrolls past "
                          f"{first_heading_after - 1} lines before any content (aim under {FIRST_SCREEN_MAX_LINES})")
    head = "\n".join(lines[: (first_heading_after or len(lines)) - 1])
    plain = re.sub(r"<[^>]+>|!\[[^\]]*\]\([^)]*\)|\[([^\]]*)\]\([^)]*\)", r"\1", head)
    plain = re.sub(r"^#.*$", "", plain, flags=re.M)
    if len(re.sub(r"[\W_]+", "", plain)) < 40:
        report("WARNING", "the first screen has no sentence that says what the project is")
    section_names = " ".join(github_slug(HEADING.match(l).group(2)) for _, l, c in marked if not c and HEADING.match(l))
    if "install" not in section_names and "getting-started" not in section_names and "quick-start" not in section_names \
            and "usage" not in section_names and "download" not in section_names:
        report("WARNING", "no Install, Quick start, Usage or Download section: how does a visitor try it?")
    if "license" not in section_names and "licence" not in section_names:
        report("WARNING", "no License section")

    order = {"ERROR": 0, "WARNING": 1}
    found.sort(key=lambda f: order[f[0]])
    for level, message in found:
        print(f"{level}: {message}")
    errors = sum(1 for level, _ in found if level == "ERROR")
    warnings = len(found) - errors
    svg_count = len(seen_svgs)
    print(f"\n{os.path.basename(readme)}: {errors} error(s), {warnings} warning(s); "
          f"{len(lines)} lines, {len(set(links))} links, {len(names)} local images ({svg_count} SVG checked), {badges} badges; host: {host}")
    return 1 if errors or (warnings and "--strict" in flags) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
