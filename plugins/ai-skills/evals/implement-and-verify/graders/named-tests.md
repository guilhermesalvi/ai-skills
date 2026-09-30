---
type: regex
target: { source: file, path: tests/test_orders.py }
pattern: '^(?=[\s\S]*def test_customer_cancels_pending_order)(?=[\s\S]*def test_other_customer_cannot_cancel)(?=[\s\S]*def test_cancel_rejected_outside_pending)(?=[\s\S]*def test_cancelled_order_rejects_transitions)(?=[\s\S]*def test_cancellation_contract)'
---

Os testes têm os nomes que as provas do plano citam.
