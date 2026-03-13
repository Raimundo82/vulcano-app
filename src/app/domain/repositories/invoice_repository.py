from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from ..entities.invoice import Invoice


class InvoiceRepository(ABC):
    """Abstract repository interface for Invoice persistence."""

    @abstractmethod
    def get_all_unpaid(self) -> List[Invoice]:
        """Return all invoices that have not been marked as paid."""

    @abstractmethod
    def get_all_paid(self) -> List[Invoice]:
        """Return all invoices that have been marked as paid."""

    @abstractmethod
    def get_by_invoice_number(self, invoice_number: str) -> Optional[Invoice]:
        """Return a single invoice by its invoice number, or None if not found."""

    @abstractmethod
    def get_by_account_number(
        self, account_number: str, limit: int = 12
    ) -> List[Invoice]:
        """Return the most recent invoices for the given account number."""

    @abstractmethod
    def get_average_total_by_account(
        self, account_number: str, months: int = 12
    ) -> float:
        """Return the average total_amount for the given account over the last N months."""

    @abstractmethod
    def save(self, invoice: Invoice) -> Invoice:
        """Persist a new invoice and return it with the generated id."""

    @abstractmethod
    def update(self, invoice: Invoice) -> Invoice:
        """Update an existing invoice and return it."""

    @abstractmethod
    def mark_as_paid(self, invoice_number: str, quita_date: datetime) -> bool:
        """Mark a single invoice as paid. Return True on success."""

    @abstractmethod
    def mark_many_as_paid(
        self, invoice_numbers: List[str], quita_date: datetime
    ) -> int:
        """Mark multiple invoices as paid. Return the number of updated rows."""

    @abstractmethod
    def delete_by_invoice_number(self, invoice_number: str) -> bool:
        """Delete a single invoice by its invoice number. Return True on success."""

    @abstractmethod
    def get_invoices_for_receipt(self, invoice_numbers: List[str]) -> List[Invoice]:
        """Return invoices needed to build a payment receipt, ordered by account."""
