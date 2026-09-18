"""Regression cases for the PRD structure check, using only temporary documents."""
import importlib.util
import re
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


SCRIPT = Path(__file__).resolve().parents[1] / "plugins" / "ai-skills" / "skills" / "prd" / "scripts" / "check_prd.py"
EXAMPLE = SCRIPT.parents[1] / "references" / "example.md"

_spec = importlib.util.spec_from_file_location("check_prd", SCRIPT)
check_prd = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_prd)
check = check_prd.check


DOCUMENT = """# Solicitações

| | |
| --- | --- |
| **Originating Context** | Requests |

Requirement prefix: `REQ`.

## Executive Summary
O consumidor acompanha a solicitação.

## Context and Problem
O consumidor precisa de um resultado identificável.

## Target User / JTBD
Consumidor: consultar o resultado.

## Proposed Solution
Retornar o resultado descrito em **REQ-100**.

## Functional Requirements
- **REQ-100 (Must)** Retornar o resultado original para uma chave repetida.
"""


def run_cli(folder):
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(SCRIPT), str(folder)],
        capture_output=True, text=True, encoding="utf-8",
    )


class PrdChecks(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.document = self.folder / "0001-requests-lifecycle.md"
        self.document.write_text(DOCUMENT, encoding="utf-8")

    def test_valid_working_document_needs_no_git_commit(self):
        self.assertEqual([], check(self.folder))

    def test_skill_example_has_no_findings(self):
        example = re.search(r"^````markdown\n(.*?)^````$", EXAMPLE.read_text(encoding="utf-8"), re.M | re.S)
        self.document.write_text(example[1], encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_instructions_are_not_treated_as_prds(self):
        (self.folder / "CLAUDE.md").write_text("# Instruções\nReferência: REQ-99\n", encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_three_digit_reference_is_not_truncated(self):
        self.document.write_text(DOCUMENT + "\nConsultar REQ-101.\n", encoding="utf-8")
        self.assertTrue(any("citation REQ-101" in f for f in check(self.folder)))

    def test_undeclared_prefix_is_not_a_citation(self):
        self.document.write_text(DOCUMENT + "\nAssinatura com SHA-256 conforme ISO-27001.\n", encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_unprefixed_id_is_reported(self):
        self.document.write_text(DOCUMENT + "\nVer FR-12.\n", encoding="utf-8")
        self.assertTrue(any("unprefixed id FR-12" in f for f in check(self.folder)))

    def test_duplicate_definition_is_reported(self):
        self.document.write_text(DOCUMENT + "\n- **REQ-100 (Must)** Outro resultado.\n", encoding="utf-8")
        self.assertTrue(any("REQ-100 defined 2 times" in f for f in check(self.folder)))

    def test_invalid_priority_and_nfr_priority_are_reported(self):
        self.document.write_text(DOCUMENT.replace("(Must)", "(Urgent)") + "\n- **REQ-NFR-01 (Must)** Limite definido.\n", encoding="utf-8")
        findings = check(self.folder)
        self.assertTrue(any("no valid MoSCoW" in f for f in findings))
        self.assertTrue(any("NFR REQ-NFR-01 carries" in f for f in findings))

    def test_missing_local_file_is_reported(self):
        self.document.write_text(DOCUMENT + "\n[Definição](missing.md)\n", encoding="utf-8")
        self.assertTrue(any("local link does not resolve" in f for f in check(self.folder)))

    def test_anchor_and_external_links_are_not_local_files(self):
        self.document.write_text(DOCUMENT + "\n[Topo](#solicitações) [Fonte](https://example.com)\n", encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_unclosed_diagram_is_reported(self):
        self.document.write_text(DOCUMENT + "\n```mermaid\nflowchart LR\n", encoding="utf-8")
        self.assertTrue(any("unclosed code fence" in f for f in check(self.folder)))

    def test_section_after_weakest_point_is_reported(self):
        self.document.write_text(DOCUMENT + "\n## Weakest Point\nDecisão frágil.\n\n## Non-goals\nNada adjacente.\n", encoding="utf-8")
        findings = check(self.folder)
        self.assertTrue(any("only References may follow Weakest Point" in f for f in findings))

    def test_empty_input_is_an_error(self):
        with TemporaryDirectory() as empty:
            with self.assertRaisesRegex(ValueError, "no numbered PRDs"):
                check(empty)

    def test_duplicate_number_is_reported(self):
        (self.folder / "0001-other.md").write_text(DOCUMENT.replace("REQ", "ALT"), encoding="utf-8")
        self.assertTrue(any("numbering: 0001" in f for f in check(self.folder)))

    def test_duplicate_prefix_is_reported(self):
        (self.folder / "0002-other.md").write_text(DOCUMENT.replace("REQ-100", "REQ-101"), encoding="utf-8")
        self.assertTrue(any("prefix: REQ belongs" in f for f in check(self.folder)))

    def test_foreign_definition_is_reported(self):
        self.document.write_text(DOCUMENT.replace("REQ-100", "ALT-100"), encoding="utf-8")
        self.assertTrue(any("foreign prefix" in f for f in check(self.folder)))


class PrdCommandLine(unittest.TestCase):
    def test_exit_codes(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            self.assertEqual(2, run_cli(folder).returncode)
            (folder / "0001-requests.md").write_text(DOCUMENT, encoding="utf-8")
            self.assertEqual(0, run_cli(folder).returncode)
            (folder / "0001-other.md").write_text(DOCUMENT.replace("REQ", "ALT"), encoding="utf-8")
            result = run_cli(folder)
            self.assertEqual(1, result.returncode)
            self.assertIn("numbering: 0001", result.stdout)


if __name__ == "__main__":
    unittest.main()
