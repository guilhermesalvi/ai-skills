"""Regression cases for the spec ID and link check, using only temporary documents."""
import importlib.util
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


SCRIPT = Path(__file__).resolve().parents[1] / "plugins" / "ai-skills" / "skills" / "sdd" / "scripts" / "check_spec.py"
EXAMPLE = SCRIPT.parents[1] / "references" / "spec-example.md"
# Keep bytecode out of the skill folder, which a local plugin install copies as is.
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
sys.dont_write_bytecode = True

_spec = importlib.util.spec_from_file_location("check_spec", SCRIPT)
check_spec = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_spec)


def check(folder):
    return check_spec.check(folder)[0]


DOCUMENT = """# Solicitações

| | |
| --- | --- |
| **Requirement Prefix** | `REQ` |

## Context
O consumidor repete solicitações quando a rede falha.

## Requirements
- **REQ-100** — QUANDO a chave se repetir, ENTÃO o sistema DEVE retornar o resultado original.

## Acceptance Scenarios
Repetir a chave retorna o resultado de REQ-100.
"""

PLAN = """# Repetição de solicitações

## Assumptions

- **O armazenamento aceita índice único.** O banco atual oferece. Se for falsa, a garantia muda de mecanismo. Confirmed? n

## Checks

- [ ] **REQ-100**: repetir a chave retorna o original — `dotnet test --filter RepeatReturnsOriginal`
- [x] Gate — `dotnet test`
"""

ENGLISH = """# Requests

| | |
| --- | --- |
| **Requirement Prefix** | `ENG` |

## Context
Clients retry requests after network failures.

## Requirements
- **ENG-01** — WHEN a key repeats THEN the system SHALL return the original result.
- **ENG-02** — The system SHALL reject a key longer than 64 characters.
"""


def run_cli(folder):
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(SCRIPT), str(folder)],
        capture_output=True, text=True, encoding="utf-8", env=ENV,
    )


def write_spec(folder, capability, text):
    path = Path(folder) / capability / "spec.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


class SpecChecks(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.document = write_spec(self.folder, "requests-lifecycle", DOCUMENT)

    def test_valid_document_has_no_findings(self):
        self.assertEqual([], check(self.folder))

    def test_titles_in_any_language_are_accepted(self):
        write_spec(self.folder, "requests-en", ENGLISH)
        self.assertEqual([], check(self.folder))

    def test_skill_example_has_no_findings(self):
        example = re.search(r"^````markdown\n(.*?)^````$", EXAMPLE.read_text(encoding="utf-8"), re.M | re.S)
        self.document.write_text(example[1], encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_instructions_outside_capabilities_are_not_read(self):
        (self.folder / "CLAUDE.md").write_text("# Instruções\nReferência: REQ-99\n", encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_plan_citations_are_checked(self):
        legacy = self.document.parent / "0001-retry"
        legacy.mkdir()
        (self.document.parent / "0002-limit.md").write_text("- [ ] REQ-100: repetição\n- [ ] REQ-103: limite\n", encoding="utf-8")
        (legacy / "tasks.md").write_text("Atende REQ-102.\n", encoding="utf-8")
        self.assertEqual([
            "requests-lifecycle/0001-retry/tasks.md: citation REQ-102 has no definition",
            "requests-lifecycle/0002-limit.md: citation REQ-103 has no definition",
        ], check(self.folder))

    def test_legacy_prd_prefixes_are_not_citations(self):
        (self.document.parent / "prd.md").write_text("- **PRX-01 (Must)** Regra de produto.\n", encoding="utf-8")
        self.document.write_text(DOCUMENT + "\nOrigem: PRX-01 e PRX-02.\n", encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_three_digit_citation_is_not_truncated(self):
        self.document.write_text(DOCUMENT + "\nConsultar REQ-101.\n", encoding="utf-8")
        self.assertIn("requests-lifecycle/spec.md: citation REQ-101 has no definition", check(self.folder))

    def test_undefined_prefix_is_not_a_citation(self):
        self.document.write_text(DOCUMENT + "\nAssinatura com SHA-256 conforme ISO-27001.\n", encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_citation_of_another_spec_resolves(self):
        write_spec(self.folder, "requests-en", ENGLISH + "\nDepends on REQ-100.\n")
        self.assertEqual([], check(self.folder))

    def test_unprefixed_id_is_reported(self):
        self.document.write_text(DOCUMENT + "\nVer FR-12.\n", encoding="utf-8")
        self.assertTrue(any("unprefixed id FR-12" in f for f in check(self.folder)))

    def test_duplicate_definition_is_reported(self):
        self.document.write_text(DOCUMENT + "\n- **REQ-100** — Outro resultado.\n", encoding="utf-8")
        self.assertIn("ids: REQ-100 defined 2 times", check(self.folder))

    def test_prefix_shared_by_two_specs_is_reported(self):
        write_spec(self.folder, "other", DOCUMENT.replace("REQ-100", "REQ-101"))
        self.assertTrue(any("prefix: REQ belongs to several specs" in f for f in check(self.folder)))

    def test_several_prefixes_in_one_spec_are_reported(self):
        self.document.write_text(DOCUMENT + "- **ALT-01** — Outra capability.\n", encoding="utf-8")
        self.assertTrue(any("definitions use several prefixes: ALT, REQ" in f for f in check(self.folder)))

    def test_header_prefix_must_match_definitions(self):
        self.document.write_text(DOCUMENT.replace("`REQ` |", "`RQS` |"), encoding="utf-8")
        self.assertIn("requests-lifecycle/spec.md: Requirement Prefix RQS differs from the definitions", check(self.folder))

    def test_missing_header_and_base_section_are_reported(self):
        text = DOCUMENT.replace("| **Requirement Prefix** | `REQ` |\n", "").replace("## Context\n", "## Background\n")
        self.document.write_text(text, encoding="utf-8")
        findings = check(self.folder)
        self.assertIn("requests-lifecycle/spec.md: missing Requirement Prefix in the header", findings)
        self.assertIn("requests-lifecycle/spec.md: missing section Context", findings)

    def test_empty_section_is_reported(self):
        self.document.write_text(DOCUMENT + "\n## Glossary\n\n", encoding="utf-8")
        self.assertEqual(["requests-lifecycle/spec.md: empty section Glossary"], check(self.folder))

    def test_assumption_without_confirmation_is_reported(self):
        assumptions = "\n## Assumptions\n\n- **Chave por cliente.** Inferida do cadastro.\n  Se falsa, muda o escopo.\n"
        self.document.write_text(DOCUMENT + assumptions, encoding="utf-8")
        self.assertTrue(any("assumption without Confirmed?" in f for f in check(self.folder)))

    def test_gap_row_with_empty_cell_is_reported(self):
        gaps = "\n## Gaps\n\n| Gap | Affects | Owner |\n| --- | --- | --- |\n| Prazo da chave | REQ-100 | |\n"
        self.document.write_text(DOCUMENT + gaps, encoding="utf-8")
        self.assertTrue(any("Gaps row with an empty cell" in f for f in check(self.folder)))

    def test_legacy_titles_are_not_checked_for_structure(self):
        self.document.write_text("# Solicitações\n\n## Requisitos\n- **REQ-100** — Resultado original.\n\n## Trade-offs\n| Decisão | Custo | Motivo |\n", encoding="utf-8")
        self.assertEqual(([], ["requests-lifecycle/spec.md"]), check_spec.check(self.folder))

    def test_valid_plan_has_no_findings(self):
        (self.document.parent / "0001-retry.md").write_text(PLAN, encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_check_without_proof_or_checkbox_is_reported(self):
        plan = PLAN.replace(" — `dotnet test --filter RepeatReturnsOriginal`", "").replace("- [x] Gate", "- Gate")
        (self.document.parent / "0001-retry.md").write_text(plan, encoding="utf-8")
        findings = check(self.folder)
        self.assertTrue(any("check without proof: - [ ] **REQ-100**" in f for f in findings))
        self.assertTrue(any("check is not a checkbox: - Gate" in f for f in findings))

    def test_proof_must_close_the_check(self):
        plan = PLAN.replace("- [x] Gate — `dotnet test`", "- [x] Criar `NATAL10` funciona")
        (self.document.parent / "0001-retry.md").write_text(plan, encoding="utf-8")
        self.assertTrue(any("check without proof: - [x] Criar `NATAL10`" in f for f in check(self.folder)))

    def test_plan_links_are_checked(self):
        (self.document.parent / "0001-retry.md").write_text(PLAN + "\n[Spec](spec.md) [ADR](missing.md)\n", encoding="utf-8")
        self.assertEqual(["requests-lifecycle/0001-retry.md: local link does not resolve: missing.md"], check(self.folder))

    def test_plan_without_checks_is_reported(self):
        (self.document.parent / "0001-retry.md").write_text(PLAN.split("## Checks")[0], encoding="utf-8")
        self.assertIn("requests-lifecycle/0001-retry.md: missing section Checks", check(self.folder))

    def test_decision_row_with_empty_cell_is_reported(self):
        table = ("\n## Technical Decisions\n\n| Decision | Choice | Rejected alternatives | Cost | Reversible |\n"
                 "| --- | --- | --- | --- | --- |\n| Unicidade | Índice único | | Migração | Não |\n")
        (self.document.parent / "0001-retry.md").write_text(PLAN + table, encoding="utf-8")
        self.assertTrue(any("Technical Decisions row with an empty cell" in f for f in check(self.folder)))

    def test_definition_inside_code_fence_is_ignored(self):
        self.document.write_text(DOCUMENT + "\n```markdown\n- **REQ-100** — Exemplo.\n```\n", encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_missing_local_file_is_reported(self):
        self.document.write_text(DOCUMENT + "\n[Plano](0001-missing.md)\n", encoding="utf-8")
        self.assertTrue(any("local link does not resolve" in f for f in check(self.folder)))

    def test_links_resolve_from_the_document_folder(self):
        (self.document.parent / "0001-retry.md").write_text("# Plano\n", encoding="utf-8")
        write_spec(self.folder, "requests-en", ENGLISH)
        self.document.write_text(DOCUMENT + "\n[Plano](0001-retry.md) [Outra](../requests-en/spec.md)\n", encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_anchor_and_external_links_are_not_local_files(self):
        self.document.write_text(DOCUMENT + "\n[Topo](#solicitações) [Fonte](https://example.com)\n", encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_unclosed_fence_is_reported(self):
        self.document.write_text(DOCUMENT + "\n```mermaid\nflowchart LR\n", encoding="utf-8")
        self.assertTrue(any("unclosed code fence" in f for f in check(self.folder)))

    def test_empty_input_is_an_error(self):
        with TemporaryDirectory() as empty:
            (Path(empty) / "requests").mkdir()
            (Path(empty) / "requests" / "0001-retry.md").write_text("# Plano\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "no specs"):
                check(empty)


class SpecCommandLine(unittest.TestCase):
    def test_exit_codes(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            self.assertEqual(2, run_cli(folder).returncode)
            write_spec(folder, "requests", DOCUMENT)
            self.assertEqual(0, run_cli(folder).returncode)
            write_spec(folder, "other", DOCUMENT.replace("REQ-100", "REQ-101"))
            result = run_cli(folder)
            self.assertEqual(1, result.returncode)
            self.assertIn("prefix: REQ", result.stdout)
