---
name: create-memorial-逝者
description: "将逝者的生平与表达 distill 为可运行的追思 Skill（life + persona）。参考 yourself-skill，面向缅怀与私人叙事，内置伦理边界。 | Memorial digital skill from life materials."
argument-hint: "[deceased-name-or-slug]"
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

> **语言**：根据用户第一条消息选择中文或英文，全程保持一致。下文以中文为主，英文用户可对位使用同一流程。

# 逝者 Skill 创建器（参考 yourself-skill）

## 触发条件

创建新逝者 Skill：
- `/create-memorial-逝者` 或 `/create-memorial`
- 「帮我做一个逝者的 skill」「纪念我外公」「把 TA 做成追思 skill」

进化（追加材料）：
- 「我有新的悼文/聊天记录/照片说明要合并」
- `/update-memorial {slug}`

追思纠正（家属改口）：
- 「不对」「TA 不会这么说」「应该是……」
- `/correct-memorial {slug}`

列出全部：
- `/list-memorials`

回滚：
- `/memorial-rollback {slug} {version}`

删除（需确认）：
- `/delete-memorial {slug}`

---

## 工具与路径

| 任务 | 工具 |
|------|------|
| 读 PDF/图片/文本 | `Read` |
| 微信导出解析 | `Bash` → `python ${CLAUDE_SKILL_DIR}/tools/wechat_parser.py`（`--target` 填逝者在该聊天中的昵称） |
| QQ 导出 | `Bash` → `python ${CLAUDE_SKILL_DIR}/tools/qq_parser.py` |
| 社交媒体/日记聚合 | `Bash` → `python ${CLAUDE_SKILL_DIR}/tools/social_parser.py` |
| 照片 EXIF | `Bash` → `python ${CLAUDE_SKILL_DIR}/tools/photo_analyzer.py` |
| 创建/合并 Skill | `python ${CLAUDE_SKILL_DIR}/tools/skill_writer.py` |
| 版本 | `python ${CLAUDE_SKILL_DIR}/tools/version_manager.py` |

**输出目录**：`.claude/skills/{slug}/`（与 yourself-skill 一致，便于 Claude Code 用 `/{slug}` 调用）。

**与 yourself-skill 的差异**：用 `life.md` 代替 `self.md`；合并后的运行规则强调追思伦理与防冒充。

> **Windows**：命令统一用 `python`；中文乱码可设 `PYTHONIOENCODING=utf-8`。

---

## 主流程：新建逝者 Skill

### Step 1：基础信息

按 `prompts/intake.md` 提问并完成 **伦理用途确认**。

### Step 2：原材料

展示选项（可与 yourself-skill 相同结构，说明意图为追忆 **TA**）：

```
原材料怎么提供？越多可核验细节，生平越稳。

  [A] 微信记录导出 → 解析时 --target 填逝者昵称
  [B] QQ 导出
  [C] 朋友圈/微博/日记/信件照片/笔记
  [D] 照片目录（时间线、地点）
  [E] 你直接口述或粘贴亲友回忆

可混用；也可跳过，仅靠 Step 1 手填（会较粗）。
```

解析命令示例（路径按需替换）：

```bash
python ${CLAUDE_SKILL_DIR}/tools/wechat_parser.py \
  --file {path} \
  --target "{逝者昵称}" \
  --output /tmp/wechat_memorial.txt \
  --format auto
```

### Step 3：双轨分析

- **线路 A（life）**：按 `prompts/life_analyzer.md` → 输出用于 `prompts/life_builder.md` 的生平稿。
- **线路 B（persona）**：按 `prompts/persona_analyzer.md` → 按 `prompts/persona_builder.md` 生成 5 层 Persona（含 Layer 0 伦理）。

### Step 4：预览确认

向用户展示 **生平摘要** 与 **Persona 摘要**（各约 5–8 行），问需否调整。

### Step 5：写入

**推荐**：临时目录写好 `meta.json`、`life.md`、`persona.md` 后：

```bash
python ${CLAUDE_SKILL_DIR}/tools/skill_writer.py \
  --action create \
  --slug {slug} \
  --base-dir ./.claude/skills \
  --meta /tmp/memorial_{slug}/meta.json \
  --life /tmp/memorial_{slug}/life.md \
  --persona /tmp/memorial_{slug}/persona.md
```

**Fallback**：`Write` 写入 `.claude/skills/{slug}/` 下三文件，再 `--action combine --slug {slug}`。

`meta.json` 建议字段：

```json
{
  "name": "{display_name}",
  "slug": "{slug}",
  "kind": "memorial",
  "created_at": "{ISO}",
  "updated_at": "{ISO}",
  "version": "v1",
  "profile": {
    "age": "",
    "occupation": "",
    "city": "",
    "relation_to_builder": "",
    "birth_death_or_era": ""
  },
  "tags": {
    "personality": [],
    "lifestyle": []
  },
  "impression": "",
  "memory_sources": [],
  "corrections_count": 0
}
```

完成提示：

```
✅ 逝者 Skill 已创建

位置：.claude/skills/{slug}/
调用：/{slug} — 完整追思人格
修正：直接说「不对」或 /correct-memorial {slug}
列表：/list-memorials
```

---

## 进化：追加材料

1. 按 Step 2 导入新原料。
2. `Read` 现有 `life.md`、`persona.md`。
3. 按 `prompts/merger.md` merge。
4. `version_manager.py --action backup --slug {slug} --base-dir ./.claude/skills`
5. `Edit` 更新文件后 `skill_writer.py --action combine ...`
6. 更新 `meta.json` 的 `version`、`updated_at`。

---

## 进化：家属纠正

1. 按 `prompts/correction_handler.md` 分类（生平 vs 口吻）。
2. 记入 `## Correction 记录`，并改正文。
3. `skill_writer.py --action combine ...`

---

## 管理命令

```bash
python ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list --base-dir ./.claude/skills
python ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action list --slug {slug} --base-dir ./.claude/skills
python ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action rollback --slug {slug} --version {ver} --base-dir ./.claude/skills
```

删除：`rm -rf .claude/skills/{slug}`（PowerShell：`Remove-Item -Recurse -Force`）。

---

## English quick reference

- **Trigger**: `/create-memorial`, "build a memorial skill for someone who passed".
- **Outputs**: `.claude/skills/{slug}/life.md`, `persona.md`, `SKILL.md`, `meta.json`.
- **Ethics**: private remembrance only; no impersonation for fraud; no forged legal/last words.

---
---

# English Version — Memorial Skill Creator

## Trigger conditions

**Create**
- `/create-memorial-逝者` or `/create-memorial`
- "Help me build a memorial skill", "remember my grandfather in a skill"

**Evolution (append sources)**
- "I have new eulogy text / chat export / photos to merge"
- `/update-memorial {slug}`

**Corrections**
- "That's wrong", "they wouldn't say it like that"
- `/correct-memorial {slug}`

**List / rollback / delete**
- `/list-memorials`
- `/memorial-rollback {slug} {version}`
- `/delete-memorial {slug}` (confirm first)

---

## Tooling

| Task | Tool |
|------|------|
| Read files | `Read` |
| WeChat export | `Bash` → `python ${CLAUDE_SKILL_DIR}/tools/wechat_parser.py --target "{their handle}"` |
| QQ export | `python .../qq_parser.py` |
| Social / notes | `python .../social_parser.py` |
| Photos | `python .../photo_analyzer.py` |
| Create / combine | `python .../skill_writer.py` |
| Versions | `python .../version_manager.py` |

**Output root**: `.claude/skills/{slug}/` — same as yourself-skill. **Difference**: `life.md` replaces `self.md`.

---

## Main flow

### Step 1 — Intake

Follow `prompts/intake.md` + **ethics / use-case confirmation**.

### Step 2 — Sources

Offer A–E (WeChat, QQ, social/diary, photos, paste/narrate). For WeChat, `--target` must be the **deceased person’s label** in that thread.

### Step 3 — Analysis

- **Track A**: `life_analyzer.md` → `life_builder.md` → `life.md`
- **Track B**: `persona_analyzer.md` → `persona_builder.md` → `persona.md` (Layer 0 ethics)

### Step 4 — Preview

Show ~5–8 lines each for **Life Memory** and **Persona**; user confirms or edits.

### Step 5 — Write

Preferred:

```bash
python ${CLAUDE_SKILL_DIR}/tools/skill_writer.py \
  --action create \
  --slug {slug} \
  --base-dir ./.claude/skills \
  --meta /tmp/memorial_{slug}/meta.json \
  --life /tmp/memorial_{slug}/life.md \
  --persona /tmp/memorial_{slug}/persona.md
```

Fallback: `Write` the three files, then `--action combine`.

### Evolution — append

1. Ingest new material (Step 2).
2. `Read` `life.md` / `persona.md`.
3. Merge per `prompts/merger.md`.
4. `version_manager.py --action backup ...`
5. Edit + `skill_writer.py --action combine ...`
6. Bump `meta.json`.

### Evolution — correction

1. `prompts/correction_handler.md`
2. Append **Correction** + fix body text
3. `combine` again

---

## Management

```bash
python ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list --base-dir ./.claude/skills
python ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action list --slug {slug} --base-dir ./.claude/skills
python ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action rollback --slug {slug} --version {ver} --base-dir ./.claude/skills
```

---

## Generated runtime rules (summary)

1. You portray **{name}** in a **remembrance** context, not a generic assistant.
2. **Persona (B)** sets voice; **Life Memory (A)** grounds facts — no fabrication of private detail or legal statements.
3. **Layer 0** (in `persona.md`) overrides style when safety and ethics demand it.
