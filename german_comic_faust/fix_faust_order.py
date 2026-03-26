#!/usr/bin/env python3
"""
fix_faust_order.py
==================
Fixes the scene order in the Faust comic HTML file.

Current (wrong):
  X   → Gretchenfrage   (scene-10)
  XI  → Garten          (scene-11)
  XII → Wald und Höhle  (scene-12)
  XIII→ Gretchenfrage   (scene-13)  ← duplicate, becomes the real one

Correct (Goethe canon):
  X   → Garten          (was scene-11)
  XI  → Wald und Höhle  (was scene-12)
  XII → Gretchenfrage   (was scene-13, the real Marthens Garten scene)
  XIII→ [deleted]       (was scene-10, wrong position duplicate)

Scenes XIV (Walpurgisnacht) and XV (Kerker) stay, renumbered to XIII and XIV.

Usage:
  python3 fix_faust_order.py index.html
  # writes index_fixed.html — review it, then rename manually.
"""

import re
import sys
import shutil
from pathlib import Path


ROMAN = ["I","II","III","IV","V","VI","VII","VIII","IX","X",
         "XI","XII","XIII","XIV","XV","XVI","XVII","XVIII","XIX","XX"]


def extract_scenes(html: str) -> list[tuple[int, int, str]]:
    """
    Returns list of (start, end, scene_html) for every .scene-wrapper div.
    start/end are character offsets into html.
    End is exclusive (points to the char after the closing </div>).
    """
    scenes = []
    pattern = re.compile(r'<div\s+id="scene-\d+"[^>]*class="scene-wrapper"')
    for m in pattern.finditer(html):
        start = m.start()
        # Walk forward counting open/close divs to find the matching close
        depth = 0
        i = start
        while i < len(html):
            open_m  = re.search(r'<div[\s>]', html[i:])
            close_m = re.search(r'</div>', html[i:])
            if open_m is None and close_m is None:
                raise ValueError(f"Unmatched div starting at offset {start}")
            use_open = (open_m is not None and
                        (close_m is None or open_m.start() < close_m.start()))
            if use_open:
                depth += 1
                i += open_m.start() + 1
            else:
                depth -= 1
                i += close_m.start() + len("</div>")
                if depth == 0:
                    scenes.append((start, i, html[start:i]))
                    break
    return scenes


def renumber_scene(scene_html: str, new_num: int) -> str:
    """
    Update id, data-scene, roman numeral, and scene-roman span inside one scene block.
    """
    roman = ROMAN[new_num - 1]

    # id="scene-N"
    scene_html = re.sub(
        r'id="scene-\d+"',
        f'id="scene-{new_num}"',
        scene_html, count=1
    )
    # data-scene="N"
    scene_html = re.sub(
        r'data-scene="\d+"',
        f'data-scene="{new_num}"',
        scene_html, count=1
    )
    # <span class="scene-roman">...</span>
    scene_html = re.sub(
        r'(<span class="scene-roman">)[^<]*(</span>)',
        rf'\g<1>{roman}\g<2>',
        scene_html, count=1
    )
    return scene_html


def fix_nav_dots(html: str, scene_order: list[tuple[int, str]]) -> str:
    """
    Rebuild the #scene-nav block to match the new order.
    scene_order: list of (new_num, title)
    """
    # Find the existing nav block
    nav_start = html.find('<nav id="scene-nav"')
    nav_end   = html.find('</nav>', nav_start) + len('</nav>')
    if nav_start == -1:
        print("  WARNING: could not find #scene-nav, skipping nav update")
        return html

    # Rebuild dots
    dots = ['<nav id="scene-nav" aria-label="Szenennavigation">']
    dots.append(f'    <a href="#cover" class="nav-dot active" data-scene="cover" title="Deckblatt">'
                f'<span class="nav-tooltip">Deckblatt</span>◆</a>')
    for new_num, title in scene_order:
        roman = ROMAN[new_num - 1]
        dots.append(
            f'    <a href="#scene-{new_num}" class="nav-dot" data-scene="{new_num}">'
            f'<span class="nav-tooltip">{title}</span>{roman}</a>'
        )
    dots.append('  </nav>')
    new_nav = '\n'.join(dots)

    return html[:nav_start] + new_nav + html[nav_end:]


def find_matching_div_end(html: str, start: int) -> int:
    """
    Given start pointing at an opening <div...>, return the index just after
    the matching </div>.
    """
    depth = 0
    i = start
    while i < len(html):
        open_m  = re.search(r'<div[\s>]', html[i:])
        close_m = re.search(r'</div>', html[i:])
        if open_m is None and close_m is None:
            raise ValueError(f"Unmatched div at offset {start}")
        use_open = (open_m is not None and
                    (close_m is None or open_m.start() < close_m.start()))
        if use_open:
            depth += 1
            i += open_m.start() + 1
        else:
            depth -= 1
            i += close_m.start() + len("</div>")
            if depth == 0:
                return i
    raise ValueError(f"No matching </div> found from offset {start}")


def fix_toc(html: str, scene_order: list[tuple[int, str, str, str]]) -> str:
    """
    Rebuild the .toc-grid block.
    scene_order: list of (new_num, title, quote, style_attrs)
    """
    toc_start = html.find('<div class="toc-grid">')
    if toc_start == -1:
        print("  WARNING: could not find .toc-grid, skipping TOC update")
        return html

    toc_end = find_matching_div_end(html, toc_start)
    toc_block = html[toc_start:toc_end]

    # Extract the cover card (always first) — use depth-aware extraction
    cover_start = toc_block.find('<div class="toc-card" data-target="cover"')
    cover_end   = find_matching_div_end(toc_block, cover_start)
    cover_card  = toc_block[cover_start:cover_end] if cover_start != -1 else ''

    cards = [f'<div class="toc-grid">', f'    {cover_card}']
    for new_num, title, quote, style in scene_order:
        roman = ROMAN[new_num - 1]
        cards.append(
            f'    <div class="toc-card" data-target="scene-{new_num}" {style}>'
            f'<div class="toc-card-roman">{roman}</div>'
            f'<div class="toc-card-title">{title}</div>'
            f'<div class="toc-card-quote">{quote}</div></div>'
        )
    cards.append('  </div>')
    new_toc = '\n'.join(cards)

    return html[:toc_start] + new_toc + html[toc_end:]


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fix_faust_order.py index.html")
        sys.exit(1)

    src = Path(sys.argv[1])
    if not src.exists():
        print(f"ERROR: {src} not found")
        sys.exit(1)

    out = src.with_name("index_fixed.html")
    shutil.copy(src, src.with_name("index.html.bak"))
    print(f"  Backup written: {src.with_name('index.html.bak')}")

    html = src.read_text(encoding="utf-8")

    # ── 1. Extract all 15 scene blocks ───────────────────────────────
    print("  Extracting scenes...")
    raw_scenes = extract_scenes(html)
    assert len(raw_scenes) == 15, f"Expected 15 scenes, got {len(raw_scenes)}"

    # Index 0-based: scene-1 = raw_scenes[0], ..., scene-15 = raw_scenes[14]
    # Current mapping (1-based scene numbers):
    #   scene-10 = Gretchenfrage (wrong position)  → DELETE
    #   scene-11 = Garten                          → becomes X  (new #10)
    #   scene-12 = Wald und Höhle                  → becomes XI (new #11)
    #   scene-13 = Gretchenfrage (Marthens Garten) → becomes XII (new #12)
    #   scene-14 = Walpurgisnacht                  → becomes XIII (new #13)
    #   scene-15 = Kerker                          → becomes XIV (new #14)
    #
    # Scenes 1-9 stay as-is.

    # New order of scene indices (0-based into raw_scenes):
    #   keep 0..8 (scenes 1-9), then 10, 11, 12, 13, 14  (skip index 9 = old scene-10)
    new_order_indices = list(range(9)) + [10, 11, 12, 13, 14]
    # That gives us 14 scenes total (15 minus the deleted duplicate)

    reordered = []
    for new_num, old_idx in enumerate(new_order_indices, start=1):
        scene_html = raw_scenes[old_idx][2]
        scene_html = renumber_scene(scene_html, new_num)
        reordered.append(scene_html)

    print(f"  Reordered {len(reordered)} scenes (deleted old scene-10 duplicate)")

    # ── 2. Splice reordered scenes back into HTML ─────────────────────
    # Replace everything from the first scene-wrapper to the last one's end
    first_start = raw_scenes[0][0]
    last_end    = raw_scenes[-1][1]

    new_scenes_block = "\n\n  ".join(reordered)
    html = html[:first_start] + "  " + new_scenes_block + "\n\n" + html[last_end:]

    # ── 3. Fix nav dots ───────────────────────────────────────────────
    print("  Updating nav dots...")
    scene_titles = [
        (1,  "Prolog im Himmel"),
        (2,  "Nacht – Erdgeist"),
        (3,  "Nacht – Suizidgedanke"),
        (4,  "Osterspaziergang"),
        (5,  "Der Pakt"),
        (6,  "Auerbachs Keller"),
        (7,  "Hexenküche"),
        (8,  "Straße – Erste Begegnung"),
        (9,  "Abend"),
        (10, "Garten"),
        (11, "Wald und Höhle"),
        (12, "Gretchenfrage"),
        (13, "Walpurgisnacht"),
        (14, "Kerker"),
    ]
    html = fix_nav_dots(html, scene_titles)

    # ── 4. Fix TOC ────────────────────────────────────────────────────
    print("  Updating TOC...")
    # Pull style attrs from original toc-cards so colours stay correct
    toc_card_pattern = re.compile(
        r'<div class="toc-card" data-target="scene-(\d+)"([^>]*)>'
        r'.*?<div class="toc-card-title">([^<]*)</div>'
        r'.*?<div class="toc-card-quote">([^<]*)</div>',
        re.DOTALL
    )
    orig_toc_data = {}
    for m in toc_card_pattern.finditer(html):
        num   = int(m.group(1))
        style = m.group(2).strip()
        title = m.group(3)
        quote = m.group(4)
        orig_toc_data[num] = (style, title, quote)

    # Build new TOC entries in new order
    # old scene numbers that map to new positions:
    old_nums_in_new_order = list(range(1, 10)) + [11, 12, 13, 14, 15]
    toc_entries = []
    new_titles_quotes = [
        ("Prolog im Himmel",        "»Die Wette gilt!«"),
        ("Nacht – Erdgeist",        "»Wer ruft mich?«"),
        ("Nacht – Suizidgedanke",   "»Laß mich den Rest hinuntertrinken!«"),
        ("Osterspaziergang",        "»Hier bin ich Mensch, hier darf ich's sein!«"),
        ("Der Pakt",                "»Werd ich zum Augenblicke sagen: Verweile doch!«"),
        ("Auerbachs Keller",        "»Ein solcher Mann hat seinen eigenen Verstand«"),
        ("Hexenküche",              "»Was seh ich? Welch ein himmlisch Bild!«"),
        ("Straße – Erste Begegnung","»Mein schönes Fräulein, darf ich wagen…«"),
        ("Abend",                   "»Wie atmet rings Gefühl der Stille!«"),
        ("Garten",                  "»Er liebt mich … liebt mich nicht …«"),
        ("Wald und Höhle",          "»Erhabner Geist, du gabst mir, gabst mir alles!«"),
        ("Gretchenfrage",           "»Wie hast du's mit der Religion?«"),
        ("Walpurgisnacht",          "»Die Welt geht unter!«"),
        ("Kerker",                  "»Heinrich! Mir graut's vor dir.«"),
    ]
    for new_num, (old_num, (title, quote)) in enumerate(
        zip(old_nums_in_new_order, new_titles_quotes), start=1
    ):
        style, _, _ = orig_toc_data.get(old_num, ('style="background-color:#111"', title, quote))
        toc_entries.append((new_num, title, quote, style))

    html = fix_toc(html, toc_entries)

    # ── 5. Write output ───────────────────────────────────────────────
    out.write_text(html, encoding="utf-8")
    print(f"\n  Done! Output: {out}")
    print("  Review index_fixed.html in browser, then:")
    print("    mv index_fixed.html index.html")


if __name__ == "__main__":
    main()
