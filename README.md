# Project Learning Skill

**主动发现参考项目 B 中值得目标项目 A 吸收的技术。**

Discover what your project can learn from another codebase, with source-backed insights and actionable adoption plans.

[![Validate skill](https://github.com/Liears/project-learning-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/Liears/project-learning-skill/actions/workflows/validate.yml)

## 它解决什么问题

给出两个项目，由 Agent 阅读源码，主动发现调度、缓存、数据处理、失败恢复、模块边界或用户交互中值得借鉴的机制，再判断它们是否适合目标项目。

你不必事先知道 B 的哪个模块值得学。可以限定“知识库”“KV Cache”“任务调度”等范围，也可以让它围绕两边项目定位探索。

核心判断：**B 的这个机制解决了 A 的什么实际问题，增量价值是否值得迁移成本？**

## 输出

- 双方源码基线和实际调查范围。
- B 的入口、启用条件、实现、失败路径和源码位置。
- A 的对应现状，识别已有等价能力和真正差距。
- 借鉴价值、适用条件、优先级、依赖和迁移风险。
- 最小迁移切口、验证方法、回退及放弃条件。
- 不适合吸收、仅文档宣称、未接线或证据不足的候选。

默认只分析并生成报告，不修改 A/B、安装其依赖或执行其代码。代码事实、收益推断与实测结果分别说明，不承诺每次都能找出值得吸收的技术。

## 安装

这是一个基于 `SKILL.md` 的 Agent Skill，附带 Codex 界面元数据。使用需要能够读取两边源码的编码 Agent；不是独立运行的命令行分析器，不需要 Embedding 服务。

Codex 新安装可以将仓库直接克隆到技能目录：

```bash
git clone https://github.com/Liears/project-learning-skill.git ~/.codex/skills/project-learning
```

Windows PowerShell：

```powershell
git clone https://github.com/Liears/project-learning-skill.git "$HOME\.codex\skills\project-learning"
```

若设置了 `CODEX_HOME`，使用其 `skills/project-learning` 目录。如果该目录已有手动安装版本，先保留备份或使用其他克隆位置，不要覆盖本地修改。

其他支持 Agent Skills 的工具可以按其技能目录约定安装；实际适配范围需在对应工具中验证。

## 使用

```text
使用 $project-learning

目标项目 A：/path/to/your-project
参考项目 B：/path/to/reference-project
范围：知识库（可省略）

主动发现 B 中值得 A 吸收的技术，
给出双边源码证据、优先级和最小迁移验证方案。
```

也支持把路径换成 GitHub 仓库 URL，并指定分支或 commit。A 是准备改进的项目，B 是参考项目；远端私有仓库需要当前环境已有访问权限。

报告默认放在 A 的既有研究目录，无约定时使用 `docs/research/`。也可以明确要求只在聊天中回答或指定输出位置。

## 文件结构

```text
SKILL.md                        技能入口与判断流程
agents/openai.yaml              Codex 显示名称与默认调用提示
references/report-template.md   报告结构
scripts/validate_skill.py       维护时的格式、元数据与本地链接校验
tests/test_validate_skill.py    校验器回归测试
```

技能的运行不依赖 `scripts/` 或 Python；这些文件服务于仓库维护。

## 更新与维护

以这个仓库作为技能源码。Git 安装可在保留本地修改的前提下快进更新：

```bash
git -C ~/.codex/skills/project-learning pull --ff-only
```

维护说明见 [CONTRIBUTING.md](CONTRIBUTING.md)。提交会自动校验技能格式、UTF-8 元数据、本地引用及校验器测试。校验通过不等于分析结论可靠，行为验证仍需要给 Agent 两个项目实际使用。

已做过一次隔离的小型跨语言案例验证：识别 A 经辅助函数已有的重试能力，从 B 找出事务性检查点机制，排除未实现/未接线的语义去重与未经测量的提速宣传。尚未据此声称适用于所有项目或 Agent。

## License

[Apache License 2.0](LICENSE)。参考项目的代码及其许可证仍需独立核实。
