#!/usr/bin/env python3
"""Build the VoxCore site — Apple HIG x Warcraft atmosphere."""

import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(ROOT, "content")
OUTPUT_DIR = os.path.join(ROOT, "docs")
STATIC_DIR = os.path.join(ROOT, "static")
DATA_DIR = os.path.join(ROOT, "data")

# ── Load external assets ─────────────────────────────────────────────────────

def _read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def _read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

CSS = _read(os.path.join(STATIC_DIR, "css", "style.css"))
JS = _read(os.path.join(STATIC_DIR, "js", "main.js"))
STATS = _read_json(os.path.join(DATA_DIR, "stats.json"))
CHANGELOG = _read_json(os.path.join(DATA_DIR, "changelog.json"))

# ── Page definitions ──────────────────────────────────────────────────────────

FEATURE_PAGES = [
    {"slug": "framework",   "title": "The Framework",  "desc": f"{STATS['custom_systems']} custom C++ systems, persistent RP commands, transmog outfits, companion AI"},
    {"slug": "pipeline",    "title": "Data Pipeline",   "desc": f"TACT extraction \u2192 CSV merge \u2192 hotfix repair \u2192 validation \u2014 {STATS['db2_tables']} tables, fully automated"},
    {"slug": "tooling",     "title": "Tooling",        "desc": f"{STATS['tools_built']} tools \u2014 data pipelines, audit validators, packet analyzers, MCP servers"},
    {"slug": "ai-workflow", "title": "AI Workflow",     "desc": f"Claude Code integration \u2014 {STATS['claude_commands']} skills, 4 MCP servers, parallel agent architecture"},
    {"slug": "status",      "title": "Project Status",  "desc": f"Database health, {STATS['dev_sessions']} sessions logged, open issues, repository activity"},
    {"slug": "opensource",  "title": "Open Source",     "desc": "9 repositories, 6 public gists, community tools and reference data"},
]

REPORT_PAGES = [
    {"slug": "data-import",        "title": "Data Import & Hotfix Repair",   "desc": f"{STATS['rows_imported_short']} rows imported, {STATS['hotfix_entries_short']} hotfix entries repaired"},
    {"slug": "npc-audits",         "title": "NPC Audits & Corrections",      "desc": f"{STATS['npc_corrections']} fixes across 27-check validator + Wowhead mega-audit"},
    {"slug": "quest-localization",  "title": "Quests & Localization",         "desc": f"{STATS['quest_chain_links']} chain links, {STATS['item_translations_short']} locale rows across 10 languages"},
    {"slug": "database-cleanup",   "title": "Database Cleanup & Integrity",   "desc": f"{STATS['dead_rows_cleaned']} dead rows removed, loot PK discovery, 47K post-import cleanup"},
    {"slug": "performance",        "title": "Performance & Build Diff",      "desc": f"{STATS['server_startup_before']} to {STATS['server_startup_after']} startup, 5-build diff audit with zero breaking changes"},
    {"slug": "placement",          "title": "Placement Audits",              "desc": "31K placement fixes generated from LoreWalkerTDB comparison"},
    {"slug": "results",            "title": "Tooling & Results",             "desc": f"{STATS['tools_built']} tools built, final DB state, before/after player impact"},
    {"slug": "hotfix-audit",       "title": "Hotfix Redundancy Audit",       "desc": f"10.8M to {STATS['final_hotfix_content_rows']} rows \u2014 {STATS['redundant_rows_percent']} reduction in 3 rounds"},
    {"slug": "discoveries",        "title": "Discoveries & Lessons",         "desc": "9 community-relevant findings for any TrinityCore project"},
    {"slug": "reference",          "title": "Timeline & Reference",          "desc": f"Full timeline, {STATS['tools_built']} tool catalog, data sources, reproducibility"},
]

ALL_PAGES = FEATURE_PAGES + REPORT_PAGES

NAV_ITEMS = [
    {"label": "Framework",   "slug": "framework"},
    {"label": "Pipeline",    "slug": "pipeline"},
    {"label": "Report",      "slug": "data-import"},
    {"label": "Tooling",     "slug": "tooling"},
    {"label": "AI",          "slug": "ai-workflow"},
    {"label": "Status",      "slug": "status"},
    {"label": "Open Source", "slug": "opensource"},
]

HERO_STATS = [
    (STATS['rows_imported_short'], "rows imported"),
    (STATS['hotfix_entries_short'], "hotfix entries repaired"),
    (STATS['redundant_rows_percent'], "redundant rows removed"),
    (STATS['npc_corrections_short'], "NPC corrections"),
    (STATS['tools_built'], "tools built"),
    (STATS['server_startup_after'], "server startup"),
]

# Executive summary data (from verified gist accuracy audit)
EXEC_SUMMARY = [
    ("Data Imported", "LoreWalkerTDB world rows", STATS['rows_imported']),
    ("", "Hotfix rows repaired", f"{STATS['hotfix_entries_repaired']} inserts + {STATS['hotfix_column_fixes']} column fixes"),
    ("", "Item locale translations", f"{STATS['item_translations']} rows across 10 languages"),
    ("", "Quest chain links", f"{STATS['quest_chain_links']} PrevQuestID/NextQuestID updates"),
    ("", "Quest POI/objectives", "2,880 POI + 5,199 points + 633 objectives"),
    ("Data Corrected", "NPC fixes", f"{STATS['npc_corrections']} ({STATS['npc_audit_corrections']} audit + {STATS['npc_wowhead_corrections']} Wowhead cross-ref)"),
    ("Data Cleaned", "Hotfix redundancy audit", f"{STATS['redundant_rows_removed']} redundant rows removed ({STATS['redundant_rows_percent']})"),
    ("", "Pre-existing orphan/dead rows", STATS['dead_rows_cleaned']),
    ("", "Pre-existing duplicate loot rows", "193,542"),
    ("", "Post-import cleanup", "~47,000"),
    ("Performance", "Server startup", f"{STATS['server_startup_before']} \u2192 {STATS['server_startup_after']} ({STATS['server_startup_reduction']}% reduction)"),
    ("", "Hotfix content tables", f"10.8M rows \u2192 {STATS['final_hotfix_content_rows']} rows"),
]

# ── SVG Icons ─────────────────────────────────────────────────────────────────

ICONS = {
    "framework": '<svg width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8"/><path d="M12 17v4"/><path d="M7 8l3 3-3 3"/><path d="M13 14h4"/></svg>',
    "tooling": '<svg width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>',
    "ai-workflow": '<svg width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M12 2v4"/><path d="M12 18v4"/><path d="M4.93 4.93l2.83 2.83"/><path d="M16.24 16.24l2.83 2.83"/><path d="M2 12h4"/><path d="M18 12h4"/><path d="M4.93 19.07l2.83-2.83"/><path d="M16.24 7.76l2.83-2.83"/><circle cx="12" cy="12" r="4"/></svg>',
    "pipeline": '<svg width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M3 12h4l3-9 4 18 3-9h4"/></svg>',
    "status": '<svg width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
    "opensource": '<svg width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/><path d="M14 4l-4 16"/></svg>',
    "data-import": '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 5v14c0 1.66-4.03 3-9 3s-9-1.34-9-3V5"/><path d="M21 12c0 1.66-4.03 3-9 3s-9-1.34-9-3"/></svg>',
    "npc-audits": '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/><path d="m8 11 2 2 4-4"/></svg>',
    "quest-localization": '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10A15.3 15.3 0 0 1 12 2z"/></svg>',
    "database-cleanup": '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M3 6h18"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="m19 6-.867 12.142A2 2 0 0 1 16.138 20H7.862a2 2 0 0 1-1.995-1.858L5 6"/><path d="M10 11v5"/><path d="M14 11v5"/></svg>',
    "performance": '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/></svg>',
    "placement": '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 1 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "results": '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M12 20V10"/><path d="M18 20V4"/><path d="M6 20v-4"/></svg>',
    "hotfix-audit": '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M12 20V10"/><path d="M18 20V4"/><path d="M6 20v-4"/><path d="m9 7-3 3-3-3"/></svg>',
    "discoveries": '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>',
    "reference": '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
}

GITHUB_ICON = '<svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>'
CHECK_ICON = '<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>'

# ── Architecture Diagram ─────────────────────────────────────────────────────

ARCH_SVG = '''<div class="arch-wrap reveal"><svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg" class="arch-diagram" role="img" aria-label="VoxCore architecture diagram">
<rect x="30" y="20" width="170" height="56" rx="12" fill="var(--bg-alt)" stroke="var(--border)" stroke-width="1"/>
<text x="115" y="44" text-anchor="middle" fill="var(--text)" font-family="var(--font-display)" font-weight="600" font-size="14">WoW 12.x Client</text>
<text x="115" y="62" text-anchor="middle" fill="var(--text-3)" font-family="var(--font-body)" font-size="11">Build 66220</text>
<rect x="315" y="20" width="170" height="56" rx="12" fill="var(--bg-alt)" stroke="var(--arcane)" stroke-width="1" stroke-opacity="0.4"/>
<text x="400" y="44" text-anchor="middle" fill="var(--text)" font-family="var(--font-display)" font-weight="600" font-size="14">Worldserver</text>
<text x="400" y="62" text-anchor="middle" fill="var(--text-3)" font-family="var(--font-body)" font-size="11">C++20 &middot; 11 Systems</text>
<rect x="600" y="20" width="170" height="56" rx="12" fill="var(--bg-alt)" stroke="var(--border)" stroke-width="1"/>
<text x="685" y="44" text-anchor="middle" fill="var(--text)" font-family="var(--font-display)" font-weight="600" font-size="14">MySQL 8.0</text>
<text x="685" y="62" text-anchor="middle" fill="var(--text-3)" font-family="var(--font-body)" font-size="11">5 Databases</text>
<rect x="30" y="136" width="170" height="56" rx="12" fill="var(--bg-alt)" stroke="var(--border)" stroke-width="1"/>
<text x="115" y="160" text-anchor="middle" fill="var(--text)" font-family="var(--font-display)" font-weight="600" font-size="14">Eluna Lua</text>
<text x="115" y="178" text-anchor="middle" fill="var(--text-3)" font-family="var(--font-body)" font-size="11">Scripting Engine</text>
<rect x="315" y="136" width="170" height="56" rx="12" fill="var(--bg-alt)" stroke="var(--arcane)" stroke-width="1" stroke-opacity="0.4"/>
<text x="400" y="160" text-anchor="middle" fill="var(--text)" font-family="var(--font-display)" font-weight="600" font-size="14">Claude Code</text>
<text x="400" y="178" text-anchor="middle" fill="var(--text-3)" font-family="var(--font-body)" font-size="11">17 Skills &middot; Agents</text>
<rect x="600" y="136" width="170" height="56" rx="12" fill="var(--bg-alt)" stroke="var(--border)" stroke-width="1"/>
<text x="685" y="160" text-anchor="middle" fill="var(--text)" font-family="var(--font-display)" font-weight="600" font-size="14">MCP Servers</text>
<text x="685" y="178" text-anchor="middle" fill="var(--text-3)" font-family="var(--font-body)" font-size="11">DB2 &middot; MySQL &middot; C++</text>
<rect x="30" y="250" width="740" height="40" rx="12" fill="var(--bg-alt)" stroke="var(--arcane)" stroke-width="1" stroke-opacity="0.2"/>
<text x="400" y="275" text-anchor="middle" fill="var(--text-2)" font-family="var(--font-display)" font-weight="500" font-size="13">Python Pipeline &mdash; 60+ Tools</text>
<line x1="200" y1="48" x2="315" y2="48" stroke="var(--border)" stroke-width="1.5"/>
<line x1="485" y1="48" x2="600" y2="48" stroke="var(--border)" stroke-width="1.5"/>
<line x1="115" y1="76" x2="115" y2="136" stroke="var(--border)" stroke-width="1.5"/>
<line x1="400" y1="76" x2="400" y2="136" stroke="var(--arcane)" stroke-width="1.5" stroke-opacity="0.35"/>
<line x1="685" y1="76" x2="685" y2="136" stroke="var(--border)" stroke-width="1.5"/>
<line x1="200" y1="164" x2="315" y2="164" stroke="var(--border)" stroke-width="1.5"/>
<line x1="485" y1="164" x2="600" y2="164" stroke="var(--arcane)" stroke-width="1.5" stroke-opacity="0.35"/>
<line x1="115" y1="192" x2="115" y2="250" stroke="var(--border)" stroke-width="1.5" stroke-dasharray="4 3"/>
<line x1="400" y1="192" x2="400" y2="250" stroke="var(--arcane)" stroke-width="1.5" stroke-opacity="0.35" stroke-dasharray="4 3"/>
<line x1="685" y1="192" x2="685" y2="250" stroke="var(--border)" stroke-width="1.5" stroke-dasharray="4 3"/>
</svg></div>'''

PIPELINE_SVG = '''<div class="arch-wrap reveal"><svg viewBox="0 0 800 200" xmlns="http://www.w3.org/2000/svg" class="arch-diagram" role="img" aria-label="Data pipeline flow diagram">
<!-- Stage 1: Extract -->
<rect x="20" y="30" width="160" height="70" rx="12" fill="var(--bg-alt)" stroke="var(--arcane)" stroke-width="1.5" stroke-opacity="0.6"/>
<text x="100" y="56" text-anchor="middle" fill="var(--text)" font-family="var(--font-display)" font-weight="600" font-size="14">1. Extract</text>
<text x="100" y="76" text-anchor="middle" fill="var(--text-3)" font-family="var(--font-body)" font-size="11">TACTSharp &middot; 1,097 DB2s</text>
<text x="100" y="90" text-anchor="middle" fill="var(--text-3)" font-family="var(--font-body)" font-size="10">~50 seconds</text>

<!-- Arrow 1 -->
<line x1="180" y1="65" x2="215" y2="65" stroke="var(--arcane)" stroke-width="1.5" stroke-opacity="0.5"/>
<polygon points="215,60 225,65 215,70" fill="var(--arcane)" fill-opacity="0.5"/>

<!-- Stage 2: Merge -->
<rect x="225" y="30" width="160" height="70" rx="12" fill="var(--bg-alt)" stroke="var(--arcane)" stroke-width="1.5" stroke-opacity="0.6"/>
<text x="305" y="56" text-anchor="middle" fill="var(--text)" font-family="var(--font-display)" font-weight="600" font-size="14">2. Merge</text>
<text x="305" y="76" text-anchor="middle" fill="var(--text-3)" font-family="var(--font-body)" font-size="11">TACT + Wago CDN</text>
<text x="305" y="90" text-anchor="middle" fill="var(--text-3)" font-family="var(--font-body)" font-size="10">+7,183 extra rows</text>

<!-- Arrow 2 -->
<line x1="385" y1="65" x2="420" y2="65" stroke="var(--arcane)" stroke-width="1.5" stroke-opacity="0.5"/>
<polygon points="420,60 430,65 420,70" fill="var(--arcane)" fill-opacity="0.5"/>

<!-- Stage 3: Repair -->
<rect x="430" y="30" width="160" height="70" rx="12" fill="var(--bg-alt)" stroke="var(--arcane)" stroke-width="1.5" stroke-opacity="0.6"/>
<text x="510" y="56" text-anchor="middle" fill="var(--text)" font-family="var(--font-display)" font-weight="600" font-size="14">3. Repair</text>
<text x="510" y="76" text-anchor="middle" fill="var(--text-3)" font-family="var(--font-body)" font-size="11">103K inserts &middot; 5 batches</text>
<text x="510" y="90" text-anchor="middle" fill="var(--text-3)" font-family="var(--font-body)" font-size="10">388 tables compared</text>

<!-- Arrow 3 -->
<line x1="590" y1="65" x2="625" y2="65" stroke="var(--arcane)" stroke-width="1.5" stroke-opacity="0.5"/>
<polygon points="625,60 635,65 625,70" fill="var(--arcane)" fill-opacity="0.5"/>

<!-- Stage 4: Validate -->
<rect x="635" y="30" width="145" height="70" rx="12" fill="var(--bg-alt)" stroke="var(--arcane)" stroke-width="1.5" stroke-opacity="0.6"/>
<text x="707" y="56" text-anchor="middle" fill="var(--text)" font-family="var(--font-display)" font-weight="600" font-size="14">4. Validate</text>
<text x="707" y="76" text-anchor="middle" fill="var(--text-3)" font-family="var(--font-body)" font-size="11">~244K genuine rows</text>
<text x="707" y="90" text-anchor="middle" fill="var(--text-3)" font-family="var(--font-body)" font-size="10">97.8% reduction</text>

<!-- Bottom: Additional Sources -->
<rect x="20" y="130" width="760" height="50" rx="12" fill="var(--bg-alt)" stroke="var(--border)" stroke-width="1" stroke-opacity="0.3"/>
<text x="400" y="155" text-anchor="middle" fill="var(--text-2)" font-family="var(--font-display)" font-weight="500" font-size="12">Additional Sources: LoreWalkerTDB (~1M rows) &middot; AllTheThings (+9,221 rows) &middot; Raidbots (1.6M locales) &middot; Wowhead (78K NPC fixes) &middot; TDB (+1,967 rewards)</text>
<line x1="400" y1="100" x2="400" y2="130" stroke="var(--border)" stroke-width="1" stroke-dasharray="4 3" stroke-opacity="0.4"/>
</svg></div>'''

# ── Markdown to HTML ──────────────────────────────────────────────────────────

def inline_md(text):
    text = re.sub(
        r'\[([^\]]+)\]\(([^)]+)\)',
        lambda m: '<a href="{}">{}</a>'.format(m.group(2).replace('.md', '.html'), m.group(1)),
        text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'(?<![*])\*([^*]+)\*(?![*])', r'<em>\1</em>', text)
    return text


def convert_table(lines):
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
    return re.sub(r'^Part\s+\d+:\s*', '', text)


def md_to_html(md_text):
    lines = md_text.split('\n')
    out = []
    i = 0
    n = len(lines)

    if lines and lines[0].strip() == '---':
        i = 1
        while i < n and lines[i].strip() != '---':
            i += 1
        i += 1

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

        if s.startswith('<p class="hero-') or s.startswith('<div class="stat-'):
            if 'stat-grid' in s:
                while i < n and '</div>' not in lines[i]:
                    i += 1
                while i < n and lines[i].strip() in ('</div>', ''):
                    i += 1
                continue
            i += 1
            continue

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

        if s == '---':
            out.append('<hr>')
            i += 1
            continue

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

        if s.startswith('```'):
            i += 1
            code_lines = []
            while i < n and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i].rstrip())
                i += 1
            if i < n:
                i += 1
            code_text = '\n'.join(code_lines)
            code_text = code_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            out.append(f'<pre><code>{code_text}</code></pre>')
            continue

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
            block_html = _style_tables_in_html(block_html)
            out.append(block_html)
            continue

        if s.startswith('>'):
            bq = []
            while i < n and lines[i].strip().startswith('>'):
                bq.append(lines[i].strip().lstrip('>').strip())
                i += 1
            out.append(f'<blockquote>{inline_md(" ".join(bq))}</blockquote>')
            continue

        if s.startswith('|') and '|' in s[1:]:
            tbl = []
            while i < n and lines[i].strip().startswith('|'):
                tbl.append(lines[i].strip())
                i += 1
            out.append(convert_table(tbl))
            continue

        if re.match(r'^[-*]\s', s):
            items = []
            while i < n and re.match(r'^[-*]\s', lines[i].strip()):
                items.append(inline_md(re.sub(r'^[-*]\s', '', lines[i].strip())))
                i += 1
            out.append('<ul>' + ''.join(f'<li>{it}</li>' for it in items) + '</ul>')
            continue

        if re.match(r'^\d+\.\s', s):
            items = []
            while i < n and re.match(r'^\d+\.\s', lines[i].strip()):
                items.append(inline_md(re.sub(r'^\d+\.\s', '', lines[i].strip())))
                i += 1
            out.append('<ol>' + ''.join(f'<li>{it}</li>' for it in items) + '</ol>')
            continue

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
                    or ls.startswith('<div class=') or ls.startswith('```'):
                break
            para.append(ls)
            i += 1
        if para:
            out.append(f'<p>{inline_md(" ".join(para))}</p>')
        if i == start_i:
            i += 1

    return '\n'.join(out)


def _style_tables_in_html(html):
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
    toc = []
    for m in re.finditer(r'<(h[23]) id="([^"]*)"[^>]*>(.*?)</\1>', html):
        level = int(m.group(1)[1])
        anchor = m.group(2)
        title = re.sub(r'<[^>]+>', '', m.group(3))
        toc.append((level, anchor, title))
    return toc


# ── First pass: extract all report TOCs ───────────────────────────────────────

def extract_all_report_data():
    """Read all report pages, convert to HTML, extract TOCs. Returns dict."""
    data = {}
    for page in REPORT_PAGES:
        md_path = os.path.join(CONTENT_DIR, f"{page['slug']}.md")
        with open(md_path, 'r', encoding='utf-8') as f:
            md = f.read()
        md = re.sub(r'^#\s+[^\n]+\n', '', md.strip(), count=1)
        html = md_to_html(md)
        toc = extract_toc(html)
        data[page['slug']] = {'html': html, 'toc': toc}
    return data


# ── HTML generation ───────────────────────────────────────────────────────────

def _is_report_page(slug):
    return any(p['slug'] == slug for p in REPORT_PAGES)


def _nav_active(current_slug):
    if _is_report_page(current_slug):
        return 'data-import'
    return current_slug


def nav_html(current_slug=None):
    active = _nav_active(current_slug) if current_slug else None
    links = ''.join(
        '<a href="{slug}.html"{cls}>{label}</a>'.format(
            slug=item['slug'], label=item['label'],
            cls=' class="active"' if item['slug'] == active else '')
        for item in NAV_ITEMS)

    mobile_feature = ''.join(f'<a href="{p["slug"]}.html">{p["title"]}</a>' for p in FEATURE_PAGES)
    mobile_report = ''.join(f'<a href="{p["slug"]}.html">{p["title"]}</a>' for p in REPORT_PAGES)

    return f'''<nav class="site-nav" role="navigation" aria-label="Main">
<div class="nav-inner">
<a href="index.html" class="nav-logo">VoxCore</a>
<div class="nav-links">{links}</div>
<div class="nav-end">
<a href="https://github.com/VoxCore84/RoleplayCore" class="nav-github" aria-label="GitHub" target="_blank" rel="noopener">{GITHUB_ICON}</a>
<button class="nav-menu-btn" aria-label="Menu" aria-expanded="false">
<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
</button>
</div>
</div>
</nav>
<div class="mobile-nav" role="dialog" aria-label="Navigation">{mobile_feature}<div class="mobile-sep"></div>{mobile_report}</div>'''


def footer_html():
    return '''<div class="footer-wrap"><footer class="site-footer">
<span>VoxCore &mdash; March 2026</span>
<a href="https://github.com/VoxCore84/RoleplayCore">GitHub</a>
</footer></div>'''


def feature_sidebar_html(toc):
    """Flat TOC sidebar for feature pages — all items visible, no tree."""
    if not toc:
        return ''
    html = '<button class="sidebar-toggle">On this page</button>'
    html += '<nav class="sidebar" aria-label="Table of contents">'
    for level, anchor, title in toc:
        cls = ' class="toc-h3"' if level == 3 else ''
        html += f'<a href="#{anchor}"{cls}>{title}</a>'
    html += '</nav>'
    return html


def report_sidebar_html(current_slug, report_data):
    """Cross-page report sidebar — full outline, current section expanded."""
    html = '<button class="sidebar-toggle">Report sections</button>'
    html += '<nav class="sidebar" aria-label="Report navigation">'

    for page in REPORT_PAGES:
        slug = page['slug']
        toc = report_data.get(slug, {}).get('toc', [])
        is_current = (slug == current_slug)

        expanded = ' expanded' if is_current else ''
        html += f'<div class="toc-section{expanded}">'

        # Page title as the parent node
        has_children = len(toc) > 0
        html += '<div class="toc-parent">'
        if has_children:
            html += '<button class="toc-toggle" aria-label="Expand">&#9654;</button>'
        else:
            html += '<span class="toc-spacer"></span>'

        current_cls = ' current' if is_current else ''
        html += f'<a href="{slug}.html" class="toc-page{current_cls}">{page["title"]}</a>'
        html += '</div>'

        if has_children:
            html += '<div class="toc-children">'
            if is_current:
                # Full h2+h3 tree with local anchors
                for level, anchor, title in toc:
                    cls = ' class="toc-h3"' if level == 3 else ''
                    html += f'<a href="#{anchor}"{cls}>{title}</a>'
            else:
                # Just h2 titles linking to the other page
                for level, anchor, title in toc:
                    if level == 2:
                        html += f'<a href="{slug}.html#{anchor}">{title}</a>'
            html += '</div>'

        html += '</div>'

    html += '</nav>'
    return html


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


BACK_TO_TOP = '''<button class="back-to-top" aria-label="Back to top">
<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M18 15l-6-6-6 6"/></svg>
</button>'''


def base_page(title, body, current_slug=None):
    desc = "VoxCore \u2014 An AI-assisted open source MMO framework built on TrinityCore for WoW 12.x Midnight"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} \u2014 VoxCore</title>
<meta name="description" content="{desc}">
<style>{CSS}</style>
</head>
<body>
{nav_html(current_slug)}
{body}
{BACK_TO_TOP}
{footer_html()}
<script>{JS}</script>
</body>
</html>'''


# ── Page builders ─────────────────────────────────────────────────────────────

def build_index():
    # Stat ribbon
    stat_items = []
    for idx, (val, label) in enumerate(HERO_STATS):
        if idx > 0:
            stat_items.append('<span class="stat-sep"></span>')
        stat_items.append(f'<div class="stat-item"><span class="stat-num" data-countup="{val}">{val}</span><span class="stat-label">{label}</span></div>')
    stats_html = ''.join(stat_items)

    # Executive summary table
    exec_rows = ''
    for cat, metric, value in EXEC_SUMMARY:
        cat_cell = f'<strong>{cat}</strong>' if cat else ''
        exec_rows += f'<tr><td>{cat_cell}</td><td>{metric}</td><td>{value}</td></tr>'

    # Pillar cards
    pillar_cards = ''
    for p in FEATURE_PAGES:
        icon = ICONS.get(p['slug'], '')
        pillar_cards += f'<a href="{p["slug"]}.html" class="pillar-card reveal"><span class="pillar-icon">{icon}</span><h3>{p["title"]}</h3><p>{p["desc"]}</p></a>\n'

    # Report cards
    report_cards = ''
    for p in REPORT_PAGES:
        icon = ICONS.get(p['slug'], '')
        report_cards += f'<a href="{p["slug"]}.html" class="card reveal"><span class="card-icon">{icon}</span><h3>{p["title"]}</h3><p>{p["desc"]}</p></a>\n'

    # Timeline
    timeline_entries = ''
    for entry in CHANGELOG:
        timeline_entries += f'<div class="timeline-entry reveal"><span class="timeline-date">{entry["date"]}</span><div><h3>{entry["title"]}</h3><p>{entry["summary"]}</p></div></div>\n'

    body = f'''<main>
<div class="hero-wrap">
<section class="hero reveal">
<p class="hero-label">WoW 12.x / Midnight</p>
<h1>VoxCore</h1>
<p class="hero-sub">An AI-Assisted Open Source MMO Framework</p>
<p class="hero-meta">Built on TrinityCore &middot; Build {STATS['build_number']} &middot; {STATS['custom_systems']} custom systems &middot; {STATS['tools_built']} tools</p>
</section>
<section class="stat-ribbon reveal">{stats_html}</section>
</div>

<div class="section-divider"></div>

<section class="vision reveal">
<p>A TrinityCore fork enhanced by an AI-assisted development workflow that produced {STATS['tools_built']} custom tools, 1M+ database corrections, and a {STATS['server_startup_reduction']}% server startup improvement in under two months. Every pipeline is scripted, every audit is reproducible, and every number on this site is backed by a commit hash.</p>
</section>

<section class="pillars">
<div class="pillars-wrap">
<div class="pillars-grid">{pillar_cards}</div>
</div>
</section>

<div class="banner reveal" style="margin-bottom: 80px">{CHECK_ICON}<span>All tooling is open and reproducible. Every operation can be re-run from scripts in the repository.</span></div>

<section class="cards-section" id="report">
<div class="cards-wrap">
<h2 class="section-title">Data Quality Report</h2>
<p class="section-sub">{STATS['rows_imported_short']} rows imported, validated, and repaired across five databases. Prepared for CaptainCore (LoreWalkerTDB) &middot; March 2026.</p>

<details class="exec-details reveal">
<summary>Executive Summary &mdash; By the Numbers</summary>
<div>
<p style="font-size:14px;color:var(--text-3);margin:0 0 16px">All figures are <strong>net</strong> &mdash; accounting for subsequent cleanup and deduplication.</p>
<div class="table-wrap"><table class="data-table"><thead><tr><th>Category</th><th>Metric</th><th>Value</th></tr></thead><tbody>{exec_rows}</tbody></table></div>
</div>
</details>

<div class="cards-grid">{report_cards}</div>
</div>
</section>

<div class="section-divider" style="margin-top:0"></div>

<section class="timeline-section">
<h2>Recent Activity</h2>
{timeline_entries}
</section>

<div class="built-with reveal">
<span>C++</span><span class="bw-dot">&middot;</span>
<span>Python</span><span class="bw-dot">&middot;</span>
<span>MySQL</span><span class="bw-dot">&middot;</span>
<span>Lua</span><span class="bw-dot">&middot;</span>
<span>Claude Code</span><span class="bw-dot">&middot;</span>
<span>CMake</span><span class="bw-dot">&middot;</span>
<span>Ninja</span><span class="bw-dot">&middot;</span>
<span>Git</span>
</div>
</main>'''

    return base_page("VoxCore", body)


def build_feature_page(page):
    md_path = os.path.join(CONTENT_DIR, f"{page['slug']}.md")
    with open(md_path, 'r', encoding='utf-8') as f:
        md = f.read()

    md = re.sub(r'^#\s+[^\n]+\n', '', md.strip(), count=1)
    html = md_to_html(md)
    toc = extract_toc(html)

    # Inject diagrams at top of specific pages
    extra_top = ''
    if page['slug'] == 'framework':
        extra_top = ARCH_SVG
    elif page['slug'] == 'pipeline':
        extra_top = PIPELINE_SVG

    body = f'''<main>
<header class="page-header">
<nav class="breadcrumb"><a href="index.html">VoxCore</a> &rsaquo; {page["title"]}</nav>
<h1>{page["title"]}</h1>
</header>
<div class="page-layout">
{feature_sidebar_html(toc)}
<article>
{extra_top}
{html}
</article>
</div>
</main>'''

    return base_page(page['title'], body, current_slug=page['slug'])


def build_report_page(page, prev_p, next_p, report_data):
    cached = report_data.get(page['slug'], {})
    html = cached.get('html', '')

    body = f'''<main>
<header class="page-header">
<nav class="breadcrumb"><a href="index.html">VoxCore</a> &rsaquo; <a href="index.html#report">Report</a> &rsaquo; {page["title"]}</nav>
<h1>{page["title"]}</h1>
</header>
<div class="page-layout">
{report_sidebar_html(page['slug'], report_data)}
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

    # First pass: extract all report page data
    report_data = extract_all_report_data()

    total_size = 0

    # Index
    html = build_index()
    path = os.path.join(OUTPUT_DIR, 'index.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    sz = os.path.getsize(path)
    total_size += sz
    print(f"  index.html ({sz // 1024}KB)")

    # Feature pages
    for page in FEATURE_PAGES:
        html = build_feature_page(page)
        path = os.path.join(OUTPUT_DIR, f"{page['slug']}.html")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        sz = os.path.getsize(path)
        total_size += sz
        print(f"  {page['slug']}.html ({sz // 1024}KB)")

    # Report pages (use cached data from first pass)
    for i, page in enumerate(REPORT_PAGES):
        prev_p = REPORT_PAGES[i - 1] if i > 0 else None
        next_p = REPORT_PAGES[i + 1] if i < len(REPORT_PAGES) - 1 else None
        html = build_report_page(page, prev_p, next_p, report_data)
        path = os.path.join(OUTPUT_DIR, f"{page['slug']}.html")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        sz = os.path.getsize(path)
        total_size += sz
        print(f"  {page['slug']}.html ({sz // 1024}KB)")

    # .nojekyll
    open(os.path.join(OUTPUT_DIR, '.nojekyll'), 'w').close()

    total = 1 + len(FEATURE_PAGES) + len(REPORT_PAGES)
    print(f"\n  {total} pages, {total_size // 1024}KB total")


if __name__ == '__main__':
    main()
