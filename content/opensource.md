# Open Source

VoxCore's tooling is distributed across nine GitHub repositories and six public gists. Four repositories and all gists are public. The remaining five contain specialized tooling available on request.

## Public Repositories

### VoxCore84/RoleplayCore

The core server. TrinityCore fork targeting WoW 12.x / Midnight with eleven custom roleplay systems, five databases, and a fully integrated AI development workflow.

- **Language:** C++
- **Status:** Active
- [View on GitHub](https://github.com/VoxCore84/RoleplayCore)

### VoxCore84/TransmogBridge

Client addon that patches a serializer bug in the 12.x transmog outfit system. The WoW client omits four or more equipment slots from outfit update packets. TransmogBridge intercepts, merges with a pre-snapshot, and delivers the complete payload.

- **Language:** Lua
- **Status:** Active
- [View on GitHub](https://github.com/VoxCore84/TransmogBridge)

### VoxCore84/tc-npc-audit

NPC audit and validation toolkit. Twenty scripts cross-reference the TrinityCore world database against Wowhead and LoreWalkerTDB. Validates factions, display models, level ranges, equipment, zones, and flags. Produced 78,475 corrections.

- **Language:** Python
- **Status:** Archived (complete)
- [View on GitHub](https://github.com/VoxCore84/tc-npc-audit)

### VoxCore84/wago-pipeline

Data enrichment pipeline for importing and validating game data from Raidbots, Wago, and LoreWalkerTDB. Six scripts with an orchestrator handle item names, quest chains, quest POI, objectives, and Wowhead scraping.

- **Language:** Python
- **Status:** Archived (complete)
- [View on GitHub](https://github.com/VoxCore84/wago-pipeline)

### VoxCore84/roleplaycore-report

This website. A static site generator with Apple HIG aesthetic, built from Markdown sources by a Python script. Outputs to GitHub Pages.

- **Language:** Python
- **Status:** Active
- [View on GitHub](https://github.com/VoxCore84/roleplaycore-report)

---

## Additional Tooling

Five repositories contain specialized development tools.

| Repository | What it does | Language |
|---|---|---|
| Wago Tooling | 61+ scripts — DB2 downloader, hotfix repair, build differ, MCP server, redundancy audit | Python |
| Code Intelligence | Hybrid ctags + clangd MCP server — 416K symbols, 8 query tools | Python |
| Claude Skills | 17 custom slash commands — build automation, lookups, packet analysis, SmartAI validation | Markdown |
| Packet Tools | Server launcher wrapper, WPP auto-parse, packet grep, build updater | Shell |
| TC NPC Audit | 20 NPC validation scripts — model, faction, level, zone, flag cross-references | Python |

---

## Public Gists

| Gist | What it contains |
|---|---|
| [Operations Runbook](https://gist.github.com/VoxCore84/84656ef0960c699927e3a555e8248f7b) | Complete reference for every tool, pipeline, and command — 22 sections |
| [Session Changelog](https://gist.github.com/VoxCore84/4c63baf8154753d2a89475d9a4f5b2cc) | Chronological log of all 50+ development sessions with commit hashes |
| [Database Report](https://gist.github.com/VoxCore84/528e801b53f6c62ce2e5c2ffe7e63e29) | Full 16-part data quality and optimization report |
| [Open Issues](https://gist.github.com/VoxCore84/2b69757faa2a53172c7acb5bfa3ad3c4) | Prioritized issue tracker — HIGH / MEDIUM / LOW / DEFERRED |
| [Packet Tools](https://gist.github.com/VoxCore84/a86d3dc8c88839c5f8aafef5908a9d5f) | Opcode analyzer (991 lines) + transmog packet extractor (342 lines) |
| [Transmog Wiki](https://gist.github.com/VoxCore84/88ba6320d249b5758753ecb954b0ded2) | 189 functions, 23 events, 24 structures across 4 client API namespaces |

---

## Reference Tools

Local development tools used in the project:

| Tool | What it does |
|---|---|
| WowPacketParser | Packet capture decoder, locally patched for build 66220 |
| wow.tools.local | Self-hosted DB2/DBC browser for visual data inspection |
| LoreWalkerTDB | Community TrinityCore database — world data import source |
| DBC2CSV | DB2-to-CSV converter with 1,315 table definition files |
| TACTSharp | Blizzard CASC storage extraction library |
| DB2Query | Interactive DB2 query CLI |
| AllTheThings Database | Community item, quest, and NPC collection data (1,576 Lua files) |
| Lua Language Server | LSP for Eluna script and addon development |
| Ymir | Retail packet sniffer for build 66220 |

---

## Quick Start

```
# Clone the core server
git clone https://github.com/VoxCore84/RoleplayCore.git

# Install the transmog addon
git clone https://github.com/VoxCore84/TransmogBridge.git
# Copy to Interface/AddOns/TransmogBridge/

# Run NPC audits
git clone https://github.com/VoxCore84/tc-npc-audit.git
python npc_audit.py --all
```
