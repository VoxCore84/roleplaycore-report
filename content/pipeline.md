# Data Pipeline

The complete data flow from raw game files to a validated, production-ready server database. Every stage is scripted and reproducible.

## Pipeline Overview

The pipeline processes data through four stages: **Extract** raw DB2 tables from the game client, **Merge** with CDN hotfix extras, **Repair** against the server database, and **Validate** the final result.

---

## Stage 1: Extract

### TACTSharp / CASC Extraction

`tact_extract.py` extracts all 1,097 DB2 tables directly from the local WoW client installation via TACTSharp. This is the **ground truth** source — no API rate limits, no oscillation artifacts, no missing data.

| Metric | Value |
|--------|-------|
| Tables extracted | 1,097 |
| Extraction time | ~50 seconds |
| Source | Local CASC (build 66220) |
| Converter | DBC2CSV (1,315 table definitions) |
| Retry handling | Automatic (DBC2CSV drops ~0.5% non-deterministically) |

### Wago.tools CDN (Fallback + Extras)

`wago_db2_downloader.py` downloads the same 1,097 tables from Wago's HTTP API. Used as a fallback and as a source of CDN-only hotfix content that doesn't exist in the local client.

| Metric | Value |
|--------|-------|
| Tables available | 1,097 |
| Known issue | SpellEffect oscillates between 269K and 608K rows across exports |
| CDN extras | Hotfix content not yet in local build |

---

## Stage 2: Merge

### Best-of-Both Dataset

`merge_csv_sources.py` combines the two sources: TACT as the base (client ground truth) with Wago-only rows appended (CDN hotfix content the client hasn't received yet).

| Metric | Value |
|--------|-------|
| TACT-only tables | 998 (Wago had same or fewer rows) |
| Merged tables | 99 (Wago had additional CDN-only rows) |
| Extra rows from Wago | 7,183 across 99 tables |
| Header normalization | DBC2CSV `[N]` converted to Wago `_N` notation |
| Output | `merged_csv/` directory — single source of truth |

All 14+ downstream consumer scripts read from `merged_csv/` automatically via `wago_common.py`.

---

## Stage 3: Repair

### Hotfix Repair System

`repair_hotfix_tables.py` compares every server hotfix table against the merged CSVs and generates repair SQL:

| Step | What happens |
|------|-------------|
| Column normalization | 28 global aliases + 23 table-specific + 6 table name overrides |
| Row comparison | Identifies zeroed columns, missing rows, custom diffs to preserve |
| SQL generation | UPDATE for zeroed columns, INSERT for missing rows |
| Registry sync | Generates hotfix_data entries so the client receives corrections |
| Batch processing | 5 batches of ~80 tables each |

| Metric | Value |
|--------|-------|
| Tables compared | 388 |
| Missing rows inserted | 103,153 |
| Zeroed columns fixed | 1,831 |
| Custom diffs preserved | 468,972 |
| hotfix_data generated | 843,894 entries |

### Redundancy Audit

Three rounds of cleanup removed data that matched the client's DBC baseline:

| Round | Method | Rows Removed |
|-------|--------|-------------|
| R1 | String comparison | 9.6M |
| R2 | WTL DBC2CSV cross-ref | 204K |
| R3 | Type-aware (float32, int32, logical PK) | 768K |
| Orphan sweep | hotfix_data registry cleanup | 175K entries |
| **Total** | | **~10.6M rows removed (97.8%)** |

---

## Stage 4: Validate

### Post-Repair Verification

| Check | Result |
|-------|--------|
| Hotfix content rows | ~244K genuine (8,396 override + 231,199 new) |
| hotfix_data registry | 226,984 entries |
| Server startup | 17s (was 3m24s before optimization) |
| Client hotfix delivery | All corrections delivered on login |
| Zero-error boot | Clean server logs after repair |

---

## Additional Data Sources

### AllTheThings Database

`att_to_sqlite.py` parses the entire AllTheThings addon database (1,576 Lua files) into a 60-table SQLite database. `att_generate_sql.py` cross-references against the server and generates validated SQL.

| Data Applied | Rows |
|-------------|------|
| Quest starters (creature_queststarter) | +4,630 |
| Quest chain links (PrevQuestID) | +3,081 |
| Vendor items (npc_vendor) | +1,510 |
| **Total** | **+9,221** |

### LoreWalkerTDB

Community TrinityCore database providing the bulk of world data:

| Category | Volume |
|----------|--------|
| World DB rows | ~1,004,000 net |
| SmartAI scripts | 294,425 validated (from ~524K attempted) |
| Loot table entries | ~242K net |

### Coordinate Transformer

`coord_transformer.py` converts Wowhead zone-percent coordinates to world XYZ positions using nearest-neighbor Z interpolation from 527K existing spawns.

| Tier | Spawns Added |
|------|-------------|
| Critical (quest NPCs) | 1,541 applied |
| Phase-duplicate resolved | 214 analyzed, 207 re-inserted |
| High (service NPCs) | 1,626 ready |

---

## Packet Capture & Client Analysis

Packet sniffers provide ground truth for protocol behavior that no database can tell you — how the retail client actually sends and receives data.

### WowPacketParser (WPP)

Decodes `.pkt` captures from private server sessions. Integrated into the server launch script — every session automatically produces parsed packet logs for analysis.

| Metric | Value |
|--------|-------|
| Opcodes tracked | 991 in the opcode dictionary |
| Auto-parse | Runs on server shutdown via `start-worldserver.sh` |
| Transmog extraction | `extract_transmog_packets.py` pulls outfit/slot data from parsed output |
| Grep tool | `wpp-inspect.sh` — 6 search modes (visible, transmog, trace, summary, opcodes, search) |

### Ymir (Retail Sniffer)

Captures packets from the live retail WoW client. Provides ground truth for protocol behavior that can't be observed on a private server.

| Metric | Value |
|--------|-------|
| Build | 66220 |
| Capture size | 2.77M parsed lines |
| Key finding | Transmog outfits are 30 entries (not 14), DT=3 means "hidden visual" not "remove" |
| Impact | Corrected transmog DT assignment and merge strategy (commit `fae00afb86`) |

### wow.tools.local

Self-hosted DB2/DBC browser for visual data inspection, build diffs, and hotfix comparison. Confirms whether hotfix values match retail DBC baselines.

### Client DBCache

`decode_dbcache.py` and `xref_dbcache.py` decode the WoW client's local hotfix cache (`DBCache.bin`) and cross-reference it against server hotfix data — confirms the client received the expected corrections.

---

## Pipeline Automation

### One-Command Rebuild

```
# Full pipeline from scratch
python tact_extract.py           # Extract 1,097 DB2 tables (~50s)
python merge_csv_sources.py      # Merge TACT + Wago CDN extras
python repair_hotfix_tables.py --batch 1  # Repair in 5 batches
python repair_hotfix_tables.py --batch 2
python repair_hotfix_tables.py --batch 3
python repair_hotfix_tables.py --batch 4
python repair_hotfix_tables.py --batch 5
```

### Build Bump Procedure

When a new WoW build drops:

1. Update `CURRENT_BUILD` in `wago_common.py`
2. Run `tact_extract.py` (re-extract from updated client)
3. Run `merge_csv_sources.py` (re-merge with updated Wago data)
4. Run `repair_hotfix_tables.py` (re-repair against new baseline)
5. All 14+ consumer scripts pick up the new build automatically
