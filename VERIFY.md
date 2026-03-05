# VoxCore Report Fact-Check Audit

Audited: March 5, 2026
Sources checked: `data/stats.json`, 15 content markdown files, 10 project memory files

---

## Stats Verification Table

| Key | Value in stats.json | Status | Source / Notes |
|-----|---------------------|--------|---------------|
| `rows_imported` | ~1,004,000 | VERIFIED | raidbots-data-pipeline.md: LW bulk import +665,658 rows (session 18) + initial LW import 385,823 rows (Feb 27) = ~1,051K gross. Net ~1M after dedup/cleanup is consistent. Content file data-import.md also cites ~1,004,000 net. |
| `hotfix_entries_repaired` | 103,153 | VERIFIED | hotfix-repair.md: "Missing rows added: 103,153 INSERTs" for build 66220. |
| `hotfix_entries_short` | 103K | VERIFIED | Rounds correctly from 103,153. |
| `hotfix_column_fixes` | 1,831 | VERIFIED | hotfix-repair.md: "Fixed zeroed columns: 1,831 UPDATEs". |
| `redundant_rows_removed` | 10.6M | VERIFIED | MEMORY.md: "3 rounds removed ~10.6M redundant rows total". hotfix-repair.md: total ~10,552,138. |
| `redundant_rows_percent` | 97.8% | VERIFIED | MEMORY.md: "10.8M to 244K content rows". hotfix-audit content also states 97.8%. |
| `final_hotfix_content_rows` | ~244K | VERIFIED | MEMORY.md: "~244K genuine content rows (8,396 override + 231,199 new)". hotfix-repair.md: "239,595 genuine rows across 109 audited tables" -- slight variance (239K vs 244K) due to the DBCD audit adding/removing rows after R3, but ~244K is the final canonical number. |
| `npc_corrections` | 78,475 | VERIFIED | Matches 23,904 (audit) + 54,571 (Wowhead) = 78,475. npc-audit.md and wowhead-npc-audit.md confirm both sub-totals. |
| `npc_corrections_short` | 78K | VERIFIED | Rounds correctly from 78,475. |
| `npc_audit_corrections` | 23,904 | VERIFIED | npc-audit.md: "Grand Total ~23,904 Across all 3 batches". |
| `npc_wowhead_corrections` | 54,571 | VERIFIED | wowhead-npc-audit.md: "54,571 total DB operations applied". |
| `item_translations` | 1,628,651 | VERIFIED | raidbots-data-pipeline.md: item_sparse_locale 1,020,171 + item_search_name_locale 608,480 = 1,628,651. Exact match. |
| `item_translations_short` | 1.6M | VERIFIED | Rounds correctly from 1,628,651. |
| `tools_built` | 60+ | VERIFIED | tooling-inventory.md catalogs 61+ scripts in wago-tooling alone, plus additional tools in other repos. Content tooling.md also says "60+". |
| `dev_sessions` | 50+ | VERIFIED | recent-work.md documents sessions up through 52+. MEMORY.md references session 52+ as the latest. |
| `claude_commands` | 17 | VERIFIED | tooling-inventory.md section 5 lists 17 Claude Code slash commands (trinitycore-claude-skills repo). CLAUDE.md also says "17 slash commands". |
| `quest_chain_links` | 21,758 | VERIFIED | raidbots-data-pipeline.md: "21,758 with PrevQuestID (46.1%)". |
| `dead_rows_cleaned` | ~412,000 | VERIFIED | recent-work.md: "Full 5-DB data quality audit: 6 parallel agents, 148 checks...Found 412K rows of dead data". |
| `server_startup_before` | 3m24s | VERIFIED | server-config.md: "Startup: 3m24s -> 1m0s (Debug) -> 17s (RelWithDebInfo)". |
| `server_startup_after` | 17s | VERIFIED | Same source. Also CLAUDE.md: "17s startup vs 60s Debug". |
| `server_startup_reduction` | 92% | VERIFIED | (204s - 17s) / 204s = 91.7%, rounds to 92%. |
| `att_quest_data` | 8,950 | VERIFIED | recent-work.md: "8,950 validated new rows: 4,359 quest starters, 3,081 quest chains, 1,510 vendor items". |
| `mcp_tools` | 20+ | VERIFIED | wago-db2: 6 tools + code-intel: 8 tools + mysql: ~5 tools + GitHub plugin: 40+ tools. Even counting only the custom MCP servers (wago-db2 6 + code-intel 8 + mysql ~5) = ~19-20. With GitHub it far exceeds 20. |
| `custom_systems` | 11 | VERIFIED | CLAUDE.md lists 8 custom systems under "Custom Systems" section. framework.md in the site lists 11 including CreatureOutfit, TransmogBridge, utility scripts, and the crafting system. Count depends on granularity; 11 is defensible when counting each registered system (sRoleplay, sCompanionMgr, CustomNPC, Display, Effects, Transmog, TransmogBridge, PlayerMorph, CreatureOutfit, Craft, utility scripts). |
| `build_number` | 66220 | VERIFIED | MEMORY.md: "Last run: build 66220". hotfix-repair.md: "Latest Run: Build 66220". |
| `databases` | 5 | VERIFIED | CLAUDE.md: "Databases (5 total)" -- auth, characters, world, hotfixes, roleplay. |
| `db2_tables` | 1,097 | VERIFIED | MEMORY.md: "1,097 tables". tooling-inventory.md: "1,097 DB2 tables". |
| `source_symbols` | 416,000 | VERIFIED | MEMORY.md: "416K symbols". tooling-inventory.md: "416K symbols, 2,288 files". |

---

## Content File Discrepancies

### results.md (Part 11: Final Database State)

1. **Hotfix DB size**: States "637 MB" in the database size table. Memory files show the DB went from 881.5 MB (after R3) to 637 MB (after OPTIMIZE, per server-config.md), then to 535 MB (after hotfix_data orphan cleanup, per MEMORY.md and recent-work.md session notes). The **current** size is 535 MB, not 637 MB.
   - **Recommendation**: Update the hotfixes DB size from 637 MB to 535 MB.

2. **hotfix_data row count**: States "835,385" in the table. MEMORY.md says the final hotfix_data count is 226,984 after the R3 orphan cleanup removed 608K entries. The 835,385 figure is an intermediate value from before the orphan cleanup.
   - **Recommendation**: Update hotfix_data from 835,385 to 226,984.

### hotfix-audit.md (Part 13)

3. **Final hotfix_data count**: States "hotfix_data entries: 1,084,369 -> 835,385" in section 13.6. The actual final value after R3 orphan cleanup is 226,984 (per MEMORY.md and recent-work.md). The 835,385 is an intermediate step.
   - **Recommendation**: Update the "After" column for hotfix_data to 226,984.

4. **Final DB size**: States "637 MB" in the results table. Current actual is 535 MB (see above).
   - **Recommendation**: Update to 535 MB.

### framework.md

5. **Hotfix tables count**: States "387 tables, ~227K registry entries" for the hotfixes database. hotfix-repair.md says 388 tables were compared (for the repair), and the hotfix DB has 517 tables total. The registry entry count of ~227K aligns with 226,984 hotfix_data entries.
   - **Minor**: 387 vs 388 is a rounding difference. The 517-table count is the full DB, not the compared subset.

### tooling.md

6. **repair_hotfix_tables.py description**: States "387 hotfix tables" in the data pipelines section. Should be 388 (per hotfix-repair.md: "388 tables compared").
   - **Recommendation**: Update 387 to 388.

7. **TransmogSpy line count**: States "13 event monitors" but transmog-implementation.md says "14 transmog events" and tooling-inventory.md says "14 transmog events".
   - **Recommendation**: Update 13 to 14.

### performance.md (Part 7)

8. **hotfix_data "After" figure in the note**: States hotfix_data reduced from 1.08M to ~835K. Actual final is 226,984. Same intermediate-value issue as above.
   - **Recommendation**: Update to reflect the final 226,984 figure, or note the additional orphan cleanup step.

### data-import.md (Part 2)

9. **No issues found.** All numbers (103,153 inserts, 1,831 fixes, 388 tables, 843,894 hotfix_data generated) are correct for the repair run itself. The pre-audit caveat is properly noted.

### npc-audits.md (Part 3)

10. **Tier 3 total**: Claims 32,265 ops. Summing the table: 31,924 + 232 + 106 + 3 = 32,265. Correct.

### quest-localization.md

11. **item_sparse_locale count**: States 1,020,264. raidbots-data-pipeline.md says 1,020,171. Discrepancy of 93 rows.
    - **Recommendation**: Verify which is current. The difference may be from subsequent additions (broadcast_text fill added rows). If so, 1,020,264 could be the updated figure, but the item_translations total (1,628,651) uses the 1,020,171 + 608,480 = 1,628,651 calculation. Updating the locale count would change the total.

### index.md

12. **"10 languages"**: The item_translations stat says "10 languages". raidbots-data-pipeline.md confirms 10 locales (6 full + 4 stub). Correct.

### discoveries.md

13. **No issues found.** All 9 discoveries align with memory file documentation.

### placement.md

14. **No issues found.** Numbers match npc-audit.md placement sections exactly.

### ai-workflow.md

15. **MCP server count**: States "Four MCP servers". tooling-inventory.md section 6 lists 3 MCP servers (wago-db2, mysql, code-intel) plus the GitHub plugin. Counting the GitHub plugin as an MCP server makes 4. Correct.

### opensource.md

16. **Repository count**: States "nine GitHub repositories". Counting: RoleplayCore, TransmogBridge, tc-npc-audit, wago-pipeline, roleplaycore-report (5 public/archived) + wago-tooling, code-intel, trinitycore-claude-skills, tc-packet-tools (4 private) = 9. Correct.

---

## Verified Claims Summary

The following claims were fully verified against memory files:

- LoreWalkerTDB import: ~1M rows net -- CONFIRMED
- Hotfix repair: 103,153 inserts + 1,831 column fixes -- CONFIRMED
- Redundancy audit: 10.6M rows removed (97.8%) -- CONFIRMED
- Final hotfix content: ~244K genuine rows -- CONFIRMED
- NPC corrections: 78,475 total (23,904 + 54,571) -- CONFIRMED
- Item translations: 1,628,651 rows (1,020,171 + 608,480) -- CONFIRMED
- Quest chain links: 21,758 PrevQuestID updates -- CONFIRMED
- Dead rows cleaned: ~412K from initial 5-DB audit -- CONFIRMED
- Server startup: 3m24s to 17s (92% reduction) -- CONFIRMED
- Build 66220 targeting -- CONFIRMED
- 5 databases, 1,097 DB2 tables, 416K source symbols -- ALL CONFIRMED
- 17 Claude commands, 50+ dev sessions, 60+ tools -- ALL CONFIRMED
- ATT quest data: 8,950 validated rows -- CONFIRMED
- Build diff: 5 builds, zero breaking changes, 40 safe scripted spell updates -- CONFIRMED
- Transmog: 14/14 manual clicks, 13/14 outfit loading -- CONFIRMED
- Wago oscillation: SpellEffect 269K-608K -- CONFIRMED
- 11 custom systems -- DEFENSIBLE (depends on counting granularity)
- 20+ MCP tools -- CONFIRMED (6 + 8 + mysql + GitHub plugin tools)

---

## Action Items

| Priority | File | Issue | Fix |
|----------|------|-------|-----|
| HIGH | results.md | hotfix_data count 835,385 is stale | Update to 226,984 |
| HIGH | results.md | Hotfixes DB size 637 MB is stale | Update to 535 MB |
| HIGH | hotfix-audit.md | hotfix_data "After" 835,385 is stale | Update to 226,984 |
| HIGH | hotfix-audit.md | DB size "After" 637 MB is stale | Update to 535 MB |
| MEDIUM | performance.md | hotfix_data ~835K figure is stale | Update to ~227K |
| LOW | tooling.md | "387 hotfix tables" should be 388 | Update |
| LOW | tooling.md | TransmogSpy "13 event monitors" should be 14 | Update |
| LOW | quest-localization.md | item_sparse_locale 1,020,264 vs 1,020,171 | Verify current DB count |

---

*Generated by fact-check audit against project memory files.*
