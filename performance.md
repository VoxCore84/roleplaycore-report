---
title: Performance & Build Diff
nav_order: 6
---

## Part 7: MySQL & Server Performance

### 7.1 Server Startup: 3m24s -> 60s -> 17s

**Phase 1: MySQL & Config Tuning (3m24s → ~60s in Debug build)**

| Optimization | Impact |
|-------------|--------|
| `tmp_table_size` was 1,024 BYTES (not MB!) | All temp tables spilled to disk — fixed to 256M |
| Disabled unused features (locales, hotswap, AH bot) | Reduced initialization overhead |
| Thread tuning (World/Hotfix DB threads 4 → 8) | Parallel loading of large tables |
| Buffer pool warm restarts | No cold cache on restart |

**Phase 2: Build Configuration (60s → 17s)**

| Optimization | Impact |
|-------------|--------|
| Switched to RelWithDebInfo (`/O2 /Ob1` vs Debug `/Od`) | Compiler optimization — biggest single improvement |

### 7.2 MySQL Configuration

| Setting | Before | After | Why |
|---------|--------|-------|-----|
| innodb_buffer_pool_size | default | 16 GB | 128 GB RAM system, keeps all data cached |
| buffer_pool_instances | 1 | 8 | Parallel access to buffer pool |
| buffer_pool_dump/load | OFF | ON | Warm restarts |
| key_buffer_size | default | 8 MB | No MyISAM tables remain |
| skip-name-resolve | OFF | ON | Faster connections |
| slow_query_log | OFF | ON (2s) | Performance monitoring |
| tmp_table_size | 1,024 bytes | 256 MB | Critical fix |

### 7.3 worldserver.conf Optimization

| Setting | Change | Impact |
|---------|--------|--------|
| Eluna.CompatibilityMode | true → false | Was forcing single-threaded map updates, nullifying MapUpdate.Threads=4 |
| MapUpdate.Threads | (now effective) | 4 parallel map processing threads |
| MaxCoreStuckTime | 0 → 600 | Freeze watchdog re-enabled |
| SocketTimeOutTimeActive | 900s → 300s | Dead connections cleaned faster |
| WorldDatabase.WorkerThreads | 4 → 8 | Faster DB operations |
| HotfixDatabase.WorkerThreads | 4 → 8 | Faster hotfix loading |
| ThreadPool | 4 → 8 | More worker threads |

### 7.4 Hotfix Pipeline Crash Fix (Critical)

With 1.08M hotfix_data rows (966K unique push IDs), the server crashed on client connect — the monolithic `SMSG_HOTFIX_CONNECT` packet exceeded the ByteBuffer 100MB assertion.

**6 bugs fixed across 3 C++ files:**

| Bug | Severity | Fix |
|-----|----------|-----|
| No chunking of HotfixConnect response | CRITICAL | Chunked at 50MB via `unique_ptr<HotfixConnect>` rotation |
| 100MB ByteBuffer assert fires before compression | CRITICAL | Assert raised to 500MB |
| Memory doubling (HotfixContent + _worldPacket copies) | HIGH | Intermediate buffers released after serialization |
| Fixed 400KB growth steps (excessive reallocation) | MEDIUM | Exponential growth (doubles capacity, capped 32MB step) |
| No cap on hotfix request count | MEDIUM | 1M request cap with warning log |

Relevant to any TC server running large hotfix datasets. Without it, 1M+ hotfix_data rows crash the server.

> **Post-audit update**: The redundancy audit ([Part 13](hotfix-audit)) reduced hotfix content tables from ~10.8M to ~244K rows and hotfix_data from 1.08M to ~835K entries. The chunked delivery system remains as a safety net, but the payload is now well within original limits.

### 7.5 Memory Leak Fixes

Fixed memory leaks in the Visual Effects system (`EffectsHandler`):
- `RemoveEffect` now properly deletes `EffectData*` before removal
- `Reset` deletes data before clearing the container
- `GetUnitInfo` deletes on invalid unit lookup
- Dead `Clear()` method removed

### 7.6 Build System

Build parallelism increased from `-j4` to `-j20` across all build configurations, leveraging the full 24-thread CPU.

---

## Part 8: Build Diff Audit (5 Builds)

### 8.1 Scope

Diffed all Wago DB2 CSV data across 5 consecutive WoW 12.0.1 builds:
**66044 → 66102 → 66192 → 66198 → 66220**

39 priority tables compared. Cross-referenced against live MySQL databases.

### 8.2 Key Discovery: Wago Export Oscillation

Wago.tools CSV exports oscillate wildly between builds for certain tables:
- SpellEffect: 269K-608K rows
- ItemSparse: 125K-171K

This is an **export artifact**, not actual content changes. Oscillation detection built into the diff tooling.

### 8.3 Actual Content Changes (66044 -> 66220)

| Category | Changes |
|----------|---------|
| Spells | +77 new, -1 removed, ~288 attribute mods |
| Items | +17 new (mounts, titles, toys), ~308 modifications |
| Quests | +9 new |
| Achievements | +5 new (Slayer's Rise PvP) |
| Creatures | +1 new display, 5 tweaks |
| Currencies | +1 new, Honor cap 15K → 4K |

### 8.4 Scripted Spell Safety

40 spells with C++ script bindings got new SpellEffect entries. **All safe** — new effects appended at higher indices (3, 4, 5+), never replacing existing 0/1/2. Verified in source: `SpellInfo.cpp:1298` uses explicit index-based assignment.

Zero breaking changes across all 5 builds.

---
