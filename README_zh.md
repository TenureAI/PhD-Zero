<div align="center">

<img src="./assets/phd-zero-mark.svg" alt="PhD-Zero logo" width="112" />

# PhD-Zero

### 面向自主 AI Scientist 的研究操作系统

<p align="center">
  <a href="./README.md">English</a> •
  <a href="./README_zh.md">简体中文</a> •
  <a href="#-phd-zero-是什么">PhD-Zero 是什么</a> •
  <a href="#-为什么要做它">为什么要做它</a> •
  <a href="#-核心-skill-栈">Skill 栈</a> •
  <a href="#-它是怎么工作的">工作方式</a> •
  <a href="#-快速开始">快速开始</a> •
  <a href="#-路线图">路线图</a> •
  <a href="#-参与贡献">参与贡献</a> •
  <a href="#-致谢">致谢</a> •
  <a href="#-引用">引用</a>
</p>

**把研究流程沉淀成可复用的 agent skills。**  
**从文献搜索、实验执行、记忆管理，到论文写作。**

*为 Codex、Claude Code，以及未来的 Autonomous AI Researcher 而构建。*

</div>

---

## 👁️ PhD-Zero 是什么？

**PhD-Zero** 是一个面向 coding agents 的开源 **AI R&D 操作层**。

它不把“研究”当成一次性 prompt，而是拆成一组结构化、可复用的 skills：

- 规划任务
- 搜索证据
- 执行实验
- 管理记忆
- 在需要时请求人工审阅
- 把结果整理成研究产物

目标很明确：

- **近期：** 做出一个能稳定处理有边界 R&D 任务的 **AI Research Intern**
- **长期：** 做出一个能贯穿完整算法研发周期的 **Autonomous AI Scientist**

一句话说，**PhD-Zero 是连接“原始模型能力”和“真实研究执行”的系统层。**

---

## 🔥 为什么要做它？

今天的强模型已经能写代码、读论文、调试脚本。

但它们普遍缺的是 **研究纪律**。

真实的 AI 研发不只是“生成一个答案”，它还要求：

- 分阶段执行
- 基于证据推理
- 跨步骤记忆
- 受控实验
- 对昂贵或高风险决策设置人工检查点

PhD-Zero 就是为了补上这层结构。

它帮助 agent 完成这些转变：

- **从模糊想法走向可执行计划**
- **从一次性 prompting 走向可复用 workflow**
- **从幻觉式自信走向证据驱动输出**
- **从孤立任务走向可积累研究记忆**

---

## 🛠️ 核心 Skill 栈

PhD-Zero 把 AI research 拆成一组 agent 可以发现并调用的模块化 skills。

| Skill | 在系统中的角色 | 类比的人类角色 |
| --- | --- | --- |
| `run-governor` | 控制阶段、执行纪律和 run 安全策略 | PI / 项目负责人 |
| `research-workflow` | 非平凡研究任务的默认编排循环 | 研究经理 |
| `research-plan` | 把开放目标变成具体计划、ablation 和研究设计 | 资深研究员 |
| `deep-research` | 搜集外部证据、对比文献并综合结论 | 文献调研者 |
| `experiment-execution` | 跑代码、定位失败并执行实验 | 研究工程师 |
| `memory-manager` | 维护工作态与可复用记忆 | 工作记忆 + 长期记忆 |
| `project-context` | 持久化项目运行上下文与约定 | 实验记录本 |
| `human-checkpoint` | 升级处理高风险、高成本或高影响决策 | 导师 / 审稿人 |
| `paper-writing` | 起草和修改论文与研究文档 | 科学写作者 |

> **研究不是单一能力，而是一组能力的协同系统。**

---

## ⚙️ 它是怎么工作的？

PhD-Zero 被设计成面向不同 coding agents 的 **共享 skill 层**。

### 对 Codex / GitHub Copilot 风格 agent

仓库级行为由 `AGENTS.md` 定义。

### 对 Claude Code

skills 通过 `.claude/skills/` 暴露。

### 单一事实源

真正的 skill 定义统一放在：

```text
.agents/skills/
```

这样同一个仓库就能为多种 agent runtime 提供同一套研究 workflow 逻辑。

---

## 📂 仓库结构

```text
.
├── AGENTS.md                  # 工作区的全局行为规范
├── REPO_CONVENTIONS.md        # 产物、日志与仓库卫生规则
├── .agents/
│   └── skills/                # 真实 skill 定义
├── .claude/
│   └── skills/                # Claude Code 的发现层
├── .github/
│   └── workflows/             # 仓库自动化
├── assets/                    # README 和其他文档资源
└── README.md
```

---

## ✨ 它和其他仓库有什么不同？

很多 “AI researcher” 仓库最后都会落到这几类之一：

- benchmark
- 论文列表
- 单 agent demo
- prompt 包

PhD-Zero 的区别在于，它关注的是 **把研究真正操作化**。

它不是只想让 agent “看起来聪明”，而是想让 agent **像一个研究系统一样工作**。

这意味着：

- 显式执行阶段
- 受控的记忆使用
- 证据优先的决策
- 用可复用 skills 替代零散 prompt
- 同时兼容多种 coding-agent 环境

---

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/TenureAI/PhD-Zero.git
cd PhD-Zero
```

### 2. 检查 skill 库

```bash
find .agents/skills -mindepth 1 -maxdepth 1 -type d
find .claude/skills -mindepth 1 -maxdepth 1 -type l
```

如果这两条命令列出的 skill 名称一致，说明共享 skill 层是连通的。

### 3. 连接你的 agent runtime

- **Codex / Copilot 风格 agent** 从 `AGENTS.md` 读取工作区规则
- **Claude Code** 通过 `.claude/skills/` 发现同一组能力

### 4. 用一个真实研究任务开始

例如：

- 复现论文结果
- 分析训练任务为什么失败
- 设计 ablation 计划
- 比较新项目方向里的多种方法
- 根据实验结果起草研究报告

---

## 🧭 路线图

PhD-Zero 是一个更大愿景的第一层。

### Phase 1 — AI Research Intern

- 有边界的文献调研
- 实验规划
- 代码执行与调试
- 报告起草

### Phase 2 — AI Research Collaborator

- 跨项目可复用记忆
- 更强的 project context 持久化
- 更好的实验迭代循环
- 更成熟的人在回路检查点

### Phase 3 — Autonomous AI Scientist

- 独立提出假设
- 自主驱动实验
- 长时程项目执行
- 端到端算法研发

---

## 🤝 参与贡献

我们正在公开构建它。

你可以这样参与：

1. 添加新的 agent skills
2. 改进已有 workflow
3. 贡献更好的 AI R&D 评测任务
4. 在真实研究循环里使用 PhD-Zero，并反馈哪里失效

如果你关心 **AI 做 AI 研究** 的未来，这个仓库就是给你的。

---

## 🙏 致谢

PhD-Zero 的构建受到了更广泛的 agent、工具链和写作辅助生态启发。

我们特别感谢：

- 为 coding-agent 环境和 workflow 规范做出贡献的开源社区
- 构建 Codex、Claude Code 及相关 agent runtime 技能系统的贡献者
- [blader/humanizer](https://github.com/blader/humanizer/tree/main)，提供了实用的人类化文本改写思路
- [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh)，提供了面向中文的人类化写作参考

这些项目并不是 PhD-Zero 的直接依赖，但它们影响了我们对“可复用 agent 行为”和“写作支持能力”的设计方式。

---

## 💡 理念

PhD-Zero 建立在一个核心判断上：

> **AI research 应该变成可编程的。**

不只是更聪明的输出。
不只是更好的 prompts。
而是可复用、可检查、可演化的研究工作流。

这是走向 autonomous AI scientist 的第一步。

---

## 📚 引用

如果 PhD-Zero 对你的工作流或研究有帮助，可以这样引用：

```bibtex
@misc{phd_zero_github,
  author       = {TenureAI Contributors},
  title        = {PhD-Zero: An Operating System for the Autonomous AI Scientist},
  year         = {2026},
  howpublished = {\url{https://github.com/TenureAI/PhD-Zero}},
  note         = {GitHub repository}
}
```

---

<div align="center">

### Built by <a href="https://github.com/TenureAI">TenureAI</a>

**Automating the grind. Scaling research.**

</div>
