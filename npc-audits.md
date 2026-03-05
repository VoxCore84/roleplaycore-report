---
title: NPC Audits & Corrections
nav_order: 3
---

## Part 3: NPC Audits & Corrections

### 3.1 Automated NPC Audit Tool (27 checks)

`npc_audit.py` validates every NPC against Wago DB2 data and Wowhead scraped data:

| Category | What it checks |
|----------|---------------|
| Levels | ContentTuningID vs expected level ranges |
| Flags | Vendor/trainer/gossip flags match actual data |
| Faction | Hostile/friendly/neutral alignment |
| Classification | Normal/Elite/Rare/Boss accuracy |
| Type | Humanoid/Beast/Undead/etc |
| Duplicates | Phase-aware stacked spawn detection |
| Names | Name accuracy vs Wago/Wowhead |
| Scale | Invisible (0) or oversized (>10) creatures |
| Speed | Absurd walk/run speeds |
| Equipment | Missing weapon/armor visuals |
| Gossip | Menu existence vs flag |
| Waypoints | Path linkage integrity |
| SmartAI | Script existence vs AI assignment |
| Loot | Killable NPCs with no loot tables |
| Auras | Invalid spell references |
| Spawn times | Abnormal respawn timers |
| Movement | Wander distance vs movement type consistency |
| + 10 more | Addon orphans, quest orphans, spells, scripts, map/zone validity, etc. |

### 3.2 Three-Batch Fix Results (23,904 operations)

**Batch 1 — Core Data Corrections:**

| Fix | Count | Details |
|-----|-------|---------|
| Duplicate spawns removed | 4,867 | Phase-aware detection preserved 4,409 intentional variants |
| Faction corrections | 4,045 | 11 categories from Wago DB2 — hostile mobs made passive, alliance/horde alignment |
| SmartAI orphan cleanup | 5,550 | AIName='SmartAI' with no actual scripts — cleared |
| Waypoint orphan fixes | 1,879 | Broken pathing switched to random movement |
| Gossip flag fixes | 1,541 | NPCs with gossip menus but missing GOSSIP flag |
| Classification fixes | 1,225 | Elite/Rare/Boss from Wago DB2 |
| Creature type fixes | 574 | Humanoid/Beast/Undead corrections |
| Trainer flag fixes | 142 | Missing TRAINER flag on trainers |
| Title fixes | 82 | Missing/wrong NPC subtitles |
| Family fixes | 67 | Creature family mismatches |
| Vendor flag fixes | 16 | Missing VENDOR flag on vendors |
| Unit class fixes | 7 | Invalid unit_class=0 → 1 |
| Invalid aura fixes | 222 | Removed references to deleted spells |

**Batch 2 — QA Pass:**

| Fix | Count | Details |
|-----|-------|---------|
| Placeholder NPCs despawned | 1,838 spawns | 399 [DNT]/[DND]/[PH] entries — invisible test NPCs |
| Vendor flag cleanup (spawned) | 631 | Had VENDOR flag but no items to sell |
| Vendor flag cleanup (unspawned) | 511 | Same, on template level |
| Name corrections | 23 | Broken spaces from CSV import, typos, dev artifacts |
| Service NPC movement fixes | 114 | Wandering vendors/trainers set stationary |
| Gossip orphan fixes | 9 | GOSSIP flag with no menu |

**Batch 3 — Comprehensive QA:**

| Fix | Count | Details |
|-----|-------|---------|
| Addon orphan cleanup | 865 | Dead creature_addon rows with no matching spawn |
| Vendor spawn time normalization | 522 | 2-hour to 700-hour respawns → 5 minutes |
| Zero wander distance fixes | 313 | Random-movement NPCs stuck in place |
| Service NPC movement | 119 | More wandering vendors/trainers set stationary |
| Name corrections | 13 | Blizzard renames, Exile's Reach updates |
| Walk speed fixes | 8 | NPCs moving at 12-20x normal speed |
| Rare spawn timer fixes | 6 | 0-second respawns → 5 minutes |
| Scale fix | 1 | Invisible creature (scale 0 → 1) |
| Title placeholder | 1 | "T1" placeholder removed |

### 3.3 Wowhead Mega-Audit (54,571 operations)

Scraped **216,284 NPCs** from Wowhead's API and cross-referenced every one against the database in three tiers:

**Tier 1 — Wowhead Cross-Reference (19,024 fixes):**

| Fix | Count |
|-----|-------|
| Type & classification remapping | 6,781 |
| Level fixes (ContentTuningID corrections) | 6,548 across 3 priority tiers |
| NPC flag additions (vendor/trainer/FM/etc) | 2,265 |
| Safe type fixes (Giant, Aberration reclassification) | 2,292 |
| Subtitle/subname corrections | 516 (+243 false-positive reverts) |
| Name corrections | 379 |

**Tier 2 — Deep Validation (3,282 fixes):**

| Fix | Count |
|-----|-------|
| ContentTuningID corrections (wrong expansion tier) | 3,013 |
| Zone hierarchy fixes | 5 |
| Incorrect service flag removals | 21 |

**Tier 3 — DB2 + Internal Consistency (32,265 fixes):**

| Fix | Count |
|-----|-------|
| Orphaned waypoint paths + nodes | 31,924 |
| Invalid per-spawn model resets | 232 |
| Orphaned SmartAI scripts | 106 |
| Hostile-faction vendor fixes | 3 |

---
