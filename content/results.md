
## Part 10: Custom Tooling Summary

Over 75 Python scripts, MCP servers, audit tools, and SQL generators were built for this project. See **[Part 16](reference.md#part-16-complete-tooling--infrastructure-catalog)** for the complete catalog.

**Top 10 tools at a glance:**

| Tool | Purpose |
|------|---------|
| `repair_hotfix_tables.py` | 5-batch hotfix DB repair against Wago DB2 baselines |
| `hotfix_differ_r3.py` | Type-aware redundancy audit (float32, int32 sign, logical PK) |
| `npc_audit.py` | 27-check NPC validator against Wago DB2 + Wowhead |
| `import_all.py` | 5-phase dependency-ordered LoreWalkerTDB import |
| `run_all_imports.py` | 8-step Raidbots/Wago orchestrator with `--dry-run` |
| `wago_db2_server.py` | MCP server: DuckDB queries across 1,094 DB2 CSVs |
| `code_intel_server.py` | MCP server: hybrid ctags + clangd C++ intelligence (416K symbols) |
| `diff_builds.py` | Row-by-row CSV differ with oscillation detection |
| `wowhead_scraper.py` | 216K NPC data scraper for cross-reference audit |
| `db_snapshot.py` | MySQL backup/rollback with snapshot, check, prune, rollback |

---

## Part 11: Final Database State

### 11.1 Table Counts (March 7, 2026)

**World database (1,054 MB):**

| Table | Rows | Notes |
|-------|------|-------|
| creature_template | 225,968 | NPC template definitions |
| creature | 611,359 | NPC spawn instances |
| creature_template_difficulty | 532,346 | Difficulty scaling (0 missing DifficultyID=0) |
| creature_template_spell | 171,590 | NPC spell assignments |
| smart_scripts | 286,436 | NPC AI behavior scripts |
| gameobject | 188,069 | World object spawn instances |
| npc_vendor | 174,364 | Vendor inventory entries |
| quest_template | 47,536 | Quest definitions |
| quest_poi | 133,026 | Quest map markers |
| creature_queststarter | 30,659 | Quest givers |
| creature_questender | 37,698 | Quest turn-ins |
| trainer_spell | 40,305 | Trainer spell offerings |
| spell_script_names | 5,467 | C++ spell script bindings |
| serverside_spell | 4,503 | Custom serverside spells |
| conditions | 25,566 | Conditional logic entries |
| creature_text | 52,700 | NPC dialogue/yell text |

**Hotfixes database (273 MB):**

| Table | Rows | Notes |
|-------|------|-------|
| spell_misc | 403,631 | Spell metadata |
| spell_name | 400,104 | Spell name registry |
| broadcast_text | 234,089 | TC community + custom text entries |
| item_sparse | 175,670 | Item data (full + overrides) |
| hotfix_blob | 60,471 | Binary hotfix data |
| hotfix_data | 22,532 | Client correction registry |

\!\!\! note
    Most hotfix tables (spell_name, spell_effect, creature_display_info, content_tuning, area_table, etc.) were nearly emptied by the redundancy audit — their data matched the client's DBC baseline and was unnecessary. The tables above show only genuine overrides and custom content. Pre-audit counts were 10-1,000x larger (see [Part 2.3](data-import.md#23-results-build-66220--march-3-2026)).

**Locale tables:**

| Table | Rows |
|-------|------|
| item_sparse_locale | 1,020,264 |
| item_search_name_locale | 608,480 |

### 11.2 Database Sizes

| Database | Size |
|----------|------|
| world | 1,054 MB |
| hotfixes | 273 MB |
| characters | 4 MB |
| auth | 1.2 MB |
| roleplay | 0.1 MB |

---

## Part 12: What It All Means for Players

### Before
- 6,548 NPCs stuck at level 1 — endgame elites one-shottable by any player
- Tens of thousands of NPCs standing motionless with no AI scripts
- 4,867+ duplicate NPCs stacked on top of each other
- Quest chains broken — no breadcrumbs, no progression tracking
- Quest objectives showing blank or missing, no map markers
- Items showing English-only names for all non-English clients
- Loot tables with 193K duplicate entries inflating drop chances (and no primary keys to prevent more)
- 1,142 vendors with VENDOR flag but zero items to sell
- Vendors with 700-hour respawn timers, NPCs moving at 12-20x speed, an invisible creature (scale 0)
- Server startup: 3 minutes 24 seconds
- 627,000+ error lines on every startup
- Server crashing on client connect (oversized hotfix packet)

### After
- All NPCs at correct levels with proper ContentTuning scaling (4,820 CT=0 creatures enriched)
- 294K+ validated SmartAI scripts — NPCs patrol, react, run events (26K net new scripts added, entire dataset validated)
- Clean spawns — no duplicates, no stacked/invisible NPCs. 3,240 missing NPCs added via coordinate transformer (quest + service tiers)
- 24,868 quest chain links (+3,081 from AllTheThings), 135K POI entries, 60K quest objectives
- 4,630 quest starters and 1,510 vendor items added from AllTheThings database
- 1.6M+ item locale entries across 10 languages
- Correct drop rates with enforced primary keys on all loot tables
- 78,475 NPC corrections (levels, factions, flags, names, pathing)
- Service NPCs actually function (vendors sell, trainers train, gossip menus work)
- 17-second server startup (92% reduction)
- Hotfix content tables reduced from 10.8M rows to ~244K (97.8% reduction)
- Clean server logs — real errors visible instead of buried in noise

### For CaptainCore / LoreWalkerTDB

**What LW data gave us:**
- ~1M net new rows of world data
- ~524K SmartAI scripts imported (294K survived validation — the rest had broken references)
- ~242K net loot table entries
- Hotfix entries (spell enchantments, sound kits, display info, phases)
- Quest starters/enders, conversation data, spawn pools, game events

**How we built on LW data:**
1. **Import pipeline** — column mismatch handling (3 tables), dependency ordering (5 phases), 15-point validation
2. **Post-import cleanup** — 47K orphans/duplicates cleaned, 627K error lines resolved, ~498K invalid SmartAI entries removed by validation
3. **Gap filling** — 1.6M Raidbots item locales, 21K Wago quest chains, 135K quest POI, 216K Wowhead NPC cross-reference
4. **Hotfix repair + trim** — 843K hotfix_data entries generated, content tables trimmed from ~10.8M to ~244K genuine rows
5. **78K NPC corrections** — validated against Wago DB2 + Wowhead

**LW data quality findings (potential upstream fixes):**
- Column count mismatches on `creature`/`gameobject`/`npc_vendor` vs current TC schema
- Gameobject rotation quaternions stored as `(0,0,0,0)` instead of identity `(0,0,0,1)`
- Quest board entries (206294/206116) stacking on modern board coordinates
- SmartAI scripts referencing non-existent spells (1,095), unsupported types (813), missing waypoints (803)
- Duplicate spawns within 1 yard (37,870 pairs)

**Collaboration opportunities:**
- `fix_column_mismatch.py` and `validate_import.py` could help anyone consuming LW data
- The hotfix repair system is build-agnostic — works for any TC hotfix database
- The hotfix redundancy audit tools are in the VoxCore repo (`hotfix_audit/`)
- If LW added composite PKs to loot tables, it would prevent the INSERT IGNORE duplication trap for all consumers

---
