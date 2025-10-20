import fitz
import re
from app.config import Config
from app.utils.invoice_parser.extractors import (
    extrair_data_emissao,
    extrair_contribuinte,
    extrair_valor_total_da_fatura,
    extract_client_by_coordinates,
    extract_address_by_coordinates,
    extract_account,
)
from app.utils.invoice_parser.processors import process_amount_to_pay
from app.utils.invoice_parser.validators import verificar_conta


def detect_invoice_type(pdf_path: str) -> str:
    """Determina o tipo de fatura com base nas contas conhecidas."""
    conta_inf = verificar_conta(pdf_path, Config.BLM_CONTRACT_NUMBERS)
    if conta_inf[0]:
        return "BLM"

    conta_inf = verificar_conta(pdf_path, Config.VOZ_CONTRACT_NUMBERS)
    if conta_inf[0]:
        return "VOZ"

    return "None"


def extract_basic_fields(pdf_path: str, text: str) -> dict:
    """Extrai campos básicos da fatura a partir do texto e coordenadas."""
    invoice_number = re.search(r"FT MV/(\d+)", text)
    reference_number = re.search(r"Nº de Referência :\s*(\d+)", text)
    issue_date = extrair_data_emissao(pdf_path)
    taxpayer_number = extrair_contribuinte(pdf_path)
    account_number = extract_account(text)
    client = extract_client_by_coordinates(pdf_path, fitz.Rect(310, 160, 550, 165))
    address = extract_address_by_coordinates(pdf_path, fitz.Rect(310, 170, 550, 230))
    cvp = re.search(r"CVP:\s*(\d{12})", text)
    invoice_period = re.search(
        r"Fatura de:\s*([a-zç]+ \d{4})|Fatura de:\s*\n\s*([a-zç]+ \d{4})",
        text,
        re.IGNORECASE,
    )

    return {
        "invoice_number": invoice_number.group(1) if invoice_number else None,
        "reference_number": reference_number.group(1) if reference_number else None,
        "issue_date": issue_date,
        "taxpayer_number": taxpayer_number,
        "account_number": account_number.group(1) if account_number else None,
        "client": client.replace("\n", "") if client else None,
        "address": address.replace("\n", "") if address else None,
        "cvp": cvp.group(1) if cvp else None,
        "invoice_period": invoice_period.group(1) if invoice_period and invoice_period.group(1) else None,
    }


def extract_amount_fields(pdf_path: str) -> tuple[float | None, float | None]:
    """Extrai os valores monetários da fatura."""
    amount_to_pay_raw = extract_address_by_coordinates(pdf_path, fitz.Rect(510, 255, 580, 265))
    total_amount = extrair_valor_total_da_fatura(pdf_path)
    amount_to_pay = process_amount_to_pay(amount_to_pay_raw) if amount_to_pay_raw else None
    return amount_to_pay, total_amount


def extract_invoice_data(pdf_path: str) -> dict | None:
    """
    Extrai todos os dados da fatura do PDF.

    Args:
        pdf_path (str): Caminho completo do ficheiro PDF.

    Returns:
        dict | None: Dicionário com os dados extraídos ou None em caso de erro.
    """
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text("text") for page in doc])

        invoice_type = detect_invoice_type(pdf_path)
        base_fields = extract_basic_fields(pdf_path, text)
        amount_to_pay, total_amount = extract_amount_fields(pdf_path)

        # Quebrar o período em mês e ano
        month, year = (None, None)
        if base_fields["invoice_period"]:
            parts = base_fields["invoice_period"].split()
            if len(parts) == 2:
                month, year = parts

        return {
            "invoice_type": invoice_type,
            "invoice_number": base_fields["invoice_number"],
            "reference_number": base_fields["reference_number"],
            "issue_date": base_fields["issue_date"],
            "taxpayer_number": base_fields["taxpayer_number"],
            "account_number": base_fields["account_number"],
            "client": base_fields["client"],
            "address": base_fields["address"],
            "cvp": base_fields["cvp"],
            "invoice_period_month": month,
            "invoice_period_year": year,
            "amount_to_pay": amount_to_pay,
            "total_amount": total_amount,
            "sent_validar": False,
            "quitar": False,
        }

    except Exception as e:
        print(f"Erro ao processar {pdf_path}: {e}")
        return None
    
