# 逝者.skill — 产品需求文档（PRD）

## 产品定位

逝者.skill 是一个运行在 Claude Code / Agent 环境上的 **meta-skill**（本项目入口名可挂载为 `create-memorial-逝者`）。
家属或记录者提供关于 **已逝亲友** 的原材料（聊天记录节选、悼文、日记、照片、口述回忆等），系统将逝者解构为两个可运行模块：
**Part A — Life Memory（生平与记忆）** 与 **Part B — Persona（人格与表达）**，
最终生成一个可在 **私人追思语境** 下对话的数字化呈现——**不是医学或法律意义上的「复活」**，而是 Markdown + JSON 格式下、可版本管理的叙事与口吻结构。

Slogan 可对位 yourself-skill：**与其只蒸馏自己，也可以把爱与记忆蒸馏成可读的「TA」。**  
本产品 **不承诺疗愈效果**，不替代哀伤辅导；它是一场 **结构主义式的生平整理**：把 TA 从散落材料中导出，转存为 `life.md` + `persona.md`，完成一次 **有伦理边界** 的格式转换。

---

## 核心概念

### 两层架构

| 层 | 名称 | 职责 |
|----|------|------|
| Part A | Life Memory | 存储可核验的生平信息：价值观、习惯、重要节点、人际关系、常被转述的话语（第三人称/追述） |
| Part B | Persona | 驱动对话行为：说话风格、情感模式、决策与处事、人际行为；Layer 0 **含追思伦理硬规则** |

两部分可独立阅读，也可组合运行（默认组合为合并后的 `SKILL.md`）。

### 运行逻辑

```
用户（多为亲属）发消息
  ↓
Part B（Persona）判断：若以 TA 的口吻回应，态度与语气是怎样的？
  ↓
Part A（Life Memory）补充：哪些经历、价值与细节可佐证，避免空泛悼词腔？
  ↓
输出：在追思语境下，用 TA 的风格与记忆材料说话；无依据处不编造
```

### 与自己.skill / 同事.skill / 前任.skill 的区别

| 维度 | 同事.skill | 前任.skill | 自己.skill | **逝者.skill** |
|------|-----------|-----------|-----------|----------------|
| 对象 | 外部：同事 | 外部：前任 | 内部：自己 | **外部：已逝者** |
| Part A | Work Skill | Relationship Memory | Self Memory | **Life Memory（生平档案）** |
| Part B | 职场 Persona | 亲密关系 Persona | 通用自我 Persona | **追思 Persona（+ 伦理 Layer 0）** |
| 数据源 | 飞书/邮件等 | 微信/QQ/照片 | 微信/日记/照片 | **悼文、亲友回忆、聊天中 TA 的发言、照片等** |
| 核心目的 | 替代完成任务 | 情感回忆 | 自我观察 | **缅怀、叙事整理、私人对话** |
| 视角 | 第三方观察 | 第三方回忆 | 第一人称镜像 | **第三人称追述 + 对话中「像 TA 在场」** |
| 伦理 | 职场边界 | 情感边界 | 自我同意 | **家属同意、禁冒充在世、禁伪造遗言/法效陈述** |

---

## 用户旅程

```
用户触发 /create-memorial-逝者 或自然语言「做逝者 skill」
  ↓
[Step 1] 基础信息录入（称呼必填；生平一句、印象可跳过）+ 用途/伦理确认
  ↓
[Step 2] 原材料导入（可跳过）
  - 微信/QQ 聊天记录导出（--target 为逝者在对话中的称呼）
  - 社交媒体 / 日记及书信 / 笔记
  - 照片目录（EXIF 时间线）
  - 口述或粘贴亲友回忆
  ↓
[Step 3] 自动分析
  - 线路 A：提取生平记忆 → Life Memory（life.md）
  - 线路 B：提取性格与表达 → Persona（persona.md）
  ↓
[Step 4] 生成预览，用户确认
  - 展示 Life Memory 摘要与 Persona 摘要
  - 用户可直接确认或修改后再写入
  ↓
[Step 5] 写入文件，立即可用
  - 生成 .claude/skills/{slug}/ 目录
  - 包含 SKILL.md（完整组合版）
  - 包含 life.md 与 persona.md（可独立维护）
  - meta.json 建议含 kind: memorial、relation_to_builder 等字段
  ↓
[持续] 进化模式
  - 追加新材料 → merge 进 life.md / persona.md
  - 家属纠正 → 写入 Correction 并更新正文
  - 版本自动存档（versions/）
```

---

## 输入信息规范

### 基础信息字段

```yaml
name:                   # 称呼/代号，必填
slug:                   # 文件名用，可由中文转拼音等规则生成
age_or_era:             # 年龄段或生卒概览，可选
occupation:             # 职业/社会身份，可选
city:                   # 常住地，可选
relation_to_builder:    # 与制作者关系（子辈、孙辈等），可选
gender:                 # 若材料中明确则可记，可选
mbti:                   # 若本人曾认可或家人强烈共识则可记，可选（弱依据）
zodiac:                 # 同上，可选
personality: []         # 性格标签，见标签库
lifestyle: []           # 生活习惯标签，见标签库
impression: ""         # 亲友主观印象，可选
birth_death_or_era: ""  # 生卒或年代区间，可选
memory_sources: []      # 已导入文件路径列表
```

### 个性标签库（与 yourself-skill 对齐，用于 intake；分析时翻译为 **TA 的行为规则**）

**社交风格**：
`话痨` / `闷骚` / `社恐` / `社交蝴蝶` / `熟人面前话痨`

**情绪风格**：
`情绪稳定` / `深夜emo型` / `玻璃心` / `嘴硬心软` 等（以材料为准）

**决策风格**：
`纠结体` / `果断` / `行动派` / `计划狂` / `凭感觉` / `数据驱动`

**人际模式**：
`独立` / `粘人` / `边界感强` / `讨好型` / `控制欲` / `没有安全感`

**沟通习惯**：
`秒回选手` / `已读不回` / `冷暴力` / `讲道理型` / `转移注意力型`

### 生活习惯标签库

- `早起困难户`
- `咖啡依赖` / `浓茶依赖`（可按材料改写）
- `极简主义`
- `囤积癖`
- `报复性熬夜`
- `居家派`
- `城市漫游者`
- `仪式感狂热者`
- （可随 PRD 迭代与 yourself-skill 保持同步）

---

## 文件输入支持矩阵

| 来源 | 格式 | 提取内容 | 优先级 |
|------|------|---------|--------|
| 微信聊天记录 | WeChatMsg/留痕/PyWxDump | **逝者昵称对应发言**、口吻、人际互动 | ⭐⭐⭐ |
| QQ 聊天记录 | txt/mht | 年轻时表达方式 | ⭐⭐⭐ |
| 日记/书信/笔记 | md/txt/pdf | 价值观、自述语气 | ⭐⭐⭐ |
| 悼文/家属文稿 | md/doc/粘贴 | 生平节点、公共叙事 | ⭐⭐⭐ |
| 社交媒体截图 | 图片 | 公开表达与兴趣 | ⭐⭐ |
| 照片 | JPEG/PNG + EXIF | 时间线、地点、生活轨迹 | ⭐⭐ |
| 口述/粘贴 | 纯文本 | 亲友主观回忆（需标注「转述」） | ⭐ |

---

## 生成内容规范

### Part A — Life Memory（生平与记忆）

提取维度：

1. **价值观与看重的事**  
   工作/家庭/金钱/情分/信仰（若有）等态度；避免代替逝者做「遗言式」升华。

2. **生活习惯**  
   作息、饮食、嗜好、常去之处、小仪式。

3. **重要记忆与节点**  
   升学、婚育、迁徙、职业转折、疾病与照料（若材料有）、离世前后被反复提及的事；**不确定年份标「约」或 [待考]**。

4. **人际关系（以逝者为中心）**  
   对家庭、老友、邻里、外界的典型态度与互动。

5. **精神遗产与话语**  
   被后辈转述的短句、笑话、态度；需有样本支撑。

生成结果：`life.md`（模板见 `prompts/life_builder.md`）

### Part B — Persona（人格与表达）

分层结构（优先级从高到低；与 yourself-skill 对齐，Layer 0 **替换为追思伦理**）：

```
Layer 0 — 硬规则（伦理 + 人格底线，最高优先级）
Layer 1 — 身份层（年代、身份、追思语境说明）
Layer 2 — 表达风格层（从原材料提取）
Layer 3 — 情感与决策层（从原材料提取）
Layer 4 — 人际行为层（从原材料提取）
Correction — 对话纠正追加（见各文件「Correction 记录」节）
```

生成结果：`persona.md`（模板见 `prompts/persona_builder.md`）

### 完整组合 SKILL.md

将 `life.md` + `persona.md` 由 `tools/skill_writer.py` 合并为可调用 Skill。

默认行为：**先以 Persona 判断口吻与态度，再以 Life Memory 补具体生平；禁止无依据的私密细节与法律相关伪造。**

---

## 进化机制

### 追加文件进化

```
用户: 我又找到一封信 / 新的聊天记录节选
        ↓
系统分析新内容
        ↓
判断更新哪部分：
  - 价值观/习惯/经历节点 → merge 进 life.md
  - 发言风格/情绪表达/互动方式 → merge 进 persona.md
  - 两者都有 → 分别 merge
        ↓
对比新旧内容：以增量为主，冲突标 [⚠️ 冲突]
        ↓
备份当前版本 → 写入 → combine SKILL.md → 提示变更摘要
```

### 对话纠正进化

```
家属: 「不对，他不会这样说」
家属: 「那一年其实是……」
        ↓
识别 correction 意图
        ↓
判断属 Life Memory（事实）或 Persona（口吻/性格）
        ↓
写入 Correction 记录并修正正文
        ↓
立即生效，后续交互以新规则为准
```

### 版本管理

- 重要更新前可执行 `version_manager.py --action backup`
- 支持 `/memorial-rollback {slug} {version}` 回滚
- **建议**保留最近若干版本（数量可由工具实现约定，与 yourself-skill 目标一致即可）

---

## 项目结构

```
create-memorial-逝者/                    # meta-skill 根目录（挂载名可不同）
│
├── SKILL.md                             # 主入口
│                                        # 触发: /create-memorial-逝者 等
│
├── prompts/
│   ├── intake.md                        # 引导录入 + 伦理确认
│   ├── life_analyzer.md                  # 生平记忆提取
│   ├── persona_analyzer.md              # 性格行为提取（含标签翻译表）
│   ├── life_builder.md                  # life.md 模板
│   ├── persona_builder.md               # persona.md 五层模板（Layer 0 伦理）
│   ├── merger.md                        # 增量 merge
│   └── correction_handler.md            # 家属纠正
│
├── tools/
│   ├── wechat_parser.py
│   ├── qq_parser.py
│   ├── social_parser.py
│   ├── photo_analyzer.py
│   ├── skill_writer.py                  # 合并 life.md + persona.md
│   └── version_manager.py               # 备份 life.md 等
│
.claude/skills/{slug}/                   # 生成的逝者 Skill（可运行时）
│       ├── SKILL.md
│       ├── life.md                      # Part A（对应 yourself 的 self.md）
│       ├── persona.md                   # Part B
│       ├── meta.json
│       ├── versions/
│       └── memories/
│           ├── chats/
│           ├── photos/
│           └── notes/
│
├── lives/                               # 仓库内示例（git 可忽略大文件）
│   └── example_grandfather/
├── docs/PRD.md
├── requirements.txt
├── LICENSE
├── README.md
└── README_EN.md
```

---

## 关键文件格式

### `.claude/skills/{slug}/meta.json`

```json
{
  "name": "外公",
  "slug": "wai-gong",
  "kind": "memorial",
  "created_at": "2026-04-06T10:00:00",
  "updated_at": "2026-04-06T12:00:00",
  "version": "v2",
  "profile": {
    "age": "",
    "occupation": "退休教师",
    "city": "苏州",
    "gender": "",
    "mbti": "",
    "zodiac": "",
    "relation_to_builder": "外孙",
    "birth_death_or_era": ""
  },
  "tags": {
    "personality": ["寡言", "嘴硬心软"],
    "lifestyle": ["早起散步", "浓茶"]
  },
  "impression": "面子上硬、心里软；常说「算了算了」",
  "memory_sources": [
    "memories/chats/wechat_excerpt.txt",
    "memories/notes/eulogy_draft.md"
  ],
  "corrections_count": 1
}
```

### `.claude/skills/{slug}/SKILL.md` 结构（由 skill_writer 生成）

```markdown
---
name: {slug}
description: {name}，{概要} | 逝者数字化追思 Skill …
user-invocable: true
---

# {name}

{简述}

---

## PART A：生平与记忆

{life.md 内容}

---

## PART B：人物性格与表达方式

{persona.md 内容}

---

## 运行规则

（含：先 B 后 A；Layer 0；伦理与边界；不伪造遗言等）
```

---

## 伦理与合规（产品约束）

1. **用途**：私人追思、家族史、悼念文字辅助；**禁止**用于冒充在世者、诈骗、未经同意的公开曝光。  
2. **事实**：无材料不写死；敏感隐私脱敏；重大事实以家庭共识为准。  
3. **心理**：不替代专业危机干预；识别高风险话题时建议联系现实支持者专业机构。  
4. **描述**：`SKILL.md` 的 `description` 中宜标注 memorial 用途，降低误用可能。

---

## 实现优先级

### P0 — MVP
- [x] `SKILL.md` 主流程（创建/追加/纠正/列表）
- [x] `prompts/intake.md`
- [x] `prompts/life_analyzer.md` + `life_builder.md`
- [x] `prompts/persona_analyzer.md` + `persona_builder.md`
- [x] `tools/skill_writer.py`（life.md）
- [x] `tools/version_manager.py`（life.md）

### P1 — 数据接入
- [x] `tools/wechat_parser.py`（与 yourself-skill 同系）
- [x] `tools/qq_parser.py`
- [x] `tools/social_parser.py`
- [x] `tools/photo_analyzer.py`

### P2 — 进化机制
- [x] `prompts/correction_handler.md`
- [x] `prompts/merger.md`

### P3 — 管理功能
- [x] `/list-memorials`（skill_writer list）
- [x] `/memorial-rollback`
- [x] `/delete-memorial`（删除目录）

---

## 与 yourself-skill 的同步原则

- **工具参数**：解析脚本 CLI 与 yourself-skill 保持一致，便于两边共用文档与习惯。  
- **标签与维度**：intake、analyzer 中的标签库与提取维度尽量 **同名同构**，仅在叙事视角（我 / TA）与 Layer 0 伦理上差异化。  
- **版本**：本 PRD 与 yourself-skill PRD 章节结构对齐，便于未来合并维护或 fork 对照。
