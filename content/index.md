---
hide:
  - navigation
  - toc
---

<style>
.md-typeset h1 { font-size: 2.4em; font-weight: 700; margin-bottom: 0; }
.hero-sub { font-size: 1.3em; opacity: 0.7; margin-bottom: 0.5em; }
.hero-meta { opacity: 0.5; font-size: 0.9em; margin-bottom: 2em; }
.stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1em; margin: 2em 0; }
.stat-card { background: var(--md-code-bg-color); border-radius: 8px; padding: 1.2em; text-align: center; border-left: 4px solid var(--md-accent-fg-color); }
.stat-card .num { font-size: 2em; font-weight: 700; color: var(--md-accent-fg-color); display: block; }
.stat-card .label { font-size: 0.85em; opacity: 0.7; margin-top: 0.3em; display: block; }
</style>

# VoxCore Database Report

<p class="hero-sub">Data Quality & Optimization Summary</p>
<p class="hero-meta">Prepared for CaptainCore (LoreWalkerTDB) · March 2026 · WoW 12.x Midnight · Build 66220</p>

<div class="stat-grid">
<div class="stat-card"><span class="num">~1M</span><span class="label">rows imported from LoreWalkerTDB</span></div>
<div class="stat-card"><span class="num">103K</span><span class="label">hotfix entries repaired</span></div>
<div class="stat-card"><span class="num">97.8%</span><span class="label">redundant hotfix rows removed</span></div>
<div class="stat-card"><span class="num">78K</span><span class="label">NPC corrections applied</span></div>
<div class="stat-card"><span class="num">1.6M</span><span class="label">item translations (10 languages)</span></div>
<div class="stat-card"><span class="num">17s</span><span class="label">server startup (was 3m24s)</span></div>
</div>

!!! success "All tooling is open and reproducible"
    Every operation documented here can be re-run from scripts in the repository. See [Reproducibility](reference.md#appendix-b-reproducibility) for the full pipeline.

---

## Quick Navigation

| # | Section | Headline |
|---|---------|----------|
| 1 | [LoreWalkerTDB Integration](data-import.md) | ~1M rows imported |
| 2 | [Hotfix Repair System](data-import.md#part-2-hotfix-repair-system) | 103K inserts + 1.8K fixes |
| 3 | [NPC Audits & Corrections](npc-audits.md) | 78,475 fixes |
| 4 | [Quest System Enrichment](quest-localization.md) | 24.8K chain links |
| 5 | [Localization](quest-localization.md#part-5-localization) | 1.6M locale rows |
| 6 | [Database Cleanup & Integrity](database-cleanup.md) | 412K dead rows removed |
| 7 | [MySQL & Server Performance](performance.md) | 3m24s → 17s startup |
| 8 | [Build Diff Audit](performance.md#part-8-build-diff-audit-5-builds) | Zero breaking changes |
| 9 | [Placement Audits](placement.md) | 31K fixes generated |
| 10 | [Custom Tooling Summary](results.md) | 65+ tools built |
| 11 | [Final Database State](results.md#part-11-final-database-state) | Current row counts |
| 12 | [What It All Means for Players](results.md#part-12-what-it-all-means-for-players) | Before / After |
| 13 | [Hotfix Redundancy Audit](hotfix-audit.md) | 10.8M → 244K (97.8%) |
| 14 | [Discoveries & Lessons](discoveries.md) | 9 community findings |
| 15 | [Timeline](reference.md) | Feb 26 – Mar 5 |
| 16 | [Complete Tooling Catalog](reference.md#part-16-complete-tooling--infrastructure-catalog) | Full inventory |
| A | [Data Sources](reference.md#appendix-a-data-sources) | 6 sources |
| B | [Reproducibility](reference.md#appendix-b-reproducibility) | 6 pipelines |

---

## Executive Summary

Over February–March 2026, VoxCore imported, validated, and repaired data from **four major sources** (LoreWalkerTDB, Wago DB2, Raidbots, and Wowhead), performed multi-pass audits across all five databases, and built a Python tooling pipeline to make the process repeatable.

### By the Numbers

All figures are **net** — accounting for subsequent cleanup and deduplication.

| Category | Metric | Value |
|----------|--------|-------|
| **Data Imported** | LoreWalkerTDB world rows | ~1,004,000 net |
| | Hotfix rows repaired | 103,153 inserts + 1,831 column fixes |
| | Item locale translations | 1,628,651 rows across 10 languages |
| | Quest chain links | 24,868 PrevQuestID/NextQuestID updates |
| | Quest POI/objectives | 2,880 POI + 5,199 points + 633 objectives |
| **Data Corrected** | NPC fixes | 78,475 (23,904 audit + 54,571 Wowhead cross-ref) |
| **Data Cleaned** | Hotfix redundancy audit | **10.6M redundant content rows removed (97.8%)** |
| | Pre-existing orphan/dead rows | ~412,000 (initial 5-DB audit) |
| | Pre-existing duplicate loot rows | 193,542 |
| | Post-import cleanup | ~47,000 |
| **Performance** | Server startup | 3m24s → 17s (92% reduction) |
| | Hotfix content tables | 10.8M rows → ~244K rows |
