<div align="center">

<img src="./assets/phd-zero-mark.svg" alt="PhD-Zero logo" width="112" />

# PhD-Zero

<p>一个面向研究型 coding agent 的工作流操作层。</p>

<p>
  <a href="./README.md">English</a> ·
  <a href="./docs/index.html">Website</a> ·
  <a href="#快速开始">快速开始</a> ·
  <a href="#核心-skills">核心 Skills</a> ·
  <a href="#参与贡献">参与贡献</a>
</p>

</div>

PhD-Zero 是一个可复用 research skills 仓库。它的目标不是让 agent 在单轮对话里“显得聪明”，而是给它一套真的能执行的研究工作流：怎么规划任务、怎么找证据、怎么跑实验、怎么保留上下文、什么时候该找人确认，以及最后怎么把结果写成别人能检查的研究产物。

同一套 skills 会暴露给不同 runtime。Codex 风格 agent 主要通过 `AGENTS.md` 读取工作区规则，Claude Code 通过 `.claude/skills/` 发现镜像层，真正的 source of truth 统一放在 `.agents/skills/`。

## 快速开始

如果你只是想先确认这个仓库的 skill 层是通的，直接跑下面几条命令：

```bash
git clone https://github.com/TenureAI/PhD-Zero.git
cd PhD-Zero

find .agents/skills -mindepth 1 -maxdepth 1 -type d
find .claude/skills -mindepth 1 -maxdepth 1 -type l
```

如果两条命令列出的 skill 名称一致，说明共享 skill 层已经接通。

接下来通常这样看：

1. 先读 `AGENTS.md`，了解 Codex 风格 agent 的工作区规则。
2. 再看 `.agents/skills/`，这里是技能的真实实现。
3. 如果你关心 Claude Code 的发现方式，再看 `.claude/skills/`。

如果你更喜欢首页式入口而不是直接翻仓库，也可以打开 [docs/index.html](./docs/index.html)。

## 仓库里有什么

这个仓库故意保持得比较克制。它不是 benchmark、framework、demo app 的混合体，主体就是 skill 库本身，加上一点规则和校验。

```text
.
├── AGENTS.md
├── REPO_CONVENTIONS.md
├── .agents/skills/      # skill 的真实定义
├── .claude/skills/      # Claude Code 的镜像发现层
├── .github/workflows/   # 仓库校验
├── assets/              # 共用视觉资源
└── docs/                # 静态 landing page
```

这个仓库的 CI 主要检查两件事：`.agents/skills` 和 `.claude/skills` 的技能目录是否同步，以及每个已跟踪 skill 是否都有可解析的 `SKILL.md`。

## 核心 Skills

现在这批 skills 覆盖的是一个研究型 agent 的基本闭环：

| Skill | 用途 |
| --- | --- |
| `run-governor` | 管阶段、执行纪律和 run 策略 |
| `research-workflow` | 非平凡研究任务的默认执行循环 |
| `research-plan` | 把开放目标收敛成具体计划 |
| `deep-research` | 做外部搜索、文献比较和综合判断 |
| `experiment-execution` | 跑代码、调试和执行实验 |
| `memory-manager` | 管工作态和可复用记忆 |
| `project-context` | 保留项目级运行上下文和约定 |
| `human-checkpoint` | 在高风险或高成本节点找人确认 |
| `paper-writing` | 起草和修改研究产物 |

这个列表以后还会扩，但基本思路不会变：把研究拆成可以复用的模块，而不是指望一个超长 prompt 包打天下。

## 这个仓库适合谁

如果你已经在研究或工程工作里使用 coding agents，并且开始在意流程纪律、实验可复现性、长任务中的上下文保持，或者想减少 agent 一路即兴发挥带来的风险，这个仓库大概率对你有用。如果你只是想看一个炫一点的 demo，它可能不是最合适的项目。

## 参与贡献

欢迎贡献，尤其是下面三类：

1. 新的 skill，但前提是它真的符合仓库范围
2. 对现有 workflows 的收紧和改进
3. 来自真实使用场景的验证和反馈

开 PR 之前建议先看一遍 `REPO_CONVENTIONS.md`。这个仓库只跟踪可复用 skill 内容，不把一次性的 run 日志或任务产物混进来。

## 致谢

PhD-Zero 的形成受到了 coding agents、research tooling 和写作辅助生态的影响。尤其是那些把 workflow 当成一等对象，而不是把 prompt 当一次性脚本来用的项目，对这个仓库的方向影响很大。

另外也感谢：

- [blader/humanizer](https://github.com/blader/humanizer/tree/main)
- [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh)

它们不是这里的运行时依赖，但在思考写作质量和可复用编辑规范时提供了很有价值的参考。

## 引用

如果 PhD-Zero 对你的工作流或研究有帮助，可以这样引用：

```bibtex
@misc{phd_zero_github,
  author       = {TenureAI Contributors},
  title        = {PhD-Zero: An Operating System for Research-Oriented Coding Agents},
  year         = {2026},
  howpublished = {\url{https://github.com/TenureAI/PhD-Zero}},
  note         = {GitHub repository}
}
```
