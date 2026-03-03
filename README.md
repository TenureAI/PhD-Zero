# AI Research Skills

这个仓库维护一份共享的 skill 内容，同时兼容 Codex 和 Claude Code。

当前 skills：

- `run-governor`
- `research-workflow`
- `memory-manager`
- `human-checkpoint`
- `experiment-execution`
- `deep-research`
- `project-context`

## 目录约定

真实内容只保留一份，统一放在 `.agents/skills/`。

每个 skill 目录下包含：

- `SKILL.md`
- 可选的 `references/`
- 可选的 `agents/`

为了兼容不同工具，仓库提供两个发现入口，全部用软链接指向同一份内容：

- Codex: 直接读取 `.agents/skills/<skill-name>/SKILL.md`
- Claude Code: `.claude/skills/<skill-name> -> ../../.agents/skills/<skill-name>`

这意味着：

- 改 skill 只改 `.agents/skills/` 下的真实目录
- 不维护第二份拷贝
- 不做内容转换

## Run 路径约定（执行时）

- 控制日志与阶段报告：`<codex-cwd>/logs/runs/<run_id>/`
- 项目实验产物：`<project-root>/runs/<run_id>/`

## AGENTS.md 的作用

`AGENTS.md` 负责项目级指令和行为规范，不负责 skill 的物理存放。

- Codex 读取 `AGENTS.md`
- skills 通过 `.agents/skills` 发现
- Claude Code 通过 `.claude/skills` 发现

## CI

仓库 CI 检查：

- `.agents/skills` 和 `.claude/skills` 的 skill 名称集合一致
- 每个 skill 都有可解析的 `SKILL.md`

## 快速检查

```bash
find .agents/skills -mindepth 1 -maxdepth 1 -type d
find .claude/skills -mindepth 1 -maxdepth 1 -type l
```
