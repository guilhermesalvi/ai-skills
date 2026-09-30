#!/usr/bin/env bash
# Seeds a billing module whose history converted every stored instant to UTC, with no ADR.
set -euo pipefail

commit() {
  git add -A
  git -c user.name=fixture -c user.email=fixture@example.com commit -qm "$1"
}

mkdir -p billing tests
: > billing/__init__.py
: > tests/__init__.py

cat > billing/invoices.py <<'EOF'
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Invoice:
    id: str
    customer_id: str
    amount: Decimal
    issued_at: datetime


def issue(invoice_id: str, customer_id: str, amount: Decimal) -> Invoice:
    return Invoice(invoice_id, customer_id, amount, datetime.now())
EOF

cat > README.md <<'EOF'
# billing

Invoice issuing for the storefront. Run the tests with `python -m unittest discover -s tests`.
EOF

git init -q
commit "feat: issue invoices"

cat > billing/clock.py <<'EOF'
from datetime import datetime, timezone


def now() -> datetime:
    """Current instant, always timezone-aware in UTC."""
    return datetime.now(timezone.utc)
EOF

cat > billing/invoices.py <<'EOF'
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from billing import clock


@dataclass
class Invoice:
    id: str
    customer_id: str
    amount: Decimal
    issued_at: datetime


def issue(invoice_id: str, customer_id: str, amount: Decimal) -> Invoice:
    return Invoice(invoice_id, customer_id, amount, clock.now())
EOF

cat > billing/storage.py <<'EOF'
from datetime import datetime, timedelta


def serialize_instant(value: datetime) -> str:
    if value.utcoffset() != timedelta(0):
        raise ValueError("instants must be stored in UTC")
    return value.isoformat()


def parse_instant(text: str) -> datetime:
    value = datetime.fromisoformat(text)
    if value.utcoffset() != timedelta(0):
        raise ValueError("stored instants must be UTC")
    return value
EOF

cat > tests/test_storage.py <<'EOF'
import unittest
from datetime import datetime, timedelta, timezone

from billing.storage import parse_instant, serialize_instant


class StorageTests(unittest.TestCase):
    def test_local_time_is_rejected(self):
        with self.assertRaises(ValueError):
            serialize_instant(datetime(2026, 1, 1, 12, tzinfo=timezone(timedelta(hours=-3))))

    def test_utc_round_trip(self):
        value = datetime(2026, 1, 1, 15, tzinfo=timezone.utc)
        self.assertEqual(value, parse_instant(serialize_instant(value)))


if __name__ == "__main__":
    unittest.main()
EOF

commit "refactor: store instants in utc"
