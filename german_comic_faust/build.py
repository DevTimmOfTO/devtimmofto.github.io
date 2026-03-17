#!/usr/bin/env python3
"""Build Faust Pop Art Comic – generates index.html"""

import re, os

BASE = os.path.dirname(os.path.abspath(__file__)) + '/'

# ─────────────────────────────────────────────
# Scene metadata
# ─────────────────────────────────────────────
SCENES = [
    {
        'file':   'faust_prolog_im_himmel.svg',
        'title':  'Prolog im Himmel',
        'roman':  'I',
        'quote':  '»Die Wette gilt!«',
        'speaker':'Mephisto',
        'bg':     '#0C0A1C',
        'accent': '#D4AF37',
        'dot':    'rgba(212,175,55,0.18)',
    },
    {
        'file':   'faust_nacht_erdgeist.svg',
        'title':  'Nacht – Erdgeist',
        'roman':  'II',
        'quote':  '»Wer ruft mich?«',
        'speaker':'Erdgeist',
        'bg':     '#160A28',
        'accent': '#9B30D0',
        'dot':    'rgba(155,48,208,0.18)',
    },
    {
        'file':   'faust_nacht_suizidgedanke.svg',
        'title':  'Nacht – Suizidgedanke',
        'roman':  'III',
        'quote':  '»Laß mich den Rest hinuntertrinken!«',
        'speaker':'Faust',
        'bg':     '#060614',
        'accent': '#4488CC',
        'dot':    'rgba(68,136,204,0.18)',
    },
    {
        'file':   'faust_osterspaziergang.svg',
        'title':  'Osterspaziergang',
        'roman':  'IV',
        'quote':  '»Hier bin ich Mensch, hier darf ich\'s sein!«',
        'speaker':'Faust',
        'bg':     '#081208',
        'accent': '#5AA020',
        'dot':    'rgba(90,160,32,0.18)',
    },
    {
        'file':   'faust_der_pakt.svg',
        'title':  'Der Pakt',
        'roman':  'V',
        'quote':  '»Werd ich zum Augenblicke sagen: Verweile doch!«',
        'speaker':'Faust',
        'bg':     '#180505',
        'accent': '#CC2200',
        'dot':    'rgba(204,34,0,0.18)',
    },
    {
        'file':   'faust_auerbachs_keller_v2.svg',
        'title':  'Auerbachs Keller',
        'roman':  'VI',
        'quote':  '»Ich bin der Geist, der stets verneint!«',
        'speaker':'Mephisto',
        'bg':     '#120900',
        'accent': '#C89010',
        'dot':    'rgba(200,144,16,0.18)',
    },
    {
        'file':   'faust_hexenkueche.svg',
        'title':  'Hexenküche',
        'roman':  'VII',
        'quote':  '»Was seh ich? Welch ein himmlisch Bild!«',
        'speaker':'Faust',
        'bg':     '#040C06',
        'accent': '#28A030',
        'dot':    'rgba(40,160,48,0.18)',
    },
    {
        'file':   'faust_strasse_erste_begegnung_v2.svg',
        'title':  'Straße – Erste Begegnung',
        'roman':  'VIII',
        'quote':  '»Mein schönes Fräulein, darf ich wagen…«',
        'speaker':'Faust',
        'bg':     '#100818',
        'accent': '#E05828',
        'dot':    'rgba(224,88,40,0.18)',
    },
    {
        'file':   'faust_abend.svg',
        'title':  'Abend',
        'roman':  'IX',
        'quote':  '»Wie atmet rings Gefühl der Stille!«',
        'speaker':'Faust',
        'bg':     '#120A00',
        'accent': '#D4901A',
        'dot':    'rgba(212,144,26,0.18)',
    },
    {
        'file':   'faust_gretchenfrage.svg',
        'title':  'Gretchenfrage',
        'roman':  'X',
        'quote':  '»Wie hast du\'s mit der Religion?«',
        'speaker':'Gretchen',
        'bg':     '#160A12',
        'accent': '#C06080',
        'dot':    'rgba(192,96,128,0.18)',
    },
    {
        'file':   'faust_garten.svg',
        'title':  'Garten',
        'roman':  'XI',
        'quote':  '»Er liebt mich … liebt mich nicht …«',
        'speaker':'Gretchen',
        'bg':     '#060E06',
        'accent': '#70B030',
        'dot':    'rgba(112,176,48,0.18)',
    },
    {
        'file':   'faust_kerker.svg',
        'title':  'Kerker',
        'roman':  'XII',
        'quote':  '»Heinrich! Mir graut\'s vor dir.«',
        'speaker':'Gretchen',
        'bg':     '#060810',
        'accent': '#3355AA',
        'dot':    'rgba(51,85,170,0.18)',
    },
]


# ─────────────────────────────────────────────
# SVG processing
# ─────────────────────────────────────────────

def process_svg(filepath, scene_idx):
    """Read SVG, prefix IDs, mark speech bubbles, return (inner_html, viewbox)."""
    with open(filepath) as f:
        raw = f.read()

    # Extract viewBox
    vb_m = re.search(r'viewBox="([^"]+)"', raw)
    viewbox = vb_m.group(1) if vb_m else '0 0 680 550'

    pfx = f's{scene_idx}'

    # ── 1. Unique IDs ───────────────────────────────────────────────
    def prefix_id(m):
        return f'id="{pfx}-{m.group(1)}"'

    def prefix_ref(m):
        return f'url(#{pfx}-{m.group(1)})'

    def prefix_href(m):
        return f'href="#{pfx}-{m.group(1)}"'

    raw = re.sub(r'\bid="([^"]+)"', prefix_id, raw)
    raw = re.sub(r'url\(#([^)]+)\)', prefix_ref, raw)
    raw = re.sub(r'href="#([^"]+)"', prefix_href, raw)

    # ── 2. Mark speech-bubble section ───────────────────────────────
    # Find the FIRST "SPEECH BUBBLE" comment and mark elements that follow
    bubble_re = re.compile(r'<!--[^-]*(?:speech\s+bubble|SPEECH\s*BUBBLE|Mephisto speech|Faust speech|Wagner speech|God\'s speech|scene label)[^-]*-->', re.IGNORECASE)
    m = bubble_re.search(raw)
    if m:
        before = raw[:m.start()]
        after  = raw[m.start():]
        # Add data-bubble="1" to every opening SVG element in the remainder
        after = re.sub(
            r'<(g|rect|path|circle|ellipse|text|polygon|line)\s',
            r'<\1 data-bubble="1" ',
            after
        )
        raw = before + after

    # ── 3. Strip outer <svg …> … </svg> wrapper ─────────────────────
    inner = re.sub(r'^<svg[^>]*>\s*', '', raw).strip()
    inner = re.sub(r'\s*</svg>\s*$', '', inner).strip()

    return inner, viewbox


# ─────────────────────────────────────────────
# HTML / CSS / JS construction
# ─────────────────────────────────────────────

CSS = r"""
/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

body {
  background: #0A0A14;
  color: #f0e8d0;
  font-family: Georgia, 'Times New Roman', serif;
  overflow-x: hidden;
}

/* ── Progress bar ── */
#progress-bar {
  position: fixed;
  top: 0; left: 0;
  height: 4px;
  width: 0%;
  background: linear-gradient(90deg, #D4AF37, #CC2200, #D4AF37);
  background-size: 200% 100%;
  animation: pb-shimmer 3s linear infinite;
  z-index: 9999;
  transition: width 0.12s linear;
  pointer-events: none;
}
@keyframes pb-shimmer {
  0%   { background-position: 100% 0; }
  100% { background-position: -100% 0; }
}

/* ── Scene nav ── */
#scene-nav {
  position: fixed;
  right: 18px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 900;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-dot {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 2px solid rgba(255,255,255,0.25);
  background: rgba(0,0,0,0.6);
  color: rgba(255,255,255,0.5);
  font-size: 9px;
  font-family: Georgia, serif;
  font-weight: bold;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}
.nav-dot:hover,
.nav-dot.active {
  border-color: var(--nav-accent, #D4AF37);
  color: var(--nav-accent, #D4AF37);
  background: rgba(0,0,0,0.85);
  transform: scale(1.25);
}
.nav-dot .nav-tooltip {
  position: absolute;
  right: 38px;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0,0,0,0.9);
  border: 1px solid rgba(255,255,255,0.2);
  color: #f0e8d0;
  font-size: 11px;
  white-space: nowrap;
  padding: 4px 10px;
  border-radius: 3px;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s;
}
.nav-dot:hover .nav-tooltip { opacity: 1; }

/* ── Panels (shared) ── */
.panel {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* ── Halftone overlay ── */
.halftone {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, var(--dot-color) 1.5px, transparent 1.5px);
  background-size: 14px 14px;
  pointer-events: none;
  z-index: 1;
}

/* ── COVER ── */
#cover {
  background: #08060E;
  padding: 0;
}
.cover-inner {
  position: relative;
  z-index: 2;
  width: min(500px, 88vw);
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: coverFadeUp 1.4s cubic-bezier(0.22,1,0.36,1) forwards;
}
.cover-inner svg {
  width: 100%;
  height: auto;
  max-height: 88vh;
  display: block;
  filter: drop-shadow(0 0 50px rgba(212,175,55,0.4)) drop-shadow(0 0 120px rgba(100,50,200,0.25));
}
@keyframes coverFadeUp {
  from { opacity: 0; transform: translateY(50px); }
  to   { opacity: 1; transform: translateY(0); }
}
.cover-scroll-hint {
  position: absolute;
  bottom: 28px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: rgba(212,175,55,0.7);
  font-size: 11px;
  letter-spacing: 3px;
  text-transform: uppercase;
  animation: bounce 2s ease-in-out infinite;
}
.cover-scroll-hint svg { opacity: 0.7; }
@keyframes bounce {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50%       { transform: translateX(-50%) translateY(8px); }
}

/* ── Scene panels ── */
.scene-panel {
  padding: 40px 20px 100px;
  gap: 0;
}

.svg-frame {
  position: relative;
  z-index: 3;
  width: min(680px, 92vw);
  flex-shrink: 0;
  border: 5px solid #000;
  outline: 2px solid rgba(255,255,255,0.08);
  box-shadow:
    6px 6px 0 #000,
    12px 12px 0 rgba(0,0,0,0.5),
    0 0 60px rgba(0,0,0,0.8),
    0 0 80px rgba(0,0,0,0.6),
    inset 0 0 0 2px rgba(0,0,0,0.3);
  background: #fff;
  overflow: hidden;
}
.svg-frame svg {
  width: 100%;
  height: auto;
  display: block;
}

/* ── Scene label bar ── */
.scene-label {
  position: absolute;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 14px;
  border: 3px solid var(--accent);
  background: rgba(0,0,0,0.88);
  padding: 8px 22px 8px 16px;
  white-space: nowrap;
  box-shadow: 3px 3px 0 rgba(0,0,0,0.6), 0 0 20px rgba(0,0,0,0.5);
}
.scene-roman {
  font-family: Georgia, serif;
  font-style: italic;
  font-size: 13px;
  color: var(--accent);
  opacity: 0.8;
  letter-spacing: 1px;
}
.scene-title-text {
  font-family: Georgia, serif;
  font-size: 15px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--accent);
  font-weight: bold;
}
.scene-quote-bar {
  position: absolute;
  bottom: 82px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  max-width: min(580px, 88vw);
  text-align: center;
  font-size: 12.5px;
  font-style: italic;
  color: var(--accent);
  opacity: 0.65;
  letter-spacing: 0.5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ── Panel entry animation (slide-up) ── */
.scene-panel .svg-frame,
.scene-panel .scene-label,
.scene-panel .scene-quote-bar {
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.7s ease, transform 0.7s ease;
}
.scene-panel.entered .svg-frame {
  opacity: 1;
  transform: translateY(0);
  transition-delay: 0.05s;
}
.scene-panel.entered .scene-quote-bar {
  opacity: 1;
  transform: translateY(0);
  transition-delay: 0.2s;
}
.scene-panel.entered .scene-label {
  opacity: 1;
  transform: translateY(0);
  transition-delay: 0.35s;
}

/* ── Mobile ── */
@media (max-width: 600px) {
  #scene-nav { right: 8px; }
  .nav-dot { width: 22px; height: 22px; font-size: 8px; }
  .scene-label { font-size: 12px; padding: 6px 14px; }
  .cover-scroll-hint { font-size: 9px; }
}
"""

JS = r"""
// ── Progress bar ──────────────────────────────────────────────────
const progressBar = document.getElementById('progress-bar');

function updateProgress() {
  const max = document.documentElement.scrollHeight - window.innerHeight;
  const pct = max > 0 ? (window.scrollY / max) * 100 : 0;
  progressBar.style.width = pct + '%';
}
window.addEventListener('scroll', updateProgress, { passive: true });
updateProgress();

// ── SVG element init: get Y coords, then hide for animation ───────
function initSvgElements(svgEl) {
  const children = Array.from(svgEl.children).filter(
    el => el.tagName.toLowerCase() !== 'defs'
  );

  children.forEach(el => {
    try {
      const bb = el.getBBox();
      el.dataset.y = bb.y + bb.height * 0.5; // centre-y
    } catch(e) {
      el.dataset.y = 0;
    }
    el.style.opacity  = '0';
    el.style.transform = 'translateY(-18px)';
    el.style.transition = 'none';
  });
}

document.querySelectorAll('.svg-frame svg').forEach(svg => initSvgElements(svg));

// ── Animate SVG elements in Y-order, bubbles last ─────────────────
function animateSvgElements(svgEl) {
  const children = Array.from(svgEl.children).filter(
    el => el.tagName.toLowerCase() !== 'defs'
  );

  const nonBubbles = children.filter(el => !el.dataset.bubble);
  const bubbles    = children.filter(el =>  el.dataset.bubble);

  const ys  = nonBubbles.map(el => parseFloat(el.dataset.y) || 0);
  const minY = Math.min(...ys, 0);
  const maxY = Math.max(...ys, 1);
  const spread = maxY - minY || 1;

  // Sort non-bubbles by Y
  const sorted = nonBubbles.slice().sort(
    (a, b) => (parseFloat(a.dataset.y)||0) - (parseFloat(b.dataset.y)||0)
  );

  const TOTAL_MS = 900; // spread of stagger

  sorted.forEach(el => {
    const y     = parseFloat(el.dataset.y) || 0;
    const delay = ((y - minY) / spread) * TOTAL_MS;
    setTimeout(() => {
      el.style.transition = 'opacity 0.45s ease, transform 0.45s ease';
      el.style.opacity    = '1';
      el.style.transform  = 'translateY(0)';
    }, delay);
  });

  // Bubbles always last
  bubbles.forEach((el, i) => {
    const delay = TOTAL_MS + 100 + i * 80;
    setTimeout(() => {
      el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      el.style.opacity    = '1';
      el.style.transform  = 'translateY(0)';
    }, delay);
  });
}

// ── Intersection observer for panels ─────────────────────────────
const navDots = document.querySelectorAll('.nav-dot[data-scene]');

const panelObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    const panel = entry.target;
    const sceneId = panel.dataset.scene;

    if (entry.isIntersecting) {
      // Trigger frame slide-in
      if (!panel.dataset.entered) {
        panel.dataset.entered = '1';
        panel.classList.add('entered');
        // Trigger SVG element animation after frame settles
        const svg = panel.querySelector('.svg-frame svg');
        if (svg) {
          setTimeout(() => animateSvgElements(svg), 300);
        }
      }
      // Highlight nav dot
      navDots.forEach(d => d.classList.remove('active'));
      const dot = document.querySelector(`.nav-dot[data-scene="${sceneId}"]`);
      if (dot) dot.classList.add('active');
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll('.scene-panel').forEach(p => panelObserver.observe(p));

// Cover observer for nav
const coverObserver = new IntersectionObserver(entries => {
  if (entries[0].isIntersecting) {
    navDots.forEach(d => d.classList.remove('active'));
    const dot = document.querySelector('.nav-dot[data-scene="cover"]');
    if (dot) dot.classList.add('active');
  }
}, { threshold: 0.3 });
const cover = document.getElementById('cover');
if (cover) coverObserver.observe(cover);
"""


def build_nav():
    items = [
        f'<a href="#cover" class="nav-dot active" data-scene="cover" title="Deckblatt">'
        f'<span class="nav-tooltip">Deckblatt</span>◆</a>'
    ]
    for i, s in enumerate(SCENES):
        items.append(
            f'<a href="#scene-{i+1}" class="nav-dot" data-scene="{i+1}">'
            f'<span class="nav-tooltip">{s["title"]}</span>{s["roman"]}</a>'
        )
    return '\n    '.join(items)


def build_cover():
    inner, vb = process_svg(BASE + 'faust_comic_cover.svg', 0)
    return f'''
  <section id="cover" class="panel" style="--dot-color:rgba(212,175,55,0.12)">
    <div class="halftone"></div>
    <div class="cover-inner">
      <svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg" aria-label="Faust – Pop Art Comic Cover">
        {inner}
      </svg>
    </div>
    <div class="cover-scroll-hint">
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M10 3v14M4 11l6 6 6-6" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      Scroll
    </div>
  </section>'''


def build_scene(idx, scene):
    inner, vb = process_svg(BASE + scene['file'], idx + 1)
    bg  = scene['bg']
    acc = scene['accent']
    dot = scene['dot']
    return f'''
  <section id="scene-{idx+1}" class="panel scene-panel"
           data-scene="{idx+1}"
           style="background-color:{bg}; --accent:{acc}; --dot-color:{dot}">
    <div class="halftone"></div>
    <div class="svg-frame">
      <svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg"
           aria-label="{scene['title']}">
        {inner}
      </svg>
    </div>
    <div class="scene-quote-bar">{scene['quote']} — {scene['speaker']}</div>
    <div class="scene-label">
      <span class="scene-roman">{scene['roman']}</span>
      <span class="scene-title-text">{scene['title']}</span>
    </div>
  </section>'''


def build_html():
    cover_html  = build_cover()
    scenes_html = '\n'.join(build_scene(i, s) for i, s in enumerate(SCENES))
    nav_html    = build_nav()

    return f'''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FAUST – Pop Art Comic</title>
  <meta name="description" content="Goethe's Faust I as a scrollable Pop Art comic – 12 scenes.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Bangers&display=swap" rel="stylesheet">
  <style>{CSS}</style>
</head>
<body>

  <div id="progress-bar"></div>

  <nav id="scene-nav" aria-label="Szenennavigation">
    {nav_html}
  </nav>

{cover_html}

{scenes_html}

  <footer style="text-align:center;padding:60px 20px;background:#06060E;
                 color:rgba(255,255,255,0.3);font-size:12px;letter-spacing:2px;">
    FAUST · Johann Wolfgang von Goethe · Pop Art Edition
  </footer>

  <script>{JS}</script>
</body>
</html>'''


if __name__ == '__main__':
    out = BASE + 'index.html'
    html = build_html()
    with open(out, 'w') as f:
        f.write(html)
    size = os.path.getsize(out)
    print(f'✓ Written {out} ({size:,} bytes / {size//1024} KB)')
