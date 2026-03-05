
## Part 6: Database Cleanup & Integrity

### 6.1 Initial 5-Database Audit (Feb 27)

148-check audit across all five databases found 412K rows of dead data:

| Category | Rows Removed |
|----------|-------------|
| Orphaned loot templates | 388,000 (63% of GO loot was dead references) |
| Duplicate spawns | 17,500 |
| Broken pool chains | 2,600 |
| Duplicate hotfix_data | 1,800 |
| SmartAI/script orphans | 928 |
| Event orphans | 413 |
| **Total** | **~412,000** |

### 6.2 Loot Table Primary Key Discovery & Deduplication

**The discovery**: `creature_loot_template` and `gameobject_loot_template` ship with **no primary key** — only a non-unique index `KEY idx_primary (Entry,ItemType,Item)`. `INSERT IGNORE` silently does nothing, and any bulk import creates exact row duplicates.

During the LW import, creature_loot ballooned from ~3.1M to 6.2M rows because every INSERT doubled the existing data. Detected, deduped via CSV round-trip (`sort -u`), and recovered:

| Table | Bloated | After Recovery | Dupes Removed |
|-------|---------|---------------|-----|
| creature_loot_template | 6,207,851 | 3,276,944 | 2,930,907 |
| gameobject_loot_template | 189,843 | 124,019 | 65,824 |

Separately, found 193,542 **pre-existing** duplicate rows across 4 loot tables that were already in the DB before any import. Removed via CREATE-SELECT-SWAP.

**Prevention:** Added proper PRIMARY KEYs to all 7 loot tables.

### 6.3 Post-Import Cleanup (47,478 rows)

After the LW bulk import, the worldserver logged ~627K error lines. Systematically cleaned the import-introduced issues:

| Category | Rows Cleaned |
|----------|-------------|
| Duplicate creature spawns (< 1 yard) | 19,385 |
| Duplicate GO spawns (< 1 yard) | 18,485 |
| SmartAI errors (bad spells, unsupported types, missing refs) | 2,808 |
| Empty pool_templates | 1,806 |
| NPC vendor issues (bad items, missing flags) | 305 |
| Empty waypoint_paths | 47 |
| Orphaned dependents from spawn deletion | 4,642 |

\!\!\! note
    Beyond the 2,808 rows in the table above, additional cleanup scripts (2026_02_25_30 through 2026_02_26_32) removed ~498K invalid SmartAI entries — scripts referencing creatures without SmartAI AIName, non-existent spells/waypoints/quests, deprecated event types, and broken link chains. This is why the final smart_scripts count (294,425) is much lower than the peak during import. The validation scripts mirror the server's own `SmartScriptMgr.cpp` checks, ensuring every remaining script is loadable without errors.

### 6.4 Other Cleanup

- **Backup tables**: 101 backup/temp tables dropped across all databases, reclaiming ~382 MB
- **MyISAM → InnoDB**: All 7 remaining MyISAM tables converted (2 required `ROW_FORMAT=DYNAMIC`) — enables row-level locking, crash recovery, buffer pool caching
- **Indexes**: 4 redundant/duplicate indexes dropped

---
