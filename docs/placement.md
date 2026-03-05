
## Part 9: Placement Audits

### 9.1 Creature Placement (vs LoreWalkerTDB)

Compared 680K LW creature spawns against our 652K:

| Finding | Count |
|---------|-------|
| Missing creature spawns | 21,771 |
| Misplaced creatures | 38 |
| Property mismatches | 3,178 |
| SQL fixes generated | 24,681 |

### 9.2 GameObject Placement (vs LoreWalkerTDB)

Compared 194K LW gameobject spawns against our 174K:

| Finding | Count |
|---------|-------|
| Missing GO spawns | 5,837 |
| Misplaced GOs | 9 |
| Property mismatches | 1,625 |
| SQL fixes generated | 6,767 |

### 9.3 Status

Placement SQL fixes have been **generated but not yet applied** — requires manual review. The rotation "mismatches" (135 total) were all LW using `(0,0,0,0)` quaternion vs our correct `(0,0,0,1)` identity quaternion. Our data is correct — LW's zero quaternion is mathematically invalid.

---
