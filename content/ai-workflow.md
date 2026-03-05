# AI Workflow

VoxCore is developed with Claude Code — an AI-powered workflow where the AI has direct access to the database, the codebase, the game data files, and the build system. Four MCP servers, 17 custom slash commands, and a parallel agent architecture turn a single developer into a team.

## MCP Servers

Model Context Protocol servers give Claude direct tool access to external systems. Each runs as a subprocess with native tool integration.

### MySQL

Direct read/write access to all five databases. Every query, audit, and fix runs through this connection.

### Wago DB2

1,097 game data tables from Wago.tools, searchable in natural language. Replaces manual CSV grep for spell, item, creature, and content tuning lookups. Six query tools: search, lookup, describe, query, validate, and table listing.

### Code Intelligence

Hybrid ctags + clangd server. 416,000 symbols across 2,288 source files. Instant symbol lookup for 95% of queries via ctags; precision type analysis, class hierarchy, and call hierarchy on demand via clangd.

| Tier | Tools | Speed |
|---|---|---|
| ctags | find_definition, find_references, list_symbols, search_symbol | ~ms |
| clangd | hover_info, class_hierarchy, call_hierarchy | seconds |

### GitHub

Full repository integration — PRs, issues, code search, reviews, and branch management via the `gh` CLI and MCP plugin.

---

## 17 Custom Skills

Slash commands that encode specific workflows as reusable prompts.

### Lookups

| Command | What it does |
|---|---|
| `/lookup-spell` | Search spells by name or ID from Wago DB2 |
| `/lookup-item` | Search items from ItemSparse |
| `/lookup-creature` | Search creatures from the world database |
| `/lookup-area` | Search zones and areas from AreaTable |
| `/lookup-faction` | Search faction templates |
| `/lookup-emote` | Search emotes |
| `/lookup-sound` | Validate SoundKit IDs |

### Build & Fix

| Command | What it does |
|---|---|
| `/build-loop` | Iterative build + auto-fix — up to 5 rounds of compile, read errors, fix, recompile |
| `/parse-errors` | Parse error log by category with counts |

### SQL & Database

| Command | What it does |
|---|---|
| `/apply-sql` | Run a SQL file against any of the 5 databases |
| `/new-sql-update` | Create a correctly-named incremental SQL update file |
| `/smartai-check` | Validate SmartAI SQL against known enums and deprecated types |

### Server & Debug

| Command | What it does |
|---|---|
| `/soap` | Send GM commands to the live server via SOAP |
| `/check-logs` | Parse server logs for errors, warnings, and patterns |
| `/parse-packet` | Map packet opcodes to TrinityCore handler functions |
| `/decode-pkt` | Decode binary .pkt capture files via WowPacketParser |

### Scaffolding

| Command | What it does |
|---|---|
| `/new-script` | Scaffold a new C++ script file and register it in the script loader |
| `/code-review` | Review a GitHub pull request |

---

## Parallel Agent Architecture

Claude spawns specialized agents for concurrent work. Each agent gets its own context window and operates independently.

| Agent Type | Access Level | Use Case |
|---|---|---|
| General-purpose | Full (edit, bash, search, write) | Multi-step implementation tasks |
| Explore | Read-only (fast) | Codebase research and tracing |
| Plan | Read-only | Architecture design before coding |

### Agent Teams

Coordinated groups sharing a task list. One agent leads, others work assigned subtasks in parallel. Used for large refactors, multi-file audits, and parallel data processing.

### Worktrees

Git worktree isolation for zero-risk experimentation. Created automatically, discardable on exit. Agents can run in worktree isolation independently.

---

## Development Methodology

A mandatory four-gate debugging pipeline enforced through project configuration:

1. **Collect Data** — Fan out parallel agents to read all relevant logs, query DB state, trace code paths. No hypothesis until data is collected.
2. **Analyze** — State hypothesis with explicit data citations. Every claim needs a log line, packet byte, DB row, or code path.
3. **Propose Fix** — One change at a time. Root cause only. Trace downstream callers before modifying any function.
4. **Verify** — Build, re-collect all data, confirm hypothesis matches. If not, back to gate 1.

---

## Workflows

### New Feature
Plan → Approve → Implement → `/build-loop` → `/check-logs` → Test in-game

### Bug Investigation
`/check-logs` → Trace with Code Intelligence → Fix → `/build-loop` → `/soap .reload`

### Large Parallel Task
Describe scope → Agents work subtasks concurrently → Results combined → Single commit

### Data Pipeline
`/lookup-*` → Generate SQL → `/smartai-check` → `/apply-sql` → `/soap .reload` → Verify in-game

---

## What This Produces

| Metric | Value |
|---|---|
| Development sessions | 55+ documented |
| Tools built | 65+ |
| Database corrections | 1M+ rows |
| Server startup improvement | 92% (3m24s → 17s) |
| Custom C++ systems | 11 registered |
| Claude Code commands | 17 custom skills |
| MCP server tools | 20+ |
