import pytest
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
