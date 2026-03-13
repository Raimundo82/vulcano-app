from typing import List

from ....domain.entities.invoice import Invoice
from ....domain.repositories.invoice_repository import InvoiceRepository


class GetInvoicesForReceiptUseCase:
    """Retrieve the invoices required to generate a payment receipt."""

    def __init__(self, invoice_repository: InvoiceRepository) -> None:
        self._repo = invoice_repository

    def execute(self, invoice_numbers: List[str]) -> List[Invoice]:
        """
        Return invoice entities for the given *invoice_numbers*, ordered by
        account number for grouping on the receipt document.
        """
        if not invoice_numbers:
            return []
        return self._repo.get_invoices_for_receipt(invoice_numbers)
