import os
from typing import List

from ....domain.repositories.invoice_repository import InvoiceRepository


class DeleteInvoicesUseCase:
    """Delete invoices and their associated PDF files (admin-only operation)."""

    def __init__(self, invoice_repository: InvoiceRepository, processed_dir: str) -> None:
        self._repo = invoice_repository
        self._processed_dir = processed_dir

    def execute(self, invoices: List[dict]) -> int:
        """
        Delete the invoices described in *invoices*.

        Each entry is expected to have the keys:
          - invoiceNumber (str)
          - invoiceYear   (str | int)
          - invoiceMonth  (str)
          - pdfFile       (str)

        Returns the number of successfully deleted records.
        """
        deleted = 0
        for invoice in invoices:
            invoice_number = invoice.get("invoiceNumber")
            if not invoice_number:
                continue

            success = self._repo.delete_by_invoice_number(invoice_number)
            if success:
                deleted += 1

            pdf_path = os.path.join(
                self._processed_dir,
                str(invoice.get("invoiceYear", "")),
                str(invoice.get("invoiceMonth", "")),
                invoice.get("pdfFile", ""),
            )
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

        return deleted
