from typing import Dict, List

from ....domain.repositories.invoice_repository import InvoiceRepository


class GetUnpaidInvoicesUseCase:
    """Return all unpaid invoices, each annotated with the 12-month average for its account."""

    def __init__(self, invoice_repository: InvoiceRepository) -> None:
        self._repo = invoice_repository

    def execute(self) -> List[Dict]:
        invoices = self._repo.get_all_unpaid()
        result = []
        for invoice in invoices:
            average = (
                self._repo.get_average_total_by_account(invoice.account_number)
                if invoice.account_number
                else 0.0
            )
            entry = invoice.__dict__.copy()
            entry["media"] = average
            result.append(entry)
        return result
