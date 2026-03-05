# Tooling

Over 60 custom tools built across Python, C++, Lua, SQL, Shell, and C#. Every data pipeline, audit, and repair operation is scripted and reproducible.

## Data Pipelines

| Tool | Language | What it does |
|---|---|---|
| `tact_extract.py` | Python | Primary DB2 source — bulk-extracts 1,097 tables from local CASC via TACTSharp in ~50s |
| `merge_csv_sources.py` | Python | Merges TACT base CSVs with Wago CDN extras into a single best-of-both dataset |
| `repair_hotfix_tables.py` | Python | Compares all 388 hotfix tables against merged DB2 CSVs, generates repair SQL in 5 batches |
| `wago_db2_downloader.py` | Python | Threaded CSV downloader for 1,097 DB2 tables from Wago.tools (fallback source) |
| `extract_lw_world.py` | Python | Parses LoreWalkerTDB's 941 MB world dump, extracts tables with dependency ordering |
| `fix_column_mismatch.py` | Python | Handles column count differences between TC forks (appends safe defaults) |
| `run_all_imports.py` | Python | Orchestrator for the full Raidbots/Wago import pipeline |
| `import_item_names.py` | Python | Imports 171K item names across 10 languages (1.6M locale rows) |
| `quest_chain_gen.py` | Python | Generates 24,868 PrevQuestID/NextQuestID chain links |
| `gen_quest_poi_sql.py` | Python | Generates quest POI and point data from Wago CSVs |
| `quest_objectives_import.py` | Python | Imports quest objective definitions |
| `att_to_sqlite.py` | Python | AllTheThings mega-parser — 60 SQLite tables from 30 data sources (52.6 MB, 174K items) |
| `att_parser.py` | Python | Lua tokenizer for the AllTheThings database (1,576 files, 47K quests) |
| `att_generate_sql.py` | Python | Cross-references ATT data against MySQL, generates validated SQL |
| `coord_transformer.py` | Python | Transforms Wowhead zone-percent coordinates to world XYZ for NPC spawns |

---

## Audit & Validation

| Tool | Language | What it does |
|---|---|---|
| `npc_audit.py` | Python | 27-check NPC validator — factions, models, levels, zones, flags, equipment |
| `go_audit.py` | Python | 15-check gameobject validator — duplicates, phases, display, type, loot, quests |
| `quest_audit.py` | Python | 15-check quest validator — chains, givers, enders, objectives, rewards, duplicates |
| `wowhead_scraper.py` | Python | Multi-entity Wowhead scraper with curl_cffi Chrome TLS fingerprinting |
| `world_health_check.py` | Python | Post-import integrity checker (15 cross-table validation checks) |
| `xref_missing_spawns.py` | Python | Cross-references creature templates against spawn data to find missing NPCs |
| `validate_transmog.py` | Python | Validates transmog outfit data against item and appearance tables |
| `npc_model_validator.py` | Python | Validates creature display IDs against DB2 model data |
| `npc_faction_check.py` | Python | Cross-references NPC factions against faction template DB2 |
| `npc_level_range_audit.py` | Python | Validates creature min/max levels against content tuning |
| `npc_equipment_audit.py` | Python | Validates creature equipment template references |
| `duplicate_spawn_finder.py` | Python | Finds exact-position duplicate creature/gameobject spawns |

---

## Hotfix System

| Tool | Language | What it does |
|---|---|---|
| `repair_hotfix_tables.py` | Python | Main repair — 103K inserts + 1,831 column fixes across 388 tables |
| `repair_scene_scripts.py` | Python | Fixes hex-encoded Lua scene scripts (36 encoding errors, 224 new scripts) |
| `hotfix_differ_r3.py` | Python | Type-aware differ for redundancy audit (float32, int32, logical PK comparison) |
| `gen_practical_sql_r3.py` | Python | Generates cleanup SQL from redundancy audit results |
| `cleanup_hotfix_data_orphans.py` | Python | Removes orphaned hotfix_data registry entries (608K removed in R3) |
| `build_table_info_r3.py` | Python | Builds table metadata for the redundancy differ |

---

## Transmog Tools

| Tool | Language | What it does |
|---|---|---|
| TransmogBridge | Lua | Client addon — patches 12.x serializer bug via 3-layer hybrid merge |
| TransmogSpy | Lua | Debug addon — 14 event monitors, pre/post state capture (~930 lines) |
| `transmog_debug.py` | Python | Full transmog state debugger — character DB, outfits, Wago cross-reference |
| `transmog_lookup.py` | Python | DB2 cross-reference for IMA IDs, items, and visual chains |
| `extract_transmog_packets.py` | Python | Extracts transmog protocol packets, addon messages, and UPDATE fields from WPP output |

---

## Packet Analysis

| Tool | Language | What it does |
|---|---|---|
| `opcode_analyzer.py` | Python | TrinityCore opcode dictionary + packet capture analyzer (991 lines) |
| `start-worldserver.sh` | Shell | Session lifecycle manager — archive, launch, auto-parse, summary |
| `wpp-inspect.sh` | Shell | Packet grep tool — visible, transmog, trace, summary, opcodes, search modes |
| `wpp-add-build.sh` | Shell | Adds new WoW builds to WPP switch statements and rebuilds |
| WowPacketParser | C# | Locally patched packet decoder for build 66220 |

---

## Extraction & Reference

| Tool | Language | What it does |
|---|---|---|
| wow.tools.local | C# | Self-hosted DB2/DBC browser at localhost |
| DBC2CSV | C# | DB2-to-CSV converter with 1,315 table definition files |
| DB2Query | C# | Interactive DB2 query CLI for cross-referencing game data |
| `decode_dbcache.py` | Python | Decodes client DBCache.bin for hotfix comparison |
| `xref_dbcache.py` | Python | Cross-references client cache against server hotfix database |
| TACTSharp | C# | Blizzard CASC storage extraction library — ground truth for DB2 data |
| `wago_enrich.py` | Python | Pre-joins DB2 CSVs into enriched analysis files |
| `enrich_content_tuning.py` | Python | Zone-based ContentTuningID enrichment for spawned creatures |
| `diff_builds.py` | Python | Cross-build differ with Wago export oscillation detection |
| lua-language-server | Lua | LSP for Eluna scripts and addon development |

---

## Build & Operations

| Tool | Language | What it does |
|---|---|---|
| `parse_dberrors.py` | Python | Categorizes DB error log entries by type with counts |
| `db_snapshot.py` | Python | Database snapshot and comparison tool |
| `content_tuning_enrich.py` | Python | Zone-based content tuning enrichment for spawned creatures |
| `wago_db2_server.py` | Python | MCP server — gives Claude direct access to 1,097 DB2 tables |
| SOAP interface | HTTP | Remote GM commands without in-game login |

---

## By the Numbers

| Metric | Value |
|---|---|
| Total tools | 65+ |
| Primary language | Python |
| Languages used | Python, C++, Lua, SQL, Shell, C# |
| DB2 tables indexed | 1,097 |
| Audit checks | 27 (NPC validator) |
| Hotfix tables repaired | 388 |
| Lines of tooling code | 15,000+ |
