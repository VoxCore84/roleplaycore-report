---
title: Discoveries & Lessons
nav_order: 10
---

## Part 14: Discoveries & Lessons (Useful for the Community)

These findings apply to any TrinityCore 12.x project:

### 14.1 Loot Table Primary Key Trap
`creature_loot_template` and `gameobject_loot_template` ship with **no primary key** — only `KEY idx_primary (Entry,ItemType,Item)`. `INSERT IGNORE` silently does nothing, every bulk import creates exact duplicates. We lost ~3M rows to this before discovering it. **Fix**: Add composite PKs after deduplication.

### 14.2 Wago DB2 CSV Export Oscillation
Wago CSV exports oscillate between builds. SpellEffect swings 269K-608K rows, ItemSparse 125K-171K. This is a partial-vs-full **export artifact**. Any diffing tool must detect this or it produces false positives. Quick check: `wc -l SpellEffect-enUS.csv` — >500K = full, <400K = reduced.

### 14.3 MySQL `tmp_table_size` Default Trap
`tmp_table_size` can default to 1,024 **bytes** depending on install. ALL temporary tables spill to disk, destroying GROUP BY/ORDER BY/JOIN performance. Symptom: inexplicably slow server startup. Fix: set to 256M+ explicitly.

### 14.4 Eluna CompatibilityMode Threading Kill
`Eluna.CompatibilityMode = true` (the default) forces **single-threaded map updates**, completely nullifying `MapUpdate.Threads`. A 4-thread config runs on 1 thread. Not documented anywhere obvious.

### 14.5 LoreWalkerTDB Column Mismatches
LW uses an older TC fork. At least 3 tables have fewer columns: `creature` (28 vs 29), `gameobject` (24 vs 26), `npc_vendor` (11 vs 12). Direct import fails. Need a column-count-aware parser to append defaults.

### 14.6 LoreWalkerTDB Rotation Data
LW stores `(0,0,0,0)` quaternion for gameobject rotations — mathematically invalid (identity is `(0,0,0,1)`). Don't overwrite valid rotations with LW data.

### 14.7 ByteBuffer Assert at Scale
TC's ByteBuffer asserts at 100MB. With 1M+ hotfix_data rows, SMSG_HOTFIX_CONNECT exceeds this on connect. Any server with a large hotfix dataset needs chunked delivery — or better yet, run a redundancy audit to trim the payload ([Part 13](#part-13-hotfix-redundancy-audit-complete)).

### 14.8 Stacked Quest Board Trap
LW import places old-framework quest boards (entries 206294/206116) at exact coordinates of modern boards. The old boards may be the ones actually serving quests (via `gameobject_queststarter`), while modern boards have zero associations. Deleting the "duplicate" breaks quest functionality. Always check quest associations first.

### 14.9 Hotfix Redundancy Is the Norm
97.8% of TC hotfix content rows were identical to the client's DBC baseline. Likely representative of any TC server that has run repair tools or imported LW hotfix data. The hotfix system is for corrections, not duplication. Any TC server can dramatically improve login speed by running a similar audit. Tools are in the RoleplayCore repo.

---
