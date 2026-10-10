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


write("billing/__init__.py", "")
write("tests/__init__.py", "")
write("billing/invoices.py", r'''from dataclasses import dataclass
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
''')

write("README.md", r'''# billing

Invoice issuing for the storefront. Run the tests with `python -m unittest discover -s tests`.
''')

git("init", "-q")
commit("feat: issue invoices")
write("billing/clock.py", r'''from datetime import datetime, timezone


def now() -> datetime:
    """Current instant, always timezone-aware in UTC."""
    return datetime.now(timezone.utc)
''')

write("billing/invoices.py", r'''from dataclasses import dataclass
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
''')

write("billing/storage.py", r'''from datetime import datetime, timedelta


def serialize_instant(value: datetime) -> str:
    if value.utcoffset() != timedelta(0):
        raise ValueError("instants must be stored in UTC")
    return value.isoformat()


def parse_instant(text: str) -> datetime:
    value = datetime.fromisoformat(text)
    if value.utcoffset() != timedelta(0):
        raise ValueError("stored instants must be UTC")
    return value
''')

write("tests/test_storage.py", r'''import unittest
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
''')

commit("refactor: store instants in utc")
