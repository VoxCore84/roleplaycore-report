
## Part 1: LoreWalkerTDB Integration

### 1.1 Hotfixes Import

LoreWalkerTDB's `hotfixes.sql` (322MB) was parsed and selectively imported. Blind import wasn't possible — VoxCore has custom entries (e.g., `broadcast_text` entries at 999999997+, custom `chr_customization_choice` data).

**Key gains:**

| Table | Rows Added | What it fixed |
|-------|-----------|--------|
| spell_item_enchantment | +1,193 | Missing enchant effects |
| sound_kit | +3,611 | Missing ambient/NPC/spell sounds |
| item + item_sparse | +2,799 / +2,810 | Items that existed in client but had no server data |
| spell_effect | +1,335 | Missing spell effects |
| spell_visual_kit | +610 | Missing visual effects |
| creature_display_info | +123 | Missing NPC models |
| phase | +595 | Missing phase definitions |
| achievement | +849 | Missing achievement data |
| lfg_dungeons | +213 | Missing dungeon finder entries |
| trait_definition | +299 | Missing talent/trait data |
| character_loadout | +157 | Missing starting loadouts |
| **+ ~30K hotfix_data entries** | | Registry entries so the client receives corrections |

### 1.2 SmartAI Import (NPC Behavior Scripts)

Two rounds of SmartAI extraction from LW's 897MB world dump:

- **Round 1**: 22,370 rows — quest scripts (17,367), creature AI (4,965), scene triggers, timed events
- **Round 2**: 166,443 rows — 165,360 creature behaviors, 169 gameobject scripts, 702 action lists, 212 scene triggers
- **Skipped**: 525K quest boilerplate rows (all identical "cast spell 82238" phase-update scripts — not useful for RP)
- **Attempted**: ~524,000 SmartAI INSERT operations across all import rounds (including Phase 4 in Section 1.3)
- **Post-validation**: Cleanup scripts removed entries referencing non-existent spells, creatures without SmartAI AIName, deprecated event types, broken link chains, and invalid waypoints (see [Section 6.3](database-cleanup.md#63-post-import-cleanup-47478-rows))
- **Final result**: 294,425 validated scripts (up from ~268K baseline — a net gain of ~26K valid scripts, plus validation of the entire existing dataset)

### 1.3 World DB Bulk Import (March 3, 2026)

5-phase dependency-ordered import of 21 tables from LoreWalkerTDB (builds 65893/65727/65299/63906, all 12.0.x):

| Phase | Tables | Key Data |
|-------|--------|----------|
| **1. Spawns** | creature, gameobject | +29,196 creatures, +19,604 gameobjects |
| **2. Loot** | creature_loot, gameobject_loot | +184,084 creature loot, +58,066 GO loot |
| **3. Dependents** | waypoints, difficulty, addons, pools, spawn_groups, text, spells, models, formations | +30K waypoint nodes, +2K creature addons, +1.8K pool templates |
| **4. SmartAI** | smart_scripts | +336,186 NPC AI scripts (INSERT IGNORE — many later removed by validation) |
| **5. Gossip/Vendor** | gossip_menu, gossip_menu_option, npc_vendor, creature_template_addon | +58 gossip menus, +44 options, +4 vendors |
| **Total** | **21 tables** | **+665,658 net new rows** |

**Column mismatch handling**: LW uses an older TC fork, so 3 tables had different column counts. `fix_column_mismatch.py` parses SQL tuple boundaries and appends safe defaults:
- `creature`: 28 → 29 columns (appended `size=-1`)
- `gameobject`: 24 → 26 columns (appended `size=-1, visibility=256`)
- `npc_vendor`: 11 → 12 columns (appended `OverrideGoldCost=-1`)

All 15 post-import integrity checks passed with zero orphans.

### 1.4 Initial LW World Data Import (February 27, 2026)

The first LW import (predating the bulk import above) added 385,823 rows across 17 tables. The SmartAI rows (167,685) are included in the Section 1.2 totals — same data, not additional:

| Table | Rows Added |
|-------|-----------|
| smart_scripts (2 passes) | 167,685 |
| creature_loot_template | 151,509 |
| gameobject_loot_template | 59,893 |
| pickpocketing_loot_template | 1,389 |
| reference_loot_template | 662 |
| skinning_loot_template | 402 |
| quest_offer_reward | 541 |
| quest_request_items | 370 |
| pool_template | 1,176 |
| pool_members | 1,164 |
| game_event_creature | 260 |
| game_event_gameobject | 164 |
| npc_vendor | 248 |
| conversation_actors | 194 |
| areatrigger_template | 142 |
| conversation_line_template | 19 |
| conversation_template | 5 |

---

## Part 2: Hotfix Repair System

### 2.1 The Problem

TrinityCore's hotfix database diverges from Blizzard's live data over time. Columns get zeroed out during schema migrations, new rows from client patches are missing, and the `hotfix_data` registry (which tells the client what corrections to apply) becomes incomplete.

### 2.2 The Solution

`repair_hotfix_tables.py` compares every hotfix DB table against authoritative DB2 CSV exports and generates repair SQL:

1. Extracts 1,097 DB2 CSV tables from local CASC via TACTSharp (`tact_extract.py`), merged with Wago CDN extras (`merge_csv_sources.py`) for best-of-both coverage
2. Normalizes column names (28 global aliases + 23 table-specific aliases + 6 table name overrides)
3. Compares every row: identifies zeroed columns, missing rows, and custom diffs to preserve
4. Generates UPDATE statements for zeroed columns, INSERT statements for missing rows
5. Generates corresponding `hotfix_data` entries so the client receives the corrections
6. Runs in 5 batches (~80 tables each) to manage memory

### 2.3 Results (Build 66220 — March 3, 2026)

| Metric | Value |
|--------|-------|
| Tables compared | 388 |
| Rows matching | 9,790,318 |
| Zeroed columns fixed | 1,831 UPDATEs |
| Custom diffs preserved | 468,972 rows (intentional overrides) |
| Missing rows inserted | 103,153 INSERTs |
| hotfix_data entries generated | 843,894 |
| Total SQL generated | ~71 MB across 5 batch files |
| **Total hotfix_data rows (pre-trim)** | **1,084,369 across 204 tables** |

> The 1,084,369 total included entries from the repair tool, LW imports, and prior TC data. The subsequent redundancy audit ([Part 13](hotfix-audit.md)) reduced hotfix content table rows to ~244K by deleting entries that matched the client's DBC baseline. The hotfix_data registry itself was reduced from 1,084,369 to 835,385 entries.

**Key table populations after repair (pre-audit — see [Part 11](results.md#part-11-final-database-state) for current):**

| Table | Rows (pre-audit) |
|-------|------|
| spell_name | 400,000 |
| spell_effect | 513,000 |
| item_sparse | 172,000 |
| creature_display_info | 118,000 |
| content_tuning | 9,800 |
| area_table | 9,800 |

### 2.4 Scene Script Repair

`repair_scene_scripts.py` handles `scene_script_text` — Lua scripts stored as hex-encoded blobs. Fixed 36 encoding errors and inserted 224 new scene scripts.

### 2.5 What This Fixed In-Game

- Items display correct names, stats, icons, and tooltips
- Spells have correct effects, visuals, and descriptions
- NPCs show proper display models
- Achievements, currencies, and dungeon data are complete
- All corrections delivered to the client via the hotfix system on login — no client modifications needed

---
