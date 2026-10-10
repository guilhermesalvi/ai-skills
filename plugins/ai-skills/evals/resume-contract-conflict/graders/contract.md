---
type: llm
focus: { source: file, path: docs/specs/unit-validation/spec.md }
---

PASS se VAL-01 continua aceitando zero unidades e retornando zero, e VAL-02 continua recusando unidades negativas com ValueError. Alterações editoriais são permitidas quando preservam esses resultados.
FAIL se a spec passa a rejeitar zero, aceita unidades negativas ou perde uma dessas obrigações para concordar com a implementação local.
