# AI Research Skills

这个仓库维护一份共享的 skill 内容，同时兼容 Codex 和 Claude Code。

当前 skills：

- `research-workflow`
- `memory-manager`
- `human-checkpoint`
- `experiment-execution`

## 目录约定

真实内容只保留一份，统一放在 `.agents/skills/`：

- `.agents/skills/research-workflow/`
- `.agents/skills/memory-manager/`
- `.agents/skills/human-checkpoint/`
- `.agents/skills/experiment-execution/`

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

## AGENTS.md 的作用

`AGENTS.md` 负责项目级指令和行为规范，不负责 skill 的物理存放。

- Codex 读取 `AGENTS.md`
- skills 通过 `.agents/skills` 发现
- Claude Code 通过 `.claude/skills` 发现

## CI

仓库内的 CI 只检查一件事：

- `.agents/skills` 和 `.claude/skills` 下的软链接都存在，并且都能解析到有效的 `SKILL.md`

## 快速检查

```bash
find .agents/skills -mindepth 1 -maxdepth 1 -type l
find .claude/skills -mindepth 1 -maxdepth 1 -type l
```
