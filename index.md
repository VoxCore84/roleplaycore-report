---
layout: home
title: Home
nav_order: 1
---

# RoleplayCore Database Report
{: .fs-9 }

Data Quality & Optimization Summary
{: .fs-6 .fw-300 }

**Prepared for CaptainCore (LoreWalkerTDB)**
**March 5, 2026 | WoW 12.x / Midnight, Build 66220**

{: .highlight }
> **TL;DR**
>
> | What | Result |
> |------|--------|
> | **Imported** | ~1M rows from LoreWalkerTDB |
> | **Repaired** | 103K hotfix entries across 388 tables |
> | **Removed** | 10.6M redundant rows (97.8% of hotfix DB) |
> | **Fixed** | 78K NPC corrections (levels, factions, flags) |
> | **Localized** | 1.6M item translations across 10 languages |
> | **Startup** | 3m24s → **17s** (92% faster) |
>
> All tooling is open and reproducible.

---

## Quick Navigation

| # | Section | Headline |
|---|---------|----------|
| — | [Executive Summary](#executive-summary) | Full numbers table |
| 1 | [LoreWalkerTDB Integration](data-import) | ~1M rows imported |
| 2 | [Hotfix Repair System](data-import#part-2-hotfix-repair-system) | 103K inserts + 1.8K fixes |
| 3 | [NPC Audits & Corrections](npc-audits) | 78,475 fixes |
| 4 | [Quest System Enrichment](quest-localization) | 21K chain links |
| 5 | [Localization](quest-localization#part-5-localization) | 1.6M locale rows |
| 6 | [Database Cleanup & Integrity](database-cleanup) | 412K dead rows removed |
| 7 | [MySQL & Server Performance](performance) | 3m24s → 17s startup |
| 8 | [Build Diff Audit](performance#part-8-build-diff-audit-5-builds) | Zero breaking changes |
| 9 | [Placement Audits](placement) | 31K fixes generated |
| 10 | [Custom Tooling Summary](results) | 50+ tools built |
| 11 | [Final Database State](results#part-11-final-database-state) | Current row counts |
| 12 | [What It All Means for Players](results#part-12-what-it-all-means-for-players) | Before / After |
| 13 | [Hotfix Redundancy Audit](hotfix-audit) | 10.8M → 244K (97.8%) |
| 14 | [Discoveries & Lessons](discoveries) | 9 community findings |
| 15 | [Timeline](reference) | Feb 26 – Mar 5 |
| 16 | [Complete Tooling Catalog](reference#part-16-complete-tooling--infrastructure-catalog) | Full inventory |
| A | [Data Sources](reference#appendix-a-data-sources) | 6 sources |
| B | [Reproducibility](reference#appendix-b-reproducibility) | 6 pipelines |

## Executive Summary

Over February-March 2026, RoleplayCore imported, validated, and repaired data from **four major sources** (LoreWalkerTDB, Wago DB2, Raidbots, and Wowhead), performed multi-pass audits across all five databases, and built a Python tooling pipeline to make the process repeatable.

### By the Numbers

All figures are **net** — accounting for subsequent cleanup and deduplication.

| Category | Metric | Value |
|----------|--------|-------|
| **Data Imported** | LoreWalkerTDB world rows | ~1,004,000 net |
| | Hotfix rows repaired | 103,153 inserts + 1,831 column fixes |
| | Item locale translations | 1,628,651 rows across 10 languages |
| | Quest chain links | 21,758 PrevQuestID/NextQuestID updates |
| | Quest POI/objectives | 2,880 POI + 5,199 points + 633 objectives |
| **Data Corrected** | NPC fixes | 78,475 (23,904 audit + 54,571 Wowhead cross-ref) |
| **Data Cleaned** | Hotfix redundancy audit | **10.6M redundant content rows removed (97.8%)** |
| | Pre-existing orphan/dead rows | ~412,000 (initial 5-DB audit) |
| | Pre-existing duplicate loot rows | 193,542 |
| | Post-import cleanup | ~47,000 |
| **Performance** | Server startup | 3m24s → 17s (92% reduction) |
| | Hotfix content tables | 10.8M rows → ~244K rows |
