
## Part 15: Timeline

| Date | Sessions | Key Milestones |
|------|----------|---------------|
| **Feb 26** | 1 | Companion AI fix, transmog wireDT fix, initial hotfix repair v1 |
| **Feb 27** | 2-7 | 5-DB audit (412K cleanup), LW import #1 (385K rows), NPC audit tool (27 checks), 3-batch NPC fixes (23,904 ops), placement audit tools |
| **Feb 28** | 8-10 | GO/quest audit tools + 2,279 DB fixes, TransmogBridge implementation, placement audits |
| **Mar 1** | 11-12 | Transmog confirmed working in-game, PR cleanup, cross-repo PR #760 |
| **Mar 3** | 13-30 | Wowhead mega-audit (54,571 ops), Raidbots/Wago pipeline (locales + quests), LW import #2 (665K rows), post-import cleanup (47K rows), hotfix repair build 66220, MySQL tuning, build diff audit (5 builds), hotfix pipeline crash fix, transmog multi-bug fixes |
| **Mar 4** | 31-38 | Hotfix redundancy audit rounds 1-3 (10.8M → 244K content rows), WTL DBC pipeline, world DB cleanup (NPC/portal fixes, SmartAI orphans), transmog client wiki, auth key update |
| **Mar 5** | 39+ | Report update, transmog diagnostics, remaining QA |

---

## Part 16: Complete Tooling & Infrastructure Catalog

<details>
<summary><strong>16.1 Python Data Pipeline Tools</strong> (14 tools)</summary>

| Tool | Location | Purpose |
|------|----------|---------|
| `repair_hotfix_tables.py` | `C:/Users/atayl/source/wago/` | 5-batch hotfix DB repair against Wago DB2 baselines |
| `repair_scene_scripts.py` | same | Scene script hex-encoded Lua repair |
| `wago_db2_downloader.py` | same | Download 1,097 DB2 CSVs from Wago.tools |
| `diff_builds.py` | same | Row-by-row CSV diffing with oscillation detection |
| `cross_ref_mysql.py` | same | Cross-reference diff results with live MySQL |
| `import_all.py` | same | 5-phase dependency-ordered LW import |
| `validate_import.py` | same | 15-check post-import integrity validator |
| `fix_column_mismatch.py` | same | Fix column count differences between TC forks |
| `run_all_imports.py` | `raidbots/` | Master 8-step Raidbots/Wago orchestrator with --dry-run and --regenerate |
| `db_snapshot.py` | `C:/Users/atayl/source/wago/` | MySQL backup/rollback (snapshot/check/list/rollback/prune) |
| `import_item_names.py` | `raidbots/` | Raidbots → 10-locale item name import |
| `quest_chain_gen.py` | `raidbots/` | Wago QuestLineXQuest → quest chain generation with DFS cycle detection |
| `gen_quest_poi_sql.py` | `raidbots/` | Wago → quest POI import |
| `quest_objectives_import.py` | `raidbots/` | Wago → quest objective import |
| `extract_lw_world.py` | `C:/Users/atayl/source/wago/` | Parse 897MB LW dump into per-table SQL |
| `validate_transmog.py` | same | Transmog data integrity check (155K appearances, 4.8K sets) |
| `transmog_lookup.py` | same | Transmog DB2 cross-reference (IMAID → item name, display) |
| `transmog_debug.py` | same | Transmog state debugger |

</details>


<details>
<summary><strong>16.2 Hotfix Audit Tools</strong> (6 tools)</summary>

| Tool | Location | Purpose |
|------|----------|---------|
| `hotfix_differ_r3.py` | `hotfix_audit/` (in repo) | Type-aware row differ — float32, int32 sign, logical PK |
| `gen_practical_sql_r3.py` | same | Cleanup SQL generator — TRUNCATE + batched DELETEs |
| `build_table_info_r3.py` | same | Column mapping builder — array index, coordinate, rename resolution |
| `merge_results.py` | same | Result aggregator and report generator |
| DBC2CSV | `C:\Tools\DBC2CSV\` | Converts WTL DB2 binaries to CSV |
| wow.tools.local (WTL) | `C:\Tools\WoW.tools\` | Local CASC browser — extracts DB2 baselines from game files |

</details>


<details>
<summary><strong>16.3 Audit Tools</strong> (6 tools)</summary>

| Tool | Checks | Scope |
|------|--------|-------|
| `npc_audit.py` | 27 | 662K creatures vs Wago DB2 + Wowhead |
| `go_audit.py` | 15 | 175K gameobjects vs Wago DB2 |
| `quest_audit.py` | 15 | 47K quests vs Wago DB2 |
| `creature_placement_audit.py` | 5 | Position comparison vs LW |
| `go_placement_audit.py` | 6 | Position comparison vs LW |
| `wowhead_scraper.py` | — | 216K NPC data scraper |

</details>


<details>
<summary><strong>16.4 MCP Servers</strong> (3 servers)</summary>

Model Context Protocol servers giving Claude Code direct access to project data:

| Server | Transport | Purpose |
|--------|-----------|---------|
| `wago_db2_server.py` | FastMCP/stdio | DuckDB-powered queries against 1,097 DB2 CSV tables |
| `code_intel_server.py` | FastMCP/stdio | Hybrid ctags+clangd C++ code intelligence (416K symbols) |
| MySQL MCP | .claude.json | Direct MySQL queries against all 5 databases |

</details>


<details>
<summary><strong>16.5 Claude Code Agents</strong> (5 agents)</summary>

Specialized agents defined in `.claude/agents/`:

| Agent | Expertise |
|-------|-----------|
| Packet Analyst | Hex dumps, opcode analysis, UpdateField wire format |
| DB Specialist | MySQL queries, DB2 cross-referencing, hotfix data |
| C++ Systems | Server handlers, opcode registration, transmog pipeline |
| Lua/Addon Dev | TransmogBridge/TransmogSpy, WoW Lua API |
| Python Tooling | Scripts, MCP servers, packet log parsers |

</details>


<details>
<summary><strong>16.6 WoW Addons</strong> (3 addons)</summary>

| Addon | Purpose |
|-------|---------|
| TransmogBridge | 3-layer hybrid merge transmog data capture, sends to server via addon message (workaround for broken 12.x CMSG) |
| TransmogSpy | Diagnostic logger — all transmog API calls to SavedVariables |
| SpawnDespawnTool | Category-based batch spawn/despawn for GMs |

</details>


<details>
<summary><strong>16.7 Packet Analysis & Server Tools</strong> (4 tools)</summary>

| Tool | Purpose |
|------|---------|
| `opcode_analyzer.py` | TC opcode parser, cross-ref with WPP captures |
| `start-worldserver.sh` | Session lifecycle with auto-archiving and WPP |
| `wpp-add-build.sh` / `wpp-inspect.sh` | WowPacketParser utilities |
| WowPacketParser (WPP) | `C:\Tools\WowPacketParser\` — retail packet parser |

</details>


<details>
<summary><strong>16.8 SQL Fix Scripts</strong> (5 scripts)</summary>

| Script | Purpose |
|--------|---------|
| `fix_quest_chains.sql` | Dangling ref cleanup + N-hop cycle fix with recursive CTE |
| `fix_locale_and_orphans.sql` | Cross-DB cleanup: stale locales + orphaned objectives |
| `fix_orphan_quest_refs.sql` | Orphaned quest reference remediation |
| Genre 5c-8a scripts | World DB cleanup: invalid maps/phases/models, SmartAI, loot |
| Auth build consolidation | Idempotent SQL for multiple Midnight builds (65893-66220) |

</details>


<details>
<summary><strong>16.9 Infrastructure</strong> (4 components)</summary>

| Component | Details |
|-----------|---------|
| **Build** | VS2022 x64, Ninja, RelWithDebInfo, `-j20` |
| **MySQL** | UniServerZ 9.5.0 — 16GB buffer pool, 8 instances, warm restarts, 256M tmp_table_size |
| **Git** | Parallel worktrees; `db_snapshot.py` for DB rollback |
| **Hardware** | Ryzen 9 9950X3D (12C/24T), 128GB DDR5-5600, RTX 5090, 2TB NVMe |

</details>


<details>
<summary><strong>16.10 Data Sources & Pipelines</strong> (5 sources)</summary>

| Source | Pipeline | Output |
|--------|----------|--------|
| Wago.tools DB2 CSVs | `wago_db2_downloader.py` → DuckDB via MCP | DB2 data for repair/audit/diff |
| wow.tools.local | WTL → DBC2CSV → CSV | Complete DBC baselines from client CASC |
| Raidbots | `run_all_imports.py --regenerate` | Item names (171K x 7 locales), quest chains, POI |
| LoreWalkerTDB | `import_all.py` + `validate_import.py` | World spawns, loot, SmartAI, hotfixes |
| Wowhead | `wowhead_scraper.py` (216K NPCs) | NPC cross-reference data |

</details>


<details>
<summary><strong>16.11 Workflow Patterns</strong> (5 patterns)</summary>

- **Snapshot-gated phases**: `db_snapshot.py snapshot --tag <phase>` before every DB mutation; rollback on failure
- **Idempotent SQL**: INSERT IGNORE, ON DUPLICATE KEY UPDATE, DELETE-before-INSERT throughout
- **Diagnostic build cycle**: Add logging → build → test → analyze logs → iterate
- **Build diffing**: `diff_builds.py` separates real content changes from Wago export oscillation
- **Parallel execution**: Separate git worktrees, subagent delegation, background builds

---

</details>

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

1. **Hotfix repair**: `python repair_hotfix_tables.py --batch {1..5}` — idempotent
2. **LW import**: `python import_all.py` + `python validate_import.py` — 15 integrity checks
3. **Raidbots pipeline**: `python run_all_imports.py --regenerate` — 8-step with --dry-run
4. **NPC audit**: `python npc_audit.py all --report --json --sql-out` — 27 checks
5. **Build diff**: `python diff_builds.py --base 66192 --target 66220`
6. **Hotfix audit**: `build_table_info_r3.py` → `hotfix_differ_r3.py` → `gen_practical_sql_r3.py` (see `hotfix_audit/README.md`)

All scripts version-controlled in private GitHub repositories.

</details>

---

*Updated March 5, 2026 | RoleplayCore — VoxCore84/RoleplayCore*
*Tools: VoxCore84/wago-tooling, VoxCore84/tc-packet-tools, VoxCore84/code-intel, VoxCore84/trinitycore-claude-skills*

---
