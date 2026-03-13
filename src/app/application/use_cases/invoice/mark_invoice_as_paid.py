from ....domain.entities.invoice import Invoice
from ....domain.repositories.invoice_repository import InvoiceRepository


class MarkInvoiceAsPaidUseCase:
    """Mark a single invoice as paid by its invoice number."""

    def __init__(self, invoice_repository: InvoiceRepository) -> None:
        self._repo = invoice_repository

    def execute(self, invoice_number: str) -> bool:
        """
        Mark the invoice identified by *invoice_number* as paid.

        Delegates to the ``Invoice.mark_as_paid()`` domain method so that
        business rules (e.g. cannot re-pay) are enforced at the entity level.

        Returns True when the record was updated, False when not found.
        """
        invoice = self._repo.get_by_invoice_number(invoice_number)
        if invoice is None:
            return False
        invoice.mark_as_paid()
        self._repo.update(invoice)
        return True
