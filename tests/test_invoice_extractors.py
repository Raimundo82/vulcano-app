import pytest
from unittest.mock import MagicMock
import fitz
from app.utils.invoice_parser.processors import process_amount_to_pay
from app.utils.invoice_parser.extractors import extrair_data_emissao, extrair_contribuinte, extrair_valor_total_da_fatura, extract_account, extract_client_by_coordinates, extract_address_by_coordinates

def test_process_amount_to_pay():
    assert process_amount_to_pay("1 234,56 €") == pytest.approx(1234.56, rel=1e-3)
    assert process_amount_to_pay("€99.9") == pytest.approx(99.9, rel=1e-3)
    assert process_amount_to_pay("invalid") is None


def test_extrair_data_emissao_returns_expected_value(mocker):
    fake_page = mocker.MagicMock()
    fake_page.search_for.return_value = [(100, 200, 300, 220)]
    fake_page.get_textbox.return_value = "2025-10-14"
    fake_doc = [fake_page]
    mocker.patch("fitz.open", return_value=fake_doc)

    result = extrair_data_emissao("fake.pdf")
    assert result == "2025-10-14"
    fake_page.search_for.assert_called_once_with("Data de emissão:")

def test_extract_account_valid_number():
    text = "Nº Conta: 987654"
    account = extract_account(text)
    assert account == "987654"

def test_extract_account_no_number():
    text = "Sem número de conta"
    match = extract_account(text)
    assert match is None

def test_extrair_contribuinte_returns_expected_value(mocker):
    fake_page = mocker.MagicMock()
    fake_page.search_for.return_value = [(100, 200, 300, 220)]
    fake_page.get_textbox.return_value = "123456789"
    fake_doc = [fake_page]
    mocker.patch("fitz.open", return_value=fake_doc)

    result = extrair_contribuinte("fake.pdf")
    assert result == "123456789"


def test_extrair_valor_total_da_fatura_valid(mocker):
    fake_page = mocker.MagicMock()
    fake_page.search_for.return_value = [(510, 100, 620, 120)]
    fake_page.get_textbox.return_value = "1 234,56 €"
    fake_doc = [fake_page]
    mocker.patch("fitz.open", return_value=fake_doc)

    valor = extrair_valor_total_da_fatura("fake.pdf")
    assert isinstance(valor, float)
    assert valor == pytest.approx(1234.56, rel=1e-3)


def test_extract_client_and_address_by_coordinates(mocker):
    fake_page = mocker.MagicMock()
    fake_page.get_textbox.return_value = "Rua do Arsenal"
    fake_doc = [fake_page]
    mocker.patch("fitz.open", return_value=fake_doc)

    result_client = extract_client_by_coordinates("fake.pdf", (0, 0, 100, 100))
    result_address = extract_address_by_coordinates("fake.pdf", (0, 0, 100, 100))
    assert "Rua" in result_client
    assert "Rua" in result_address

# 1️⃣ Falha ao abrir o PDF (cobre blocos try/except iniciais)
def test_extrair_data_emissao_handles_open_error(mocker):
    mocker.patch("fitz.open", side_effect=Exception("file error"))
    result = extrair_data_emissao("bad.pdf")
    assert result is None


def test_extrair_contribuinte_handles_search_error(mocker):
    fake_page = MagicMock()
    fake_page.search_for.side_effect = Exception("read fail")
    mocker.patch("fitz.open", return_value=[fake_page])
    result = extrair_contribuinte("broken.pdf")
    assert result is None


# 2️⃣ Nenhuma caixa encontrada (search_for vazio)
def test_extrair_valor_total_da_fatura_empty_result(mocker):
    fake_page = MagicMock()
    fake_page.search_for.return_value = []
    mocker.patch("fitz.open", return_value=[fake_page])
    result = extrair_valor_total_da_fatura("empty.pdf")
    assert result is None


# 3️⃣ Texto malformado (sem número, sem símbolo €)
def test_extrair_valor_total_da_fatura_invalid_text(mocker):
    fake_page = MagicMock()
    fake_page.search_for.return_value = [(0, 0, 100, 100)]
    fake_page.get_textbox.return_value = "texto sem número"
    mocker.patch("fitz.open", return_value=[fake_page])
    result = extrair_valor_total_da_fatura("weird.pdf")
    assert result is None


# 4️⃣ extract_account com múltiplos matches e espaços estranhos
def test_extract_account_with_extra_spaces():
    text = "Nº Conta :     00123"
    result = extract_account(text)
    assert result == "00123"


# 5️⃣ extract_client_by_coordinates com erro interno
def test_extract_client_by_coordinates_handles_error(mocker):
    mocker.patch("fitz.open", side_effect=Exception("fail"))
    result = extract_client_by_coordinates("broken.pdf", fitz.Rect(0, 0, 10, 10))
    assert result is None


# 6️⃣ extract_address_by_coordinates devolve vazio
def test_extract_address_by_coordinates_empty(mocker):
    fake_page = MagicMock()
    fake_page.get_textbox.return_value = ""
    mocker.patch("fitz.open", return_value=[fake_page])
    result = extract_address_by_coordinates("fake.pdf", fitz.Rect(0, 0, 10, 10))
    assert result is None


# 7️⃣ Funções que retornam múltiplas páginas — testam loops
def test_extrair_data_emissao_multiple_pages(mocker):
    page1 = MagicMock()
    page2 = MagicMock()
    page1.search_for.return_value = []
    page2.search_for.return_value = [(1, 2, 3, 4)]
    page2.get_textbox.return_value = "2025-01-01"
    mocker.patch("fitz.open", return_value=[page1, page2])
    result = extrair_data_emissao("multi.pdf")
    assert result == "2025-01-01"
