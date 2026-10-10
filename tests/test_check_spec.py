"""Regression cases for the spec ID, link and schema check, using only temporary documents."""
import importlib.util
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


SCRIPT = Path(__file__).resolve().parents[1] / "plugins" / "ai-skills" / "skills" / "sdd" / "scripts" / "check_spec.py"
SKILL = SCRIPT.parents[1]
EXAMPLE = SKILL / "references" / "spec-example.md"
# Keep bytecode out of the skill folder, which a local plugin install copies as is.
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
sys.dont_write_bytecode = True

_spec = importlib.util.spec_from_file_location("check_spec", SCRIPT)
check_spec = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_spec)


def check(folder):
    return check_spec.check(folder)


NOT_APPLICABLE = "; ".join(f"{dimension}: fora do módulo" for dimension in check_spec.DIMENSIONS
                           if dimension != "Idempotency and duplication")

SPEC_SECTIONS = {
    "Context": "O consumidor repete solicitações quando a rede falha.",
    "Requirements": "- **REQ-100** — QUANDO a chave se repetir, ENTÃO o sistema DEVE retornar o resultado original.",
    "Acceptance Scenarios": "Repetir a chave retorna o resultado de REQ-100.",
    "Observable Decisions": ("| Surface or dimension | Landing |\n| --- | --- |\n"
                             f"| Idempotency and duplication | REQ-100 |\n| `n/a` | {NOT_APPLICABLE} |"),
}


def document(extra=None, drop=(), header="| **Requirement Prefix** | `REQ` |\n", title="Solicitações"):
    """Render a spec with the given sections in the schema order and unknown titles at the end."""
    parts = {**SPEC_SECTIONS, **(extra or {})}
    order = [t for t in check_spec.SPEC_SECTIONS if t in parts] + [t for t in parts if t not in check_spec.SPEC_SECTIONS]
    body = "".join(f"\n## {t}\n\n{parts[t]}\n" for t in order if t not in drop)
    return f"# {title}\n\n| | |\n| --- | --- |\n{header}{body}"


DOCUMENT = document()

PLAN = """# Repetição de solicitações

| | |
| --- | --- |
| **Requirements in Scope** | `REQ-100` |

## Assumptions

- **O armazenamento aceita índice único.** A configuração do banco ainda precisa ser conferida. Se não houver esse recurso, a garantia precisará de outro mecanismo.

## Checks

- [ ] **REQ-100**: repetir a chave retorna o original — `dotnet test --filter RepeatReturnsOriginal`
- [x] Gate — `dotnet test`
"""

ENGLISH = document({"Context": "Clients retry requests after network failures.",
                    "Requirements": ("- **ENG-01** — WHEN a key repeats THEN the system SHALL return the original result.\n"
                                     "- **ENG-02** — The system SHALL reject a key longer than 64 characters."),
                    "Acceptance Scenarios": "Repeating the key returns the result of ENG-01.",
                    "Observable Decisions": SPEC_SECTIONS["Observable Decisions"].replace("REQ-100", "ENG-01")},
                   header="| **Requirement Prefix** | `ENG` |\n", title="Requests")


def run_cli(folder):
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(SCRIPT), str(folder)],
        capture_output=True, text=True, encoding="utf-8", env=ENV,
    )


def git(folder, *args):
    subprocess.run(["git", "-C", str(folder), *args], check=True, capture_output=True)


def commit_all(folder):
    """Commit the folder as HEAD to exercise checks against recorded artifacts."""
    if not (Path(folder) / ".git").exists():
        git(folder, "init", "-q")
    git(folder, "add", "-A")
    git(folder, "-c", "user.name=test", "-c", "user.email=test@example.com", "commit", "-qm", "base")


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

    def test_prose_in_any_language_is_accepted(self):
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
        (legacy / "tasks.md").write_text("Atende REQ-102.\n", encoding="utf-8")
        self.assertEqual(["requests-lifecycle/0001-retry/tasks.md: citation REQ-102 has no definition"],
                         check(self.folder))

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
        self.document.write_text(document(drop=("Context",), header=""), encoding="utf-8")
        findings = check(self.folder)
        self.assertIn("requests-lifecycle/spec.md: missing Requirement Prefix in the header", findings)
        self.assertIn("requests-lifecycle/spec.md: missing section Context", findings)

    def test_empty_section_is_reported(self):
        self.document.write_text(document({"Glossary": ""}), encoding="utf-8")
        self.assertEqual(["requests-lifecycle/spec.md: empty section Glossary"], check(self.folder))

    def test_gap_row_with_empty_cell_is_reported(self):
        gaps = "| Gap | Affects | Owner |\n| --- | --- | --- |\n| Prazo da chave | REQ-100 | |"
        self.document.write_text(document({"Gaps": gaps}), encoding="utf-8")
        self.assertTrue(any("Gaps row with an empty cell" in f for f in check(self.folder)))

    def test_placeholder_cell_is_reported_and_unknown_owner_is_accepted(self):
        gaps = "| Gap | Affects | Owner |\n| --- | --- | --- |\n| Prazo da chave | REQ-100 | ? |\n| Limite | TBD | Operação |"
        self.document.write_text(document({"Gaps": gaps}), encoding="utf-8")
        self.assertEqual(["requests-lifecycle/spec.md: Gaps row with a placeholder cell: Limite | TBD | Operação"],
                         check(self.folder))

    def test_template_field_is_reported(self):
        self.document.write_text(document({"Scope": "{{O que entra e o que fica fora}}"}), encoding="utf-8")
        self.assertEqual(["requests-lifecycle/spec.md: template field left: {{O que entra e o que fica fora}}"],
                         check(self.folder))

    def test_definition_inside_code_fence_is_ignored(self):
        self.document.write_text(DOCUMENT + "\n```markdown\n- **REQ-100** — Exemplo.\n```\n", encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_missing_local_file_is_reported(self):
        self.document.write_text(DOCUMENT + "\n[Plano](0001-missing.md)\n", encoding="utf-8")
        self.assertTrue(any("local link does not resolve" in f for f in check(self.folder)))

    def test_links_resolve_from_the_document_folder(self):
        (self.document.parent / "notes.md").write_text("# Notas\n", encoding="utf-8")
        write_spec(self.folder, "requests-en", ENGLISH)
        self.document.write_text(DOCUMENT + "\n[Notas](notes.md) [Outra](../requests-en/spec.md)\n", encoding="utf-8")
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


class NewArtifacts(unittest.TestCase):
    """Validate the schema of uncommitted artifacts."""

    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.document = write_spec(self.folder, "requests-lifecycle", DOCUMENT)

    def test_translated_titles_are_reported(self):
        self.document.write_text("# Solicitações\n\n## Contexto\n\nAlgo.\n\n## Requisitos\n\n- **REQ-100** — Resultado.\n",
                                 encoding="utf-8")
        findings = check(self.folder)
        self.assertIn("requests-lifecycle/spec.md: section Contexto is not in the schema", findings)
        self.assertIn("requests-lifecycle/spec.md: missing section Requirements", findings)
        self.assertIn("requests-lifecycle/spec.md: missing Requirement Prefix in the header", findings)

    def test_unknown_section_and_order_are_reported(self):
        text = document({"State Transitions": "| State | Identifier |"}).replace("## Context", "## Scope\n\nTudo.\n\n## Context")
        self.document.write_text(text, encoding="utf-8")
        findings = check(self.folder)
        self.assertIn("requests-lifecycle/spec.md: section State Transitions is not in the schema", findings)
        self.assertTrue(any("sections are out of the schema order" in f for f in findings))

    def test_minimal_spec_does_not_need_observable_decisions(self):
        self.document.write_text(document(drop=("Observable Decisions",)), encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_only_relevant_dimensions_are_accepted(self):
        table = "| Surface or dimension | Landing |\n| --- | --- |\n| Idempotency and duplication | REQ-100 |"
        self.document.write_text(document({"Observable Decisions": table}), encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_legacy_not_applicable_entry_still_needs_a_reason(self):
        table = SPEC_SECTIONS["Observable Decisions"].replace("Authorization: fora do módulo", "Authorization")
        self.document.write_text(document({"Observable Decisions": table}), encoding="utf-8")
        findings = check(self.folder)
        self.assertEqual(1, len(findings))
        self.assertIn("n/a entry needs a dimension and reason: Authorization", findings[0])

    def test_not_applicable_entry_citing_a_requirement_is_reported(self):
        table = SPEC_SECTIONS["Observable Decisions"].replace("Observability: fora do módulo",
                                                               "Observability: coberta por REQ-100")
        self.document.write_text(document({"Observable Decisions": table}), encoding="utf-8")
        self.assertEqual(["requests-lifecycle/spec.md: n/a entry cites a requirement, so the dimension applies; "
                          "give it its own row: Observability: coberta por REQ-100"], check(self.folder))

    def test_dimension_marked_not_applicable_in_its_own_row_is_reported(self):
        table = SPEC_SECTIONS["Observable Decisions"] + "\n| Observability | `n/a`: sem métricas |"
        self.document.write_text(document({"Observable Decisions": table}), encoding="utf-8")
        self.assertEqual(["requests-lifecycle/spec.md: Observability is marked n/a in its own row; "
                          "move it to the single n/a row"], check(self.folder))

    def test_empty_header_row_is_reported(self):
        self.document.write_text(document(header="| **Requirement Prefix** | `REQ` |\n| **Affected Capabilities** | |\n"),
                                 encoding="utf-8")
        self.assertEqual(["requests-lifecycle/spec.md: header row Affected Capabilities is empty; "
                          "delete the row when it does not apply"], check(self.folder))

    def test_assumptions_accept_natural_prose_in_either_language(self):
        for item in (
            "- **Chave por cliente.** Inferida do cadastro; se a chave for global, muda o escopo.",
            "- **Keys belong to a customer.** Inferred from registration. Global keys would change the scope.",
            "- **Chave por cliente.** Inferida do cadastro.\n  Se a chave for global, muda o escopo.",
        ):
            with self.subTest(item=item):
                self.document.write_text(document({"Assumptions": item}), encoding="utf-8")
                self.assertEqual([], check(self.folder))

    def test_assumption_needs_a_statement_and_explanation(self):
        for item in ("- Chave por cliente. Inferida do cadastro.", "- **Chave por cliente.**", "- ** ** Explicação."):
            with self.subTest(item=item):
                self.document.write_text(document({"Assumptions": item}), encoding="utf-8")
                self.assertTrue(any("assumption needs a bold title followed by explanation" in f
                                    for f in check(self.folder)))


class Plans(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.document = write_spec(self.folder, "requests-lifecycle", DOCUMENT)
        self.plan = self.document.parent / "0001-retry.md"

    def write_plan(self, text):
        self.plan.write_text(text, encoding="utf-8")

    def test_valid_plan_has_no_findings(self):
        self.write_plan(PLAN)
        self.assertEqual([], check(self.folder))

    def test_new_plan_assumption_uses_the_same_structure_check(self):
        self.write_plan(PLAN.replace("**O armazenamento aceita índice único.**", "O armazenamento aceita índice único."))
        self.assertTrue(any("0001-retry.md: assumption needs" in f for f in check(self.folder)))

    def test_check_without_proof_or_checkbox_is_reported(self):
        self.write_plan(PLAN.replace(" — `dotnet test --filter RepeatReturnsOriginal`", "").replace("- [x] Gate", "- Gate"))
        findings = check(self.folder)
        self.assertTrue(any("check without proof: - [ ] **REQ-100**" in f for f in findings))
        self.assertTrue(any("check is not a checkbox: - Gate" in f for f in findings))

    def test_proof_must_close_the_check(self):
        self.write_plan(PLAN.replace("- [x] Gate — `dotnet test`", "- [x] Criar `NATAL10` funciona"))
        self.assertTrue(any("check without proof: - [x] Criar `NATAL10`" in f for f in check(self.folder)))

    def test_placeholder_proof_is_reported(self):
        self.write_plan(PLAN.replace("`dotnet test --filter RepeatReturnsOriginal`", "`TBD`"))
        self.assertTrue(any("check with a placeholder proof: - [ ] **REQ-100**" in f for f in check(self.folder)))

    def test_plan_links_are_checked(self):
        self.write_plan(PLAN + "\n[Spec](spec.md) [ADR](missing.md)\n")
        self.assertEqual(["requests-lifecycle/0001-retry.md: local link does not resolve: missing.md"], check(self.folder))

    def test_plan_without_checks_is_reported(self):
        self.write_plan(PLAN.split("## Checks")[0])
        self.assertIn("requests-lifecycle/0001-retry.md: missing section Checks", check(self.folder))

    def test_decision_row_with_empty_cell_is_reported(self):
        table = ("\n## Technical Decisions\n\n| Decision | Choice | Rejected alternatives | Cost | Reversible |\n"
                 "| --- | --- | --- | --- | --- |\n| Unicidade | Índice único | | Migração | Não |\n")
        self.write_plan(PLAN.replace("\n## Assumptions", table + "\n## Assumptions"))
        self.assertTrue(any("Technical Decisions row with an empty cell" in f for f in check(self.folder)))

    def test_new_plan_needs_requirements_in_scope(self):
        self.write_plan(PLAN.replace("| **Requirements in Scope** | `REQ-100` |\n", ""))
        self.assertEqual(["requests-lifecycle/0001-retry.md: missing Requirements in Scope in the header"],
                         check(self.folder))

    def test_requirement_in_scope_needs_a_check(self):
        self.document.write_text(document({"Requirements": SPEC_SECTIONS["Requirements"] + "\n- **REQ-101** — Limite."}),
                                 encoding="utf-8")
        self.write_plan(PLAN.replace("`REQ-100` |", "`REQ-100`, `REQ-101` |"))
        self.assertEqual(["requests-lifecycle/0001-retry.md: requirement REQ-101 in scope has no check"], check(self.folder))

    def test_check_outside_scope_is_reported(self):
        self.write_plan(PLAN.replace("`REQ-100` |", "none |"))
        self.assertEqual(["requests-lifecycle/0001-retry.md: check cites REQ-100 outside Requirements in Scope"],
                         check(self.folder))

    def test_scope_without_ids_is_reported(self):
        self.write_plan(PLAN.replace("`REQ-100` |", "todos |"))
        self.assertIn("requests-lifecycle/0001-retry.md: Requirements in Scope lists no ID; write none when the change "
                      "alters no requirement", check(self.folder))

    def test_plan_citation_without_definition_is_reported(self):
        self.write_plan(PLAN + "\nDepende de REQ-103.\n")
        self.assertEqual(["requests-lifecycle/0001-retry.md: citation REQ-103 has no definition"], check(self.folder))

    def test_two_plans_with_one_number_are_reported(self):
        self.write_plan(PLAN)
        (self.document.parent / "0001-limit.md").write_text(PLAN, encoding="utf-8")
        self.assertEqual(["requests-lifecycle: plan number 0001 used by 0001-limit.md, 0001-retry.md"], check(self.folder))


class GroupedBehaviors(unittest.TestCase):
    def test_nested_specs_resolve_cross_behavior_ids_and_links(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            first = write_spec(folder, "orders/cancel-order", document(drop=("Observable Decisions",)))
            second = write_spec(folder, "orders/repeat-request", ENGLISH)
            first.write_text(first.read_text(encoding="utf-8") + "\nContrato de [repetição](../repeat-request/spec.md): ENG-01.\n",
                             encoding="utf-8")
            (first.parent / "0001-change.md").write_text(PLAN, encoding="utf-8")
            (second.parent / "0001-change.md").write_text(PLAN.replace("REQ-100", "ENG-01"), encoding="utf-8")
            (folder / "orders/CLAUDE.md").write_text("Regras: REQ-99", encoding="utf-8")
            self.assertEqual([], check(folder))
            second.write_text(ENGLISH.replace("ENG-01", "ENG-03"), encoding="utf-8")
            self.assertTrue(any("cancel-order/spec.md: citation ENG-01 has no definition" in f for f in check(folder)))

    def test_same_behavior_name_in_distinct_groups_has_its_own_plan_sequence(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            for grouping, prefix in (("orders", "REQ"), ("invoices", "INV")):
                spec = write_spec(folder, f"{grouping}/cancel", DOCUMENT.replace("REQ", prefix))
                (spec.parent / "0001-cancel.md").write_text(PLAN.replace("REQ", prefix), encoding="utf-8")
            self.assertEqual([], check(folder))
            (spec.parent / "0001-other.md").write_text(PLAN.replace("REQ", prefix), encoding="utf-8")
            self.assertEqual(["invoices/cancel: plan number 0001 used by 0001-cancel.md, 0001-other.md"], check(folder))


class ExecutionGraph(unittest.TestCase):
    setUp = Plans.setUp
    write_plan = Plans.write_plan

    TABLE = """## Execution

| Item | Outcome | Depends on | Context | Checks |
| --- | --- | --- | --- | --- |
| storage-rule | Restrição de unicidade disponível | none | [Contrato](spec.md) | REQ-100 |
| request-result | Repetição integrada ao armazenamento | storage-rule | [Contrato](spec.md) | REQ-100, Gate |

"""

    def test_valid_dependency_graph_is_accepted(self):
        self.write_plan(PLAN.replace("## Checks", self.TABLE + "## Checks"))
        self.assertEqual([], check(self.folder))

    def test_dependency_order_in_table_does_not_matter(self):
        lines = self.TABLE.splitlines()
        lines[4], lines[5] = lines[5], lines[4]
        self.write_plan(PLAN.replace("## Checks", "\n".join(lines) + "\n## Checks"))
        self.assertEqual([], check(self.folder))

    def test_unknown_dependency_is_reported(self):
        self.write_plan(PLAN.replace("## Checks", self.TABLE.replace("| storage-rule | [Contrato]", "| absent | [Contrato]") + "## Checks"))
        self.assertTrue(any("request-result depends on unknown absent" in f for f in check(self.folder)))

    def test_self_dependency_is_reported(self):
        self.write_plan(PLAN.replace("## Checks", self.TABLE.replace("| none |", "| storage-rule |") + "## Checks"))
        self.assertTrue(any("storage-rule depends on itself" in f for f in check(self.folder)))

    def test_cycle_and_its_blocked_dependents_are_reported(self):
        self.write_plan(PLAN.replace("## Checks", self.TABLE.replace("| none |", "| request-result |") + "## Checks"))
        self.assertTrue(any("Execution dependency cycle blocks: request-result, storage-rule" in f for f in check(self.folder)))

    def test_duplicate_item_is_reported(self):
        self.write_plan(PLAN.replace("## Checks", self.TABLE.replace("| request-result |", "| storage-rule |") + "## Checks"))
        self.assertTrue(any("duplicate Execution item: storage-rule" in f for f in check(self.folder)))

    def test_malformed_execution_table_is_reported(self):
        for table, expected in ((self.TABLE.replace("| Depends on |", "| Dependencies |"), "Execution needs columns"),
                                (self.TABLE.replace("| request-result |", "| RequestResult |"), "invalid Execution item name"),
                                (self.TABLE.replace("| REQ-100, Gate |", "|"), "Execution row needs 5 cells"),
                                ("\n".join(self.TABLE.splitlines()[:4]), "Execution has no items")):
            with self.subTest(expected=expected):
                self.write_plan(PLAN.replace("## Checks", table + "\n## Checks"))
                self.assertTrue(any(expected in f for f in check(self.folder)))


class CommittedArtifacts(unittest.TestCase):
    """Recorded artifacts obey the same schema; concluded plans retain historical citations."""

    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.document = write_spec(self.folder, "requests-lifecycle", DOCUMENT)

    def test_committed_artifact_with_unknown_titles_is_reported(self):
        self.document.write_text("# Solicitações\n\n## Requisitos\n- **REQ-100** — Resultado original.\n\n## Trade-offs\n"
                                 "| Decisão | Custo | Motivo |\n", encoding="utf-8")
        commit_all(self.folder)
        findings = check(self.folder)
        self.assertIn("requests-lifecycle/spec.md: section Requisitos is not in the schema", findings)
        self.assertIn("requests-lifecycle/spec.md: missing Requirement Prefix in the header", findings)

    def test_committed_minimal_spec_is_accepted(self):
        self.document.write_text(document(drop=("Observable Decisions",)), encoding="utf-8")
        commit_all(self.folder)
        self.assertEqual([], check(self.folder))

    def test_committed_assumption_without_explanation_is_reported(self):
        item = "- **Chave por cliente.**"
        self.document.write_text(document({"Assumptions": item}), encoding="utf-8")
        commit_all(self.folder)
        self.assertTrue(any("assumption needs" in f for f in check(self.folder)))
        self.document.write_text(document({"Assumptions": item + " Inferida do cadastro; se falsa, muda o escopo."}),
                                 encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_unchanged_natural_assumption_and_new_assumption_are_accepted(self):
        original = "- **Chave por cliente.** Inferida do cadastro; se falsa, muda o escopo."
        self.document.write_text(document({"Assumptions": original}), encoding="utf-8")
        commit_all(self.folder)
        added = "- **Uma solicitação por vez.** Inferida do consumidor; concorrência exigiria uma trava."
        self.document.write_text(document({"Assumptions": original + "\n" + added}), encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_committed_open_plan_needs_scope_header(self):
        plan = self.document.parent / "0001-retry.md"
        plan.write_text(PLAN.replace("| **Requirements in Scope** | `REQ-100` |\n", ""), encoding="utf-8")
        commit_all(self.folder)
        self.assertIn("requests-lifecycle/0001-retry.md: missing Requirements in Scope in the header", check(self.folder))

    def test_concluded_plan_still_needs_scope_header(self):
        plan = self.document.parent / "0001-retry.md"
        text = PLAN.replace("| **Requirements in Scope** | `REQ-100` |\n", "").replace("- [ ]", "- [x]")
        plan.write_text(text, encoding="utf-8")
        commit_all(self.folder)
        self.assertIn("requests-lifecycle/0001-retry.md: missing Requirements in Scope in the header", check(self.folder))

    def test_committed_artifact_checks_section_order_and_legacy_reasons(self):
        text = document({"Observable Decisions": "| Surface or dimension | Landing |\n| --- | --- |\n"
                                                 "| Idempotency and duplication | REQ-100 |\n| n/a | Authorization |"})
        text = text.replace("## Context", "## References")
        self.document.write_text(text, encoding="utf-8")
        commit_all(self.folder)
        findings = check(self.folder)
        self.assertTrue(any("sections are out of the schema order" in f for f in findings))
        self.assertTrue(any("n/a entry needs a dimension and reason" in f for f in findings))

    def test_concluded_plan_keeps_citations_of_retired_ids(self):
        plan = self.document.parent / "0001-retry.md"
        plan.write_text(PLAN.replace("- [ ] **REQ-100**", "- [x] **REQ-100**"), encoding="utf-8")
        commit_all(self.folder)
        self.document.write_text(DOCUMENT.replace("REQ-100", "REQ-101"), encoding="utf-8")
        self.assertEqual([], check(self.folder))

    def test_open_plan_still_reports_retired_ids(self):
        plan = self.document.parent / "0001-retry.md"
        plan.write_text(PLAN, encoding="utf-8")
        commit_all(self.folder)
        self.document.write_text(DOCUMENT.replace("REQ-100", "REQ-101"), encoding="utf-8")
        findings = check(self.folder)
        self.assertIn("requests-lifecycle/0001-retry.md: citation REQ-100 has no definition", findings)
        self.assertIn("requests-lifecycle/0001-retry.md: Requirements in Scope has undefined REQ-100", findings)


class Templates(unittest.TestCase):
    def test_templates_follow_the_schema_and_flag_their_fields(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            spec = write_spec(folder, "requests", (SKILL / "assets" / "spec.md").read_text(encoding="utf-8"))
            (spec.parent / "0001-change.md").write_text((SKILL / "assets" / "plan.md").read_text(encoding="utf-8"),
                                                       encoding="utf-8")
            findings = check(folder)
            self.assertTrue(any("requests/spec.md: template field left" in f for f in findings))
            self.assertTrue(any("requests/0001-change.md: template field left" in f for f in findings))
            schema_errors = ("not in the schema", "out of the schema order", "Observable Decisions misses",
                             "empty section", "empty cell", "placeholder", "assumption needs")
            self.assertEqual([], [f for f in findings if any(error in f for error in schema_errors)])


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
