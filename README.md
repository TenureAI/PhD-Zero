<div align="center">

# 🎓 PhD-Zero

### An Operating System for the Autonomous AI Scientist

<p align="center">
  <a href="#-what-is-phd-zero">What is PhD-Zero?</a> •
  <a href="#-why-it-exists">Why it exists</a> •
  <a href="#-core-skill-stack">Skill Stack</a> •
  <a href="#-how-it-works">How it works</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-roadmap">Roadmap</a> •
  <a href="#-contributing">Contributing</a>
</p>

**Turn research workflows into reusable agent skills.**  
**From literature search to experiment execution, memory, and paper writing.**

*Built for Codex, Claude Code, and the future autonomous AI researcher.*

</div>

---

## 👁️ What is PhD-Zero?

**PhD-Zero** is an open-source **AI R&D operating layer** for coding agents.

Instead of treating research as a single prompt, PhD-Zero breaks it into structured, reusable skills:
- plan the work,
- search for evidence,
- execute experiments,
- manage memory,
- request human review when needed,
- and turn results into research artifacts.

The goal is simple:

- **Near term:** build an **intern-level AI researcher** that can reliably handle scoped R&D tasks.
- **Long term:** build an **autonomous AI scientist** that can navigate the full algorithm-development lifecycle.

In short, **PhD-Zero is the systems layer between raw model capability and real research execution.**

---

## 🔥 Why it exists

Today, strong models can already code, read papers, and debug scripts.

What they still lack is **research discipline**.

Real AI R&D is not just “generate an answer.” It requires:
- staged execution,
- evidence-backed reasoning,
- memory across steps,
- controlled experimentation,
- and human checkpoints for expensive or risky decisions.

PhD-Zero exists to provide that missing structure.

It helps agents move:
- **from vague ideas to executable plans**
- **from one-shot prompting to reusable workflows**
- **from hallucinated confidence to evidence-backed outputs**
- **from isolated tasks to compounding research memory**

---

## 🛠️ Core skill stack

PhD-Zero decomposes AI research into modular skills that agents can discover and invoke.

| Skill | Role in the system | Human analogy |
| --- | --- | --- |
| `run-governor` | Controls stages, execution discipline, and run safety | PI / project lead |
| `research-workflow` | Default orchestration loop for non-trivial research tasks | Research manager |
| `research-plan` | Turns open-ended goals into concrete plans, ablations, and study designs | Senior researcher |
| `deep-research` | Collects external evidence, compares literature, and synthesizes findings | Literature reviewer |
| `experiment-execution` | Runs code, debugs failures, and executes experiments | Research engineer |
| `memory-manager` | Maintains working state and promotes reusable memory | Working + long-term memory |
| `project-context` | Persists project-specific runtime context and conventions | Lab notebook |
| `human-checkpoint` | Escalates risky, expensive, or high-impact decisions | Advisor / reviewer |
| `paper-writing` | Drafts and revises research artifacts and paper text | Scientific writer |

> **Research is not one capability. It is a coordinated system of capabilities.**

---

## ⚙️ How it works

PhD-Zero is designed as a **shared skill layer** for different coding agents.

### For Codex / GitHub Copilot-style agents
Repository-level behavior is defined through `AGENTS.md`.

### For Claude Code
Skills are exposed through `.claude/skills/`.

### Source of truth
The canonical skill definitions live in:

```text
.agents/skills/
```

This lets one repository drive multiple agent runtimes with the same research workflow logic.

---

## 📂 Repository structure

```text
.
├── AGENTS.md                  # Global operating rules for the workspace
├── REPO_CONVENTIONS.md        # Artifact, logging, and repo hygiene rules
├── .agents/
│   └── skills/                # Canonical skill definitions
├── .claude/
│   └── skills/                # Claude Code discovery layer
├── .github/
│   └── workflows/             # Repo automation
└── README.md
```

---

## ✨ What makes this different?

Most “AI researcher” repos are one of these:

* a benchmark,
* a paper list,
* a single-agent demo,
* or a prompt pack.

PhD-Zero is different because it focuses on **operationalizing research**.

It is not just trying to make an agent sound smart.
It is trying to make an agent **work like a research system**.

That means:

* explicit execution stages,
* controlled memory usage,
* evidence-first decisions,
* reusable skills instead of ad hoc prompts,
* and compatibility with multiple coding-agent environments.

---

## 🚀 Quick start

### 1. Clone the repository

```bash
git clone https://github.com/TenureAI/PhD-Zero.git
cd PhD-Zero
```

### 2. Inspect the skill library

```bash
find .agents/skills -mindepth 1 -maxdepth 1 -type d
```

### 3. Connect your agent runtime

* **Codex / Copilot-style agents** read workspace rules from `AGENTS.md`
* **Claude Code** discovers the same capabilities through `.claude/skills/`

### 4. Start with a real research task

Examples:

* reproduce a paper result
* investigate why a training run failed
* design an ablation plan
* compare methods for a new project direction
* draft a research report from experiment evidence

---

## 🧭 Roadmap

PhD-Zero is the first layer of a larger vision.

### Phase 1 — AI Research Intern

* scoped literature investigation
* experiment planning
* code execution and debugging
* report drafting

### Phase 2 — AI Research Collaborator

* reusable memory across projects
* stronger project context persistence
* better experiment iteration loops
* improved human-in-the-loop checkpoints

### Phase 3 — Autonomous AI Scientist

* independent hypothesis generation
* self-directed experimentation
* long-horizon project execution
* end-to-end algorithm development

---

## 🤝 Contributing

We are building this in the open.

You can contribute by:

1. adding new agent skills,
2. improving existing workflows,
3. contributing better evaluation tasks for AI R&D,
4. or using PhD-Zero in real research loops and sharing what breaks.

If you care about the future of **AI doing AI research**, this repo is for you.

---

## 💡 Philosophy

PhD-Zero is based on one belief:

> **AI research should become programmable.**

Not just smarter outputs.
Not just better prompts.
But reusable, inspectable, evolving research workflows.

That is the first step toward the autonomous AI scientist.

---

<div align="center">

### Built by <a href="https://github.com/TenureAI">TenureAI</a>

**Automating the grind. Scaling research.**

</div>
```
