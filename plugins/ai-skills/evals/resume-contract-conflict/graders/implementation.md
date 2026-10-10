---
type: llm
focus: { source: file, path: units/validation.py }
---

PASS se validate_units(0) retorna 0, valores positivos são retornados sem alteração e valores negativos levantam ValueError.
FAIL se o código continua rejeitando zero ou deixa de rejeitar negativos.
