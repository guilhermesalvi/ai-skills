"""Seed an isolated evaluation fixture; requires an empty directory and Git."""

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


def commit(message):
    git("add", "-A")
    git("-c", "user.name=fixture", "-c", "user.email=fixture@example.com", "commit", "-qm", message)


write("orders/__init__.py", "")
write("tests/__init__.py", "")
write("orders/orders.py", r'''from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


class InvalidTransition(Exception):
    pass


@dataclass
class OrderItem:
    sku: str
    quantity: int
    unit_price: Decimal


@dataclass
class Order:
    id: str
    customer_id: str
    items: list[OrderItem]
    status: OrderStatus = OrderStatus.PENDING
    paid_at: datetime | None = None
    history: list[tuple[OrderStatus, datetime]] = field(default_factory=list)

    @property
    def total(self) -> Decimal:
        return sum((i.unit_price * i.quantity for i in self.items), Decimal("0"))


class PaymentGateway:
    """Adapter over the payment provider. charge() returns a provider transaction id."""

    def charge(self, customer_id: str, amount: Decimal) -> str:
        raise NotImplementedError


def _move(order: Order, target: OrderStatus) -> None:
    order.status = target
    order.history.append((target, datetime.now(timezone.utc)))


def pay(order: Order, gateway: PaymentGateway) -> str:
    if order.status is not OrderStatus.PENDING:
        raise InvalidTransition(f"cannot pay order in {order.status.value}")
    transaction_id = gateway.charge(order.customer_id, order.total)
    order.paid_at = datetime.now(timezone.utc)
    _move(order, OrderStatus.PAID)
    return transaction_id


def ship(order: Order) -> None:
    if order.status is not OrderStatus.PAID:
        raise InvalidTransition(f"cannot ship order in {order.status.value}")
    _move(order, OrderStatus.SHIPPED)


def deliver(order: Order) -> None:
    if order.status is not OrderStatus.SHIPPED:
        raise InvalidTransition(f"cannot deliver order in {order.status.value}")
    _move(order, OrderStatus.DELIVERED)
''')

write("tests/test_orders.py", r'''import unittest
from decimal import Decimal

from orders.orders import InvalidTransition, Order, OrderItem, OrderStatus, PaymentGateway, pay, ship


class FakeGateway(PaymentGateway):
    def __init__(self):
        self.charges = []

    def charge(self, customer_id, amount):
        self.charges.append((customer_id, amount))
        return f"tx-{len(self.charges)}"


def make_order():
    return Order("o-1", "c-1", [OrderItem("A", 2, Decimal("10.00")), OrderItem("B", 1, Decimal("5.50"))])


class OrderTests(unittest.TestCase):
    def test_pay_charges_total(self):
        gateway = FakeGateway()
        order = make_order()
        pay(order, gateway)
        self.assertEqual(gateway.charges, [("c-1", Decimal("25.50"))])
        self.assertIs(order.status, OrderStatus.PAID)

    def test_cannot_ship_unpaid(self):
        with self.assertRaises(InvalidTransition):
            ship(make_order())


if __name__ == "__main__":
    unittest.main()
''')

write("README.md", r'''# orders

Order lifecycle for the storefront backend. Run the tests with `python -m unittest discover -s tests`.
''')

write("docs/specs/order-lifecycle/spec.md", r'''# Ciclo do pedido

| | |
| --- | --- |
| **Requirement Prefix** | `OLC` |

## Context

O cliente da loja não tem como desistir de um pedido: o ciclo em `orders/orders.py` só avança de `PENDING` para `PAID`, `SHIPPED` e `DELIVERED`. O backend da loja chama este módulo em nome do cliente e precisa distinguir o cancelamento feito, o pedido de outro cliente e o estado que não permite cancelar. OLC-01 a OLC-05 descrevem o comportamento observado em `orders/orders.py:51-69`, do qual o cancelamento depende.

## Scope

Cancelamento pelo cliente dono do pedido e as regras de estado de que ele depende. Ficam fora o cancelamento pela operação, o cancelamento parcial de itens e o reembolso, que depende da lacuna registrada.

## Assumptions

- **O chamador entrega ao módulo a identidade autenticada do cliente que pede o cancelamento.** O módulo só conhece o cliente por `Order.customer_id` (`orders/orders.py:28`); o dono do backend da loja ainda precisa verificar a origem autenticada do solicitante. Provisoriamente, o cancelamento recebe esse identificador e confere a propriedade antes do estado (OLC-07). Se a identidade não vier autenticada, quem conhecer o identificador de um cliente poderá cancelar os pedidos dele.
- **Pedido pago é recusado enquanto a política de reembolso não for decidida.** Para atender provisoriamente a lacuna do reembolso, `PAID` é recusado, como `SHIPPED`, `DELIVERED` e `CANCELLED` (OLC-08). Se a política permitir o cancelamento de pedidos pagos, essa recusa precisará mudar; enquanto isso, o cliente dependerá do atendimento para desistir.
- **O chamador serializa as operações sobre o mesmo pedido.** O módulo altera o `Order` em memória, sem trava, e `pay` cobra antes de gravar `PAID` (`orders/orders.py:51-57`); a serialização pelo chamador ainda precisa ser verificada pelo dono do backend da loja. Se ela não existir, um cancelamento concorrente com o pagamento poderá deixar um pedido cobrado em `CANCELLED`.

## Gaps

| Gap | Affects | Owner |
| --- | --- | --- |
| Se o cliente pode cancelar pedido em `PAID` e a política de reembolso | OLC-08, membro `PAID` | ? |

## Requirements

```mermaid
stateDiagram-v2
    [*] --> PENDING: criação (OLC-01)
    PENDING --> PAID: pagamento (OLC-02)
    PAID --> SHIPPED: envio (OLC-03)
    SHIPPED --> DELIVERED: entrega (OLC-04)
    PENDING --> CANCELLED: cancelamento pelo cliente (OLC-06)
```

| State | Identifier | Meaning |
| --- | --- | --- |
| Pendente | `PENDING` | Pedido criado e ainda não pago |
| Pago | `PAID` | Pagamento cobrado, aguardando envio |
| Enviado | `SHIPPED` | Pedido despachado |
| Entregue | `DELIVERED` | Resultado terminal de entrega |
| Cancelado | `CANCELLED` | Resultado terminal de cancelamento pelo cliente |

- **OLC-01** — O sistema DEVE criar todo pedido em `PENDING`.
- **OLC-02** — QUANDO o pagamento de um pedido em `PENDING` for cobrado, ENTÃO o sistema DEVE mover o pedido para `PAID`.
- **OLC-03** — QUANDO o envio de um pedido em `PAID` for registrado, ENTÃO o sistema DEVE mover o pedido para `SHIPPED`.
- **OLC-04** — QUANDO a entrega de um pedido em `SHIPPED` for registrada, ENTÃO o sistema DEVE mover o pedido para `DELIVERED`.
- **OLC-05** — SE o pagamento, o envio ou a entrega for solicitado para um pedido fora do estado de origem da transição, ENTÃO o sistema DEVE recusar a operação com `InvalidTransition` e manter o pedido inalterado, sem cobrar o cliente, porque a verificação do estado precede a cobrança (`orders/orders.py:52-54`).
- **OLC-06** — QUANDO o cliente do pedido solicitar o cancelamento de um pedido em `PENDING`, ENTÃO o sistema DEVE mover o pedido para `CANCELLED` e acrescentar ao histórico o estado `CANCELLED` com o instante UTC do cancelamento.
- **OLC-07** — SE o cancelamento for solicitado por um cliente diferente do cliente do pedido, ENTÃO o sistema DEVE recusá-lo com um erro distinto de `InvalidTransition`, qualquer que seja o estado do pedido, e manter o pedido inalterado.
- **OLC-08** — SE o cliente do pedido solicitar o cancelamento de um pedido em `PAID`, `SHIPPED`, `DELIVERED` ou `CANCELLED`, ENTÃO o sistema DEVE recusá-lo com `InvalidTransition` e manter o pedido inalterado.

## Observable Decisions

| Surface or dimension | Landing |
| --- | --- |
| Módulo: formato do erro | OLC-07, com erro próprio de propriedade; OLC-08, com `InvalidTransition` (`orders/orders.py:14-15`) |
| Authorization | OLC-07 e a premissa **O chamador entrega ao módulo a identidade autenticada do cliente que pede o cancelamento.** |
| Idempotency and duplication | OLC-08, membro `CANCELLED`: repetir o cancelamento é recusado e não duplica o histórico |
| Concurrency and ordering | Premissa **O chamador serializa as operações sobre o mesmo pedido.** |
| State transitions | OLC-01 a OLC-08 e o diagrama |
| Observability | OLC-06: o histórico registra o instante do cancelamento |
| Cross-capability consistency | Lacuna do reembolso em `PAID` |
| `n/a` | Validation and limits: o cancelamento só recebe o pedido e o solicitante; Failure and partial failure: cancelar não chama outro sistema; External dependency failure: cancelar não chama o provedor; Rate limiting: chamada no mesmo processo; Data lifecycle: o módulo não persiste pedidos |
''')

write("docs/specs/order-lifecycle/0001-customer-cancellation.md", r'''# Cancelamento de pedido pelo cliente

| | |
| --- | --- |
| **Requirements in Scope** | `OLC-05`, `OLC-06`, `OLC-07`, `OLC-08` |

## Context

Base de comparação: o commit que traz esta spec e este plano. Nela, `python -m unittest discover -s tests` executa 2 testes e passa. Foram inspecionados `orders/orders.py`, `tests/test_orders.py` e `README.md`; os chamadores do módulo não estão no repositório.

## Technical Decisions

| Decision | Choice | Rejected alternatives | Cost | Reversible |
| --- | --- | --- | --- | --- |
| Operação de cancelamento | `def cancel(order: Order, customer_id: str) -> None`, função do módulo como `pay`, `ship` e `deliver` | Conferir a propriedade no chamador: o módulo não garantiria OLC-07 | O chamador informa o solicitante em toda chamada | Não: assinatura pública que o chamador consome |
| Erro de propriedade | `class NotOrderOwner(Exception)`, sem herdar de `InvalidTransition` | Reusar `InvalidTransition`: o chamador só distinguiria as recusas pelo texto, contra OLC-07 | Um tipo de erro a mais para o chamador tratar | Não: contrato que o chamador consome |
| Representação do cancelamento | Membro `CANCELLED = "cancelled"` em `OrderStatus` | Campo `cancelled_at` sem estado novo: as guardas de `pay`, `ship` e `deliver` leem só `status` | Quem trata `OrderStatus` de forma exaustiva recebe um valor novo | Não: valor que o chamador pode persistir |
| Preservação nas recusas | Validar propriedade e estado antes de chamar `_move(order, OrderStatus.CANCELLED)`, reutilizando o registro de estado e histórico | Aplicar `_move` antes das guardas: uma recusa deixaria estado ou histórico alterado | As guardas precisam continuar antes de qualquer efeito | Sim |

## Execution

| Item | Outcome | Depends on | Context | Checks |
| --- | --- | --- | --- | --- |
| cancel-operation | Cancelamento e recusas disponíveis no contrato público do módulo | none | [Spec](spec.md), `orders/orders.py`: guardas antes de `_move`; forma literal em Technical Decisions | OLC-06, OLC-07, OLC-08, Erro de propriedade e representação do cancelamento |
| transition-regression | Cancelamento integrado ao ciclo existente sem permitir cobrança, envio ou entrega de pedido cancelado | cancel-operation | [Spec](spec.md), `pay`, `ship` e `deliver` em `orders/orders.py`; preservar os testes existentes | OLC-05, Gate |

## Checks

- [ ] **OLC-06**: `cancel(order, "c-1")` sobre um pedido de `c-1` em `PENDING` deixa `order.status` em `CANCELLED` e acrescenta um único item `(CANCELLED, instante UTC)` ao histórico — `python -m unittest tests.test_orders.OrderTests.test_customer_cancels_pending_order`
- [ ] **OLC-07**: para cada um dos 5 estados, `cancel(order, "c-2")` sobre um pedido de `c-1` levanta `NotOrderOwner` e mantém `status` e `history` — `python -m unittest tests.test_orders.OrderTests.test_other_customer_cannot_cancel`
- [ ] **OLC-08**: para cada um dos estados `PAID`, `SHIPPED`, `DELIVERED` e `CANCELLED`, `cancel(order, "c-1")` levanta `InvalidTransition` e mantém `status` e `history` — `python -m unittest tests.test_orders.OrderTests.test_cancel_rejected_outside_pending`
- [ ] **OLC-05**: `pay`, `ship` e `deliver` sobre um pedido em `CANCELLED` levantam `InvalidTransition`, `pay` não registra cobrança, e o pedido continua em `CANCELLED` — `python -m unittest tests.test_orders.OrderTests.test_cancelled_order_rejects_transitions`
- [ ] Erro de propriedade e representação do cancelamento: `NotOrderOwner` não é subclasse de `InvalidTransition`, e `OrderStatus.CANCELLED.value == "cancelled"` — `python -m unittest tests.test_orders.OrderTests.test_cancellation_contract`
- [ ] Gate: a suíte inteira passa — `python -m unittest discover -s tests`
''')

git("init", "-q")
commit("docs: specify customer cancellation")
