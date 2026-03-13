from dataclasses import dataclass
from typing import List

from ....domain.repositories.invoice_repository import InvoiceRepository


@dataclass
class AccountDetails:
    account_number: str
    client: str
    labels: List[str]
    amounts: List[float]
    average_value: float


class GetAccountDetailsUseCase:
    """Return chart data and statistics for a single account number."""

    def __init__(self, invoice_repository: InvoiceRepository) -> None:
        self._repo = invoice_repository

    def execute(self, account_number: str) -> AccountDetails:
        """
        Collect the last 12 invoices for *account_number* and return an
        :class:`AccountDetails` object suitable for rendering a trend chart.
        """
        invoices = self._repo.get_by_account_number(account_number, limit=12)

        client = invoices[0].client if invoices else "Cliente não encontrado"

        # Reverse to chronological order for the chart
        invoices_asc = list(reversed(invoices))
        labels = [
            inv.issue_date.strftime("%Y-%m")
            if hasattr(inv.issue_date, "strftime")
            else str(inv.issue_date)
            for inv in invoices_asc
        ]
        amounts = [float(inv.total_amount) if inv.total_amount else 0.0 for inv in invoices_asc]

        average_value = self._repo.get_average_total_by_account(account_number)

        return AccountDetails(
            account_number=account_number,
            client=client,
            labels=labels,
            amounts=amounts,
            average_value=round(average_value, 2),
        )
