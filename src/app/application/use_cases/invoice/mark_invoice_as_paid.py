from datetime import datetime

from ....domain.repositories.invoice_repository import InvoiceRepository


class MarkInvoiceAsPaidUseCase:
    """Mark a single invoice as paid by its invoice number."""

    def __init__(self, invoice_repository: InvoiceRepository) -> None:
        self._repo = invoice_repository

    def execute(self, invoice_number: str) -> bool:
        """
        Mark the invoice identified by *invoice_number* as paid.

        Returns True when the record was updated, False otherwise.
        """
        quita_date = datetime.now()
        return self._repo.mark_as_paid(invoice_number, quita_date)
