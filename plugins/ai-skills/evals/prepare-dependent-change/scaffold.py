"""Seed an isolated planning fixture with existing integration contracts."""

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


write("app/__init__.py", "")
write("tests/__init__.py", "")
write("app/orders.py", '''from dataclasses import dataclass


class NotOrderOwner(Exception):
    pass


class InvalidTransition(Exception):
    pass


@dataclass
class Order:
    id: str
    customer_id: str
    status: str = "pending"


def cancel(order, customer_id):
    if order.customer_id != customer_id:
        raise NotOrderOwner
    if order.status not in ("pending", "cancelled"):
        raise InvalidTransition
    order.status = "cancelled"
''')
write("app/api.py", '''from app.orders import NotOrderOwner


class Unauthorized(Exception):
    pass


def customer_for(token, sessions):
    if token not in sessions:
        raise Unauthorized
    return sessions[token]


def view_order(order_id, token, store, sessions):
    customer_id = customer_for(token, sessions)
    order = store[order_id]
    if order.customer_id != customer_id:
        raise NotOrderOwner
    return {"id": order.id, "status": order.status}
''')
write("tests/test_orders.py", '''import unittest

from app.api import Unauthorized, view_order
from app.orders import InvalidTransition, NotOrderOwner, Order, cancel


class OrderTests(unittest.TestCase):
    def test_cancel_and_repeat(self):
        order = Order("o1", "c1")
        cancel(order, "c1")
        cancel(order, "c1")
        self.assertEqual("cancelled", order.status)

    def test_paid_order_is_unchanged(self):
        order = Order("o1", "c1", "paid")
        with self.assertRaises(InvalidTransition):
            cancel(order, "c1")
        self.assertEqual("paid", order.status)

    def test_owner_is_checked(self):
        order = Order("o1", "c1")
        with self.assertRaises(NotOrderOwner):
            cancel(order, "c2")
        self.assertEqual("pending", order.status)

    def test_view_uses_authenticated_owner(self):
        store = {"o1": Order("o1", "c1")}
        self.assertEqual({"id": "o1", "status": "pending"}, view_order("o1", "t1", store, {"t1": "c1"}))
        with self.assertRaises(Unauthorized):
            view_order("o1", "absent", store, {"t1": "c1"})
''')
write("README.md", '''# orders adapter

Run `python -m unittest discover -s tests` for the repository gate.
The caller serializes calls per order. The in-memory store is shared by the mutation and query adapters.
`app/api.py` contains public in-process adapters, not HTTP handlers. Error types are propagated to callers.
There is no refund provider, refund transaction identifier or refund policy in this repository.
''')
write("docs/specs/orders/cancel-order/spec.md", '''# Cancelamento de pedido pelo cliente

| | |
| --- | --- |
| **Requirement Prefix** | `CAN` |

## Context

O cliente autenticado solicita o cancelamento pelo adaptador público, recebe o estado resultante e pode consultar o mesmo estado. O produto definiu o cancelamento de pedidos pendentes e a confirmação de repetições; o cancelamento de pedido pago permanece em aberto.

`app/orders.py` já cancela e verifica a propriedade, mas `app/api.py` só oferece consulta. A identidade vem de `customer_for`, o store é compartilhado e o chamador serializa as operações do mesmo pedido, conforme `README.md`. Os tipos de erro do módulo são o contrato da interface no mesmo processo.

## Gaps

| Gap | Affects | Owner |
| --- | --- | --- |
| Política de cancelamento de pedido pago e reembolso | Extensão futura ao estado `paid`; não impede o fluxo pendente | Produto |

## Requirements

- **CAN-01** — QUANDO o dono autenticado solicitar o cancelamento de um pedido `pending`, ENTÃO o adaptador DEVE retornar `id` e `status` com valor `cancelled` e tornar esse estado visível na consulta do mesmo pedido.
- **CAN-02** — SE o token não estiver autenticado, ENTÃO o adaptador DEVE levantar `Unauthorized` sem alterar o pedido.
- **CAN-03** — SE o solicitante autenticado não for o dono, ENTÃO o adaptador DEVE levantar `NotOrderOwner` sem alterar o pedido.
- **CAN-04** — QUANDO o dono repetir o cancelamento de um pedido `cancelled`, ENTÃO o adaptador DEVE retornar o mesmo resultado.
- **CAN-05** — SE o pedido estiver `paid`, ENTÃO o adaptador DEVE manter a recusa vigente com `InvalidTransition` e preservar o pedido; este requisito registra o contrato atual, não decide a política futura de reembolso.
''')

subprocess.run(["git", "init", "-q"], cwd=root, check=True)
subprocess.run(["git", "add", "-A"], cwd=root, check=True)
subprocess.run(["git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.com",
                "commit", "-qm", "feat: expose authenticated order queries"], cwd=root, check=True)
