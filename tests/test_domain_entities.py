"""Tests for the domain entities."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from app.domain.entities.invoice import Invoice
from app.domain.entities.unit import Unit
from app.domain.entities.user import User


class TestInvoiceEntity:
    def test_minimal_creation(self):
        inv = Invoice(invoice_number="12345", invoice_type="BLM")
        assert inv.invoice_number == "12345"
        assert inv.invoice_type == "BLM"
        assert inv.id is None
        assert inv.quitar is False
        assert inv.sent_validar is False

    def test_full_creation(self):
        inv = Invoice(
            id=1,
            invoice_number="99999",
            invoice_type="VOZ",
            account_number="1234567890",
            client="Test Client",
            amount_to_pay=150.0,
            total_amount=180.0,
            quitar=True,
        )
        assert inv.id == 1
        assert inv.invoice_type == "VOZ"
        assert inv.quitar is True
        assert inv.total_amount == 180.0


class TestUserEntity:
    def test_creation(self):
        user = User(username="jdoe", display_name="John Doe", email="jdoe@test.com")
        assert user.username == "jdoe"
        assert user.display_name == "John Doe"
        assert user.email == "jdoe@test.com"
        assert user.is_admin is False
        assert user.id is None
        assert user.last_login is None

    def test_admin_user(self):
        user = User(
            id=1,
            username="admin",
            display_name="Admin User",
            email="admin@test.com",
            is_admin=True,
        )
        assert user.is_admin is True


class TestUnitEntity:
    def test_minimal_creation(self):
        unit = Unit(num_cliente="99999", unidade="Test Unit")
        assert unit.num_cliente == "99999"
        assert unit.unidade == "Test Unit"
        assert unit.id is None
        assert unit.poc is None
        assert unit.email_poc is None

    def test_full_creation(self):
        unit = Unit(
            id=5,
            num_cliente="11111",
            unidade="Navy HQ",
            poc="Commander Smith",
            email_poc="smith@navy.pt",
        )
        assert unit.id == 5
        assert unit.poc == "Commander Smith"
        assert unit.email_poc == "smith@navy.pt"
