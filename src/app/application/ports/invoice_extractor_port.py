from abc import ABC, abstractmethod
from typing import Optional


class InvoiceExtractorPort(ABC):
    """
    Port (interface) for PDF invoice extraction.

    The concrete adapter that wraps PyMuPDF lives in the infrastructure layer
    and is injected at runtime.  This keeps the application layer free of any
    dependency on PDF libraries.
    """

    @abstractmethod
    def extract(self, pdf_path: str) -> Optional[dict]:
        """
        Extract invoice data from the PDF at *pdf_path*.

        Returns a dictionary with the extracted fields (see
        ``models.invoice.extract_invoice_data`` for the expected keys) or
        ``None`` when extraction fails.
        """

    @abstractmethod
    def verify_account(self, pdf_path: str) -> tuple:
        """
        Check whether the account number in the PDF belongs to a known contract.

        Returns a ``(found: bool, account_number: str | None)`` tuple consistent
        with the existing ``verificar_conta`` helper.
        """
