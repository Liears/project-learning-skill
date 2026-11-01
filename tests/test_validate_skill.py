"""Packaging regressions; these do not assess an agent's research quality."""
import tempfile
import unittest
from pathlib import Path

from scripts.validate_skill import validate_skill


class SkillValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "agents").mkdir()
        (self.root / "references").mkdir()
        self.write("SKILL.md", "---\nname: project-learning\ndescription: 跨项目技术吸收分析\n---\n\n[报告](references/report.md)\n")
        self.write("references/report.md", "# 报告\n")
        self.write("agents/openai.yaml", 'interface:\n  display_name: "双项目技术吸收"\n  short_description: "主动发现参考项目中值得目标项目吸收的技术机制并提供源码证据"\n  default_prompt: "使用 $project-learning 比较两个项目。"\n')

    def write(self, relative, value):
        (self.root / relative).write_text(value, encoding="utf-8")

    def test_valid_unicode_package(self):
        self.assertEqual(validate_skill(self.root), [])

    def test_missing_report_is_reported(self):
        (self.root / "references/report.md").unlink()
        self.assertTrue(any("report.md" in error for error in validate_skill(self.root)))

    def test_invalid_frontmatter_type_is_reported(self):
        self.write("SKILL.md", "---\n- project-learning\n---\n")
        self.assertTrue(any("mapping" in error for error in validate_skill(self.root)))

    def test_non_utf8_ui_is_reported(self):
        (self.root / "agents/openai.yaml").write_bytes("interface: 中文".encode("gbk"))
        self.assertTrue(any("UTF-8" in error for error in validate_skill(self.root)))

    def test_prompt_must_invoke_the_declared_skill(self):
        path = self.root / "agents/openai.yaml"
        self.write("agents/openai.yaml", path.read_text(encoding="utf-8").replace("$project-learning", "$other-skill"))
        self.assertTrue(any("$project-learning" in error for error in validate_skill(self.root)))

    def test_missing_ui_file_is_reported(self):
        (self.root / "agents/openai.yaml").unlink()
        self.assertTrue(any("openai.yaml" in error for error in validate_skill(self.root)))

    def test_remote_links_and_local_anchors_are_allowed(self):
        path = self.root / "SKILL.md"
        self.write("SKILL.md", path.read_text(encoding="utf-8") + "\n[远端](https://example.org/docs) [本节](#报告)\n")
        self.assertEqual(validate_skill(self.root), [])


if __name__ == "__main__":
    unittest.main()
