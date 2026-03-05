
## Part 13: Hotfix Redundancy Audit (Complete)

### 13.1 The Problem

After the hotfix repair ([Part 2](data-import.md#part-2-hotfix-repair-system)), the hotfix database carried **~10.8M content rows** across 517 tables. The hotfix system sends only **corrections** to client data — rows that override the client's built-in DBC/DB2 files. But 97.8% of those rows were **identical** to what the client already had. This:

- Increased login time (every hotfix entry sent via SMSG_HOTFIX_CONNECT)
- Required chunked packet delivery ([Part 7.4](performance.md#74-hotfix-pipeline-crash-fix-critical)) just to avoid crashing
- Wasted server memory caching duplicate data

### 13.2 Approach: 3-Round Audit

A custom diff pipeline (`hotfix_audit/` in the repo) compares every hotfix row against DBC baselines extracted from the WoW 12.0.1.66220 client via **wow.tools.local (WTL)**. WTL extracts complete DB2 files from the client's CASC archive — more complete than Wago CSV exports, which can be partial.

Each row is classified:

| Category | Meaning | Action |
|----------|---------|--------|
| **Redundant** | Identical to DBC baseline | DELETE |
| **Override** | Differs from baseline | KEEP (genuine correction) |
| **New** | Not in DBC at all | KEEP (custom/community content) |
| **Negative Build** | VerifiedBuild < 0 | KEEP (TC deletion marker) |

### 13.3 Round 1 — Discovery

String-level comparison against DBC2CSV exports:

| Metric | Value |
|--------|-------|
| Tables audited | 388 |
| Total rows examined | ~10.8M |
| Redundant (string match) | ~9.6M (88.9%) |
| Override | ~468K |
| New (not in DBC) | ~232K |

### 13.4 Round 2 — Refined Diff

| Improvement | Details |
|-------------|---------|
| Better CSV baseline | WTL DBC2CSV instead of Wago partial exports |
| Column mapping fixes | Corrected array index off-by-one errors |
| Batch DELETE SQL | TRUNCATE for fully-redundant tables, IN-clause batches for partial |
| Orphan cleanup | 175K orphaned hotfix_data entries (referencing deleted tables) |

Removed ~204K additional redundant rows + 175K orphaned entries.

### 13.5 Round 3 — Type-Aware Cleanup

Introduced type-aware comparison to catch false negatives from string diffing:

| Fix | Details |
|-----|---------|
| **Float32 precision** | IEEE 754 bit-level comparison via `struct.pack('f')` — MySQL FLOAT truncates to ~6 sig digits during serialization |
| **Signed/unsigned int32** | Same 32-bit pattern comparison (e.g., -1 == 4294967295 as uint32) |
| **Logical primary keys** | `broadcast_text_duration` uses `(BroadcastTextID, Locale)` not `ID` |
| **Array index mapping** | DB `Foo1` → CSV `Foo[0]` (1-indexed to 0-indexed) |

Found 767,672 additional redundant rows across 109 tables.

### 13.6 Final Results

| Metric | Before | After |
|--------|--------|-------|
| **Hotfix content rows** | ~10.8M | ~244,000 |
| **Content reduction** | — | **97.8%** |
| hotfix_data entries | 1,084,369 | 226,984 |
| Hotfix DB on disk | 1,309 MB | 535 MB |

\!\!\! note
    The content table cleanup (deleting redundant rows from tables like spell_name, spell_effect, etc.) was fully applied across all 3 rounds. The hotfix_data registry was cleaned through orphan removal in R2 and R3, reducing it from 1.08M to ~227K entries. These correspond to the ~244K genuine content rows (some content rows share hotfix_data entries).

**Remaining ~244K content rows:**

| Category | Rows | Details |
|----------|------|---------|
| **Overrides** | ~8,400 | Genuine corrections (chr_customization_choice, spell_item_enchantment, item_sparse, content_tuning, creature_display_info) |
| **New content** | ~231,000 | Not in client DBC — broadcast_text (~224K from TC community data), phase (~5,700), custom items (~400) |

### 13.7 Safety

Three `db_snapshot.py` snapshots taken at each phase boundary. Each round's SQL applied only after verifying the previous round.

### 13.8 What This Fixed In-Game

- **Faster login**: SMSG_HOTFIX_CONNECT sends far less data — ~244K content rows instead of 10.8M
- **Eliminated crash risk**: Payload now well within ByteBuffer limits without chunking
- **Every remaining content row has a reason to exist** — either a genuine correction or custom content

### 13.9 Reproducibility

Tools in `hotfix_audit/` with full README. 3-step process: `build_table_info_r3.py` → `hotfix_differ_r3.py` → `gen_practical_sql_r3.py`.

---
