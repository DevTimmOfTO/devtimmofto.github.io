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

/* ── TOC button ── */
#toc-btn {
  position: fixed;
  top: 16px; left: 16px;
  z-index: 960;
  width: 40px; height: 40px;
  border-radius: 6px;
  border: 2px solid rgba(255,255,255,0.18);
  background: rgba(0,0,0,0.72);
  color: rgba(255,255,255,0.65);
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  gap: 0;
  transition: border-color 0.2s, color 0.2s, background 0.2s;
  backdrop-filter: blur(6px);
  padding: 0;
}
#toc-btn:hover, #toc-btn.open {
  border-color: #D4AF37;
  color: #D4AF37;
  background: rgba(0,0,0,0.92);
}

/* ── TOC overlay ── */
#toc-overlay {
  position: fixed;
  inset: 0;
  z-index: 950;
  background: rgba(5,3,10,0.97);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 70px 24px 48px;
  overflow-y: auto;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.25s ease;
}
#toc-overlay.open {
  opacity: 1;
  pointer-events: all;
}
#toc-overlay h2 {
  font-size: 10px;
  letter-spacing: 6px;
  text-transform: uppercase;
  color: rgba(212,175,55,0.55);
  margin-bottom: 36px;
  text-align: center;
}
#toc-close {
  position: absolute;
  top: 16px; right: 20px;
  background: none;
  border: none;
  color: rgba(255,255,255,0.4);
  font-size: 22px;
  cursor: pointer;
  line-height: 1;
  padding: 4px 8px;
  transition: color 0.2s;
}
#toc-close:hover { color: #D4AF37; }

.toc-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 10px;
  width: 100%;
  max-width: 920px;
}
.toc-card {
  cursor: pointer;
  border: 2px solid rgba(255,255,255,0.06);
  border-radius: 4px;
  padding: 14px 12px 12px;
  transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
  text-decoration: none;
  display: block;
  background-image: radial-gradient(circle, var(--card-accent) 1px, transparent 1px);
  background-size: 12px 12px;
  background-position: 0 0;
}
.toc-card:hover {
  border-color: var(--card-accent);
  transform: translateY(-3px);
  box-shadow: 0 8px 28px rgba(0,0,0,0.7);
}
.toc-card-roman {
  font-family: Georgia, serif;
  font-style: italic;
  font-size: 26px;
  color: var(--card-accent);
  opacity: 0.35;
  line-height: 1;
  margin-bottom: 6px;
}
.toc-card-title {
  font-size: 9.5px;
  letter-spacing: 1.8px;
  text-transform: uppercase;
  color: var(--card-accent);
  font-weight: bold;
  line-height: 1.45;
}
.toc-card-quote {
  font-size: 8.5px;
  font-style: italic;
  color: rgba(255,255,255,0.3);
  margin-top: 7px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* ── Prev / Next scene buttons ── */
#page-nav {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 900;
  display: flex;
  gap: 10px;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
}
#page-nav.visible {
  opacity: 1;
  pointer-events: all;
}
.page-nav-btn {
  background: rgba(0,0,0,0.75);
  border: 2px solid rgba(255,255,255,0.2);
  color: rgba(255,255,255,0.6);
  font-size: 11px;
  letter-spacing: 2px;
  text-transform: uppercase;
  padding: 8px 18px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  backdrop-filter: blur(6px);
  font-family: Georgia, serif;
}
.page-nav-btn:hover {
  border-color: #D4AF37;
  color: #D4AF37;
  background: rgba(0,0,0,0.92);
}
.page-nav-btn:disabled {
  opacity: 0.2;
  cursor: default;
  pointer-events: none;
}

/* ── Mobile ── */
@media (max-width: 600px) {
  #scene-nav { display: none; }
  .scene-label { font-size: 12px; padding: 6px 14px; }
  .cover-scroll-hint { font-size: 9px; }
  .scene-wrapper { height: calc(100vh + 600px); }
  .toc-grid { grid-template-columns: repeat(2, 1fr); }
  #page-nav { bottom: 16px; gap: 8px; }
  .page-nav-btn { font-size: 10px; padding: 8px 14px; }
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

// ── Scene ID list (cover + all scenes) ───────────────────────────
const SCENE_IDS = [
  'cover',
  ...Array.from(document.querySelectorAll('.scene-wrapper[data-scene]')).map(w => w.id)
];

function getActiveIdx() {
  const wrappers = document.querySelectorAll('.scene-wrapper');
  for (let i = wrappers.length - 1; i >= 0; i--) {
    if (wrappers[i].getBoundingClientRect().top <= 1) return i + 1;
  }
  return 0;
}

function scrollToIdx(idx) {
  idx = Math.max(0, Math.min(idx, SCENE_IDS.length - 1));
  const el = document.getElementById(SCENE_IDS[idx]);
  if (el) el.scrollIntoView({ behavior: 'smooth' });
}

// ── Prev / Next buttons ───────────────────────────────────────────
const pageNav  = document.getElementById('page-nav');
const prevBtn  = document.getElementById('nav-prev');
const nextBtn  = document.getElementById('nav-next');

function updatePageNav() {
  const idx = getActiveIdx();
  // Show nav once past the cover
  pageNav.classList.toggle('visible', idx > 0 || window.scrollY > window.innerHeight * 0.4);
  if (prevBtn) prevBtn.disabled = (idx === 0);
  if (nextBtn) nextBtn.disabled = (idx === SCENE_IDS.length - 1);
}

prevBtn?.addEventListener('click', () => scrollToIdx(getActiveIdx() - 1));
nextBtn?.addEventListener('click', () => scrollToIdx(getActiveIdx() + 1));

// piggyback on existing RAF loop
const _origUpdate = updateScroll;
window._scrollUpdateHook = updatePageNav;

// ── TOC ───────────────────────────────────────────────────────────
const tocOverlay = document.getElementById('toc-overlay');
const tocBtn     = document.getElementById('toc-btn');
const tocClose   = document.getElementById('toc-close');

function openToc()  { tocOverlay.classList.add('open');    tocBtn.classList.add('open'); }
function closeToc() { tocOverlay.classList.remove('open'); tocBtn.classList.remove('open'); }
function toggleToc(){ tocOverlay.classList.contains('open') ? closeToc() : openToc(); }

tocBtn?.addEventListener('click', toggleToc);
tocClose?.addEventListener('click', closeToc);
tocOverlay?.addEventListener('click', e => { if (e.target === tocOverlay) closeToc(); });

document.querySelectorAll('.toc-card').forEach(card => {
  card.addEventListener('click', () => {
    closeToc();
    const el = document.getElementById(card.dataset.target);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  });
});

// ── Keyboard navigation ───────────────────────────────────────────
document.addEventListener('keydown', e => {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

  if (e.key === 'Escape') { closeToc(); return; }
  if (e.key === 't' || e.key === 'T') {
    if (!tocOverlay.classList.contains('open')) { openToc(); return; }
  }
  if (tocOverlay.classList.contains('open')) return;

  if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
    e.preventDefault(); scrollToIdx(getActiveIdx() + 1);
  } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
    e.preventDefault(); scrollToIdx(getActiveIdx() - 1);
  } else if (e.key === 'Home') {
    e.preventDefault(); scrollToIdx(0);
  } else if (e.key === 'End') {
    e.preventDefault(); scrollToIdx(SCENE_IDS.length - 1);
  }
});

// Hook page-nav update into scroll
window.addEventListener('scroll', updatePageNav, { passive: true });
updatePageNav();
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


def build_toc():
    cards = []
    # Cover card
    cards.append(
        '<div class="toc-card" data-target="cover"'
        ' style="background-color:#08060E; --card-accent:#D4AF37">'
        '<div class="toc-card-roman">◆</div>'
        '<div class="toc-card-title">Deckblatt</div>'
        '</div>'
    )
    for i, s in enumerate(SCENES):
        cards.append(
            f'<div class="toc-card" data-target="scene-{i+1}"'
            f' style="background-color:{s["bg"]}; --card-accent:{s["accent"]}">'
            f'<div class="toc-card-roman">{s["roman"]}</div>'
            f'<div class="toc-card-title">{s["title"]}</div>'
            f'<div class="toc-card-quote">{s["quote"]}</div>'
            f'</div>'
        )
    return (
        '<div id="toc-overlay" role="dialog" aria-modal="true" aria-label="Inhaltsverzeichnis">\n'
        '  <button id="toc-close" aria-label="Schließen">✕</button>\n'
        '  <h2>Inhaltsverzeichnis</h2>\n'
        '  <div class="toc-grid">\n    '
        + '\n    '.join(cards)
        + '\n  </div>\n</div>'
    )


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
    toc_html    = build_toc()

    return f'''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FAUST – Pop Art Comic</title>
  <meta name="description" content="Goethe's Faust I as a scrollable Pop Art comic – 15 scenes.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Bangers&display=swap" rel="stylesheet">
  <style>{CSS}</style>
</head>
<body>

  <div id="progress-bar"></div>

  <!-- TOC toggle button -->
  <button id="toc-btn" aria-label="Inhaltsverzeichnis öffnen" title="Inhaltsverzeichnis (T)">
    <svg width="18" height="14" viewBox="0 0 18 14" fill="none">
      <rect x="0" y="0"  width="18" height="2" rx="1" fill="currentColor"/>
      <rect x="0" y="6"  width="12" height="2" rx="1" fill="currentColor"/>
      <rect x="0" y="12" width="15" height="2" rx="1" fill="currentColor"/>
    </svg>
  </button>

  <!-- TOC overlay -->
  {toc_html}

  <!-- Side nav (desktop) -->
  <nav id="scene-nav" aria-label="Szenennavigation">
    {nav_html}
  </nav>

  <!-- Prev / Next buttons -->
  <div id="page-nav" role="navigation" aria-label="Szenensteuerung">
    <button class="page-nav-btn" id="nav-prev" aria-label="Vorherige Szene">← Zurück</button>
    <button class="page-nav-btn" id="nav-next" aria-label="Nächste Szene">Weiter →</button>
  </div>

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
