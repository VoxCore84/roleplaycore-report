
## Part 4: Quest System Enrichment

### 4.1 Quest Chains

Using Wago's `QuestLineXQuest` DB2 CSV data, generated `PrevQuestID` and `NextQuestID` links:

| Metric | Value |
|--------|-------|
| Total quest_template_addon rows | 49,736 |
| Quests with PrevQuestID | 24,868 (50.0%) |
| Quests with NextQuestID | 17,636 (35.5%) |
| Chain starters identified | 1,862 |
| Quest lines processed | 1,605 |
| ATT chain links added | +3,081 (from AllTheThings database cross-reference) |

Zero self-references, zero circular chains, zero dangling references. Cycle detection (DFS-based) and dangling reference cleanup built into the pipeline.

### 4.2 Quest Points of Interest (POI)

From Wago `QuestPOIBlob` and `QuestPOIPoint` CSVs:

| Table | Already in DB | Added | Final Total |
|-------|-------------|----------|-------------|
| quest_poi | 131,976 | 2,880 | 134,856 |
| quest_poi_points | 287,778 | 5,199 | 292,977 |

### 4.3 Quest Objectives

From Wago `QuestObjective` CSV: 633 new objectives across 227 quests added to the existing 59,566. Final total: 60,199.

### 4.4 Quest Starters & Enders

Reimported from LoreWalkerTDB to ensure completeness:

| Table | Rows |
|-------|------|
| creature_queststarter | 30,746 (+4,630 from AllTheThings) |
| creature_questender | 33,496 |
| gameobject_queststarter | 1,615 |
| gameobject_questender | 1,610 |

### 4.5 Hero's Call / Warchief's Command Board Dedup

LW import artifact: old-framework quest boards (entries 206294/206116) were stacked on top of modern boards at identical coordinates. 25 duplicate board spawns removed, quest associations migrated from old entries to the 4 modern entries that had zero quests.

---

## Part 5: Localization

### 5.1 Item Locales (from Raidbots)

Using Raidbots' `item-names.json` (171K items, 7 locales including en_US), imported 6 non-English locales plus 4 stub locales from TC's base data:

| Table | Total Rows |
|-------|-----------|
| item_sparse_locale | 1,020,264 |
| item_search_name_locale | 608,480 |

**Full coverage** (~170K items each): German, Spanish, French, Italian, Portuguese (Brazil), Russian

**Stub coverage** (29-59 items each, from TC base data): Mexican Spanish, Korean, Chinese (Simplified/Traditional)

Players using non-English clients now see item names in their language.

---
