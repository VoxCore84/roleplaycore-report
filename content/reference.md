
## Part 15: Timeline

| Date | Sessions | Key Milestones |
|------|----------|---------------|
| **Feb 26** | 1 | Companion AI fix, transmog wireDT fix, initial hotfix repair v1 |
| **Feb 27** | 2-7 | 5-DB audit (412K cleanup), LW import #1 (385K rows), NPC audit tool (27 checks), 3-batch NPC fixes (23,904 ops), placement audit tools |
| **Feb 28** | 8-10 | GO/quest audit tools + 2,279 DB fixes, TransmogBridge implementation, placement audits |
| **Mar 1** | 11-12 | Transmog confirmed working in-game, PR cleanup, cross-repo PR #760 |
| **Mar 3** | 13-30 | Wowhead mega-audit (54,571 ops), Raidbots/Wago pipeline (locales + quests), LW import #2 (665K rows), post-import cleanup (47K rows), hotfix repair build 66263, MySQL tuning, build diff audit (5 builds), hotfix pipeline crash fix, transmog multi-bug fixes |
| **Mar 4** | 31-38 | Hotfix redundancy audit rounds 1-3 (10.8M to 244K content rows), WTL DBC pipeline, world DB cleanup (NPC/portal fixes, SmartAI orphans), transmog client wiki, auth key update |
| **Mar 5** | 39-64 | TACT extraction pipeline, CSV merge tool, ATT mega-parser, 3,240 NPC spawns deployed, transmog 5-phase audit, Arcane Codex website, gap scrape, quest reward text, Midnight data, build 66263 |

---

## Complete Tooling Catalog

For the full inventory of 75+ tools across Python, C++, Lua, SQL, Shell, and C#, see the dedicated [Tooling](tooling.html) page.

---

## Appendix A: Data Sources

| Source | Data Type | Volume |
|--------|----------|--------|
| **LoreWalkerTDB** | World DB, Hotfixes DB | 1.2 GB SQL dumps |
| **TACTSharp / CASC** | 1,094 DB2 tables extracted from local client (ground truth) | ~50s extraction |
| **Wago.tools DB2 CSVs** | 1,094 client DB2 tables, CDN hotfix extras | ~5.5K CSV files |
| **wow.tools.local** | DB2 baselines from client CASC (build 66263) | ~1,094 DB2 tables |
| **AllTheThings Database** | Quest, NPC, item, transmog collection data (1,576 Lua files) | 52.6 MB SQLite |
| **Raidbots** | Item names (171K x 7 locales), talents | 168 MB JSON |
| **Wowhead** | 216K NPC tooltips, names, types, levels | 218K JSON files |
| **TrinityCore upstream** | Periodic merge + SQL updates | Git merge |

---

## Appendix B: Reproducibility

Every operation is fully reproducible:

1. **DB2 extraction**: `python tact_extract.py` then `python merge_csv_sources.py` -- TACT ground truth + Wago CDN extras
2. **Hotfix repair**: `python repair_hotfix_tables.py --batch {1..5}` -- idempotent
3. **LW import**: `python import_all.py` + `python validate_import.py` -- 15 integrity checks
4. **Raidbots pipeline**: `python run_all_imports.py --regenerate` -- 8-step with --dry-run
5. **NPC audit**: `python npc_audit.py all --report --json --sql-out` -- 27 checks
6. **ATT import**: `python att_to_sqlite.py` then `python att_generate_sql.py` -- 60 tables, cross-referenced
7. **Build diff**: `python diff_builds.py --base 66192 --target 66220`
8. **Hotfix audit**: `build_table_info_r3.py` then `hotfix_differ_r3.py` then `gen_practical_sql_r3.py`

All scripts version-controlled in GitHub repositories.

---

*Updated March 5, 2026 | VoxCore -- VoxCore84*
*Tools: VoxCore84/wago-tooling, VoxCore84/tc-packet-tools, VoxCore84/code-intel, VoxCore84/trinitycore-claude-skills*

---
