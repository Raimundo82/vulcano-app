import os
import shutil
from typing import List

from ....domain.entities.invoice import Invoice
from ....domain.repositories.invoice_repository import InvoiceRepository
from ...ports.invoice_extractor_port import InvoiceExtractorPort


class ProcessInvoicesUseCase:
    """
    Process all PDF files found in the staging directory.

    Each PDF is parsed via the injected :class:`InvoiceExtractorPort`, the
    invoice data is extracted, the file is moved to the processed directory
    organised by year/month, and the record is persisted via the repository.
    """

    def __init__(
        self,
        invoice_repository: InvoiceRepository,
        invoice_extractor: InvoiceExtractorPort,
        pdfs_dir: str,
        processed_dir: str,
    ) -> None:
        self._repo = invoice_repository
        self._extractor = invoice_extractor
        self._pdfs_dir = pdfs_dir
        self._processed_dir = processed_dir

    def execute(self) -> List[dict]:
        """
        Process every .pdf file in the staging directory.

        Returns a list of extracted invoice data dictionaries for the
        processed invoices.
        """
        invoices_data = []

        for filename in os.listdir(self._pdfs_dir):
            if not filename.endswith(".pdf"):
                continue

            pdf_path = os.path.join(self._pdfs_dir, filename)
            data = self._extractor.extract(pdf_path)

            if not data:
                continue

            total_amount = float(data["total_amount"]) if data["total_amount"] else 0.0
            data["total_amount"] = total_amount
            data.setdefault("sent_validar", False)
            data.setdefault("quitar", False)

            year = data.get("invoice_period_year") or "unknown"
            month = data.get("invoice_period_month") or "unknown"
            destination_folder = os.path.join(self._processed_dir, year, month)
            os.makedirs(destination_folder, exist_ok=True)

            new_filename = (
                f"{data['invoice_type']}_"
                f"{str(data['issue_date'])}_"
                f"FT_{str(data['invoice_number'])}_"
                f"{data['client']}.pdf"
            )
            destination_path = os.path.join(destination_folder, new_filename)
            data["pdffile"] = new_filename

            if os.path.exists(destination_path):
                os.remove(destination_path)

            shutil.move(pdf_path, destination_path)

            invoice = Invoice(
                invoice_number=data["invoice_number"],
                invoice_type=data["invoice_type"],
                reference_number=data.get("reference_number"),
                issue_date=data.get("issue_date"),
                taxpayer_number=data.get("taxpayer_number"),
                account_number=data.get("account_number"),
                client=data.get("client"),
                address=data.get("address"),
                cvp=data.get("cvp"),
                invoice_period_month=data.get("invoice_period_month"),
                invoice_period_year=data.get("invoice_period_year"),
                amount_to_pay=data.get("amount_to_pay"),
                total_amount=data.get("total_amount"),
                sent_validar=data.get("sent_validar", False),
                quitar=data.get("quitar", False),
                pdffile=data.get("pdffile"),
            )
            self._repo.save(invoice)
            invoices_data.append(data)

        return invoices_data
