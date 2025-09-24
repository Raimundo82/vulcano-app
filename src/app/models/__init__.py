# Import functions from invoice.py
from .invoice import (
    process_amount_to_pay,
    extrair_data_emissao,
    extrair_contribuinte,
    extrair_valor_total_da_fatura,
    extract_client_by_coordinates,
    extract_address_by_coordinates,
    extract_invoice_data,
    verificar_tarifario,
    save_to_database,
)

# Import functions from user.py
from .user import register_user, get_users, add_user, edit_user, delete_user

# Import functions from unit.py
from .unit import get_units, add_unit, edit_unit, delete_unit  # Adicione este bloco

# Optionally, you can define what gets imported when using `from app.models import *`
__all__ = [
    "process_amount_to_pay",
    "extrair_data_emissao",
    "extrair_contribuinte",
    "extrair_valor_total_da_fatura",
    "extract_client_by_coordinates",
    "extract_address_by_coordinates",
    "extract_invoice_data",
    "verificar_tarifario",
    "save_to_database",
    "register_user",
    "get_users",
    "add_user",
    "edit_user",
    "delete_user",
    "get_units",
    "add_unit",
    "edit_unit",
    "delete_unit",
]
