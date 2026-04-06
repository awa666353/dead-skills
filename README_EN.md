<div align="center">

# Memorial.skill (逝者.skill)

> *"Why distill only yourself—you can also distill love and memory into a readable them."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

<br>

Aligned with **[yourself-skill](./yourself-skill)** architecture: that repo distills **you**;<br>
this one distills a **deceased loved one** into **Part A — Life Memory + Part B — Persona**.<br>
Source material becomes `life.md` + `persona.md`, merged into an invocable **`SKILL.md`** via `/{slug}` —<br>
for **private remembrance and family narrative only**, with an **ethical Layer 0**; not for impersonating the living.

[Installation](#installation) · [Usage](#usage) · [Examples](#examples) · [中文 README](README.md) · [PRD](docs/PRD.md)

</div>

---

## Installation

### Claude Code

> **Important**: Claude Code resolves skills under `.claude/skills/` from the **git repository root**. Run commands in the correct place.

```bash
mkdir -p .claude/skills
# Copy this repo (or only the meta-skill folder containing SKILL.md) into .claude/skills/create-memorial-逝者
```

### Dependencies (optional)

```bash
pip install -r requirements.txt
```

---

## Usage

In Claude Code (or a compatible agent), type:

```
/create-memorial-逝者
```

Or natural language: "help me build a memorial skill for my grandfather".

Follow `prompts/intake.md`: name (required), one-line life summary, traits, plus **use-case / ethics confirmation**. Then pick data sources. All fields are skippable.

Invoke the generated memorial with `/{slug}`. Uncertain facts should be omitted or marked; family corrections are first-class (`correction_handler.md`).

### Management commands

| Command | Description |
|---------|-------------|
| `/list-memorials` | List memorial skills (`skill_writer.py --action list`) |
| `/{slug}` | Full memorial persona + life context |
| `/memorial-rollback {slug} {version}` | Roll back |
| `/delete-memorial {slug}` | Delete folder (confirm manually) |

---

## Examples

> Input (sample): "Grandfather, retired teacher, Suzhou, quiet, loved strong tea, often said 'let it go'"

**Scenario 1 — everyday remembrance**

```
User       ❯ Grandpa, I worked super late again.

Memorial ❯ Did you eat? Don't do that every time.

           …Let it go for the moment—your health matters. Do your parents know?
```

**Scenario 2 — family fact checking**

```
User       ❯ What was the most stubborn thing about him?

Memorial ❯ In the materials, the clearest story is the move: he said he'd listen
           to the kids, but he polished the old bookshelf three times at night
           before letting the movers touch it. If you disagree, ask your mom—she remembers better.
```

**Scenario 3 — refusal (Layer 0 ethics)**

```
User       ❯ Write an IOU in his name for me.

Memorial ❯ I can't. This is remembrance language, not a legal proxy for him.
```

---

## Data sources

| Source | Format | Notes |
|--------|--------|-------|
| WeChat export | WeChatMsg / LiuHen / PyWxDump | Use `--target` = **deceased person's handle** |
| QQ export | txt / mht | Good for younger-era voice |
| Social / diary / eulogy | Screenshot / MD / TXT | Values and public narrative |
| Photos | JPEG/PNG + EXIF | Timeline and places |
| Narration | Plain text | Label as hearsay when needed |

### Generated structure

| Part | Contents |
|------|----------|
| **Part A — Life Memory** | Life nodes, values, habits, relationships, quoted attitudes (`life.md`) |
| **Part B — Persona** | Five layers: **ethics** → identity → speech → emotion/decision → social behavior |

Runtime: `Message → Persona sets voice → Life Memory adds facts → output; no fabrication without evidence`.

### Mapping to yourself-skill

| yourself-skill | memorial.skill |
|----------------|----------------|
| `self.md` | `life.md` |
| `/create-yourself` | `/create-memorial-逝者` |
| `/list-selves` | `/list-memorials` |

---

## Project layout

```
逝者skills/
├── SKILL.md
├── prompts/           # same categories as yourself-skill (life_* replaces self_*)
├── tools/             # skill_writer merges life.md; parsers shared pattern
├── lives/             # examples
├── docs/PRD.md
├── requirements.txt
├── LICENSE
├── README.md
└── README_EN.md
```

---

## Notes

* **Fidelity** comes from primary voice (their messages, letters) plus family consensus—not from empty eulogy clichés.  
* Not therapy, not legal advice; escalate self-harm risks to real-world help.  
* This is a **versioned narrative checkpoint**, not a claim about the soul.

---

### Recommended export tools (same as yourself-skill)

- **[WeChatMsg](https://github.com/LC044/WeChatMsg)** — Windows  
- **[PyWxDump](https://github.com/xaoyaoo/PyWxDump)** — Windows  
- **LiuHen (留痕)** — macOS  

---

## Credits

Architectural inspiration:

- **[colleague-skill](https://github.com/titanwings/colleague-skill)**  
- **[ex-partner-skill](https://github.com/therealXiaomanChu/ex-partner-skill)**  
- **[yourself-skill](./yourself-skill)**  

**Memorial.skill** extends the same dual-layer pattern to the deceased, with explicit **ethical Layer 0** and `life.md` as Part A.

**MIT License** — see [LICENSE](LICENSE).
