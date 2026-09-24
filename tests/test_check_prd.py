"""Regression cases for the PRD ID and link check, using only temporary documents."""
import importlib.util
import re
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


SCRIPT = Path(__file__).resolve().parents[1] / "plugins" / "ai-skills" / "skills" / "sdd" / "scripts" / "check_prd.py"
EXAMPLE = SCRIPT.parents[1] / "references" / "prd" / "example.md"

_spec = importlib.util.spec_from_file_location("check_prd", SCRIPT)
check_prd = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_prd)
check = check_prd.check


DOCUMENT = """# Solicitações

Prefixo dos requisitos: `REQ`.

## Requisitos funcionais
- **REQ-100 (Must)** Retornar o resultado original para uma chave repetida.

## Critérios de aceitação
Repetir a chave retorna o resultado de REQ-100.
"""

ENGLISH = """# Requests

Requirement prefix: `ENG`.

## Functional Requirements
- **ENG-01 (Should)** Return the original result for a repeated key.

## Non-functional Requirements
- **ENG-02 (Must)** Answer within 2 seconds at the 95th percentile.
"""


def run_cli(folder):
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(SCRIPT), str(folder)],
        capture_output=True, text=True, encoding="utf-8",
    )


def write_prd(folder, capability, text):
    path = Path(folder) / capability / "prd.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


class PrdChecks(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.document = write_prd(self.folder, "requests-lifecycle", DOCUMENT)

    def test_valid_document_has_no_findings(self):
        self.assertEqual([], check(self.folder))

    def test_titles_in_any_language_are_accepted(self):
        write_prd(self.folder, "requests-en", ENGLISH)
        self.assertEqual([], check(self.folder))

    def test_skill_example_has_no_findings(self):
        example = re.search(r"^````markdown\n(.*?)^````$", EXAMPLE.read_text(encoding="utf-8"), re.M | re.S)
        self.document.write_text(example[1], encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_specs_and_instructions_are_not_read(self):
        (self.folder / "CLAUDE.md").write_text("# Instruções\nReferência: REQ-99\n", encoding="utf-8")
        (self.document.parent / "spec.md").write_text("- **REQ-100 (Must)** Cópia.\n[Ausente](missing.md)\n", encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_three_digit_citation_is_not_truncated(self):
        self.document.write_text(DOCUMENT + "\nConsultar REQ-101.\n", encoding="utf-8")
        self.assertIn("requests-lifecycle/prd.md: citation REQ-101 has no definition", check(self.folder))

    def test_undefined_prefix_is_not_a_citation(self):
        self.document.write_text(DOCUMENT + "\nAssinatura com SHA-256 conforme ISO-27001.\n", encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_citation_of_another_prd_resolves(self):
        write_prd(self.folder, "requests-en", ENGLISH + "\nDepends on REQ-100.\n")
        self.assertEqual([], check(self.folder))

    def test_overview_citations_are_checked(self):
        (self.folder / "overview.md").write_text("# Visão geral\n\nREQ-100 e REQ-102.\n", encoding="utf-8")
        self.assertEqual(["overview.md: citation REQ-102 has no definition"], check(self.folder))

    def test_unprefixed_id_is_reported(self):
        self.document.write_text(DOCUMENT + "\nVer FR-12.\n", encoding="utf-8")
        self.assertTrue(any("unprefixed id FR-12" in f for f in check(self.folder)))

    def test_duplicate_definition_is_reported(self):
        self.document.write_text(DOCUMENT + "\n- **REQ-100 (Must)** Outro resultado.\n", encoding="utf-8")
        self.assertIn("ids: REQ-100 defined 2 times", check(self.folder))

    def test_invalid_priority_is_reported(self):
        self.document.write_text(DOCUMENT.replace("(Must)", "(Urgente)"), encoding="utf-8")
        self.assertIn("requests-lifecycle/prd.md: REQ-100 has no valid MoSCoW priority", check(self.folder))

    def test_missing_priority_is_reported(self):
        self.document.write_text(DOCUMENT + "\n## Requisitos não funcionais\n- **REQ-101** Limite definido.\n", encoding="utf-8")
        self.assertIn("requests-lifecycle/prd.md: REQ-101 has no valid MoSCoW priority", check(self.folder))

    def test_prefix_shared_by_two_prds_is_reported(self):
        write_prd(self.folder, "other", DOCUMENT.replace("REQ-100", "REQ-101"))
        self.assertTrue(any("prefix: REQ belongs to several PRDs" in f for f in check(self.folder)))

    def test_several_prefixes_in_one_prd_are_reported(self):
        self.document.write_text(DOCUMENT + "- **ALT-01 (Could)** Outra capability.\n", encoding="utf-8")
        self.assertTrue(any("definitions use several prefixes: ALT, REQ" in f for f in check(self.folder)))

    def test_definition_inside_code_fence_is_ignored(self):
        self.document.write_text(DOCUMENT + "\n```markdown\n- **REQ-100 (Must)** Exemplo.\n```\n", encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_missing_local_file_is_reported(self):
        self.document.write_text(DOCUMENT + "\n[Definição](missing.md)\n", encoding="utf-8")
        self.assertTrue(any("local link does not resolve" in f for f in check(self.folder)))

    def test_links_resolve_from_the_document_folder(self):
        (self.document.parent / "spec.md").write_text("# Spec\n", encoding="utf-8")
        (self.folder / "overview.md").write_text("[PRD](requests-lifecycle/prd.md)\n", encoding="utf-8")
        self.document.write_text(DOCUMENT + "\n[Spec](spec.md) [Visão geral](../overview.md)\n", encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_anchor_and_external_links_are_not_local_files(self):
        self.document.write_text(DOCUMENT + "\n[Topo](#solicitações) [Fonte](https://example.com)\n", encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_unclosed_fence_is_reported(self):
        self.document.write_text(DOCUMENT + "\n```mermaid\nflowchart LR\n", encoding="utf-8")
        self.assertTrue(any("unclosed code fence" in f for f in check(self.folder)))

    def test_empty_input_is_an_error(self):
        with TemporaryDirectory() as empty:
            (Path(empty) / "overview.md").write_text("# Visão geral\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "no PRDs"):
                check(empty)


class PrdCommandLine(unittest.TestCase):
    def test_exit_codes(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            self.assertEqual(2, run_cli(folder).returncode)
            write_prd(folder, "requests", DOCUMENT)
            self.assertEqual(0, run_cli(folder).returncode)
            write_prd(folder, "other", DOCUMENT.replace("REQ-100", "REQ-101"))
            result = run_cli(folder)
            self.assertEqual(1, result.returncode)
            self.assertIn("prefix: REQ", result.stdout)


if __name__ == "__main__":
    unittest.main()
