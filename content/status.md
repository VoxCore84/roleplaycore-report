# Project Status

Current state of the VoxCore project — database health, recent activity, and open work items.

## Database Health

### Size & Row Counts (March 5, 2026)

| Database | Tables | Size | Key Table | Rows |
|----------|--------|------|-----------|------|
| **world** | 259 | 1,267 MB | creature | 665,776 |
| | | | smart_scripts | 294,416 |
| | | | creature_loot_template | 2,904,341 |
| | | | npc_vendor | 173,855 |
| | | | quest_template_addon | 47,164 |
| **hotfixes** | 517 | 535 MB | hotfix_data | 227,377 |
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
| 64 | Mar 5 | Build 66263 | New client build, 1,094 DB2 tables extracted, 1,492 high-tier spawns |
| 63 | Mar 5 | Transmog Audit | 5-phase audit — 26/26 items across Bridge/Spy/Server/Player.cpp |
| 62 | Mar 5 | Gap Scrape | 8,799 vendor items + 592 quest starters from Wowhead |
| 61 | Mar 5 | Quest Reward Text | 30-worker Tor scraper — 13,494 offer_reward + 6,792 request_items |
| 60 | Mar 5 | Midnight Data | 38 guide + 586 entity pages — 58 starters, 819 loot, 526 abilities |
| 59 | Mar 5 | Missing Spawns | 3,240 NPCs deployed (quest + service tiers), phase-dupes resolved |
| 58 | Mar 5 | Website Assets | wow-export pipeline config, 83-asset checklist |
| 57 | Mar 5 | Arcane Codex | Dark-only arcane theme, Tool Explorer, pipeline animation, toasts |
| 56 | Mar 5 | BtWQuests Import | 1,062 quest starters from addon, 14,670 chain connections |
| 55 | Mar 5 | Website QA | Cross-page sidebar, accuracy audit (30/30 verified) |

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

- Missing Spawns High Tier — 1,492 service NPC spawns deployed
- Quest Reward Text Scrape — 13,494 offer_reward + 6,792 request_items imported
- Transmog 5-Phase Audit — 26/26 items fixed across 4 source files
- Midnight Expansion Data — 1,463 rows applied (starters, enders, loot, abilities)

---

## Repository Activity

| Repository | Latest Commit | Recent Work |
|-----------|--------------|-------------|
| VoxCore84/RoleplayCore | `fcf1cf2738` | Phase-duplicate spawn fix, transmog audit |
| VoxCore84/wago-tooling | `966e0eb` | Midnight scraper, gap scrape, ATT mega-parser |
| VoxCore84/tc-packet-tools | `821e74f` | WPP script hardening |
| VoxCore84/roleplaycore-report | latest | Arcane Codex visual overhaul, data accuracy audit |
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
| **Total** | **75+** | Across Python, C++, Lua, SQL, Shell, C# |

---

## Public Resources

- [Operations Runbook](https://gist.github.com/VoxCore84/84656ef0960c699927e3a555e8248f7b) — 22-section reference for every tool and pipeline
- [Session Changelog](https://gist.github.com/VoxCore84/4c63baf8154753d2a89475d9a4f5b2cc) — 64+ sessions with commit hashes
- [Database Report](https://gist.github.com/VoxCore84/528e801b53f6c62ce2e5c2ffe7e63e29) — Full 16-part data quality report
- [Open Issues](https://gist.github.com/VoxCore84/2b69757faa2a53172c7acb5bfa3ad3c4) — Prioritized issue tracker
