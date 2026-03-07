# Project Status

Current state of the VoxCore project — database health, recent activity, and open work items.

## Database Health

### Size & Row Counts (March 7, 2026)

| Database | Size | Key Table | Rows |
|----------|------|-----------|------|
| **world** | 1,054 MB | creature_template | 225,968 |
| | | creature | 611,359 |
| | | creature_template_difficulty | 532,346 |
| | | creature_template_spell | 171,590 |
| | | smart_scripts | 286,436 |
| | | gameobject | 188,069 |
| | | npc_vendor | 174,364 |
| | | quest_template | 47,536 |
| | | quest_poi | 133,026 |
| | | creature_queststarter | 30,659 |
| | | creature_questender | 37,698 |
| | | trainer_spell | 40,305 |
| | | spell_script_names | 5,467 |
| | | serverside_spell | 4,503 |
| | | conditions | 25,566 |
| | | creature_text | 52,700 |
| **hotfixes** | 273 MB | spell_name | 400,104 |
| | | spell_misc | 403,631 |
| | | broadcast_text | 234,089 |
| | | item_sparse | 175,670 |
| | | hotfix_blob | 60,471 |
| | | hotfix_data | 22,532 |
| **characters** | 4 MB | | |
| **auth** | 1.2 MB | | |
| **roleplay** | 0.1 MB | | |

### Data Quality Indicators

| Check | Status | Detail |
|-------|--------|--------|
| Hotfix redundancy | Clean | 97.8% redundant rows removed (10.6M to 244K) |
| SmartAI integrity | Clean | 0 orphans (5,894 cleared, 181 GUID-based restored) |
| ContentTuningID coverage | 98% | 4,820 of 4,918 spawned CT=0 creatures enriched |
| DifficultyID=0 coverage | 100% | 0 missing DifficultyID=0 rows (532,346 total) |
| Broadcast text coverage | 100% | 393 missing entries filled from Wago DB2 |
| Hotfix_data orphans | Clean | 608K orphaned entries removed |
| Loot table PKs | Enforced | 193K pre-existing duplicates removed |
| NPC model validation | Clean | 78,475 corrections applied |
| SQL updates | Current | All 212 SQL files applied |

---

## Recent Sessions

| # | Date | Focus | Key Result |
|---|------|-------|------------|
| 91 | Mar 7 | Doc Audit | doc/ 20 to 13 files, deleted 7 obsolete, fixed mojibake DB report |
| 90 | Mar 7 | SQL Directory Audit | 12 issues fixed, pruned 19,416 old TDB files from git (3.8 GB) |
| 88 | Mar 7 | Spell Audit Pipeline | 1,842 C++ stubs + SQL for all 13 classes, 3 classification bugs fixed |
| 86 | Mar 7 | Grand Consolidation QA | 200+ old path refs fixed, memory files consolidated, GitHub cleaned |
| 85 | Mar 6 | Grand Consolidation | Moved everything to ~/VoxCore/, organized personal docs, rebuilt |
| 84 | Mar 6 | Windows Performance Tuning | 30+ registry tweaks, NVIDIA App config, system hardened |
| 64 | Mar 5 | Build 66263 | New client build, 1,094 DB2 tables extracted, 1,492 high-tier spawns |
| 63 | Mar 5 | Transmog Audit | 5-phase audit — 26/26 items across Bridge/Spy/Server/Player.cpp |
| 62 | Mar 5 | Gap Scrape | 8,799 vendor items + 592 quest starters from Wowhead |
| 61 | Mar 5 | Quest Reward Text | 30-worker Tor scraper — 13,494 offer_reward + 6,792 request_items |

---

## Project Metrics

| Metric | Value |
|--------|-------|
| Commits this week | 154 |
| Total sessions | 99 |
| Build config | RelWithDebInfo (current) |
| Custom slash commands | 19 |
| SQL files applied | 212 |

---

## Open Issues

### HIGH Priority

- **Build 66263 Auth Keys** — Bypass active; waiting for TrinityCore to publish keys
- **Transmog: In-Game Verification** — All 5 bugs fixed (A-E), deployed, awaiting testing
- **Transmog: Unverified Features** — MH enchant illusions, clear single slot — deployed, never verified

### MEDIUM Priority

- Skyriding / Dragonriding — TODO outside Dragon Isles
- Dead HandleTransmogrifyItems handler — 400 lines of unused code (Phase 4 sync, may be needed)
- Melee first-swing NotInRange bug — CombatReach=0 or same-tick race

### COMPLETED (since last update)

- Spell Audit Pipeline — 1,842 C++ stubs, 114 serverside stubs, 18 proc entries generated
- Doc Audit — doc/ cleaned from 20 to 13 files
- SQL Directory Audit — 12 issues fixed, 19K old TDB files pruned (3.8 GB saved)
- Grand Consolidation — all paths moved to ~/VoxCore/, 200+ refs updated
- Missing Spawns High Tier — 1,492 service NPC spawns deployed
- Quest Reward Text Scrape — 13,494 offer_reward + 6,792 request_items imported
- Transmog 5-Phase Audit — 26/26 items fixed across 4 source files
- Midnight Expansion Data — 1,463 rows applied (starters, enders, loot, abilities)

---

## Repository Activity

| Repository | Recent Work |
|-----------|-------------|
| VoxCore84/RoleplayCore | Spell audit pipeline, doc/SQL audit, desktop shortcuts, code quality pass |
| VoxCore84/wago-tooling | Midnight scraper, gap scrape, ATT mega-parser |
| VoxCore84/tc-packet-tools | WPP script hardening |
| VoxCore84/roleplaycore-report | Data update — March 7, 2026 |
| VoxCore84/trinitycore-claude-skills | 19 custom slash commands |

---

## Tool Inventory Summary

| Category | Count | Examples |
|----------|-------|---------|
| Data pipelines | 15 | tact_extract, merge_csv_sources, repair_hotfix_tables |
| Audit & validation | 12 | npc_audit (27 checks), go_audit (15), quest_audit (15) |
| Hotfix system | 6 | hotfix_differ_r3, cleanup_hotfix_data_orphans |
| Transmog tools | 5 | TransmogBridge, extract_transmog_packets |
| Packet analysis | 5 | opcode_analyzer, wpp-inspect |
| Extraction & reference | 9 | TACTSharp, wow.tools.local, DB2Query |
| Build & operations | 5 | wago_db2_server (MCP), SOAP interface |
| Web scrapers | 6 | wowhead_scraper, att_to_sqlite, import_quest_rewards |
| **Total** | **75+** | Across Python, C++, Lua, SQL, Shell, C# |

---

## Public Resources

- [Operations Runbook](https://gist.github.com/VoxCore84/84656ef0960c699927e3a555e8248f7b) — 22-section reference for every tool and pipeline
- [Session Changelog](https://gist.github.com/VoxCore84/4c63baf8154753d2a89475d9a4f5b2cc) — 99 sessions with commit hashes
- [Database Report](https://gist.github.com/VoxCore84/528e801b53f6c62ce2e5c2ffe7e63e29) — Full 16-part data quality report
- [Open Issues](https://gist.github.com/VoxCore84/2b69757faa2a53172c7acb5bfa3ad3c4) — Prioritized issue tracker
