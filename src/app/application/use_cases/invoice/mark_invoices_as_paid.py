from datetime import datetime
from typing import List

from ....domain.repositories.invoice_repository import InvoiceRepository


class MarkInvoicesAsPaidUseCase:
    """Mark a batch of invoices as paid."""

    def __init__(self, invoice_repository: InvoiceRepository) -> None:
        self._repo = invoice_repository

    def execute(self, invoice_numbers: List[str]) -> int:
        """
        Mark every invoice in *invoice_numbers* as paid with the current timestamp.

        Returns the number of successfully updated records.
        """
        if not invoice_numbers:
            return 0
        quita_date = datetime.now()
        return self._repo.mark_many_as_paid(invoice_numbers, quita_date)
