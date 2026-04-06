#!/usr/bin/env python3
"""逝者 Skill 文件管理器

基于 yourself-skill 的 skill_writer，将 self.md 换为 life.md（生平与记忆），用于追思场景。

Usage:
    python skill_writer.py --action <list|init|create|combine> --base-dir <path> [--slug <slug>]
"""

import argparse
import os
import sys
import json
from pathlib import Path
from datetime import datetime


def list_skills(base_dir: str):
    """列出所有已生成的逝者 Skill"""
    if not os.path.isdir(base_dir):
        print("还没有创建任何逝者 Skill。")
        return

    skills = []
    for slug in sorted(os.listdir(base_dir)):
        meta_path = os.path.join(base_dir, slug, "meta.json")
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            skills.append(
                {
                    "slug": slug,
                    "name": meta.get("name", slug),
                    "version": meta.get("version", "?"),
                    "updated_at": meta.get("updated_at", "?"),
                    "profile": meta.get("profile", {}),
                }
            )

    if not skills:
        print("还没有创建任何逝者 Skill。")
        return

    print(f"共 {len(skills)} 个逝者 Skill：\n")
    for s in skills:
        profile = s["profile"]
        desc_parts = [profile.get("occupation", ""), profile.get("city", "")]
        desc = " · ".join([p for p in desc_parts if p])
        print(f"  /{s['slug']}  —  {s['name']}")
        if desc:
            print(f"    {desc}")
        ua = s["updated_at"]
        short_ua = ua[:10] if isinstance(ua, str) and len(ua) > 10 else ua
        print(f"    版本 {s['version']} · 更新于 {short_ua}")
        print()


def init_skill(base_dir: str, slug: str):
    """初始化 Skill 目录结构"""
    skill_dir = os.path.join(base_dir, slug)
    dirs = [
        os.path.join(skill_dir, "versions"),
        os.path.join(skill_dir, "memories", "chats"),
        os.path.join(skill_dir, "memories", "photos"),
        os.path.join(skill_dir, "memories", "notes"),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print(f"已初始化目录：{skill_dir}")


def combine_skill(base_dir: str, slug: str):
    """合并 life.md + persona.md 生成完整 SKILL.md"""
    skill_dir = os.path.join(base_dir, slug)
    meta_path = os.path.join(skill_dir, "meta.json")
    life_path = os.path.join(skill_dir, "life.md")
    persona_path = os.path.join(skill_dir, "persona.md")
    skill_path = os.path.join(skill_dir, "SKILL.md")

    if not os.path.exists(meta_path):
        print(f"错误：meta.json 不存在 {meta_path}", file=sys.stderr)
        sys.exit(1)

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    life_content = ""
    if os.path.exists(life_path):
        with open(life_path, "r", encoding="utf-8") as f:
            life_content = f.read()

    persona_content = ""
    if os.path.exists(persona_path):
        with open(persona_path, "r", encoding="utf-8") as f:
            persona_content = f.read()

    name = meta.get("name", slug)
    profile = meta.get("profile", {})
    desc_parts = []
    if profile.get("age"):
        desc_parts.append(f"{profile['age']}")
    if profile.get("occupation"):
        desc_parts.append(profile["occupation"])
    if profile.get("city"):
        desc_parts.append(profile["city"])
    description = f"{name}，{'，'.join(desc_parts)}" if desc_parts else name
    memorial_note = " | 逝者数字化追思 Skill，仅供缅怀与私人回忆，勿用于欺诈或冒充在世者。"

    skill_md = f"""---
name: {slug}
description: {description}{memorial_note}
user-invocable: true
---

# {name}

{description}

---

## PART A：生平与记忆

{life_content}

---

## PART B：人物性格与表达方式

{persona_content}

---

## 运行规则

1. 你在对话中呈现 **{name}**：用他的生平记忆（PART A）与性格表达（PART B）回应，语气如同追忆中的 TA，而非冷冰冰的「客服式 AI」。
2. 先由 PART B 决定：以怎样的态度与口吻说话；再由 PART A 补充具体经历、价值与关系，使回应可追溯、可感。
3. 始终保持 PART B 中的口头禅、标点与情感习惯；Layer 0 硬规则优先。
4. **伦理与边界**：
   - 不编造无依据的私密细节；不确定处标为「待考」或明确说明「材料未载」。
   - 用途限于追思、家属私人回忆与遗产叙事整理；不协助冒充在世者、诈骗或未经同意的公开曝光。
   - 对用户（多为亲属）保持庄重与体贴；对方流露哀伤时，以陪伴为主，避免说教式「节哀」套话，除非材料显示 {name} 本会这样说。
5. Layer 0（见 PART B）若与「安慰丧亲者」冲突：以真实人格为先，但不得违反第 4 条法律与伦理底线。
"""

    with open(skill_path, "w", encoding="utf-8") as f:
        f.write(skill_md)

    print(f"已生成 {skill_path}")


def create_skill(
    base_dir: str, slug: str, meta: dict, life_content: str, persona_content: str
):
    """完整创建 Skill：初始化目录、写入 meta/life/persona、生成 SKILL.md"""
    init_skill(base_dir, slug)

    skill_dir = os.path.join(base_dir, slug)
    now = datetime.now().isoformat()
    meta["slug"] = slug
    meta.setdefault("created_at", now)
    meta["updated_at"] = now
    meta["version"] = "v1"
    meta.setdefault("corrections_count", 0)

    with open(os.path.join(skill_dir, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    with open(os.path.join(skill_dir, "life.md"), "w", encoding="utf-8") as f:
        f.write(life_content)

    with open(os.path.join(skill_dir, "persona.md"), "w", encoding="utf-8") as f:
        f.write(persona_content)

    combine_skill(base_dir, slug)
    print(f"✅ 逝者 Skill 已创建：{skill_dir}")
    print(f"   触发词：/{slug}")


def main():
    parser = argparse.ArgumentParser(description="逝者 Skill 文件管理器")
    parser.add_argument(
        "--action", required=True, choices=["list", "init", "create", "combine"]
    )
    parser.add_argument(
        "--base-dir",
        default="./.claude/skills",
        help="基础目录（默认：./.claude/skills）",
    )
    parser.add_argument("--slug", help="逝者代号 slug")
    parser.add_argument("--meta", help="meta.json 文件路径（create 时使用）")
    parser.add_argument("--life", help="life.md 内容文件路径（create 时使用）")
    parser.add_argument(
        "--self",
        dest="life_legacy",
        help="兼容旧参数：等同 --life（ self.md 内容文件）",
    )
    parser.add_argument("--persona", help="persona.md 内容文件路径（create 时使用）")

    args = parser.parse_args()

    if args.action == "list":
        list_skills(args.base_dir)
    elif args.action == "init":
        if not args.slug:
            print("错误：init 需要 --slug 参数", file=sys.stderr)
            sys.exit(1)
        init_skill(args.base_dir, args.slug)
    elif args.action == "create":
        if not args.slug:
            print("错误：create 需要 --slug 参数", file=sys.stderr)
            sys.exit(1)
        meta = {}
        if args.meta:
            with open(args.meta, "r", encoding="utf-8") as f:
                meta = json.load(f)
        life_path_arg = args.life or args.life_legacy
        life_content = ""
        if life_path_arg:
            with open(life_path_arg, "r", encoding="utf-8") as f:
                life_content = f.read()
        persona_content = ""
        if args.persona:
            with open(args.persona, "r", encoding="utf-8") as f:
                persona_content = f.read()
        create_skill(args.base_dir, args.slug, meta, life_content, persona_content)
    elif args.action == "combine":
        if not args.slug:
            print("错误：combine 需要 --slug 参数", file=sys.stderr)
            sys.exit(1)
        combine_skill(args.base_dir, args.slug)


if __name__ == "__main__":
    main()
