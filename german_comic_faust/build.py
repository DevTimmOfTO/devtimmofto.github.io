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
        'file':   'faust_nacht_erdgeist_v5.svg',
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
        'file':   'faust_wald_und_hoehle.svg',
        'title':  'Wald und Höhle',
        'roman':  'XII',
        'quote':  '»Erhabner Geist, du gabst mir, gabst mir alles!«',
        'speaker':'Faust',
        'bg':     '#060C08',
        'accent': '#4A8040',
        'dot':    'rgba(74,128,64,0.18)',
    },
    {
        'file':   'faust_gretchenfrage.svg',
        'title':  'Gretchenfrage',
        'roman':  'XIII',
        'quote':  '»Wie hast du\'s mit der Religion?«',
        'speaker':'Gretchen',
        'bg':     '#160A12',
        'accent': '#C06080',
        'dot':    'rgba(192,96,128,0.18)',
    },
    {
        'file':   'faust_walpurgisnacht_brocken.svg',
        'title':  'Walpurgisnacht',
        'roman':  'XIV',
        'quote':  '»Die Welt geht unter!«',
        'speaker':'Mephisto',
        'bg':     '#0A0414',
        'accent': '#8820C0',
        'dot':    'rgba(136,32,192,0.18)',
    },
    {
        'file':   'faust_kerker_v2.svg',
        'title':  'Kerker',
        'roman':  'XV',
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
    # Use the LAST match — speech bubbles live at the end of the SVG;
    # earlier label comments (e.g. "Mephisto shadow speech bubble") must not
    # trigger the section too soon and swallow character body elements.
    m = None
    for m in bubble_re.finditer(raw):
        pass  # keep iterating to get the last match
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
    # Use [\s\S]*? to handle files with XML declaration before <svg>
    inner = re.sub(r'^[\s\S]*?<svg[^>]*>\s*', '', raw).strip()
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

/* ── Global progress bar ── */
#progress-bar {
  position: fixed;
  top: 0; left: 0;
  height: 3px;
  width: 0%;
  background: linear-gradient(90deg, #D4AF37, #CC2200, #D4AF37);
  background-size: 200% 100%;
  animation: pb-shimmer 3s linear infinite;
  z-index: 9999;
  transition: width 0.1s linear;
  pointer-events: none;
}
@keyframes pb-shimmer {
  0%   { background-position: 100% 0; }
  100% { background-position: -100% 0; }
}

/* ── Side nav dots ── */
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
  width: 28px; height: 28px;
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
.nav-dot:hover, .nav-dot.active {
  border-color: var(--nav-accent, #D4AF37);
  color: var(--nav-accent, #D4AF37);
  background: rgba(0,0,0,0.85);
  transform: scale(1.25);
}
.nav-dot .nav-tooltip {
  position: absolute;
  right: 38px; top: 50%;
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

/* ── Cover ── */
#cover {
  background: #08060E;
  position: relative;
  height: 100vh;
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

.cover-inner {
  position: relative;
  z-index: 2;
  width: min(500px, 88vw);
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: coverFadeUp 1.4s cubic-bezier(0.22,1,0.36,1) forwards;
}
.cover-inner svg {
  width: 100%; height: auto;
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
  bottom: 28px; left: 50%;
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

/* ── Scene wrapper: gives scroll space for the build animation ── */
.scene-wrapper {
  position: relative;
  height: calc(100vh + 900px);
}
.scene-sticky {
  position: sticky;
  top: 0;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* ── SVG panel frame ── */
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
    inset 0 0 0 2px rgba(0,0,0,0.3);
  background: #fff;
  overflow: hidden;
}
.svg-frame svg { width: 100%; height: auto; display: block; }

/* ── Scene info overlays ── */
.scene-label {
  position: absolute;
  bottom: 32px; left: 50%;
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
  opacity: 0;
  transition: opacity 0.7s ease;
}
.scene-label.visible { opacity: 1; }
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
  bottom: 82px; left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  max-width: min(580px, 88vw);
  text-align: center;
  font-size: 12.5px;
  font-style: italic;
  color: var(--accent);
  opacity: 0;
  letter-spacing: 0.5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: opacity 0.7s ease 0.15s;
}
.scene-quote-bar.visible { opacity: 0.65; }

/* ── Thin build-progress stripe at bottom of sticky panel ── */
.build-bar {
  position: absolute;
  bottom: 0; left: 0;
  height: 2px;
  width: 0%;
  background: var(--accent);
  opacity: 0.55;
  z-index: 20;
  transition: width 0.08s linear;
}

/* ── Mobile ── */
@media (max-width: 600px) {
  #scene-nav { right: 8px; }
  .nav-dot { width: 22px; height: 22px; font-size: 8px; }
  .scene-label { font-size: 12px; padding: 6px 14px; }
  .cover-scroll-hint { font-size: 9px; }
  .scene-wrapper { height: calc(100vh + 600px); }
}
"""

JS = r"""
// ── Constants ─────────────────────────────────────────────────────
const BUILD_SCROLL = 900; // px of scroll to reveal a full scene
const STAGGER_MS   = 18;  // ms between successive element reveals
const MAX_STAGGER  = 8;   // cap stagger depth to avoid long queues

// ── Global progress bar ───────────────────────────────────────────
const progressBar = document.getElementById('progress-bar');

// ── Per-scene init ────────────────────────────────────────────────
function initScene(wrapper) {
  if (wrapper._inited) return;
  wrapper._inited   = true;
  wrapper._revealed = -1;

  const svg = wrapper.querySelector('.svg-frame svg');
  if (!svg) { wrapper._elements = []; return; }

  const children = Array.from(svg.children).filter(
    el => el.tagName.toLowerCase() !== 'defs'
  );

  // Measure Y centre via getBBox
  children.forEach(el => {
    try {
      const bb = el.getBBox();
      el._cy = bb.y + bb.height * 0.5;
    } catch(e) {
      el._cy = 0;
    }
    // Hide initially
    el.style.opacity    = '0';
    el.style.transition = 'none';
    if (!el.hasAttribute('transform')) {
      el.style.transform = 'translateY(10px)';
    }
  });

  // Order: non-bubbles sorted top→bottom, then bubbles
  const nonBubbles = children.filter(el => !el.dataset.bubble);
  const bubbles    = children.filter(el =>  el.dataset.bubble);
  nonBubbles.sort((a, b) => (a._cy || 0) - (b._cy || 0));
  wrapper._elements = [...nonBubbles, ...bubbles];
}

// ── Reveal a single element ───────────────────────────────────────
function revealEl(el) {
  if (el.hasAttribute('transform')) {
    el.style.transition = 'opacity 0.38s ease';
  } else {
    el.style.transition = 'opacity 0.38s ease, transform 0.38s ease';
    el.style.transform  = 'translateY(0)';
  }
  el.style.opacity = '1';
}

// ── Main scroll driver ────────────────────────────────────────────
function updateScroll() {
  const scrollY = window.scrollY;
  const vh      = window.innerHeight;
  const docH    = document.documentElement.scrollHeight;

  // Global progress bar
  progressBar.style.width =
    (docH > vh ? (scrollY / (docH - vh)) * 100 : 0) + '%';

  let activeScene = null;

  // Cover: active while still on screen
  const coverEl = document.getElementById('cover');
  if (coverEl) {
    const cr = coverEl.getBoundingClientRect();
    if (cr.bottom >= vh * 0.4) activeScene = 'cover';
  }

  document.querySelectorAll('.scene-wrapper').forEach(wrapper => {
    initScene(wrapper);
    const elements = wrapper._elements;
    if (!elements.length) return;

    const rect = wrapper.getBoundingClientRect();
    // Skip far-offscreen wrappers
    if (rect.bottom < -vh || rect.top > vh * 2.5) return;

    // scrolledPast = how many px the wrapper top has moved above viewport top
    const scrolledPast = Math.max(0, -rect.top);
    const progress     = Math.min(1, scrolledPast / BUILD_SCROLL);
    const targetIdx    = Math.round(progress * elements.length) - 1;

    // Reveal newly reached elements with a small stagger
    if (targetIdx > wrapper._revealed) {
      const start = wrapper._revealed + 1;
      for (let i = start; i <= targetIdx; i++) {
        const lag = Math.min(i - start, MAX_STAGGER) * STAGGER_MS;
        const el  = elements[i];
        if (lag === 0) {
          revealEl(el);
        } else {
          setTimeout(() => revealEl(el), lag);
        }
      }
      wrapper._revealed = targetIdx;
    }

    // Build-progress stripe
    const buildBar = wrapper.querySelector('.build-bar');
    if (buildBar) buildBar.style.width = (progress * 100) + '%';

    // Show label + quote once scene is ~80 % built
    if (progress >= 0.80) {
      wrapper.querySelector('.scene-label')?.classList.add('visible');
      wrapper.querySelector('.scene-quote-bar')?.classList.add('visible');
    }

    // Active nav: sticky panel covers viewport center
    if (rect.top <= 0 && rect.bottom >= vh * 0.5) {
      activeScene = wrapper.dataset.scene;
    }
  });

  // Sync nav dots
  if (activeScene !== null) {
    document.querySelectorAll('.nav-dot[data-scene]').forEach(d => {
      d.classList.toggle('active', d.dataset.scene === activeScene);
    });
  }
}

// RAF-throttled scroll listener
let _ticking = false;
function onScroll() {
  if (!_ticking) {
    _ticking = true;
    requestAnimationFrame(() => { updateScroll(); _ticking = false; });
  }
}
window.addEventListener('scroll', onScroll, { passive: true });
window.addEventListener('resize', () => {
  // Re-init all scenes on resize
  document.querySelectorAll('.scene-wrapper').forEach(w => {
    w._inited   = false;
    w._revealed = -1;
  });
  updateScroll();
}, { passive: true });

updateScroll();
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
  <div id="scene-{idx+1}" class="scene-wrapper" data-scene="{idx+1}"
       style="background-color:{bg}">
    <div class="scene-sticky"
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
      <div class="build-bar"></div>
    </div>
  </div>'''


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
