import os
import shutil
import tempfile
from typing import List, Tuple

from ...ports.invoice_extractor_port import InvoiceExtractorPort


class UploadInvoicesUseCase:
    """
    Validate and stage uploaded invoice PDF files.

    Each file is checked against the configured contract numbers (via the
    injected :class:`InvoiceExtractorPort`) and copied to the staging
    directory only when the account number is recognised.
    """

    def __init__(
        self, invoice_extractor: InvoiceExtractorPort, pdfs_dir: str
    ) -> None:
        self._extractor = invoice_extractor
        self._pdfs_dir = pdfs_dir

    def execute(self, files) -> Tuple[List[str], List[str], List[str]]:
        """
        Process a list of werkzeug FileStorage objects.

        Returns a three-tuple of (accepted, rejected, invalid) filename lists:
          - accepted: PDFs with a recognised contract number
          - rejected: PDFs whose account number was not found in the contract lists
          - invalid:  Files that are not PDFs
        """
        accepted: List[str] = []
        rejected: List[str] = []
        invalid: List[str] = []

        for file in files:
            if not file.filename.endswith(".pdf"):
                invalid.append(file.filename)
                continue

            temp_path = os.path.join(tempfile.gettempdir(), file.filename)
            file.save(temp_path)

            try:
                found, _ = self._extractor.verify_account(temp_path)
                if found:
                    dest = os.path.join(self._pdfs_dir, file.filename)
                    shutil.copy(temp_path, dest)
                    accepted.append(file.filename)
                else:
                    rejected.append(file.filename)
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        return accepted, rejected, invalid
