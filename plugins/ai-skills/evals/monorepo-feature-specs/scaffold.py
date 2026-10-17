"""Seed a monorepo with independent order features and an unrelated billing app."""

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


write("README.md", """# Commerce monorepo

This monorepo contains two applications:
- `apps/storefront`: order management, including cancellation and order history.
- `apps/billing`: invoice generation.

Product decisions for orders are in `docs/product/orders.md`.
""")
write("docs/product/orders.md", """# Pedidos

O chamador fornece a identidade autenticada e serializa as operações sobre o mesmo pedido.
O cliente só pode cancelar ou consultar o histórico dos próprios pedidos.
O cancelamento aceita pedidos em PENDING e registra CANCELLED no histórico, com instante UTC.
Repetir o cancelamento confirma CANCELLED sem acrescentar outro registro.
Pedidos em PAID ou SHIPPED não podem ser cancelados; a recusa preserva pedido e histórico.
A consulta retorna o histórico na ordem em que os registros foram acrescentados; sem registros, retorna uma lista vazia.
As recusas por propriedade e por estado precisam ser distinguíveis. Não há reembolso neste pedido.
""")
write("apps/storefront/orders.py", '''from dataclasses import dataclass, field
from datetime import datetime


class OwnershipError(Exception):
    pass


class InvalidTransition(Exception):
    pass


@dataclass
class Order:
    id: str
    customer_id: str
    status: str = "PENDING"
    history: list[tuple[str, datetime]] = field(default_factory=list)


def get_history(order: Order, customer_id: str) -> list[tuple[str, datetime]]:
    if order.customer_id != customer_id:
        raise OwnershipError(order.id)
    return list(order.history)
''')
write("apps/billing/invoices.py", '''from decimal import Decimal


def invoice_total(amounts: list[Decimal]) -> Decimal:
    return sum(amounts, Decimal("0"))
''')
subprocess.run(["git", "init", "-q"], cwd=root, check=True)
subprocess.run(["git", "add", "-A"], cwd=root, check=True)
subprocess.run(["git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.com",
                "commit", "-qm", "feat: add commerce applications"], cwd=root, check=True)
