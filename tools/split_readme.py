import json
import pathlib
import re
import sys

FENCE = re.compile(r"^\s*(```|~~~)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def slugify(text):
    text = re.sub(r"<[^>]+>", "", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def parse(markdown):
    blocks = []
    current = {"level": 0, "title": "", "lines": []}
    fenced = False
    for line in markdown.splitlines():
        if FENCE.match(line):
            fenced = not fenced
        match = None if fenced else HEADING.match(line)
        if match and len(match.group(1)) in (2, 3):
            blocks.append(current)
            current = {"level": len(match.group(1)), "title": match.group(2), "lines": []}
        elif match and len(match.group(1)) == 1:
            continue
        else:
            current["lines"].append(line)
    blocks.append(current)
    return blocks


def sections(blocks):
    intro = blocks[0]["lines"]
    h2 = []
    for block in blocks[1:]:
        if block["level"] == 2:
            h2.append({"title": block["title"], "lines": block["lines"], "children": []})
        elif h2:
            h2[-1]["children"].append(block)
    return intro, h2


def shift(lines, amount):
    out = []
    fenced = False
    for line in lines:
        if FENCE.match(line):
            fenced = not fenced
        match = None if fenced else HEADING.match(line)
        if match and amount:
            level = max(2, len(match.group(1)) - amount)
            out.append("#" * level + " " + match.group(2))
        else:
            out.append(line)
    return out


def render(h2, keep_heading, excluded=frozenset()):
    lines = []
    if keep_heading:
        lines.append("## " + h2["title"])
    lines.extend(h2["lines"])
    for child in h2["children"]:
        if child["title"] in excluded:
            continue
        lines.append(("## " if not keep_heading else "### ") + child["title"])
        lines.extend(shift(child["lines"], 1 if not keep_heading else 0))
    return lines


def render_h3(child, keep_heading):
    lines = []
    if keep_heading:
        lines.append("## " + child["title"])
    lines.extend(shift(child["lines"], 1))
    return lines


def strip_rules(lines):
    cleaned = [line for line in lines if line.strip() not in ("---", "***")]
    while cleaned and not cleaned[0].strip():
        cleaned.pop(0)
    while cleaned and not cleaned[-1].strip():
        cleaned.pop()
    return cleaned


def main():
    config = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    readme = pathlib.Path(config["readme"]).read_text(encoding="utf-8")
    out = pathlib.Path(config["out"])
    out.mkdir(parents=True, exist_ok=True)
    intro, h2s = sections(parse(readme))
    by_title = {section["title"]: section for section in h2s}
    h3_index = {}
    for section in h2s:
        for child in section["children"]:
            h3_index[child["title"]] = (section, child)

    used = set(config.get("skip", []))
    taken_h3 = {part[4:] for page in config["pages"] for part in page["take"] if part.startswith("### ")}
    anchors = {}
    pages = []
    for order, page in enumerate(config["pages"]):
        parts = page["take"]
        single = len(parts) == 1 and parts[0] != "@intro"
        body = []
        for part in parts:
            if part == "@intro":
                body.extend(intro)
                continue
            if part.startswith("### "):
                title = part[4:]
                section, child = h3_index[title]
                used.add("### " + title)
                body.extend(render_h3(child, not single))
                anchors[slugify(title)] = (page["slug"], None if single else slugify(title))
                continue
            section = by_title[part]
            used.add(part)
            for child in section["children"]:
                if child["title"] in taken_h3:
                    continue
                used.add("### " + child["title"])
                anchors.setdefault(slugify(child["title"]), (page["slug"], slugify(child["title"])))
            body.extend(render(section, not single, taken_h3))
            anchors[slugify(part)] = (page["slug"], None if single else slugify(part))
        pages.append((order, page, strip_rules(body)))

    missing = []
    for section in h2s:
        if section["title"] in used:
            continue
        children = [("### " + child["title"]) in used for child in section["children"]]
        if not children or not all(children):
            missing.append(section["title"])
        elif any(line.strip() and line.strip() not in ("---", "***") for line in section["lines"]):
            missing.append(section["title"] + " (its own intro text)")
    if missing:
        raise SystemExit("unassigned sections: " + ", ".join(missing))

    base = config["base"]
    repo = config["repo"]

    def fix_links(text):
        def replace(match):
            label, target = match.group(1), match.group(2)
            if target.startswith("#"):
                found = anchors.get(target[1:])
                if found is None:
                    return label
                slug, anchor = found
                url = f"{base}{slug}/" if slug else base
                return f"[{label}]({url}{'#' + anchor if anchor else ''})"
            if re.match(r"^[a-z]+://", target) or target.startswith("mailto:"):
                return match.group(0)
            return f"[{label}](https://github.com/SpirtySprite/{repo}/blob/main/{target})"
        return re.sub(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)\)", replace, text)

    for order, page, lines in pages:
        text = fix_links("\n".join(lines))
        text = re.sub(r"\s*[—–]\s*", ", ", text)
        if config.get("version"):
            text = re.sub(r"<version>[^<]*</version>", f"<version>{config['version']}</version>", text)
            text = re.sub(r"(com\.github\.SpirtySprite:[\w-]+:)[\w.]+", r"\g<1>" + config["version"], text)
            text = text.replace("</dependency\n", "</dependency>\n")
        front = ["---", f"title: {json.dumps(page['title'])}"]
        if page.get("description"):
            front.append(f"description: {json.dumps(page['description'])}")
        front.append("sidebar:")
        front.append(f"  order: {order}")
        if page.get("label"):
            front.append(f"  label: {json.dumps(page['label'])}")
        front.append("---")
        name = "index.md" if page["slug"] == "" else page["slug"] + ".md"
        (out / name).write_text("\n".join(front) + "\n\n" + text.strip() + "\n", encoding="utf-8", newline="\n")
    print(config["out"], len(pages), "pages")


main()
