<div align="center">

# 🎓 PhD-Zero

**The First Step Toward the Autonomous AI Scientist.**

<p align="center">
<a href="#-the-vision">The Vision</a> •
<a href="#-why-phd-zero">Why Zero?</a> •
<a href="#-included-skills">Capabilities</a> •
<a href="#-quick-start">Quick Start</a> •
<a href="#-contributing">Contribute</a>
</p>

*"Research is a search problem. PhD-Zero is the solver."*

</div>

---

## 👁️ The Vision

**PhD-Zero** is the foundational layer of the **TenureAI** initiative: a project dedicated to building an autonomous AI Scientist capable of independent experimentation, discovery, and development.

Current AI R&D is bottlenecked by human "manual labor"—scraping Arxiv, boilerplate coding, monitoring logs, and drafting reports. PhD-Zero transforms these research intuitions into **programmable agent skills**.

* **Short-term Goal**: An intern-level AI researcher capable of executing specific R&D tasks.
* **Ultimate Goal**: A full-stack AI Scientist that automates the entire algorithm development lifecycle.

---

## 🔥 Why PhD-Zero?

In the era of "Scale is All You Need," simple prompting is no longer sufficient for complex research. PhD-Zero provides a **standardized operating layer** for your coding agents (Codex / Claude Code):

* **From Intuition to Algorithm**: Translates vague research ideas into rigorous `experiment-execution` pipelines.
* **Unified Skill Interface**: One codebase that drives both Codex and Claude Code through a shared skill-discovery protocol.
* **Evidence-Backed Reasoning**: Enforces `deep-research` and data collection to eliminate hallucination.
* **Operational Discipline**: Uses the `run-governor` to prevent agents from spiraling into infinite loops or wasting tokens.

---

## 🛠️ Capability Matrix (Included Skills)

PhD-Zero decomposes the research process into modular, reusable skills:

| Skill | Primary Function | Equivalent Human Role |
| --- | --- | --- |
| **`run-governor`** | Execution discipline and stage control | **Principal Investigator** |
| **`research-plan`** | Task decomposition and logical modeling | **Senior Researcher** |
| **`deep-research`** | Automated Arxiv retrieval and synthesis | **Literature Specialist** |
| **`experiment-execution`** | Automated coding, execution, and debugging | **Algorithm Engineer** |
| **`memory-manager`** | Context restoration and progress tracking | **Human Working Memory** |
| **`paper-writing`** | LaTeX drafting and academic polishing | **Scientific Writer** |
| **`human-checkpoint`** | High-risk gatekeeping and feedback loops | **Reviewer / Advisor** |

---

## 🚀 Quick Start

### 1. Initialize the Lab

```bash
git clone https://github.com/TenureAI/PhD-Zero.git
cd PhD-Zero

```

### 2. Connect Your Agents

PhD-Zero uses a dual-discovery mechanism to ensure cross-platform compatibility:

```bash
# Verify available skills
find .agents/skills -mindepth 1 -maxdepth 1 -type d

```

* **Codex (GitHub Copilot)**: Reads repository-level instructions from `AGENTS.md`.
* **Claude Code**: Discovers capabilities via symlinks in the `.claude/skills/` directory.

---

## 📂 Repository Layout

```text
.
├── AGENTS.md                # The Agent Constitution & Operating Rules
├── .agents/
│   └── skills/              # Source of Truth: Modular skill definitions
├── .claude/
│   └── skills/              # Claude Code discovery layer (Symlinks)
└── logs/                    # Execution traces and stage reports

```

---

## 🤝 Join the Evolution

We are looking for engineers and researchers who want to automate themselves out of the grind.

1. **Star This Repo**: If you believe the future of AI development belongs to AI.
2. **Submit a Skill**: Help PhD-Zero evolve by contributing your research workflows.
3. **Spread the Word**: Follow the journey via **#TenureAI** on Twitter.

---

<div align="center">

**Built with 🧠 by [TenureAI](https://github.com/TenureAI)** *Automating the grind. Scaling the genius.*

</div>