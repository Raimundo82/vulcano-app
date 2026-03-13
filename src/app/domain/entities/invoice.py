from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class InvoiceType(str, Enum):
    """Classification of a telecommunications invoice by contract type."""

    BLM = "BLM"  # Broadband / data contracts
    VOZ = "VOZ"  # Voice / telephony contracts
    UNKNOWN = "None"  # Account number not matched to any contract list


class PaymentStatus(str, Enum):
    """
    Lifecycle status of an invoice payment.

    PENDING           — invoice received, awaiting internal validation
    SENT_FOR_VALIDATION — invoice submitted for qualitative/quantitative sign-off
    PAID              — invoice settled; quita_date is set
    """

    PENDING = "PENDING"
    SENT_FOR_VALIDATION = "SENT_FOR_VALIDATION"
    PAID = "PAID"


@dataclass(frozen=True)
class BillingPeriod:
    """
    Value object representing the billing month covered by an invoice.

    Both *month* (e.g. ``"janeiro"``) and *year* (e.g. ``"2024"``) are
    kept as strings to preserve the original Portuguese month names used
    in MEO invoices and in folder organisation.
    """

    month: str
    year: str

    def __str__(self) -> str:
        return f"{self.month} {self.year}"


@dataclass
class Invoice:
    """
    Domain entity representing a MEO telecommunications invoice.

    An invoice is issued by MEO for a single telecommunications account
    (contract).  It covers one billing period and moves through a defined
    payment lifecycle tracked by :attr:`payment_status`.

    Identity is the MEO-assigned ``invoice_number`` (e.g. the number after
    ``FT MV/``).
    """

    invoice_number: str
    invoice_type: InvoiceType
    account_number: str

    id: Optional[int] = None

    # Billing metadata
    billing_period: Optional[BillingPeriod] = None
    issue_date: Optional[str] = None
    reference_number: Optional[str] = None
    cvp: Optional[str] = None  # Control/payment tracking number

    # Financial amounts (EUR)
    total_amount: Optional[float] = None
    amount_to_pay: Optional[float] = None

    # Client data as it appears on the invoice (denormalised from MEO document)
    client: Optional[str] = None
    address: Optional[str] = None
    taxpayer_number: Optional[str] = None

    # Payment lifecycle
    payment_status: PaymentStatus = field(default=PaymentStatus.PENDING)
    paid_on: Optional[datetime] = None

    # Stored PDF filename (relative to the processed directory)
    pdffile: Optional[str] = None

    # ------------------------------------------------------------------
    # Business behaviour
    # ------------------------------------------------------------------

    def send_for_validation(self) -> None:
        """Advance the invoice to the SENT_FOR_VALIDATION stage."""
        if self.payment_status is PaymentStatus.PAID:
            raise ValueError(
                f"Invoice {self.invoice_number} is already paid and cannot be re-submitted."
            )
        self.payment_status = PaymentStatus.SENT_FOR_VALIDATION

    def mark_as_paid(self, paid_on: Optional[datetime] = None) -> None:
        """Settle the invoice, optionally recording the payment timestamp."""
        self.payment_status = PaymentStatus.PAID
        self.paid_on = paid_on or datetime.now()

    def is_paid(self) -> bool:
        return self.payment_status is PaymentStatus.PAID

    def is_pending(self) -> bool:
        return self.payment_status is PaymentStatus.PENDING
