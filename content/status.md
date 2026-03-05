# Project Status

Current state of the VoxCore project — database health, recent activity, and open work items.

## Database Health

### Size & Row Counts (March 5, 2026)

| Database | Tables | Size | Key Table | Rows |
|----------|--------|------|-----------|------|
| **world** | 259 | 1,267 MB | creature | 662,536 |
| | | | smart_scripts | 294,425 |
| | | | creature_loot_template | 2,904,341 |
| | | | npc_vendor | 167,312 |
| | | | quest_template_addon | 49,736 |
| **hotfixes** | 517 | 535 MB | hotfix_data | 226,984 |
| | | | broadcast_text | 224,233 |
| | | | item_sparse | 1,418 |
| **characters** | 151 | 7.6 MB | | |
| **auth** | 50 | 1.9 MB | | |
| **roleplay** | 5 | 0.1 MB | | |

### Data Quality Indicators

| Check | Status | Detail |
|-------|--------|--------|
| Hotfix redundancy | Clean | 97.8% redundant rows removed (10.6M to 244K) |
| SmartAI integrity | Clean | 0 orphans (5,894 cleared, 181 GUID-based restored) |
| ContentTuningID coverage | 98% | 4,820 of 4,918 spawned CT=0 creatures enriched |
| DifficultyID=0 coverage | 100% | 26,745 missing Diff0 rows filled |
| Broadcast text coverage | 100% | 393 missing entries filled from Wago DB2 |
| Hotfix_data orphans | Clean | 608K orphaned entries removed |
| Loot table PKs | Enforced | 193K pre-existing duplicates removed |
| NPC model validation | Clean | 78,475 corrections applied |

---

## Recent Sessions

| # | Date | Focus | Key Result |
|---|------|-------|------------|
| 55 | Mar 5 | Website QA | Cross-page sidebar, accuracy audit (30/30 verified) |
| 54 | Mar 5 | ATT Mega-Parser | 60 SQLite tables from 30 data sources (52.6 MB) |
| 53 | Mar 5 | TACT/CSV Merge | Best-of-both dataset — 1,097 tables, 7,183 Wago extras |
| 52 | Mar 5 | Retail Sniffer | DT=3 reverted, merge strategy corrected from 2.77M packet lines |
| 51 | Mar 5 | Missing Spawns | 1,748 quest NPCs deployed, 214 phase-dupes resolved |
| 50 | Mar 5 | ATT Parser | 8,950 validated rows — quest starters, chains, vendor items |
| 49 | Mar 5 | TDB Delta | +1,967 quest_offer_reward rows, scraper hardened |
| 48 | Mar 5 | World DB QA | 9 SQL updates — CTD, SmartAI, spawns, waypoints, loot |
| 47 | Mar 5 | Gist Audit | Verified all report numbers, cleaned 608K hotfix_data orphans |
| 46 | Mar 5 | WPP Hardening | 20-bug QA across 4 packet analysis scripts |

---

## Open Issues

### HIGH Priority

- **Transmog: 5-Bug Investigation** — Diagnostic build deployed, DT/merge reverts applied from retail sniffer data. Next: expand slotMap from 14 to 30 entries
- **Transmog: PR #760 Bugs** — SetID mapping (F), pad byte parsing (G), CMSG never fires (H)
- **Stale Hotfix Overrides** — 7,119 entries where TACT+Wago agree but our hotfix disagrees (958 ItemSparse confirmed wrong)

### MEDIUM Priority

- Skyriding / Dragonriding — TODO outside Dragon Isles
- Dead HandleTransmogrifyItems handler — 400 lines of unused code
- Melee first-swing NotInRange bug — CombatReach=0 or same-tick race

### READY TO RUN

- **Missing Spawns High Tier** — 1,626 service NPC spawns transformable (`coord_transformer.py --tier high`)
- **Quest Reward Text Scrape** — 27,328 quests ready for Wowhead scrape (~2 hours)

---

## Repository Activity

| Repository | Latest Commit | Recent Work |
|-----------|--------------|-------------|
| VoxCore84/RoleplayCore | `fae00afb86` | Transmog sniffer-informed fixes |
| VoxCore84/wago-tooling | `b1f0bd0` | ATT mega-parser, TACT pipeline |
| VoxCore84/tc-packet-tools | `821e74f` | WPP script hardening |
| VoxCore84/roleplaycore-report | `068c81c` | Website QA round 2 |
| VoxCore84/trinitycore-claude-skills | `25967f7` | 17 custom slash commands |

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
| **Total** | **65+** | Across Python, C++, Lua, SQL, Shell, C# |

---

## Public Resources

- [Operations Runbook](https://gist.github.com/VoxCore84/84656ef0960c699927e3a555e8248f7b) — 22-section reference for every tool and pipeline
- [Session Changelog](https://gist.github.com/VoxCore84/4c63baf8154753d2a89475d9a4f5b2cc) — 55+ sessions with commit hashes
- [Database Report](https://gist.github.com/VoxCore84/528e801b53f6c62ce2e5c2ffe7e63e29) — Full 16-part data quality report
- [Open Issues](https://gist.github.com/VoxCore84/2b69757faa2a53172c7acb5bfa3ad3c4) — Prioritized issue tracker
