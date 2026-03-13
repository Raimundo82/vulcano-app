"""Tests for the application layer use cases using in-memory test doubles."""
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from app.domain.entities.invoice import Invoice
from app.domain.entities.unit import Unit
from app.domain.entities.user import User
from app.domain.repositories.invoice_repository import InvoiceRepository
from app.domain.repositories.unit_repository import UnitRepository
from app.domain.repositories.user_repository import UserRepository
from app.application.ports.user_authenticator_port import UserAuthenticatorPort
from app.application.use_cases.invoice.get_unpaid_invoices import GetUnpaidInvoicesUseCase
from app.application.use_cases.invoice.get_paid_invoices import GetPaidInvoicesUseCase
from app.application.use_cases.invoice.mark_invoice_as_paid import MarkInvoiceAsPaidUseCase
from app.application.use_cases.invoice.mark_invoices_as_paid import MarkInvoicesAsPaidUseCase
from app.application.use_cases.invoice.delete_invoices import DeleteInvoicesUseCase
from app.application.use_cases.invoice.get_invoices_for_receipt import GetInvoicesForReceiptUseCase
from app.application.use_cases.user.authenticate_user import AuthenticateUserUseCase
from app.application.use_cases.user.list_users import ListUsersUseCase
from app.application.use_cases.user.add_user import AddUserUseCase
from app.application.use_cases.user.edit_user import EditUserUseCase
from app.application.use_cases.user.delete_user import DeleteUserUseCase
from app.application.use_cases.user.update_last_login import UpdateLastLoginUseCase
from app.application.use_cases.unit.list_units import ListUnitsUseCase
from app.application.use_cases.unit.add_unit import AddUnitUseCase
from app.application.use_cases.unit.edit_unit import EditUnitUseCase
from app.application.use_cases.unit.delete_unit import DeleteUnitUseCase


# ---------------------------------------------------------------------------
# In-memory test doubles
# ---------------------------------------------------------------------------

class InMemoryInvoiceRepository(InvoiceRepository):
    def __init__(self):
        self._store: Dict[str, Invoice] = {}

    def get_all_unpaid(self) -> List[Invoice]:
        return [inv for inv in self._store.values() if not inv.quitar]

    def get_all_paid(self) -> List[Invoice]:
        return [inv for inv in self._store.values() if inv.quitar]

    def get_by_invoice_number(self, invoice_number: str) -> Optional[Invoice]:
        return self._store.get(invoice_number)

    def get_by_account_number(self, account_number: str, limit: int = 12) -> List[Invoice]:
        results = [i for i in self._store.values() if i.account_number == account_number]
        return results[:limit]

    def get_average_total_by_account(self, account_number: str, months: int = 12) -> float:
        invoices = [
            i for i in self._store.values() if i.account_number == account_number and i.total_amount
        ]
        if not invoices:
            return 0.0
        return sum(i.total_amount for i in invoices) / len(invoices)

    def save(self, invoice: Invoice) -> Invoice:
        invoice.id = len(self._store) + 1
        self._store[invoice.invoice_number] = invoice
        return invoice

    def update(self, invoice: Invoice) -> Invoice:
        self._store[invoice.invoice_number] = invoice
        return invoice

    def mark_as_paid(self, invoice_number: str, quita_date: datetime) -> bool:
        inv = self._store.get(invoice_number)
        if not inv:
            return False
        inv.quitar = True
        inv.quita_date = quita_date
        return True

    def mark_many_as_paid(self, invoice_numbers: List[str], quita_date: datetime) -> int:
        count = 0
        for num in invoice_numbers:
            if self.mark_as_paid(num, quita_date):
                count += 1
        return count

    def delete_by_invoice_number(self, invoice_number: str) -> bool:
        if invoice_number in self._store:
            del self._store[invoice_number]
            return True
        return False

    def get_invoices_for_receipt(self, invoice_numbers: List[str]) -> List[Invoice]:
        return [self._store[n] for n in invoice_numbers if n in self._store]


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._store: Dict[int, User] = {}
        self._next_id = 1

    def get_all(self) -> List[User]:
        return sorted(self._store.values(), key=lambda u: (not u.is_admin, u.username))

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self._store.get(user_id)

    def get_by_username(self, username: str) -> Optional[User]:
        return next((u for u in self._store.values() if u.username == username), None)

    def save(self, user: User) -> User:
        user.id = self._next_id
        self._store[self._next_id] = user
        self._next_id += 1
        return user

    def update(self, user: User) -> User:
        self._store[user.id] = user
        return user

    def delete(self, user_id: int) -> bool:
        if user_id in self._store:
            del self._store[user_id]
            return True
        return False

    def update_last_login(self, username: str) -> bool:
        user = self.get_by_username(username)
        if not user:
            return False
        user.last_login = datetime.now()
        return True


class InMemoryUnitRepository(UnitRepository):
    def __init__(self):
        self._store: Dict[int, Unit] = {}
        self._next_id = 1

    def get_all(self) -> List[Unit]:
        return sorted(self._store.values(), key=lambda u: (u.num_cliente, u.unidade))

    def get_by_id(self, unit_id: int) -> Optional[Unit]:
        return self._store.get(unit_id)

    def save(self, unit: Unit) -> Unit:
        unit.id = self._next_id
        self._store[self._next_id] = unit
        self._next_id += 1
        return unit

    def update(self, unit: Unit) -> Unit:
        self._store[unit.id] = unit
        return unit

    def delete(self, unit_id: int) -> bool:
        if unit_id in self._store:
            del self._store[unit_id]
            return True
        return False


# ---------------------------------------------------------------------------
# Invoice use case tests
# ---------------------------------------------------------------------------

class TestGetUnpaidInvoicesUseCase:
    def test_returns_only_unpaid(self):
        repo = InMemoryInvoiceRepository()
        repo.save(Invoice(invoice_number="A1", invoice_type="BLM", account_number="111", total_amount=100.0))
        repo.save(Invoice(invoice_number="A2", invoice_type="VOZ", account_number="222", total_amount=200.0, quitar=True))

        use_case = GetUnpaidInvoicesUseCase(repo)
        result = use_case.execute()

        assert len(result) == 1
        assert result[0]["invoice_number"] == "A1"
        assert "media" in result[0]

    def test_includes_average(self):
        repo = InMemoryInvoiceRepository()
        repo.save(Invoice(invoice_number="B1", invoice_type="BLM", account_number="333", total_amount=100.0))
        repo.save(Invoice(invoice_number="B2", invoice_type="BLM", account_number="333", total_amount=200.0))

        use_case = GetUnpaidInvoicesUseCase(repo)
        result = use_case.execute()

        assert len(result) == 2
        for r in result:
            assert r["media"] == 150.0


class TestGetPaidInvoicesUseCase:
    def test_returns_only_paid(self):
        repo = InMemoryInvoiceRepository()
        repo.save(Invoice(invoice_number="C1", invoice_type="BLM", quitar=False))
        repo.save(Invoice(invoice_number="C2", invoice_type="BLM", quitar=True))

        use_case = GetPaidInvoicesUseCase(repo)
        result = use_case.execute()

        assert len(result) == 1
        assert result[0]["invoice_number"] == "C2"


class TestMarkInvoiceAsPaidUseCase:
    def test_marks_single_invoice(self):
        repo = InMemoryInvoiceRepository()
        repo.save(Invoice(invoice_number="D1", invoice_type="BLM"))

        use_case = MarkInvoiceAsPaidUseCase(repo)
        result = use_case.execute("D1")

        assert result is True
        assert repo.get_by_invoice_number("D1").quitar is True

    def test_returns_false_for_missing(self):
        repo = InMemoryInvoiceRepository()
        use_case = MarkInvoiceAsPaidUseCase(repo)
        assert use_case.execute("nonexistent") is False


class TestMarkInvoicesAsPaidUseCase:
    def test_marks_multiple(self):
        repo = InMemoryInvoiceRepository()
        repo.save(Invoice(invoice_number="E1", invoice_type="BLM"))
        repo.save(Invoice(invoice_number="E2", invoice_type="BLM"))

        use_case = MarkInvoicesAsPaidUseCase(repo)
        count = use_case.execute(["E1", "E2"])

        assert count == 2
        assert repo.get_by_invoice_number("E1").quitar is True
        assert repo.get_by_invoice_number("E2").quitar is True

    def test_empty_list_returns_zero(self):
        repo = InMemoryInvoiceRepository()
        use_case = MarkInvoicesAsPaidUseCase(repo)
        assert use_case.execute([]) == 0


class TestDeleteInvoicesUseCase:
    def test_deletes_invoice_record(self, tmp_path):
        repo = InMemoryInvoiceRepository()
        repo.save(Invoice(invoice_number="F1", invoice_type="BLM"))

        use_case = DeleteInvoicesUseCase(repo, str(tmp_path))
        count = use_case.execute([
            {"invoiceNumber": "F1", "invoiceYear": "2024", "invoiceMonth": "jan", "pdfFile": "test.pdf"}
        ])

        assert count == 1
        assert repo.get_by_invoice_number("F1") is None

    def test_also_removes_pdf_file(self, tmp_path):
        repo = InMemoryInvoiceRepository()
        repo.save(Invoice(invoice_number="G1", invoice_type="BLM"))

        pdf_dir = tmp_path / "2024" / "jan"
        pdf_dir.mkdir(parents=True)
        pdf_file = pdf_dir / "test.pdf"
        pdf_file.write_text("fake pdf content")

        use_case = DeleteInvoicesUseCase(repo, str(tmp_path))
        use_case.execute([
            {"invoiceNumber": "G1", "invoiceYear": "2024", "invoiceMonth": "jan", "pdfFile": "test.pdf"}
        ])

        assert not pdf_file.exists()


class TestGetInvoicesForReceiptUseCase:
    def test_returns_requested_invoices(self):
        repo = InMemoryInvoiceRepository()
        repo.save(Invoice(invoice_number="H1", invoice_type="BLM"))
        repo.save(Invoice(invoice_number="H2", invoice_type="VOZ"))

        use_case = GetInvoicesForReceiptUseCase(repo)
        result = use_case.execute(["H1"])

        assert len(result) == 1
        assert result[0].invoice_number == "H1"

    def test_empty_list_returns_empty(self):
        repo = InMemoryInvoiceRepository()
        use_case = GetInvoicesForReceiptUseCase(repo)
        assert use_case.execute([]) == []


# ---------------------------------------------------------------------------
# User use case tests
# ---------------------------------------------------------------------------

class TestAuthenticateUserUseCase:
    def test_returns_user_on_valid_credentials(self):
        repo = InMemoryUserRepository()
        repo.save(User(username="jdoe", display_name="John", email="jdoe@test.com", is_admin=False))

        authenticator = MagicMock(spec=UserAuthenticatorPort)
        authenticator.authenticate.return_value = {"username": "jdoe", "display_name": "John Doe"}

        use_case = AuthenticateUserUseCase(repo, authenticator)
        user = use_case.execute("jdoe", "secret")

        assert user is not None
        assert user.username == "jdoe"
        assert user.display_name == "John Doe"

    def test_returns_none_on_bad_credentials(self):
        repo = InMemoryUserRepository()
        authenticator = MagicMock(spec=UserAuthenticatorPort)
        authenticator.authenticate.return_value = None

        use_case = AuthenticateUserUseCase(repo, authenticator)
        assert use_case.execute("jdoe", "wrong") is None

    def test_returns_none_when_user_not_in_db(self):
        repo = InMemoryUserRepository()
        authenticator = MagicMock(spec=UserAuthenticatorPort)
        authenticator.authenticate.return_value = {"username": "unknown", "display_name": "Unknown"}

        use_case = AuthenticateUserUseCase(repo, authenticator)
        assert use_case.execute("unknown", "pw") is None


class TestListUsersUseCase:
    def test_returns_all_users(self):
        repo = InMemoryUserRepository()
        repo.save(User(username="alice", display_name="Alice", email="alice@test.com"))
        repo.save(User(username="bob", display_name="Bob", email="bob@test.com"))

        use_case = ListUsersUseCase(repo)
        users = use_case.execute()
        assert len(users) == 2


class TestAddUserUseCase:
    def test_creates_user(self):
        repo = InMemoryUserRepository()
        use_case = AddUserUseCase(repo)
        user = use_case.execute("alice", "Alice Smith", "alice@test.com")

        assert user.id is not None
        assert user.username == "alice"
        assert user.email == "alice@test.com"
        assert user.is_admin is False

    def test_raises_on_missing_fields(self):
        repo = InMemoryUserRepository()
        use_case = AddUserUseCase(repo)
        try:
            use_case.execute("", "Name", "email@test.com")
            assert False, "Expected ValueError"
        except ValueError:
            pass


class TestEditUserUseCase:
    def test_updates_user(self):
        repo = InMemoryUserRepository()
        user = repo.save(User(username="old", display_name="Old", email="old@test.com"))

        use_case = EditUserUseCase(repo)
        updated = use_case.execute(user.id, "new", "New Name", "new@test.com", True)

        assert updated.username == "new"
        assert updated.is_admin is True

    def test_raises_on_unknown_user(self):
        repo = InMemoryUserRepository()
        use_case = EditUserUseCase(repo)
        try:
            use_case.execute(999, "x", "X", "x@test.com")
            assert False, "Expected LookupError"
        except LookupError:
            pass


class TestDeleteUserUseCase:
    def test_deletes_user(self):
        repo = InMemoryUserRepository()
        user = repo.save(User(username="del", display_name="Del", email="del@test.com"))

        use_case = DeleteUserUseCase(repo)
        result = use_case.execute(user.id, requesting_user_id=999)
        assert result is True
        assert repo.get_by_id(user.id) is None

    def test_raises_on_self_deletion(self):
        repo = InMemoryUserRepository()
        user = repo.save(User(username="self", display_name="Self", email="self@test.com"))

        use_case = DeleteUserUseCase(repo)
        try:
            use_case.execute(user.id, requesting_user_id=user.id)
            assert False, "Expected PermissionError"
        except PermissionError:
            pass


class TestUpdateLastLoginUseCase:
    def test_updates_timestamp(self):
        repo = InMemoryUserRepository()
        repo.save(User(username="jane", display_name="Jane", email="jane@test.com"))

        use_case = UpdateLastLoginUseCase(repo)
        result = use_case.execute("jane")

        assert result is True
        assert repo.get_by_username("jane").last_login is not None

    def test_returns_false_for_unknown(self):
        repo = InMemoryUserRepository()
        use_case = UpdateLastLoginUseCase(repo)
        assert use_case.execute("nobody") is False


# ---------------------------------------------------------------------------
# Unit use case tests
# ---------------------------------------------------------------------------

class TestListUnitsUseCase:
    def test_returns_all_units(self):
        repo = InMemoryUnitRepository()
        repo.save(Unit(num_cliente="111", unidade="Alpha"))
        repo.save(Unit(num_cliente="222", unidade="Beta"))

        use_case = ListUnitsUseCase(repo)
        units = use_case.execute()
        assert len(units) == 2


class TestAddUnitUseCase:
    def test_creates_unit(self):
        repo = InMemoryUnitRepository()
        use_case = AddUnitUseCase(repo)
        unit = use_case.execute("999", "Test Unit", "John Doe", "john@test.com")

        assert unit.id is not None
        assert unit.num_cliente == "999"
        assert unit.poc == "John Doe"

    def test_raises_on_missing_fields(self):
        repo = InMemoryUnitRepository()
        use_case = AddUnitUseCase(repo)
        try:
            use_case.execute("", "Unit")
            assert False, "Expected ValueError"
        except ValueError:
            pass


class TestEditUnitUseCase:
    def test_updates_unit(self):
        repo = InMemoryUnitRepository()
        unit = repo.save(Unit(num_cliente="111", unidade="Old"))

        use_case = EditUnitUseCase(repo)
        updated = use_case.execute(unit.id, "222", "New", "Jane", "jane@test.com")

        assert updated.num_cliente == "222"
        assert updated.unidade == "New"

    def test_raises_on_unknown_unit(self):
        repo = InMemoryUnitRepository()
        use_case = EditUnitUseCase(repo)
        try:
            use_case.execute(999, "x", "X")
            assert False, "Expected LookupError"
        except LookupError:
            pass


class TestDeleteUnitUseCase:
    def test_deletes_unit(self):
        repo = InMemoryUnitRepository()
        unit = repo.save(Unit(num_cliente="111", unidade="ToDelete"))

        use_case = DeleteUnitUseCase(repo)
        result = use_case.execute(unit.id)
        assert result is True
        assert repo.get_by_id(unit.id) is None

    def test_returns_false_for_missing(self):
        repo = InMemoryUnitRepository()
        use_case = DeleteUnitUseCase(repo)
        assert use_case.execute(999) is False
