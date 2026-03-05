# The Framework

VoxCore is a TrinityCore fork targeting WoW 12.x / Midnight, built for roleplay. Eleven custom C++ systems transform stock GM debug tools into persistent, player-accessible features — morph, scale, visual effects, companion squads, custom NPCs, and a full transmog outfit system reverse-engineered from the 12.x client.

## Architecture

Built on C++20 with CMake and Ninja. The server compiles in two configurations: Debug for development and RelWithDebInfo for runtime, where startup drops from 60 seconds to 17.

| Component | Detail |
|---|---|
| Language | C++20 (structured bindings, `contains()`, `string_view`) |
| Build | CMake + Ninja, MSVC (Visual Studio 2022) |
| Scripting | Eluna Lua engine integrated |
| Runtime | 17-second startup (RelWithDebInfo) |
| Database | MySQL 8.0 — five databases |

All custom systems register through a single entry point (`custom_script_loader.cpp`) and share state through the `sRoleplay` singleton, backed by a dedicated fifth database.

---

## Five Databases

| Database | Purpose |
|---|---|
| `auth` | Accounts, RBAC permissions (custom range 1000+) |
| `characters` | Player data, inventories, companions, transmog outfits |
| `world` | Game world — creatures, items, spells, SmartAI, spawns |
| `hotfixes` | Client hotfix overrides (387 tables, ~227K registry entries) |
| `roleplay` | Custom: creature extras, custom NPCs, player morph, server settings |

---

## Custom Systems

### sRoleplay Singleton

The central custom system. Loads at world startup, manages creature extras, custom NPCs, and player extras across all other systems. Located at `src/server/game/RolePlay/`.

### Custom NPC System

Create fully customizable player-race NPCs from scratch — no pre-existing template required. Over 20 subcommands cover creation, equipment, appearance, and spawning.

- **Command:** `.cnpc` (alias: `.customnpc`)
- **Workflow:** `.cnpc add` → `.cnpc set` → `.cnpc equip` → `.cnpc spawn`

### Display System

Per-slot item appearance overrides. Any item visual on any equipment slot, no collection required, no NPC visit needed. Fourteen slots supported.

- **Command:** `.display <slot> <itemId>`

### Visual Effects

Persistent SpellVisualKit effects that survive relog and automatically sync to late-joining observers. Ten subcommands across self and target variants including persistent add, timed cast, channel beams, and toggle.

- **Command:** `.effect self|target add|cast|channel|toggle|remove|reset`

### Companion Squad

AI companion NPCs that follow and fight alongside you. Role-based AI with tank, healer, and DPS behaviors. Five seed companions across Warrior, Rogue, Hunter, Mage, and Priest classes.

- **Command:** `.comp`
- **Status:** In progress

### Transmog Outfits

Full wardrobe outfit handling for the 12.x client. Four CMSG packet parsers reverse-engineered from hex dumps. Fourteen of fourteen manual transmog clicks working, thirteen of fourteen outfit loads confirmed.

The critical discovery: all four outfit packets send the transmogrifier NPC's GUID, not the player's. This blocked all operations for over a day before being identified — the validation check silently rejected every request at DEBUG log level.

- **Slot mapping:** 15 slots including secondary shoulder
- **Spell effect 347:** `SPELL_EFFECT_EQUIP_TRANSMOG_OUTFIT`

### TransmogBridge Addon

Client addon that patches a serializer bug in the 12.x wardrobe system. The client omits head, main-hand, off-hand, and enchant slots from outfit update packets. TransmogBridge intercepts the incomplete data, merges it with a pre-snapshot of the full outfit state, and sends the corrected payload via addon messaging.

- **Three-layer hybrid merge** with stale detection and timing guarantees
- [View on GitHub](https://github.com/VoxCore84/TransmogBridge)

### Player Morph & Scale

Persistent morph and scale with auto-restore on login. The `.remorph` command has no stock equivalent — it re-applies morph and scale after mount, shapeshift, or death from in-memory cache without touching the database.

- **Commands:** `.wmorph`, `.wscale`, `.remorph`
- **RBAC:** Player-level permissions (no GM required)

### CreatureOutfit

NPC player-race appearance overlay. Used internally by the Custom NPC system to apply equipment and customization data to creature display models.

### Utility Scripts

Skyriding spell handling, toy item scripts, and social commands — barbershop anywhere, typing animation, group casting, and time control.

---

## RP vs Stock

Where stock TrinityCore provides temporary GM debug tools, VoxCore provides persistent, player-accessible roleplay features.

| Feature | Stock TrinityCore | VoxCore |
|---|---|---|
| **Morph** | `.morph` — GM only, lost on relog | `.wmorph` — Player, persistent, `.remorph` restore |
| **Scale** | `.modify scale` — GM, temporary | `.wscale` — Player, persistent |
| **Appearance** | Wardrobe UI, requires collection | `.display` — any item, anywhere |
| **Effects** | `.cast` — actual spell, gameplay impact | `.effect` — visual only, permanent, survives relog |
| **Barbershop** | Must visit NPC | `.barbershop` — opens UI anywhere |
| **Typing** | `/e types` — text only | `.typing` — actual animation |
| **Companions** | No equivalent | `.comp` — 5 squad slots, role-based AI |
| **Custom NPCs** | `.npc add` — needs existing template | `.cnpc` — creates from scratch, 20+ subcommands |

---

## In-Game Commands

### Morph & Scale

| Command | What it does | Persists |
|---|---|---|
| `.wmorph <displayId>` | Morph to creature model | Yes |
| `.wmorph 0` | Remove morph | — |
| `.wscale <0.1–10.0>` | Change visual scale | Yes |
| `.remorph` | Re-apply after mount/death | — |

### Display

`.display <slot> <itemId>` — override any slot's appearance. `.display <slot> 0` — clear.

**Slots:** head, shoulders, lshoulder, shirt, chest, waist, legs, feet, wrists, hands, back, tabard, mainhand, offhand

### Visual Effects

| Command | What it does |
|---|---|
| `.effect self add <kitId> [mode]` | Persistent SpellVisualKit |
| `.effect self cast <kitId> <dur>` | Timed cast visual |
| `.effect self channel <kitId>` | Channel beam to target |
| `.effect self toggle <kitId>` | Toggle on/off |
| `.effect self remove <kitId>` | Remove specific |
| `.effect self reset` | Remove all |

Target variants: `.effect target add|toggle|remove|reset`

### Companion Squad

| Command | What it does |
|---|---|
| `.comp roster` | List companions |
| `.comp set <slot> <name>` | Assign to slot |
| `.comp summon` / `.comp dismiss` | Summon or dismiss squad |
| `.comp mode` | Set behavior mode |

### Custom NPCs

| Command | What it does |
|---|---|
| `.cnpc add` | Create NPC (clones your character) |
| `.cnpc spawn` | Spawn persistently |
| `.cnpc equip armor/right/left <itemId>` | Set equipment |
| `.cnpc set race/gender/name/guild/scale` | Customize appearance |
| `.cnpc delete` | Remove targeted NPC |

### Social & Utility

| Command | What it does |
|---|---|
| `.barbershop` | Open barbershop anywhere |
| `.typing` | Play typing animation |
| `.castgroup <spellId>` | Cast on all group members |
| `.settime <h> <m>` | Freeze server time (GM) |
