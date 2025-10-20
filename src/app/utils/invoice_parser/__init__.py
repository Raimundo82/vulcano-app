"""
Pacote de utilitários responsável por extrair, processar e validar dados de faturas PDF.

Módulos incluídos:
- parser.py: Função principal `extract_invoice_data()` para processar PDFs completos.
- extractors.py: Funções de extração específicas (datas, contribuinte, valores, etc.).
- processors.py: Funções de conversão e normalização de dados (ex: valores monetários).
- validators.py: Funções de verificação (contas, tarifários, etc.).
"""

from app.utils.invoice_parser.parser import extract_invoice_data
from app.utils.invoice_parser.extractors import (
    extrair_data_emissao,
    extrair_contribuinte,
    extrair_valor_total_da_fatura,
    extract_client_by_coordinates,
    extract_address_by_coordinates,
    extract_account,
)
from app.utils.invoice_parser.processors import process_amount_to_pay
from app.utils.invoice_parser.validators import verificar_conta, verificar_tarifario

__all__ = [
    "extract_invoice_data",
    "extrair_data_emissao",
    "extrair_contribuinte",
    "extrair_valor_total_da_fatura",
    "extract_client_by_coordinates",
    "extract_address_by_coordinates",
    "extract_account",
    "process_amount_to_pay",
    "verificar_conta",
    "verificar_tarifario",
]