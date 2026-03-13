"""Tests for the domain entities."""
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from app.domain.entities.invoice import (
    BillingPeriod,
    Invoice,
    InvoiceType,
    PaymentStatus,
)
from app.domain.entities.unit import Contact, Unit
from app.domain.entities.user import User


class TestInvoiceType:
    def test_values(self):
        assert InvoiceType.BLM == "BLM"
        assert InvoiceType.VOZ == "VOZ"
        assert InvoiceType.UNKNOWN == "None"


class TestPaymentStatus:
    def test_values(self):
        assert PaymentStatus.PENDING == "PENDING"
        assert PaymentStatus.SENT_FOR_VALIDATION == "SENT_FOR_VALIDATION"
        assert PaymentStatus.PAID == "PAID"


class TestBillingPeriod:
    def test_str_representation(self):
        bp = BillingPeriod(month="janeiro", year="2024")
        assert str(bp) == "janeiro 2024"

    def test_frozen(self):
        bp = BillingPeriod(month="fevereiro", year="2024")
        try:
            bp.month = "março"  # type: ignore[misc]
            assert False, "Expected FrozenInstanceError"
        except Exception:
            pass


class TestInvoiceEntity:
    def test_minimal_creation(self):
        inv = Invoice(
            invoice_number="12345",
            invoice_type=InvoiceType.BLM,
            account_number="111111",
        )
        assert inv.invoice_number == "12345"
        assert inv.invoice_type is InvoiceType.BLM
        assert inv.account_number == "111111"
        assert inv.id is None
        assert inv.payment_status is PaymentStatus.PENDING
        assert inv.paid_on is None

    def test_full_creation_with_billing_period(self):
        bp = BillingPeriod(month="março", year="2024")
        inv = Invoice(
            id=1,
            invoice_number="99999",
            invoice_type=InvoiceType.VOZ,
            account_number="222222",
            billing_period=bp,
            total_amount=180.0,
            amount_to_pay=150.0,
            payment_status=PaymentStatus.PAID,
        )
        assert inv.invoice_type is InvoiceType.VOZ
        assert inv.billing_period.month == "março"
        assert inv.payment_status is PaymentStatus.PAID
        assert inv.is_paid()

    def test_mark_as_paid_sets_status_and_timestamp(self):
        inv = Invoice(
            invoice_number="A1",
            invoice_type=InvoiceType.BLM,
            account_number="333",
        )
        assert inv.is_pending()
        inv.mark_as_paid()
        assert inv.is_paid()
        assert inv.paid_on is not None

    def test_mark_as_paid_accepts_explicit_date(self):
        inv = Invoice(
            invoice_number="A2",
            invoice_type=InvoiceType.BLM,
            account_number="333",
        )
        ts = datetime(2024, 3, 1, 12, 0, 0)
        inv.mark_as_paid(paid_on=ts)
        assert inv.paid_on == ts

    def test_send_for_validation(self):
        inv = Invoice(
            invoice_number="A3",
            invoice_type=InvoiceType.VOZ,
            account_number="444",
        )
        inv.send_for_validation()
        assert inv.payment_status is PaymentStatus.SENT_FOR_VALIDATION
        assert not inv.is_paid()

    def test_cannot_resend_paid_invoice(self):
        inv = Invoice(
            invoice_number="A4",
            invoice_type=InvoiceType.BLM,
            account_number="555",
        )
        inv.mark_as_paid()
        try:
            inv.send_for_validation()
            assert False, "Expected ValueError"
        except ValueError:
            pass


class TestContactValueObject:
    def test_creation(self):
        c = Contact(name="Commander Smith", email="smith@navy.pt")
        assert c.name == "Commander Smith"
        assert c.email == "smith@navy.pt"

    def test_frozen(self):
        c = Contact(name="X", email="x@test.com")
        try:
            c.name = "Y"  # type: ignore[misc]
            assert False, "Expected FrozenInstanceError"
        except Exception:
            pass


class TestUnitEntity:
    def test_minimal_creation(self):
        unit = Unit(num_cliente="99999", name="Test Unit")
        assert unit.num_cliente == "99999"
        assert unit.name == "Test Unit"
        assert unit.id is None
        assert unit.contact is None

    def test_with_contact(self):
        contact = Contact(name="Commander Smith", email="smith@navy.pt")
        unit = Unit(
            id=5,
            num_cliente="11111",
            name="Navy HQ",
            contact=contact,
        )
        assert unit.id == 5
        assert unit.contact.name == "Commander Smith"
        assert unit.contact.email == "smith@navy.pt"


class TestUserEntity:
    def test_creation(self):
        user = User(username="jdoe", display_name="John Doe", email="jdoe@test.com")
        assert user.username == "jdoe"
        assert user.is_admin is False
        assert user.last_login is None

    def test_admin_flag(self):
        user = User(
            id=1,
            username="admin",
            display_name="Admin",
            email="admin@test.com",
            is_admin=True,
        )
        assert user.is_admin is True
        assert user.can_administrate() is True

    def test_non_admin_cannot_administrate(self):
        user = User(username="jdoe", display_name="J", email="j@test.com")
        assert user.can_administrate() is False
