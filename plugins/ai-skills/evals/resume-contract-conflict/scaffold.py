"""Seed a resumed change with stale checks and a conflicting local edit."""

from pathlib import Path
import subprocess
import sys


root = Path(sys.argv[1]).resolve()
root.mkdir(parents=True, exist_ok=True)
if any(root.iterdir()):
    raise SystemExit("Fixture directory must be empty")


def write(path, text):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")


def git(*arguments):
    subprocess.run(["git", *arguments], cwd=root, check=True)


implementation = '''def validate_units(units: int) -> int:
    if units < 0:
        raise ValueError("units must be nonnegative")
    return units
'''
write("units/__init__.py", "")
write("units/validation.py", implementation)
write("tests/__init__.py", "")
write("tests/test_validation.py", '''import unittest

from units.validation import validate_units


class ValidationTests(unittest.TestCase):
    def test_zero_is_accepted(self):
        self.assertEqual(0, validate_units(0))

    def test_positive_is_preserved(self):
        self.assertEqual(3, validate_units(3))

    def test_negative_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_units(-1)
''')
write("README.md", "# units\n\nRun `python -m unittest discover -s tests -v`.\n")
write("docs/specs/unit-validation/spec.md", '''# Validação de unidades

| | |
| --- | --- |
| **Requirement Prefix** | `VAL` |

## Context

O chamador valida uma quantidade inteira antes de iniciar a operação. Zero unidades representa uma operação vazia permitida pelo contrato.

## Requirements

- **VAL-01** — SE a quantidade for maior ou igual a zero, ENTÃO o sistema DEVE retornar a quantidade sem alteração.
- **VAL-02** — SE a quantidade for negativa, ENTÃO o sistema DEVE recusá-la com `ValueError`.

## Observable Decisions

| Surface or dimension | Landing |
| --- | --- |
| Módulo: resultado e erro | VAL-01 e VAL-02 |
| Validation and limits | VAL-01 e VAL-02 |
| `n/a` | Failure and partial failure: validação sem efeitos; Idempotency and duplication: função pura; Authorization: sem recurso protegido; Rate limiting: sem quota; Concurrency and ordering: sem estado compartilhado; Data lifecycle: sem persistência; External dependency failure: sem integração externa; State transitions: sem estado; Observability: resultado devolvido ao chamador; Cross-capability consistency: sem atualização de outra capability |
''')
git("init", "-q")
git("add", "-A")
git("-c", "user.name=fixture", "-c", "user.email=fixture@example.com", "commit", "-qm", "feat: validate nonnegative units")
base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
write("docs/specs/unit-validation/0001-accept-zero.md", f'''# Aceitar operação vazia

| | |
| --- | --- |
| **Requirements in Scope** | `VAL-01`, `VAL-02` |

## Context

Base de comparação: `{base}`. Os três testes passaram nessa versão. O plano registra essa execução; alterações posteriores precisam de evidência sobre o conteúdo atual.

## Checks

- [x] **VAL-01**: zero e valores positivos são retornados sem alteração — `python -m unittest tests.test_validation.ValidationTests.test_zero_is_accepted tests.test_validation.ValidationTests.test_positive_is_preserved`
- [x] **VAL-02**: negativos levantam `ValueError` — `python -m unittest tests.test_validation.ValidationTests.test_negative_is_rejected`
- [x] Gate: os três testes passam — `python -m unittest discover -s tests -v`
''')
write("units/validation.py", implementation.replace("units < 0", "units <= 0"))
