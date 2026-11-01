# 维护与贡献

`SKILL.md` 是执行指导的单一事实源；`references/report-template.md` 只负责交付结构。README 用于安装与介绍，避免复制整套执行规则。

## 修改前

用一个真实请求或小型案例说明准备改善的行为，例如漏查 A 的已有能力、把 B 的 README 宣传当实现、没有明确的迁移验证条件。

保留默认只分析的边界、双边源码证据和“无需凑足推荐数量”的判断空间。修改引入条件分支时，给出能触发该分支的使用场景。

## 本地检查

建议使用独立虚拟环境；仅校验维护工具需要 Python 和 PyYAML。

```bash
python -m venv .venv
# Bash: source .venv/bin/activate
# PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python scripts/validate_skill.py .
python -m unittest discover -s tests -v
git diff --check
```

格式校验检查前置元数据、UI 默认提示和技能文档的本地链接；它不能证明 Agent 会正确分析项目。

## 行为验证

较大调整用隔离的两个项目进行实际试用，只给验证 Agent 请求、技能与源码，不提示预期结论。检查输出是否：

- 主动发现有实际价值的 B 机制，并复原真实调用路径。
- 回查 A 的间接实现和扩展路径，排除伪缺口。
- 区分代码事实、推断与已执行测试，拒绝未经证实的性能数字。
- 保留目标项目约束，给出最小迁移与可判定的验证条件。
- 对未接线、占位和不适合的候选给出准确边界。

案例优先采用合成或可公开源码，不把私人项目、密钥或业务数据加入仓库。记录实际运行条件和已知局限，不把单次通过写成通用保证。

## 提交

Skill 行为、格式工具与文档修改按职责拆分。PR 描述写明触发问题、变更和验证结果；测试未运行时明确标注。
