from typing import List

from ....domain.repositories.invoice_repository import InvoiceRepository


class MarkInvoicesAsPaidUseCase:
    """Mark a batch of invoices as paid."""

    def __init__(self, invoice_repository: InvoiceRepository) -> None:
        self._repo = invoice_repository

    def execute(self, invoice_numbers: List[str]) -> int:
        """
        Mark every invoice in *invoice_numbers* as paid.

        Each invoice's domain method ``mark_as_paid()`` is called so that
        business rules are enforced consistently regardless of the caller.

        Returns the number of successfully updated records.
        """
        if not invoice_numbers:
            return 0
        updated = 0
        for invoice_number in invoice_numbers:
            invoice = self._repo.get_by_invoice_number(invoice_number)
            if invoice is None:
                continue
            invoice.mark_as_paid()
            self._repo.update(invoice)
            updated += 1
        return updated
