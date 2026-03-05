
## Part 15: Timeline

| Date | Sessions | Key Milestones |
|------|----------|---------------|
| **Feb 26** | 1 | Companion AI fix, transmog wireDT fix, initial hotfix repair v1 |
| **Feb 27** | 2-7 | 5-DB audit (412K cleanup), LW import #1 (385K rows), NPC audit tool (27 checks), 3-batch NPC fixes (23,904 ops), placement audit tools |
| **Feb 28** | 8-10 | GO/quest audit tools + 2,279 DB fixes, TransmogBridge implementation, placement audits |
| **Mar 1** | 11-12 | Transmog confirmed working in-game, PR cleanup, cross-repo PR #760 |
| **Mar 3** | 13-30 | Wowhead mega-audit (54,571 ops), Raidbots/Wago pipeline (locales + quests), LW import #2 (665K rows), post-import cleanup (47K rows), hotfix repair build 66220, MySQL tuning, build diff audit (5 builds), hotfix pipeline crash fix, transmog multi-bug fixes |
| **Mar 4** | 31-38 | Hotfix redundancy audit rounds 1-3 (10.8M to 244K content rows), WTL DBC pipeline, world DB cleanup (NPC/portal fixes, SmartAI orphans), transmog client wiki, auth key update |
| **Mar 5** | 39+ | Report update, transmog diagnostics, remaining QA |

---

## Complete Tooling Catalog

For the full inventory of 60+ tools across Python, C++, Lua, SQL, Shell, and C#, see the dedicated [Tooling](tooling.html) page.

---

## Appendix A: Data Sources

| Source | Data Type | Volume |
|--------|----------|--------|
| **LoreWalkerTDB** | World DB, Hotfixes DB | 1.2 GB SQL dumps |
| **Wago.tools DB2 CSVs** | 1,097 client DB2 tables, 5 builds | ~5.5K CSV files |
| **wow.tools.local** | DB2 baselines from client CASC (build 66220) | ~1,097 DB2 tables |
| **Raidbots** | Item names (171K x 7 locales), talents | 168 MB JSON |
| **Wowhead** | 216K NPC tooltips, names, types, levels | 218K JSON files |
| **TrinityCore upstream** | Periodic merge + SQL updates | Git merge |

---

## Appendix B: Reproducibility

Every operation is fully reproducible:

1. **Hotfix repair**: `python repair_hotfix_tables.py --batch {1..5}` -- idempotent
2. **LW import**: `python import_all.py` + `python validate_import.py` -- 15 integrity checks
3. **Raidbots pipeline**: `python run_all_imports.py --regenerate` -- 8-step with --dry-run
4. **NPC audit**: `python npc_audit.py all --report --json --sql-out` -- 27 checks
5. **Build diff**: `python diff_builds.py --base 66192 --target 66220`
6. **Hotfix audit**: `build_table_info_r3.py` then `hotfix_differ_r3.py` then `gen_practical_sql_r3.py` (see `hotfix_audit/README.md`)

All scripts version-controlled in GitHub repositories.

---

*Updated March 5, 2026 | VoxCore -- VoxCore84*
*Tools: VoxCore84/wago-tooling, VoxCore84/tc-packet-tools, VoxCore84/code-intel, VoxCore84/trinitycore-claude-skills*

---
