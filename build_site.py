#!/usr/bin/env python3
"""Build the VoxCore Report static site — Apple HIG aesthetic."""

import re
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(ROOT, "content")
OUTPUT_DIR = os.path.join(ROOT, "docs")

# ── Page definitions (no section numbers) ─────────────────────────────────────

PAGES = [
    {"slug": "data-import",       "title": "Data Import & Hotfix Repair",  "desc": "~1M rows imported, 103K hotfix entries repaired"},
    {"slug": "npc-audits",        "title": "NPC Audits & Corrections",     "desc": "78,475 fixes across 27-check validator + Wowhead mega-audit"},
    {"slug": "quest-localization", "title": "Quests & Localization",        "desc": "21K chain links, 1.6M locale rows across 10 languages"},
    {"slug": "database-cleanup",  "title": "Database Cleanup & Integrity",  "desc": "412K dead rows removed, loot PK discovery, 47K post-import cleanup"},
    {"slug": "performance",       "title": "Performance & Build Diff",     "desc": "3m24s to 17s startup, 5-build diff audit with zero breaking changes"},
    {"slug": "placement",         "title": "Placement Audits",             "desc": "31K placement fixes generated from LoreWalkerTDB comparison"},
    {"slug": "results",           "title": "Tooling & Results",            "desc": "50+ tools built, final DB state, before/after player impact"},
    {"slug": "hotfix-audit",      "title": "Hotfix Redundancy Audit",      "desc": "10.8M to 244K rows \u2014 97.8% reduction in 3 rounds"},
    {"slug": "discoveries",       "title": "Discoveries & Lessons",        "desc": "9 community-relevant findings for any TrinityCore project"},
    {"slug": "reference",         "title": "Timeline & Reference",         "desc": "Full timeline, 50+ tool catalog, data sources, reproducibility"},
]

HERO_STATS = [
    ("~1M",   "rows imported"),
    ("103K",  "hotfix entries repaired"),
    ("97.8%", "redundant rows removed"),
    ("78K",   "NPC corrections"),
    ("1.6M",  "item translations"),
    ("17s",   "server startup"),
]

EXEC_GROUPS = [
    ("Data Imported", [
        ("LoreWalkerTDB world rows",  "~1,004,000 net"),
        ("Hotfix rows repaired",      "103,153 inserts + 1,831 fixes"),
        ("Item locale translations",  "1,628,651 rows (10 languages)"),
        ("Quest chain links",         "21,758 updates"),
        ("Quest POI / objectives",    "2,880 POI + 5,199 pts + 633 obj"),
    ]),
    ("Corrected & Cleaned", [
        ("NPC fixes (audit + Wowhead)", "78,475 corrections"),
        ("Hotfix redundancy audit",     "10.6M rows removed (97.8%)"),
        ("Pre-existing dead rows",      "~412,000"),
        ("Duplicate loot rows",         "193,542"),
        ("Post-import cleanup",         "~47,000"),
    ]),
    ("Performance", [
        ("Server startup",          "3m24s \u2192 17s (92%)"),
        ("Hotfix content tables",   "10.8M \u2192 ~244K rows"),
    ]),
]

# ── SVG icons (24px, 1.5px stroke, rounded) ──────────────────────────────────

ICONS = {
    "data-import": '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 5v14c0 1.66-4.03 3-9 3s-9-1.34-9-3V5"/><path d="M21 12c0 1.66-4.03 3-9 3s-9-1.34-9-3"/></svg>',
    "npc-audits": '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/><path d="m8 11 2 2 4-4"/></svg>',
    "quest-localization": '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10A15.3 15.3 0 0 1 12 2z"/></svg>',
    "database-cleanup": '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M3 6h18"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="m19 6-.867 12.142A2 2 0 0 1 16.138 20H7.862a2 2 0 0 1-1.995-1.858L5 6"/><path d="M10 11v5"/><path d="M14 11v5"/></svg>',
    "performance": '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/></svg>',
    "placement": '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 1 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "results": '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>',
    "hotfix-audit": '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M12 20V10"/><path d="M18 20V4"/><path d="M6 20v-4"/><path d="m9 7-3 3-3-3"/></svg>',
    "discoveries": '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>',
    "reference": '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
}

# ── CSS ───────────────────────────────────────────────────────────────────────

CSS = """\
:root {
  --font-body: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-display: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-mono: "SF Mono", SFMono-Regular, ui-monospace, Menlo, Consolas, monospace;
  --bg: #fff; --bg-alt: #f5f5f7; --bg-card: #fff;
  --text: #1d1d1f; --text-2: #6e6e73; --text-3: #86868b;
  --accent: #0071e3; --accent-hover: #2997ff;
  --border: #d2d2d7; --code-bg: #f5f5f7;
  --nav-bg: rgba(255,255,255,0.72); --nav-border: rgba(0,0,0,0.08);
  --card-shadow: 0 4px 12px rgba(0,0,0,0.08);
  --callout-bg: rgba(0,113,227,0.04);
  --table-stripe: rgba(0,0,0,0.02);
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #000; --bg-alt: #1d1d1f; --bg-card: #1d1d1f;
    --text: #f5f5f7; --text-2: #a1a1a6; --text-3: #86868b;
    --accent: #2997ff; --accent-hover: #2997ff;
    --border: #424245; --code-bg: #1d1d1f;
    --nav-bg: rgba(29,29,31,0.72); --nav-border: rgba(255,255,255,0.08);
    --card-shadow: 0 4px 12px rgba(0,0,0,0.3);
    --callout-bg: rgba(41,151,255,0.06);
    --table-stripe: rgba(255,255,255,0.02);
  }
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: var(--font-body); font-size: 17px; line-height: 1.7;
  color: var(--text); background: var(--bg);
  -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;
}
h1, h2, h3, h4, h5, h6 { font-family: var(--font-display); color: var(--text); line-height: 1.15; }
h1 { font-size: 48px; font-weight: 700; letter-spacing: -0.03em; }
h2 { font-size: 32px; font-weight: 600; letter-spacing: -0.02em; margin: 72px 0 20px; }
h3 { font-size: 24px; font-weight: 600; margin: 48px 0 14px; }
h4 { font-size: 20px; font-weight: 600; margin: 32px 0 10px; }
h5 { font-size: 17px; font-weight: 600; margin: 24px 0 8px; }
article h2:first-child { margin-top: 0; }
a { color: var(--accent); text-decoration: none; transition: color 0.2s; }
a:hover { color: var(--accent-hover); }
p { margin: 0 0 20px; color: var(--text-2); }
strong { color: var(--text); font-weight: 600; }
em { font-style: italic; }
code {
  font-family: var(--font-mono); font-size: 0.875em;
  background: var(--code-bg); padding: 2px 6px; border-radius: 4px;
}
hr { border: none; border-top: 1px solid var(--border); margin: 64px 0; }
ul, ol { margin: 0 0 20px 24px; color: var(--text-2); }
li { margin-bottom: 6px; line-height: 1.6; }
li strong { color: var(--text); }
blockquote {
  border-left: 3px solid var(--accent); padding: 0 0 0 20px;
  margin: 24px 0; color: var(--text-2); font-style: italic;
}

/* ── Nav ── */
.site-nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 100; height: 48px;
  background: var(--nav-bg); backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid var(--nav-border);
}
.nav-inner {
  max-width: 980px; margin: 0 auto; padding: 0 24px;
  height: 100%; display: flex; align-items: center; gap: 20px;
}
.nav-logo {
  font-family: var(--font-display); font-weight: 600; font-size: 17px;
  color: var(--text); text-decoration: none; flex-shrink: 0;
  letter-spacing: -0.02em;
}
.nav-links {
  display: flex; gap: 6px; overflow-x: auto; flex: 1;
  -webkit-overflow-scrolling: touch; scrollbar-width: none;
  mask-image: linear-gradient(to right, #000 calc(100% - 32px), transparent);
  -webkit-mask-image: linear-gradient(to right, #000 calc(100% - 32px), transparent);
}
.nav-links.no-fade {
  mask-image: none; -webkit-mask-image: none;
}
.nav-links::-webkit-scrollbar { display: none; }
.nav-links a {
  font-size: 12px; font-weight: 500; color: var(--text-2);
  text-decoration: none; white-space: nowrap; padding: 4px 6px;
  letter-spacing: 0.01em; transition: color 0.2s; border-radius: 4px;
}
.nav-links a:hover { background: var(--bg-alt); }
.nav-links a:hover, .nav-links a.active { color: var(--text); }
.nav-links a.active { font-weight: 600; }
.nav-end { flex-shrink: 0; display: flex; align-items: center; gap: 16px; }
.nav-github { color: var(--text-3); transition: color 0.2s; display: flex; }
.nav-github:hover { color: var(--text); }
.nav-menu-btn {
  display: none; background: none; border: none; cursor: pointer;
  color: var(--text-2); padding: 4px;
}
.mobile-nav {
  display: none; position: fixed; inset: 0; z-index: 99;
  background: var(--nav-bg); backdrop-filter: saturate(180%) blur(40px);
  -webkit-backdrop-filter: saturate(180%) blur(40px);
  padding: 72px 32px 32px; flex-direction: column; gap: 4px;
}
.mobile-nav.open { display: flex; }
.mobile-nav a {
  font-size: 17px; font-weight: 400; color: var(--text-2);
  padding: 12px 0; border-bottom: 1px solid var(--border);
  text-decoration: none; transition: color 0.2s;
}
.mobile-nav a:hover { color: var(--text); }

/* ── Hero ── */
.hero { text-align: center; padding: 100px 24px 60px; max-width: 720px; margin: 0 auto; }
.hero-label { font-size: 14px; font-weight: 500; color: var(--text-3); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 12px; }
.hero h1 { font-size: clamp(48px, 8vw, 72px); margin-bottom: 12px; }
.hero-sub { font-size: 21px; color: var(--text-2); margin-bottom: 8px; font-weight: 400; }
.hero-meta { font-size: 14px; color: var(--text-3); font-weight: 500; }

/* ── Stat ribbon ── */
.stat-ribbon {
  display: flex; justify-content: center; align-items: center; flex-wrap: wrap;
  gap: 0; padding: 48px 24px; max-width: 980px; margin: 0 auto;
}
.stat-item { text-align: center; padding: 0 28px; }
.stat-sep { width: 1px; height: 40px; background: var(--border); flex-shrink: 0; }
.stat-num {
  font-family: var(--font-display); font-size: 32px; font-weight: 700;
  color: var(--text); letter-spacing: -0.02em; display: block;
}
.stat-label { font-size: 13px; color: var(--text-2); margin-top: 2px; display: block; }

/* ── Banner ── */
.banner {
  background: var(--callout-bg); padding: 20px 32px;
  max-width: 980px; margin: 0 auto 64px; border-radius: 12px;
  display: flex; align-items: center; gap: 12px;
  font-size: 15px; color: var(--text-2);
}
.banner svg { flex-shrink: 0; color: var(--accent); }
.banner a { font-weight: 500; }

/* ── Summary grid ── */
.summary { max-width: 980px; margin: 0 auto; padding: 0 24px 80px; }
.summary h2 { font-size: 32px; margin-bottom: 8px; }
.summary > p { color: var(--text-2); margin-bottom: 40px; font-size: 17px; }
.summary-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; }
.summary-col h3 {
  font-size: 13px; font-weight: 600; color: var(--text-3);
  letter-spacing: 0.06em; text-transform: uppercase; margin: 0 0 20px;
}
.summary-row {
  display: flex; justify-content: space-between; align-items: baseline;
  padding: 8px 0; border-bottom: 1px solid var(--border);
}
.summary-row:last-child { border-bottom: none; }
.summary-row .label { font-size: 14px; color: var(--text-2); }
.summary-row .value { font-size: 14px; font-weight: 600; color: var(--text); white-space: nowrap; margin-left: 16px; }

/* ── Section cards ── */
.cards-section { background: var(--bg-alt); padding: 80px 24px; }
.cards-wrap { max-width: 1120px; margin: 0 auto; }
.cards-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;
}
.card {
  background: var(--bg-card); border-radius: 18px; padding: 32px;
  text-decoration: none; color: var(--text); display: block;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.card:hover { transform: translateY(-2px); box-shadow: var(--card-shadow); color: var(--text); }
.card-icon { color: var(--text-3); margin-bottom: 16px; display: block; }
.card:hover .card-icon { color: var(--accent); }
.card h3 { font-size: 20px; font-weight: 600; margin: 0 0 8px; letter-spacing: -0.01em; }
.card p { font-size: 15px; color: var(--text-2); margin: 0; line-height: 1.5; }
.card:hover h3 { color: var(--accent); }

/* ── Page layout (interior) ── */
.page-header { max-width: 980px; margin: 0 auto; padding: 80px 24px 0; }
.breadcrumb { font-size: 13px; color: var(--text-3); margin-bottom: 12px; }
.breadcrumb a { color: var(--text-3); font-weight: 500; }
.breadcrumb a:hover { color: var(--accent); }
.page-header h1 { margin-bottom: 32px; }
.page-layout {
  display: grid; grid-template-columns: 200px 1fr; gap: 60px;
  max-width: 980px; margin: 0 auto; padding: 0 24px 80px;
  align-items: start;
}
.sidebar { position: sticky; top: 72px; max-height: calc(100vh - 96px); overflow-y: auto; padding: 8px 0; }
.sidebar a {
  display: block; font-size: 13px; color: var(--text-3); text-decoration: none;
  padding: 5px 12px; border-left: 2px solid transparent; transition: all 0.2s;
  line-height: 1.4;
}
.sidebar a:hover { color: var(--text-2); }
.sidebar a.active { color: var(--accent); border-left-color: var(--accent); font-weight: 500; }
.sidebar a.toc-h3 { padding-left: 24px; font-size: 12px; }
.sidebar-toggle {
  display: none; background: var(--bg-alt); border: 1px solid var(--border);
  border-radius: 8px; padding: 10px 16px; width: 100%; text-align: left;
  font-size: 14px; color: var(--text-2); cursor: pointer; margin-bottom: 24px;
  font-family: var(--font-body);
}
article { min-width: 0; }

/* ── Data tables ── */
.data-table { width: 100%; border-collapse: collapse; margin: 24px 0; font-size: 15px; }
.data-table th {
  text-align: left; font-weight: 600; font-size: 13px; color: var(--text-2);
  padding: 10px 16px; border-bottom: 1px solid var(--border);
  letter-spacing: 0.02em;
}
.data-table td { padding: 10px 16px; border-bottom: 1px solid var(--border); color: var(--text-2); vertical-align: top; }
.data-table tr:nth-child(even) td { background: var(--table-stripe); }
.data-table td strong { color: var(--text); }
.data-table code { font-size: 0.8em; }

/* ── Callout ── */
.callout {
  background: var(--callout-bg); border-left: 4px solid var(--accent);
  border-radius: 12px; padding: 20px 24px; margin: 24px 0;
  font-size: 15px; color: var(--text-2);
}
.callout strong { color: var(--text); }

/* ── Details ── */
details { margin: 24px 0; border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
details summary {
  cursor: pointer; padding: 16px 20px; font-weight: 600; color: var(--text);
  list-style: none; display: flex; align-items: center; justify-content: space-between;
  transition: background 0.2s;
}
details summary:hover { background: var(--bg-alt); }
details summary::-webkit-details-marker { display: none; }
details summary::after { content: "+"; font-weight: 400; color: var(--text-3); font-size: 20px; }
details[open] summary::after { content: "\\2212"; }
details > div, details > p, details > table { padding: 0 20px 16px; }
details .data-table { margin: 0 0 8px; }

/* ── Prev/Next nav ── */
.page-nav {
  display: flex; justify-content: space-between; margin-top: 80px;
  padding-top: 32px; border-top: 1px solid var(--border);
}
.page-nav a {
  font-size: 15px; color: var(--text-2); text-decoration: none;
  transition: color 0.2s; max-width: 45%;
}
.page-nav a:hover { color: var(--accent); }
.page-nav .nav-label { font-size: 12px; color: var(--text-3); display: block; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.04em; font-weight: 500; }
.page-nav .next { text-align: right; margin-left: auto; }

/* ── Footer ── */
.site-footer {
  border-top: 1px solid var(--border); padding: 24px; margin-top: 0;
  display: flex; justify-content: space-between; align-items: center;
  max-width: 980px; margin: 0 auto; font-size: 13px; color: var(--text-3);
}
.site-footer a { color: var(--text-3); text-decoration: none; }
.site-footer a:hover { color: var(--accent); }
.footer-wrap { border-top: 1px solid var(--border); margin-top: 80px; }

/* ── Animations ── */
.reveal { opacity: 0; transform: translateY(20px); transition: opacity 0.7s cubic-bezier(0.25,0.46,0.45,0.94), transform 0.7s cubic-bezier(0.25,0.46,0.45,0.94); }
.reveal.visible { opacity: 1; transform: none; }
@media (prefers-reduced-motion: reduce) {
  .reveal { opacity: 1; transform: none; transition: none; }
  .card { transition: none; }
  .card:hover { transform: none; }
}

/* ── Responsive ── */
@media (max-width: 1024px) {
  .page-layout { grid-template-columns: 1fr; gap: 0; }
  .sidebar { display: none; }
  .sidebar-toggle { display: block; }
  .summary-grid { grid-template-columns: 1fr 1fr; }
  .cards-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 768px) {
  h1 { font-size: 36px; }
  h2 { font-size: 26px; margin-top: 48px; }
  h3 { font-size: 20px; margin-top: 32px; }
  .nav-links { display: none; }
  .nav-menu-btn { display: block; }
  .summary-grid { grid-template-columns: 1fr; gap: 32px; }
  .cards-grid { grid-template-columns: 1fr; }
  .stat-ribbon { flex-direction: column; gap: 20px; }
  .stat-sep { width: 40px; height: 1px; }
  .page-nav { flex-direction: column; gap: 16px; }
  .page-nav .next { text-align: left; margin-left: 0; }
  .hero { padding-top: 72px; }
  .page-header { padding-top: 64px; }
}
"""

# ── JavaScript ────────────────────────────────────────────────────────────────

JS = """\
(function(){
  // Reduced motion check
  var rm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Scroll reveal
  if (!rm) {
    var obs = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) { if (e.isIntersecting) e.target.classList.add('visible'); });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    document.querySelectorAll('.reveal').forEach(function(el) { obs.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function(el) { el.classList.add('visible'); });
  }

  // Count-up animation
  document.querySelectorAll('[data-countup]').forEach(function(el) {
    if (rm) return;
    var o = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        if (e.isIntersecting) { countUp(el, el.getAttribute('data-countup')); o.unobserve(el); }
      });
    }, { threshold: 0.5 });
    o.observe(el);
  });

  function countUp(el, target) {
    var m = target.match(/([~]?)([\\d,.]+)(.*)/);
    if (!m) { el.textContent = target; return; }
    var pfx = m[1], num = parseFloat(m[2].replace(/,/g, '')), sfx = m[3];
    var hasDot = m[2].indexOf('.') !== -1, start = performance.now();
    function tick(now) {
      var p = Math.min((now - start) / 1400, 1);
      var e = 1 - Math.pow(1 - p, 3);
      var c = num * e;
      var d = hasDot ? c.toFixed(1) : (num >= 1000 ? Math.floor(c).toLocaleString() : Math.floor(c).toString());
      el.textContent = pfx + d + sfx;
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  // Mobile nav
  var btn = document.querySelector('.nav-menu-btn');
  var mn = document.querySelector('.mobile-nav');
  if (btn && mn) {
    btn.addEventListener('click', function() {
      mn.classList.toggle('open');
      btn.setAttribute('aria-expanded', mn.classList.contains('open'));
    });
  }

  // Nav scroll fade — remove mask when scrolled to end
  var nl = document.querySelector('.nav-links');
  if (nl) {
    function checkFade() {
      if (nl.scrollWidth <= nl.clientWidth || nl.scrollLeft + nl.clientWidth >= nl.scrollWidth - 4) {
        nl.classList.add('no-fade');
      } else {
        nl.classList.remove('no-fade');
      }
    }
    nl.addEventListener('scroll', checkFade);
    checkFade();
    window.addEventListener('resize', checkFade);
  }

  // Sidebar TOC active tracking
  var tocLinks = document.querySelectorAll('.sidebar a');
  if (tocLinks.length > 0) {
    var headings = [];
    tocLinks.forEach(function(a) {
      var id = a.getAttribute('href');
      if (id && id.charAt(0) === '#') {
        var el = document.getElementById(id.slice(1));
        if (el) headings.push({ el: el, link: a });
      }
    });
    var tocObs = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        if (e.isIntersecting) {
          tocLinks.forEach(function(l) { l.classList.remove('active'); });
          headings.forEach(function(h) {
            if (h.el === e.target) h.link.classList.add('active');
          });
        }
      });
    }, { rootMargin: '-80px 0px -60% 0px' });
    headings.forEach(function(h) { tocObs.observe(h.el); });
  }

  // Sidebar toggle (mobile/tablet)
  var st = document.querySelector('.sidebar-toggle');
  var sb = document.querySelector('.sidebar');
  if (st && sb) {
    st.addEventListener('click', function() {
      sb.style.display = sb.style.display === 'block' ? 'none' : 'block';
    });
  }
})();
"""

# ── Markdown to HTML ──────────────────────────────────────────────────────────

def inline_md(text):
    """Process inline markdown: links, bold, code, italic."""
    text = re.sub(
        r'\[([^\]]+)\]\(([^)]+)\)',
        lambda m: '<a href="{}">{}</a>'.format(m.group(2).replace('.md', '.html'), m.group(1)),
        text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'(?<![*])\*([^*]+)\*(?![*])', r'<em>\1</em>', text)
    return text


def convert_table(lines):
    """Convert markdown table lines to HTML table."""
    if len(lines) < 2:
        return ''
    headers = [c.strip() for c in lines[0].split('|')[1:-1]]
    start = 2 if re.match(r'^[\s|:-]+$', lines[1]) else 1
    rows = [[c.strip() for c in line.split('|')[1:-1]] for line in lines[start:]]

    th = ''.join(f'<th>{inline_md(h)}</th>' for h in headers)
    trs = ''.join(
        '<tr>' + ''.join(f'<td>{inline_md(c)}</td>' for c in row) + '</tr>'
        for row in rows)
    return f'<div class="table-wrap"><table class="data-table"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def strip_heading_numbers(text):
    """Strip 'Part N:' prefix from headings."""
    text = re.sub(r'^Part\s+\d+:\s*', '', text)
    return text


def md_to_html(md_text):
    """Convert markdown to semantic HTML."""
    lines = md_text.split('\n')
    out = []
    i = 0
    n = len(lines)

    # Skip YAML frontmatter
    if lines and lines[0].strip() == '---':
        i = 1
        while i < n and lines[i].strip() != '---':
            i += 1
        i += 1

    # Skip <style> blocks
    while i < n:
        s = lines[i].strip()
        if s.startswith('<style'):
            while i < n and '</style>' not in lines[i]:
                i += 1
            i += 1
        elif not s:
            i += 1
        else:
            break

    while i < n:
        s = lines[i].strip()

        if not s:
            i += 1
            continue

        # Skip MkDocs-specific HTML
        if s.startswith('<p class="hero-') or s.startswith('<div class="stat-'):
            if 'stat-grid' in s:
                while i < n and '</div>' not in lines[i]:
                    i += 1
                while i < n and lines[i].strip() in ('</div>', ''):
                    i += 1
                continue
            i += 1
            continue

        # Admonitions
        if s.startswith('!!!') or s.startswith('\\!\\!\\!'):
            m = re.match(r'[\\!]+\s+(\w+)\s*(?:"([^"]*)")?', s)
            atitle = (m.group(2) if m and m.lastindex and m.lastindex >= 2 and m.group(2) else 'Note')
            i += 1
            body = []
            while i < n and (lines[i].startswith('    ') or not lines[i].strip()):
                if lines[i].strip():
                    body.append(lines[i].strip())
                i += 1
            out.append(f'<div class="callout"><strong>{atitle}.</strong> {inline_md(" ".join(body))}</div>')
            continue

        # HR
        if s == '---':
            out.append('<hr>')
            i += 1
            continue

        # Headers
        hm = re.match(r'^(#{1,6})\s+(.+)$', s)
        if hm:
            level = len(hm.group(1))
            raw = strip_heading_numbers(hm.group(2))
            text = inline_md(raw)
            anchor = re.sub(r'[^a-z0-9 -]', '', raw.lower()).strip().replace(' ', '-')
            anchor = re.sub(r'-+', '-', anchor)
            out.append(f'<h{level} id="{anchor}">{text}</h{level}>')
            i += 1
            continue

        # Details blocks
        if s.startswith('<details'):
            block = []
            depth = 0
            while i < n:
                line = lines[i]
                if '<details' in line:
                    depth += 1
                if '</details>' in line:
                    depth -= 1
                block.append(line)
                i += 1
                if depth == 0:
                    break
            block_html = '\n'.join(block)
            block_html = re.sub(r'\.md(#|")', r'.html\1', block_html)
            block_html = re.sub(r'`([^`]+)`', r'<code>\1</code>', block_html)
            # Convert tables inside details
            block_html = _style_tables_in_html(block_html)
            out.append(block_html)
            continue

        # Blockquotes
        if s.startswith('>'):
            bq = []
            while i < n and lines[i].strip().startswith('>'):
                bq.append(lines[i].strip().lstrip('>').strip())
                i += 1
            out.append(f'<blockquote>{inline_md(" ".join(bq))}</blockquote>')
            continue

        # Tables
        if s.startswith('|') and '|' in s[1:]:
            tbl = []
            while i < n and lines[i].strip().startswith('|'):
                tbl.append(lines[i].strip())
                i += 1
            out.append(convert_table(tbl))
            continue

        # Unordered list
        if re.match(r'^[-*]\s', s):
            items = []
            while i < n and re.match(r'^[-*]\s', lines[i].strip()):
                items.append(inline_md(re.sub(r'^[-*]\s', '', lines[i].strip())))
                i += 1
            out.append('<ul>' + ''.join(f'<li>{it}</li>' for it in items) + '</ul>')
            continue

        # Ordered list
        if re.match(r'^\d+\.\s', s):
            items = []
            while i < n and re.match(r'^\d+\.\s', lines[i].strip()):
                items.append(inline_md(re.sub(r'^\d+\.\s', '', lines[i].strip())))
                i += 1
            out.append('<ol>' + ''.join(f'<li>{it}</li>' for it in items) + '</ol>')
            continue

        # Paragraph
        para = []
        start_i = i
        while i < n:
            ls = lines[i].strip()
            if not ls or ls.startswith('#') or ls.startswith('|') or ls == '---' \
                    or ls.startswith('>') or ls.startswith('- ') or ls.startswith('* ') \
                    or re.match(r'^\d+\.\s', ls) or ls.startswith('!!!') \
                    or ls.startswith('\\!\\!\\!') or ls.startswith('<details') \
                    or ls.startswith('</details') or ls.startswith('<summary') \
                    or ls.startswith('</summary') or ls.startswith('<p class=') \
                    or ls.startswith('<div class='):
                break
            para.append(ls)
            i += 1
        if para:
            out.append(f'<p>{inline_md(" ".join(para))}</p>')
        if i == start_i:
            i += 1

    return '\n'.join(out)


def _style_tables_in_html(html):
    """Convert markdown tables inside raw HTML blocks."""
    lines = html.split('\n')
    result = []
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith('|') and s.endswith('|') and '<' not in s:
            tbl = []
            while i < len(lines) and lines[i].strip().startswith('|') and lines[i].strip().endswith('|') and '<' not in lines[i]:
                tbl.append(lines[i].strip())
                i += 1
            if len(tbl) >= 2:
                result.append(convert_table(tbl))
            else:
                result.extend(tbl)
        else:
            result.append(lines[i])
            i += 1
    return '\n'.join(result)


def extract_toc(html):
    """Extract h2/h3 headings for sidebar TOC."""
    toc = []
    for m in re.finditer(r'<(h[23]) id="([^"]*)"[^>]*>(.*?)</\1>', html):
        level = int(m.group(1)[1])
        anchor = m.group(2)
        title = re.sub(r'<[^>]+>', '', m.group(3))
        toc.append((level, anchor, title))
    return toc


# ── HTML generation ───────────────────────────────────────────────────────────

GITHUB_ICON = '<svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>'
CHECK_ICON = '<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>'


NAV_LABELS = {
    "Data Import & Hotfix Repair": "Import",
    "NPC Audits & Corrections": "NPCs",
    "Quests & Localization": "Quests",
    "Database Cleanup & Integrity": "Cleanup",
    "Performance & Build Diff": "Performance",
    "Placement Audits": "Placement",
    "Tooling & Results": "Tooling",
    "Hotfix Redundancy Audit": "Hotfix Audit",
    "Discoveries & Lessons": "Discoveries",
    "Timeline & Reference": "Timeline",
}


def nav_label(title):
    return NAV_LABELS.get(title, title)


def nav_html(current_slug=None):
    links = ''.join(
        '<a href="{s}.html"{c}>{t}</a>'.format(
            s=p['slug'],
            t=nav_label(p['title']),
            c=' class="active"' if p['slug'] == current_slug else '')
        for p in PAGES)

    mobile_links = ''.join(
        f'<a href="{p["slug"]}.html">{p["title"]}</a>' for p in PAGES)

    return f'''<nav class="site-nav" role="navigation" aria-label="Main">
<div class="nav-inner">
<a href="index.html" class="nav-logo">VoxCore</a>
<div class="nav-links">{links}</div>
<div class="nav-end">
<a href="https://github.com/VoxCore84/roleplaycore-report" class="nav-github" aria-label="GitHub">{GITHUB_ICON}</a>
<button class="nav-menu-btn" aria-label="Menu" aria-expanded="false">
<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
</button>
</div>
</div>
</nav>
<div class="mobile-nav" role="dialog" aria-label="Navigation">{mobile_links}</div>'''


def footer_html():
    return '''<div class="footer-wrap"><footer class="site-footer">
<span>VoxCore &mdash; March 2026</span>
<a href="https://github.com/VoxCore84/roleplaycore-report">GitHub</a>
</footer></div>'''


def sidebar_html(toc):
    if not toc:
        return ''
    links = ''.join(
        f'<a href="#{anchor}" class="{"toc-h3" if level == 3 else ""}">{title}</a>'
        for level, anchor, title in toc)
    return f'<button class="sidebar-toggle">On this page</button><nav class="sidebar" aria-label="Table of contents">{links}</nav>'


def prev_next_html(prev_page, next_page):
    parts = []
    if prev_page:
        parts.append(f'<a href="{prev_page["slug"]}.html" class="prev"><span class="nav-label">Previous</span>\u2190 {prev_page["title"]}</a>')
    else:
        parts.append('<span></span>')
    if next_page:
        parts.append(f'<a href="{next_page["slug"]}.html" class="next"><span class="nav-label">Next</span>{next_page["title"]} \u2192</a>')
    else:
        parts.append('<span></span>')
    return f'<nav class="page-nav">{parts[0]}{parts[1]}</nav>'


def base_page(title, body, current_slug=None, is_index=False):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — VoxCore</title>
<meta name="description" content="VoxCore Database Report — Data Quality & Optimization Summary">
<style>{CSS}</style>
</head>
<body>
{nav_html(current_slug)}
{body}
{footer_html()}
<script>{JS}</script>
</body>
</html>'''


# ── Page builders ─────────────────────────────────────────────────────────────

def build_index():
    # Stat ribbon
    stat_items = []
    for i, (val, label) in enumerate(HERO_STATS):
        if i > 0:
            stat_items.append('<span class="stat-sep"></span>')
        stat_items.append(f'<div class="stat-item"><span class="stat-num" data-countup="{val}">{val}</span><span class="stat-label">{label}</span></div>')
    stats_html = ''.join(stat_items)

    # Exec summary
    cols = ''
    for cat, items in EXEC_GROUPS:
        rows = ''.join(
            f'<div class="summary-row"><span class="label">{label}</span><span class="value">{value}</span></div>'
            for label, value in items)
        cols += f'<div class="summary-col"><h3>{cat}</h3>{rows}</div>'

    # Section cards
    cards = ''
    for p in PAGES:
        icon = ICONS.get(p['slug'], '')
        cards += f'<a href="{p["slug"]}.html" class="card reveal"><span class="card-icon">{icon}</span><h3>{p["title"]}</h3><p>{p["desc"]}</p></a>\n'

    body = f'''<main>
<section class="hero reveal">
<p class="hero-label">Database Report</p>
<h1>VoxCore</h1>
<p class="hero-sub">Data Quality & Optimization Summary</p>
<p class="hero-meta">Prepared for CaptainCore (LoreWalkerTDB) &middot; March 2026 &middot; WoW 12.x Midnight &middot; Build 66220</p>
</section>

<section class="stat-ribbon reveal">{stats_html}</section>

<div class="banner reveal">{CHECK_ICON}<span>All tooling is open and reproducible. Every operation can be re-run from scripts in the repository. See <a href="reference.html#appendix-b-reproducibility">Reproducibility</a>.</span></div>

<section class="summary reveal">
<h2>Executive Summary</h2>
<p>Over February\u2013March 2026, VoxCore imported, validated, and repaired data from four major sources, performed multi-pass audits across all five databases, and built a Python tooling pipeline to make the process repeatable.</p>
<div class="summary-grid">{cols}</div>
</section>

<section class="cards-section">
<div class="cards-wrap">
<div class="cards-grid">{cards}</div>
</div>
</section>
</main>'''

    return base_page("Database Report", body, is_index=True)


def build_page(page, prev_p, next_p):
    md_path = os.path.join(CONTENT_DIR, f"{page['slug']}.md")
    with open(md_path, 'r', encoding='utf-8') as f:
        md = f.read()

    # Strip first heading
    md = re.sub(r'^#\s+[^\n]+\n', '', md.strip(), count=1)

    html = md_to_html(md)
    toc = extract_toc(html)

    body = f'''<main>
<header class="page-header">
<nav class="breadcrumb"><a href="index.html">VoxCore</a> &rsaquo; {page["title"]}</nav>
<h1>{page["title"]}</h1>
</header>
<div class="page-layout">
{sidebar_html(toc)}
<article>
{html}
{prev_next_html(prev_p, next_p)}
</article>
</div>
</main>'''

    return base_page(page['title'], body, current_slug=page['slug'])


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # Index
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(build_index())
    print("Built: index.html")

    # Interior pages
    for i, page in enumerate(PAGES):
        prev_p = PAGES[i - 1] if i > 0 else None
        next_p = PAGES[i + 1] if i < len(PAGES) - 1 else None
        html = build_page(page, prev_p, next_p)
        with open(os.path.join(OUTPUT_DIR, f"{page['slug']}.html"), 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Built: {page['slug']}.html")

    # .nojekyll to prevent GitHub Pages Jekyll processing
    open(os.path.join(OUTPUT_DIR, '.nojekyll'), 'w').close()

    print(f"\nDone: {len(PAGES) + 1} pages in {OUTPUT_DIR}/")


if __name__ == '__main__':
    main()
