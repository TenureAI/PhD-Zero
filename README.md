<div align="center">

<img src="./assets/phd-zero-mark.svg" alt="PhD-Zero logo" width="112" />

# PhD-Zero

<p>An operating system for research-oriented coding agents.</p>

<p>
  <a href="./README_zh.md">简体中文</a> ·
  <a href="./docs/index.html">Website</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#core-skills">Core Skills</a> ·
  <a href="#contributing">Contributing</a>
</p>

</div>

PhD-Zero is a repository of reusable skills for AI research work. The point is not to make an agent sound smart for one turn. The point is to give it a workflow it can actually follow: plan the task, gather evidence, run experiments, keep context, ask for human review when needed, and write results down in a form another person can inspect.

The same skill library is exposed to different runtimes. Codex-style agents read workspace rules from `AGENTS.md`. Claude Code sees a mirrored discovery layer under `.claude/skills/`. The actual source of truth lives in `.agents/skills/`.

## Quick start

If you just want to see whether the repo is wired correctly, do this:

```bash
git clone https://github.com/TenureAI/PhD-Zero.git
cd PhD-Zero

find .agents/skills -mindepth 1 -maxdepth 1 -type d
find .claude/skills -mindepth 1 -maxdepth 1 -type l
```

Those two commands should list the same skill names. If they do, the shared skill layer is in place.

From there:

1. Read `AGENTS.md` to understand the workspace rules used by Codex-style agents.
2. Inspect `.agents/skills/` if you want the canonical skill implementations.
3. Inspect `.claude/skills/` if you want to verify the Claude Code mirror.

If you prefer a landing page over the raw repository view, there is also a static site under [docs/index.html](./docs/index.html).

## What is in this repository?

The repository is intentionally small. It does not try to be a benchmark suite, a framework, and a demo app all at once. It is mostly a skill library plus the rules that tell agents how to use it.

```text
.
├── AGENTS.md
├── REPO_CONVENTIONS.md
├── .agents/skills/      # canonical skill definitions
├── .claude/skills/      # Claude Code mirror layer
├── .github/workflows/   # repository validation
├── assets/              # shared visual assets
└── docs/                # static landing page
```

The CI in this repo checks that the skill directories under `.agents/skills` and `.claude/skills` stay in sync, and that every tracked skill has a readable `SKILL.md`.

## Core skills

The current skill set covers the basic loop of a research-oriented agent:

| Skill | What it is for |
| --- | --- |
| `run-governor` | Stage control, run discipline, and execution policy |
| `research-workflow` | The default loop for non-trivial research tasks |
| `research-plan` | Turning an open-ended goal into a concrete plan |
| `deep-research` | External search, literature comparison, and synthesis |
| `experiment-execution` | Running code, debugging, and experiment execution |
| `memory-manager` | Working state and reusable memory |
| `project-context` | Project-specific runtime context and conventions |
| `human-checkpoint` | Human review for risky or expensive decisions |
| `paper-writing` | Drafting and revising research artifacts |

That list will probably grow, but the idea is stable: break research into pieces that can be reused instead of trying to solve everything with one giant prompt.

## Who this is for

PhD-Zero is for people who are already using coding agents in research or engineering-adjacent work and want more discipline around the process. If you care about literature review, experiment planning, reproducibility, or keeping an agent from improvising its way through a long task, this repo is meant to be useful. If you just want a flashy demo, it is probably not the right project.

## Contributing

Contributions are welcome, especially in three areas:

1. new skills that fit the repository's scope
2. tighter workflows for the existing skills
3. validation and examples from real usage

Before opening a PR, check `REPO_CONVENTIONS.md`. This repo keeps reusable skill content in version control and keeps task-specific logs or run artifacts out.

## Acknowledgements

PhD-Zero is shaped by the broader ecosystem around coding agents, research tooling, and writing support. In particular, the repository draws useful ideas from projects that treat workflows as first-class artifacts rather than one-off prompts.

We also want to acknowledge:

- [blader/humanizer](https://github.com/blader/humanizer/tree/main)
- [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh)

These are not runtime dependencies here, but they were useful references when thinking about writing quality and reusable editing guidance.

## Cite

If PhD-Zero is useful in your workflow or research, you can cite it as:

```bibtex
@misc{phd_zero_github,
  author       = {TenureAI Contributors},
  title        = {PhD-Zero: An Operating System for Research-Oriented Coding Agents},
  year         = {2026},
  howpublished = {\url{https://github.com/TenureAI/PhD-Zero}},
  note         = {GitHub repository}
}
```
