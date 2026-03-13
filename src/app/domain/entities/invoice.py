from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Invoice:
    """Domain entity representing a telecommunications invoice."""

    invoice_number: str
    invoice_type: str  # "BLM", "VOZ" or "None"
    id: Optional[int] = None
    reference_number: Optional[str] = None
    issue_date: Optional[str] = None
    taxpayer_number: Optional[str] = None
    account_number: Optional[str] = None
    client: Optional[str] = None
    address: Optional[str] = None
    cvp: Optional[str] = None
    invoice_period_month: Optional[str] = None
    invoice_period_year: Optional[str] = None
    amount_to_pay: Optional[float] = None
    total_amount: Optional[float] = None
    sent_validar: bool = field(default=False)
    quitar: bool = field(default=False)
    quita_date: Optional[datetime] = None
    pdffile: Optional[str] = None
