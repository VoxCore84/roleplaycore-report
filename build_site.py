#!/usr/bin/env python3
"""Build the VoxCore Report static site from markdown content."""

import re
import os
import shutil

SCRIPT_BLOCK = """<script>
// Scroll reveal
const obs=new IntersectionObserver(e=>e.forEach(x=>{if(x.isIntersecting)x.target.classList.add('visible')}),{threshold:0.1,rootMargin:'0px 0px -50px 0px'});
document.querySelectorAll('.reveal').forEach(el=>obs.observe(el));

// Count-up animation
document.querySelectorAll('[data-countup]').forEach(el=>{
const o=new IntersectionObserver(e=>e.forEach(x=>{if(x.isIntersecting){animate(el,el.getAttribute('data-countup'));o.unobserve(el)}}),{threshold:0.5});
o.observe(el);
});
function animate(el,t){
const m=t.match(/([~]?)([\\d,.]+)(.*)/);if(!m){el.textContent=t;return}
const pfx=m[1],num=parseFloat(m[2].replace(/,/g,'')),sfx=m[3],hasDot=m[2].includes('.'),start=performance.now();
function up(now){
const p=Math.min((now-start)/1500,1),e=1-Math.pow(1-p,3),c=num*e;
let d=hasDot?c.toFixed(1):num>=1000?Math.floor(c).toLocaleString():Math.floor(c).toString();
el.textContent=pfx+d+sfx;if(p<1)requestAnimationFrame(up)}
requestAnimationFrame(up)}

// Nav dropdown
const toggle=document.getElementById('nav-toggle');
const dropdown=document.getElementById('nav-dropdown');
if(toggle&&dropdown){
toggle.addEventListener('click',e=>{e.stopPropagation();dropdown.classList.toggle('open')});
document.addEventListener('click',()=>dropdown.classList.remove('open'));
dropdown.addEventListener('click',e=>e.stopPropagation());
}
</script>"""

SITE_DIR = os.path.join(os.path.dirname(__file__), "site")
DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")

PAGES = [
    {"slug": "data-import", "title": "Data Import & Hotfix Repair", "parts": "Parts 1\u20132"},
    {"slug": "npc-audits", "title": "NPC Audits & Corrections", "parts": "Part 3"},
    {"slug": "quest-localization", "title": "Quests & Localization", "parts": "Parts 4\u20135"},
    {"slug": "database-cleanup", "title": "Database Cleanup", "parts": "Part 6"},
    {"slug": "performance", "title": "Performance & Build Diff", "parts": "Parts 7\u20138"},
    {"slug": "placement", "title": "Placement Audits", "parts": "Part 9"},
    {"slug": "results", "title": "Tooling & Results", "parts": "Parts 10\u201312"},
    {"slug": "hotfix-audit", "title": "Hotfix Redundancy Audit", "parts": "Part 13"},
    {"slug": "discoveries", "title": "Discoveries & Lessons", "parts": "Part 14"},
    {"slug": "reference", "title": "Timeline & Reference", "parts": "Parts 15\u201316, Appendices"},
]

NAV_CARDS = [
    ("data-import.html", "1\u20132", "Data Import & Hotfix Repair", "~1M rows imported, 103K hotfix entries repaired"),
    ("npc-audits.html", "3", "NPC Audits & Corrections", "78,475 fixes across 27-check validator + Wowhead mega-audit"),
    ("quest-localization.html", "4\u20135", "Quests & Localization", "21K chain links, 1.6M locale rows across 10 languages"),
    ("database-cleanup.html", "6", "Database Cleanup & Integrity", "412K dead rows removed, loot PK discovery, 47K post-import cleanup"),
    ("performance.html", "7\u20138", "Performance & Build Diff", "3m24s to 17s startup, 5-build diff audit"),
    ("placement.html", "9", "Placement Audits", "31K placement fixes generated"),
    ("results.html", "10\u201312", "Tooling & Results", "50+ tools built, final DB state, before/after"),
    ("hotfix-audit.html", "13", "Hotfix Redundancy Audit", "10.8M to 244K rows (97.8% reduction)"),
    ("discoveries.html", "14", "Discoveries & Lessons", "9 community findings for any TC project"),
    ("reference.html", "15\u201316", "Timeline & Reference", "Full timeline, 50+ tool catalog, reproducibility"),
]

HERO_STATS = [
    ("~1M", "rows imported", ""),
    ("103K", "hotfix entries repaired", ""),
    ("97.8%", "redundant rows removed", ""),
    ("78K", "NPC corrections", ""),
    ("1.6M", "item translations", ""),
    ("17s", "server startup", "(was 3m24s)"),
]

EXEC_GROUPS = [
    ("Data Imported", [
        ("LoreWalkerTDB world rows", "~1,004,000 net"),
        ("Hotfix rows repaired", "103,153 inserts + 1,831 fixes"),
        ("Item locale translations", "1,628,651 rows (10 languages)"),
        ("Quest chain links", "21,758 updates"),
        ("Quest POI/objectives", "2,880 POI + 5,199 pts + 633 obj"),
    ]),
    ("Data Corrected", [
        ("NPC fixes", "78,475 total"),
    ]),
    ("Data Cleaned", [
        ("Hotfix redundancy audit", "10.6M rows removed (97.8%)"),
        ("Pre-existing dead rows", "~412,000"),
        ("Duplicate loot rows", "193,542"),
        ("Post-import cleanup", "~47,000"),
    ]),
    ("Performance", [
        ("Server startup", "3m24s \u2192 17s (92% reduction)"),
        ("Hotfix content tables", "10.8M \u2192 ~244K rows"),
    ]),
]


def fix_links(text):
    """Fix .md links to .html."""
    return re.sub(r'\.md(#|")', r'.html\1', text)


def inline_md(text):
    """Convert inline markdown to HTML."""
    # Links
    text = re.sub(
        r'\[([^\]]+)\]\(([^)]+)\)',
        lambda m: '<a href="{}" class="text-amber-400 hover:text-amber-300 underline decoration-amber-400/30 hover:decoration-amber-400 transition-colors">{}</a>'.format(
            m.group(2).replace('.md', '.html'), m.group(1)),
        text
    )
    # Bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code class="text-amber-400/80 bg-white/5 px-1.5 py-0.5 rounded text-sm">\1</code>', text)
    # Italic (single *)
    text = re.sub(r'(?<![*])\*([^*]+)\*(?![*])', r'<em>\1</em>', text)
    return text


def convert_table(lines):
    """Convert a list of markdown table lines to HTML."""
    if len(lines) < 2:
        return ''
    headers = [c.strip() for c in lines[0].strip('|').split('|') if c.strip() or True]
    headers = [c.strip() for c in lines[0].split('|')[1:-1]]  # skip empty first/last

    start = 2 if len(lines) > 1 and re.match(r'^[\s|:-]+$', lines[1]) else 1
    rows = []
    for line in lines[start:]:
        cells = [c.strip() for c in line.split('|')[1:-1]]
        rows.append(cells)

    th = ''.join(f'<th class="px-4 py-3 text-left text-xs font-semibold text-amber-400/80 uppercase tracking-wider">{inline_md(h)}</th>' for h in headers)
    trs = ''
    for row in rows:
        tds = ''.join(f'<td class="px-4 py-3 text-sm text-white/70 border-t border-white/5">{inline_md(c)}</td>' for c in row)
        trs += f'<tr class="hover:bg-white/[0.02] transition-colors">{tds}</tr>'

    return f'''<div class="overflow-x-auto my-6 rounded-lg border border-white/10">
<table class="w-full"><thead class="bg-white/[0.03]"><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'''


def md_to_html(md_text):
    """Line-by-line markdown to HTML conversion."""
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

        # Empty
        if not s:
            i += 1
            continue

        # MkDocs-specific HTML (skip stat-grid, hero-sub etc)
        if s.startswith('<p class="hero-') or s.startswith('<div class="stat-'):
            # Skip until closing div for stat-grid
            if 'stat-grid' in s:
                while i < n and '</div>' not in lines[i]:
                    i += 1
                # Skip remaining closing tags
                while i < n and lines[i].strip() in ('</div>', ''):
                    i += 1
                continue
            i += 1
            continue

        # MkDocs admonition (!!! type)
        if s.startswith('!!!') or s.startswith('\\!\\!\\!'):
            m = re.match(r'[\\!]+\s+(\w+)\s*(?:"([^"]*)")?', s)
            atype = m.group(1) if m else 'note'
            atitle = (m.group(2) if m and m.group(2) else atype.capitalize())
            i += 1
            body_lines = []
            while i < n and (lines[i].startswith('    ') or not lines[i].strip()):
                if lines[i].strip():
                    body_lines.append(lines[i].strip())
                i += 1
            body = inline_md(' '.join(body_lines))
            icon = {'success': '\u2713', 'note': '\u2139', 'warning': '\u26a0'}.get(atype, '\u2139')
            out.append(f'<div class="bg-amber-400/5 border border-amber-400/20 rounded-lg p-6 my-8"><div class="flex items-start gap-3"><span class="text-amber-400 text-lg mt-0.5">{icon}</span><div><div class="font-semibold text-amber-400 mb-1">{atitle}</div><p class="text-white/70 text-sm leading-relaxed">{body}</p></div></div></div>')
            continue

        # HR
        if s == '---':
            out.append('<hr class="border-white/10 my-12">')
            i += 1
            continue

        # Headers
        hm = re.match(r'^(#{1,6})\s+(.+)$', s)
        if hm:
            level = len(hm.group(1))
            text = inline_md(hm.group(2))
            raw = hm.group(2).lower()
            anchor = re.sub(r'[^a-z0-9 -]', '', raw).strip().replace(' ', '-')
            anchor = re.sub(r'-+', '-', anchor)
            sizes = {1:'text-4xl font-bold tracking-tight mb-8 mt-16',2:'text-3xl font-bold tracking-tight mb-6 mt-14',3:'text-2xl font-semibold mb-4 mt-10',4:'text-xl font-semibold mb-3 mt-8',5:'text-lg font-semibold mb-2 mt-6',6:'text-base font-semibold mb-2 mt-4'}
            cls = sizes.get(level, sizes[6])
            out.append(f'<h{level} id="{anchor}" class="{cls}">{text}</h{level}>')
            i += 1
            continue

        # Details blocks — pass through with styling
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
            # Fix links
            block_html = fix_links(block_html)
            # Apply inline markdown to table cells and text
            block_html = re.sub(r'`([^`]+)`', r'<code class="text-amber-400/80 bg-white/5 px-1 py-0.5 rounded text-xs">\1</code>', block_html)
            # Style the details element
            block_html = block_html.replace('<details>', '<details class="group bg-white/[0.02] border border-white/10 rounded-lg my-4 overflow-hidden">')
            block_html = block_html.replace('<details\n', '<details class="group bg-white/[0.02] border border-white/10 rounded-lg my-4 overflow-hidden"\n')
            block_html = re.sub(r'<summary>', '<summary class="cursor-pointer px-6 py-4 hover:bg-white/[0.03] transition-colors">', block_html)
            # Style any tables inside
            block_html = style_tables_in_html(block_html)
            out.append(block_html)
            continue

        # Blockquotes
        if s.startswith('>'):
            bq = []
            while i < n and lines[i].strip().startswith('>'):
                bq.append(lines[i].strip().lstrip('>').strip())
                i += 1
            out.append(f'<blockquote class="border-l-2 border-amber-400/40 pl-6 my-6 text-white/60 italic">{inline_md(" ".join(bq))}</blockquote>')
            continue

        # Tables
        if '|' in s and s.startswith('|'):
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
            lis = ''.join(f'<li class="text-white/70 leading-relaxed">{it}</li>' for it in items)
            out.append(f'<ul class="list-disc list-inside space-y-2 my-4 ml-4">{lis}</ul>')
            continue

        # Ordered list
        if re.match(r'^\d+\.\s', s):
            items = []
            while i < n and re.match(r'^\d+\.\s', lines[i].strip()):
                items.append(inline_md(re.sub(r'^\d+\.\s', '', lines[i].strip())))
                i += 1
            lis = ''.join(f'<li class="text-white/70 leading-relaxed">{it}</li>' for it in items)
            out.append(f'<ol class="list-decimal list-inside space-y-2 my-4 ml-4">{lis}</ol>')
            continue

        # Paragraph — collect until next block element
        para = []
        start_i = i
        while i < n:
            ls = lines[i].strip()
            if not ls or ls.startswith('#') or ls.startswith('|') or ls == '---' or ls.startswith('>') or ls.startswith('- ') or ls.startswith('* ') or re.match(r'^\d+\.\s', ls) or ls.startswith('!!!') or ls.startswith('\\!\\!\\!') or ls.startswith('<details') or ls.startswith('</details') or ls.startswith('<p class=') or ls.startswith('<div class=') or ls.startswith('<summary') or ls.startswith('</summary'):
                break
            para.append(ls)
            i += 1
        if para:
            out.append(f'<p class="text-white/70 leading-relaxed my-4">{inline_md(" ".join(para))}</p>')
        if i == start_i:
            i += 1  # safety: skip unrecognized line to prevent infinite loop

    return '\n'.join(out)


def style_tables_in_html(html):
    """Find markdown-style tables in HTML and convert them."""
    lines = html.split('\n')
    result = []
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        # Only match lines that look like markdown table rows (not HTML containing |)
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


def base_html(title, body, is_index=False):
    nav_items = ''.join(
        f'<a href="{p["slug"]}.html" class="block px-4 py-2.5 text-sm text-white/60 hover:text-amber-400 hover:bg-white/[0.03] transition-colors rounded-lg">{p["parts"]} &mdash; {p["title"]}</a>'
        for p in PAGES
    )
    back = '' if is_index else '<a href="index.html" class="inline-flex items-center gap-2 text-amber-400/70 hover:text-amber-400 transition-colors text-sm mb-8"><svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>Back to Overview</a>'

    return f'''<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — VoxCore</title>
<meta name="description" content="VoxCore Database Report — Data Quality & Optimization Summary">
<script src="https://cdn.tailwindcss.com"></script>
<link rel="preconnect" href="https://api.fontshare.com">
<link href="https://api.fontshare.com/v2/css?f[]=clash-display@400;500;600;700&f[]=satoshi@400;500;700&display=swap" rel="stylesheet">
<style>
body {{ font-family: 'Satoshi', system-ui, sans-serif; background: #0a0a0b; color: #e5e5e5; }}
h1,h2,h3,h4,h5,h6 {{ font-family: 'Clash Display', 'Satoshi', system-ui, sans-serif; }}
.glass {{ background: rgba(255,255,255,0.03); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.06); }}
.glass-nav {{ background: rgba(10,10,11,0.8); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255,255,255,0.06); }}
.stat-glow {{ box-shadow: 0 0 40px rgba(245,158,11,0.05); }}
.reveal {{ opacity: 0; transform: translateY(20px); transition: opacity 0.6s ease, transform 0.6s ease; }}
.reveal.visible {{ opacity: 1; transform: translateY(0); }}
.nav-card {{ transition: all 0.3s ease; }}
.nav-card:hover {{ transform: translateY(-2px); box-shadow: 0 8px 30px rgba(245,158,11,0.08); border-color: rgba(245,158,11,0.3); }}
.nav-dropdown {{ opacity: 0; transform: translateY(-8px); pointer-events: none; transition: opacity 0.2s ease, transform 0.2s ease; }}
.nav-dropdown.open {{ opacity: 1; transform: translateY(0); pointer-events: auto; }}
details summary::-webkit-details-marker {{ display: none; }}
details summary {{ list-style: none; }}
::-webkit-scrollbar {{ width: 8px; }}
::-webkit-scrollbar-track {{ background: #0a0a0b; }}
::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.1); border-radius: 4px; }}
::-webkit-scrollbar-thumb:hover {{ background: rgba(255,255,255,0.2); }}
</style>
</head>
<body class="min-h-screen">
<nav class="glass-nav fixed top-0 left-0 right-0 z-50">
<div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
<a href="index.html" class="text-lg font-semibold tracking-tight" style="font-family:'Clash Display',sans-serif"><span class="text-amber-400">Vox</span><span class="text-white/90">Core</span></a>
<div class="flex items-center gap-4">
<a href="https://github.com/VoxCore84/roleplaycore-report" class="text-white/40 hover:text-white/70 transition-colors" aria-label="GitHub">
<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
</a>
<div class="relative">
<button id="nav-toggle" class="flex items-center gap-2 text-sm text-white/60 hover:text-white/90 transition-colors px-3 py-1.5 rounded-lg border border-white/10 hover:border-white/20">
<span>Sections</span>
<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
</button>
<div id="nav-dropdown" class="nav-dropdown absolute right-0 top-full mt-2 w-72 py-2 rounded-xl border border-white/10 bg-[#0a0a0b]/95 backdrop-blur-xl shadow-2xl shadow-black/50">
{nav_items}
</div>
</div>
</div>
</div>
</nav>
<main class="max-w-4xl mx-auto px-6 pt-24 pb-20">{back}{body}</main>
<footer class="border-t border-white/5 mt-20">
<div class="max-w-6xl mx-auto px-6 py-12 flex flex-col md:flex-row items-center justify-between gap-4">
<div class="text-white/30 text-sm"><span class="text-amber-400/60">VoxCore</span> &mdash; March 2026 &mdash; VoxCore84</div>
<div class="flex gap-6 text-white/30 text-sm">
<a href="https://github.com/VoxCore84/roleplaycore-report" class="hover:text-amber-400 transition-colors">GitHub</a>
<a href="reference.html" class="hover:text-amber-400 transition-colors">Reference</a>
</div>
</div>
</footer>
{SCRIPT_BLOCK}
</body>
</html>'''


def build_index():
    # Stat cards
    stats = ''
    for i, (val, label, sfx) in enumerate(HERO_STATS):
        sx = f' <span class="text-white/30 text-sm">{sfx}</span>' if sfx else ''
        stats += f'<div class="glass rounded-xl p-6 text-center stat-glow reveal" style="transition-delay:{i*100}ms"><span class="text-3xl md:text-4xl font-bold text-amber-400 block" style="font-family:\'Clash Display\',sans-serif" data-countup="{val}">{val}</span><span class="text-white/50 text-sm mt-2 block">{label}{sx}</span></div>\n'

    # Exec summary groups
    exec_html = ''
    for cat, items in EXEC_GROUPS:
        rows = ''
        for label, value in items:
            rows += f'<div class="flex justify-between items-baseline py-2 border-b border-white/5 last:border-0"><span class="text-white/60 text-sm">{label}</span><span class="text-white/90 text-sm font-medium tabular-nums">{value}</span></div>'
        exec_html += f'<div class="glass rounded-xl p-6 reveal"><h4 class="text-amber-400/80 text-xs font-semibold uppercase tracking-wider mb-4">{cat}</h4>{rows}</div>\n'

    # Nav cards
    cards = ''
    for href, num, title, desc in NAV_CARDS:
        cards += f'''<a href="{href}" class="nav-card glass rounded-xl p-6 block group reveal">
<div class="flex items-start justify-between mb-3"><span class="text-amber-400/60 text-xs font-semibold uppercase tracking-wider">Parts {num}</span>
<svg class="w-4 h-4 text-white/20 group-hover:text-amber-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg></div>
<h3 class="text-lg font-semibold text-white/90 mb-2" style="font-family:'Clash Display',sans-serif">{title}</h3>
<p class="text-white/50 text-sm leading-relaxed">{desc}</p></a>\n'''

    body = f'''
<div class="text-center pt-16 pb-12 reveal">
<p class="text-amber-400/60 text-sm font-semibold uppercase tracking-[0.2em] mb-4">Database Report</p>
<h1 class="text-5xl md:text-7xl font-bold tracking-tight mb-4" style="font-family:'Clash Display',sans-serif"><span class="text-white">Vox</span><span class="text-amber-400">Core</span></h1>
<p class="text-white/50 text-lg max-w-xl mx-auto mb-2">Data Quality & Optimization Summary</p>
<p class="text-white/30 text-sm">Prepared for CaptainCore (LoreWalkerTDB) &middot; March 2026 &middot; WoW 12.x Midnight &middot; Build 66220</p>
</div>
<div class="grid grid-cols-2 md:grid-cols-3 gap-4 my-16">{stats}</div>
<div class="glass rounded-xl p-6 my-12 border-l-4 border-amber-400/40 reveal">
<div class="flex items-start gap-3"><span class="text-amber-400 text-lg">\u2713</span><div>
<div class="font-semibold text-white/90 mb-1">All tooling is open and reproducible</div>
<p class="text-white/60 text-sm">Every operation documented here can be re-run from scripts in the repository. See <a href="reference.html#appendix-b-reproducibility" class="text-amber-400 hover:text-amber-300 underline decoration-amber-400/30">Reproducibility</a> for the full pipeline.</p>
</div></div></div>
<section class="my-20 reveal">
<h2 class="text-3xl font-bold tracking-tight mb-3" style="font-family:'Clash Display',sans-serif">Executive Summary</h2>
<p class="text-white/50 text-sm mb-8">Over February\u2013March 2026, VoxCore imported, validated, and repaired data from four major sources, performed multi-pass audits across all five databases, and built a Python tooling pipeline to make the process repeatable.</p>
<div class="grid md:grid-cols-2 gap-4">{exec_html}</div>
</section>
<section class="my-20">
<h2 class="text-3xl font-bold tracking-tight mb-8 reveal" style="font-family:'Clash Display',sans-serif">Explore the Report</h2>
<div class="grid md:grid-cols-2 gap-4">{cards}</div>
</section>'''

    return base_html("Database Report", body, is_index=True)


def build_page(page):
    md_path = os.path.join(DOCS_DIR, f"{page['slug']}.md")
    with open(md_path, 'r', encoding='utf-8') as f:
        md = f.read()

    # Strip first heading (we provide our own)
    md = re.sub(r'^#\s+[^\n]+\n', '', md.strip(), count=1)

    html = md_to_html(md)

    body = f'''
<div class="reveal">
<p class="text-amber-400/60 text-xs font-semibold uppercase tracking-[0.2em] mb-3">{page['parts']}</p>
<h1 class="text-4xl md:text-5xl font-bold tracking-tight mb-8" style="font-family:'Clash Display',sans-serif">{page['title']}</h1>
</div>
<article class="reveal">{html}</article>'''

    return base_html(page['title'], body)


def main():
    if os.path.exists(SITE_DIR):
        shutil.rmtree(SITE_DIR)
    os.makedirs(SITE_DIR)

    with open(os.path.join(SITE_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(build_index())
    print("Built: index.html")

    for page in PAGES:
        html = build_page(page)
        with open(os.path.join(SITE_DIR, f"{page['slug']}.html"), 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Built: {page['slug']}.html")

    print(f"\nDone: {len(PAGES) + 1} pages in site/")


if __name__ == '__main__':
    main()
