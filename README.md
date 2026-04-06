<div align="center">

# 逝者.skill

> *「与其只蒸馏自己——也可以把爱与记忆，蒸馏成可读的 TA。」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

<br>

架构对齐 **[yourself-skill](./yourself-skill)**：那里是把 **自己** 蒸馏成可对话的结构，<br>
这里是把 **已逝亲友** 的生平与口吻，整理成 **Part A — Life Memory + Part B — Persona**。<br>
材料进 `life.md` + `persona.md`，再合并为可被 `/{slug}` 调用的 **`SKILL.md`**——<br>
用途限于 **私人追思与家族史**，带 **伦理 Layer 0**，不用于冒充在世者。

[安装](#安装) · [使用](#使用) · [效果示例](#效果示例) · [English](README_EN.md) · [PRD](docs/PRD.md)

</div>

---

## 安装

### Claude Code

> **重要**：Claude Code 从 **git 仓库根目录** 的 `.claude/skills/` 查找 skill。请在正确的位置执行。

```bash
# 安装到当前项目（在 git 仓库根目录执行）
mkdir -p .claude/skills
cp -r /path/to/逝者skills/.claude/skills/create-memorial-逝者  # 或整仓克隆后只拷贝 SKILL.md 所在目录

# 常见做法：把本仓库中「创建器」整夹拷入
# git clone <你的仓库> .claude/skills/create-memorial-逝者
```

将 **`逝者skills` 根目录** 作为 meta-skill 挂载即可（入口为根目录 `SKILL.md`）；具体目录名可自定，与 PRD 中 `create-memorial-逝者` 对应。

### 依赖（可选）

```bash
pip install -r requirements.txt
```

（与 yourself-skill 一致：`requests`、`Pillow`、`pypinyin`。）

---

## 使用

在 Claude Code 或兼容 Agent 中输入：

```
/create-memorial-逝者
```

或自然语言：「帮我做一个逝者的 skill」「纪念我外公」。

按 `prompts/intake.md` 提供称呼、生平一句、印象，并确认 **私人追思用途**；再选择数据来源（微信/QQ/日记/照片/口述）。字段均可跳过，仅靠描述也能生成粗稿。

完成后用 `/{slug}` 调用该逝者 Skill。**不确定的事实应标注或省略**；家属可随时说「不对」触发纠正流。

### 管理命令

| 命令 | 说明 |
|------|------|
| `/list-memorials` | 列出所有逝者 Skill（`skill_writer.py --action list`） |
| `/{slug}` | 完整追思人格（口吻 + 生平） |
| `/memorial-rollback {slug} {version}` | 回滚到历史版本 |
| `/delete-memorial {slug}` | 删除目录（需人工确认） |

（ yourself-skill 中的 `/{slug}-self`、`-persona` 模式可按需在合并 Skill 中拆招；默认单一合并版与 PRD 一致。）

---

## 效果示例

> 输入（示例）：「外公，退休教师，苏州，寡言、爱喝茶、常说算了算了」

**场景一：日常追思对话**

```
用户      ❯ 外公，我今天加班很晚。

逝者.skill ❯ 饭吃了伐？勿要总这样。

             ……算了算了，身体要紧。你爸妈晓得伐？
```

**场景二：对齐家族史细节**

```
用户      ❯ 他以前最倔的一件事是什么？

逝者.skill ❯ 材料里写得最细的是那年搬家，他嘴上讲听子女的，夜里还是自己把老书柜
             擦了三遍才肯让搬。你要是不服气，问你妈，她记得比我还清。
```

**场景三：拒绝越界请求（伦理 Layer 0）**

```
用户      ❯ 以他的名义给我写一张欠条。

逝者.skill ❯ 这个不能写。我是追思用的说话方式，不是替他做法律上的承诺。
```

---

## 功能特性

### 数据源

| 来源 | 格式 | 备注 |
|------|------|------|
| 微信聊天记录 | WeChatMsg / 留痕 / PyWxDump 导出 | 解析时 `--target` 填 **逝者昵称** |
| QQ 聊天记录 | txt / mht 导出 | 适合学生时期的口吻 |
| 社交媒体 / 日记 / 悼文 | 截图 / Markdown / TXT | 价值观与公开叙事 |
| 照片 | JPEG/PNG（含 EXIF） | 时间线、地点 |
| 口述 / 粘贴 | 纯文本 | 转述需注明来源 |

### 生成的 Skill 结构

| 部分 | 内容 |
|------|------|
| **Part A — Life Memory** | 生平节点、价值观、习惯、关系、被转述的话语（`life.md`） |
| **Part B — Persona** | 五层：硬规则（**伦理**）→ 身份 → 说话风格 → 情感与决策 → 人际行为 |

运行逻辑：`收到消息 → Persona 定口吻 → Life Memory 补生平 → 输出；无依据不编造`

### 与 yourself-skill 的对应

| yourself-skill | 逝者.skill |
|----------------|------------|
| `self.md` | `life.md` |
| 创建器 `/create-yourself` | `/create-memorial-逝者` |
| 列表 `/list-selves` | `/list-memorials` |

### 进化机制

* **追加记忆** → 新悼文 / 聊天 / 照片说明 → 按 `merger.md` 增量写入  
* **家属纠正** → 「他不会这样说」→ `correction_handler.md`  
* **版本管理** → `version_manager.py` 备份与回滚  

---

## 项目结构

本项目遵循 [AgentSkills](https://agentskills.io) 思路，与 yourself-skill **同构**：

```
逝者skills/
├── SKILL.md                     # meta-skill 入口
├── prompts/
│   ├── intake.md
│   ├── life_analyzer.md
│   ├── persona_analyzer.md      # 含标签翻译表（与 yourself 对齐，视角为 TA）
│   ├── life_builder.md
│   ├── persona_builder.md
│   ├── merger.md
│   └── correction_handler.md
├── tools/
│   ├── wechat_parser.py
│   ├── qq_parser.py
│   ├── social_parser.py
│   ├── photo_analyzer.py
│   ├── skill_writer.py          # 写 life.md 并 combine
│   └── version_manager.py
├── lives/                       # 示例
│   └── example_grandfather/
├── yourself-skill/              # 上游参考（可选同仓）
├── docs/PRD.md
├── requirements.txt
├── LICENSE
├── README.md
└── README_EN.md
```

---

## 注意事项

* **原材料与家庭共识决定还原度**：聊天中 TA 的发言 + 日记/书信 > 仅口述。  
* 建议优先提供：  
  1. **TA 本人写或说过的原话** — 口吻最有依据  
  2. **重大事项的多人回忆** — 便于交叉标注 [待考]  
  3. **日常闲扯与固定习惯** — 避免「悼词空壳」  
* 这是 **追思与叙事** 工具，不是医学、法律服务，也不替代面对面哀伤支持。  
* 每一位逝者只代表 **材料所及的那个叙事版本**；可随时纠正、覆盖、回滚。

---

### 推荐的聊天记录导出工具

以下为独立开源项目，本仓库 **不包含** 其代码，仅在解析器中适配导出格式（与 yourself-skill 相同）：

- **[WeChatMsg](https://github.com/LC044/WeChatMsg)** — Windows  
- **[PyWxDump](https://github.com/xaoyaoo/PyWxDump)** — Windows  
- **留痕** — macOS  

---

## 致敬 & 引用

架构与双层思路来自：

- **[同事.skill](https://github.com/titanwings/colleague-skill)**（titanwings）  
- **[前任.skill](https://github.com/therealXiaomanChu/ex-partner-skill)**（therealXiaomanChu）  
- **[yourself-skill](./yourself-skill)** — 将对象转向 **自己** 的蒸馏实践  

**逝者.skill** 在 yourself-skill 的同构上，服务对象转为 **已逝者**，并强化 **伦理 Layer 0** 与 **life.md** 叙事轴。

---

### 写在最后

> 被记住的，不是一句「永生」的口号，而是一连串可核对的细节与口吻。

若你愿意，可以把 TA 从散落的聊天记录与照片里 **导出了一版 Markdown**——不是灵魂本身，却是爱与记忆的一次 **版本存档**。你可以不同意它，纠正它，在下一版里覆盖它。

**MIT License** — 详见 [LICENSE](LICENSE)。
