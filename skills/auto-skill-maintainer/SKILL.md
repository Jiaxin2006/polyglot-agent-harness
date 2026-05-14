---
name: "auto-skill-maintainer"
description: "当发现既有 workflow/测试写法不正确或缺失时：自动补齐/新增 skill，并在满足门禁时自动提交并 push。"
---

# Auto Skill Maintainer（自动补齐技能）

## 触发条件

当你明确发现以下任一情况时，必须执行本技能：

- 之前的测试写法/目录落点/配置方式是错误的或与仓库惯例冲突
- 构建/测试链路存在“隐式知识”，导致后续容易重复踩坑
- 为了跑通实验临时做了 workaround，但正确做法应固化为可复用 skill

## 门禁（push 安全策略）

- 默认只做 **落盘 + 提交（commit）**。
- 只有同时满足以下条件才允许 push：
  - 本地仓库存在 `origin` remote
  - 环境变量 `HARNESS_AUTO_PUSH=1`
  - 运行命令显式带 `--push`

## 执行步骤

1. 选择 skill 名称与目标：优先更新已有 skill；若不存在再创建新 skill。
2. 用脚本生成/确保 skill 与 plugin 注册：
   - `python3 scripts/auto-skill.py ensure --name <skill-name> --description '<desc>' --commit`
3. 把新知识写进 skill 的 `skills/<skill-name>/SKILL.md`（覆盖占位内容），并再次提交：
   - `git add skills/<skill-name>/SKILL.md plugin.json`
   - `git commit -m 'harness: refine <skill-name>'`
4. 如果需要推送（满足门禁）：
   - `HARNESS_AUTO_PUSH=1 python3 scripts/auto-skill.py ensure --name <skill-name> --description '<desc>' --push`

## 输出要求

- skill 必须可复用：写清“什么时候用、怎么用、交付是什么”
- plugin.json 必须包含该 skill 的 `skills/<name>/SKILL.md`
