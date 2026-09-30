#!/usr/bin/env bash
# Seeds a small Python order module, committed, with no spec yet.
set -euo pipefail

mkdir -p orders tests
: > orders/__init__.py
: > tests/__init__.py

cat > orders/orders.py <<'EOF'
from dataclasses import dataclass, field
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
EOF

cat > tests/test_orders.py <<'EOF'
import unittest
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
EOF

cat > README.md <<'EOF'
# orders

Order lifecycle for the storefront backend. Run the tests with `python -m unittest discover -s tests`.
EOF

git init -q
git add -A
git -c user.name=fixture -c user.email=fixture@example.com commit -qm "feat: order lifecycle"
