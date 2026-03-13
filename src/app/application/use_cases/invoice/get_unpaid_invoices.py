from typing import Dict, List, Tuple

from ....domain.entities.invoice import Invoice
from ....domain.repositories.invoice_repository import InvoiceRepository


class GetUnpaidInvoicesUseCase:
    """Return all unpaid invoices, each annotated with the 12-month average for its account."""

    def __init__(self, invoice_repository: InvoiceRepository) -> None:
        self._repo = invoice_repository

    def execute(self) -> List[Tuple[Invoice, float]]:
        """
        Return a list of ``(invoice, average)`` pairs for all unpaid invoices.

        The *average* is the 12-month rolling average of ``total_amount`` for
        the invoice's account, used to highlight anomalous charges.
        """
        invoices = self._repo.get_all_unpaid()
        result = []
        for invoice in invoices:
            average = (
                self._repo.get_average_total_by_account(invoice.account_number)
                if invoice.account_number
                else 0.0
            )
            result.append((invoice, average))
        return result
