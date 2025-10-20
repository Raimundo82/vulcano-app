from app.utils.invoice_parser.parser import verificar_conta, extract_invoice_data
from app.utils.invoice_parser.extractors import verificar_tarifario, extrair_data_emissao
import pytest

def test_verificar_conta_detecta_conta(mocker):
    fake_pdf = mocker.MagicMock()
    fake_page = mocker.MagicMock()
    fake_page.get_text.return_value = "Nº Conta: 12345"
    fake_pdf.__iter__.return_value = [fake_page]

    mocker.patch("fitz.open", return_value=fake_pdf)
    result = verificar_conta("fake_path.pdf", ["12345"])  # <--- passa a lista aqui
    assert result == (True, "12345")


def test_verificar_tarifario_true(mocker):
    # cria página falsa
    fake_page = mocker.MagicMock()
    fake_page.get_text.return_value = "Plano X inclui TARIFARIO GOLD"

    # cria "documento" falso que funciona como context manager e iterável
    fake_doc = mocker.MagicMock()
    fake_doc.__iter__.return_value = [fake_page]
    fake_doc.__enter__.return_value = fake_doc
    fake_doc.__exit__.return_value = None

    # patch ao fitz.open para devolver o nosso documento falso
    mocker.patch("fitz.open", return_value=fake_doc)

    assert verificar_tarifario("fake.pdf", "TARIFARIO GOLD") is True


def test_verificar_tarifario_false(mocker):
    fake_page = mocker.MagicMock()
    fake_page.get_text.return_value = "Sem tarifário"

    fake_doc = mocker.MagicMock()
    fake_doc.__iter__.return_value = [fake_page]
    fake_doc.__enter__.return_value = fake_doc
    fake_doc.__exit__.return_value = None

    mocker.patch("fitz.open", return_value=fake_doc)

    assert verificar_tarifario("fake.pdf", "TARIFARIO GOLD") is False


from app.utils.invoice_parser import parser
def test_extract_invoice_data_full(mocker):
    fake_page = mocker.MagicMock()
    fake_page.get_text.return_value = (
        "FT MV/4321 Nº Contribuinte: 111111111 Nº Conta: 55555 CVP: 123456789012 Fatura de: Janeiro 2025"
    )
    fake_doc = [fake_page]
    mocker.patch("fitz.open", return_value=fake_doc)

    # Patches para todas as dependências internas
    mocker.patch("app.utils.invoice_parser.parser.extrair_data_emissao", return_value="2025-01-01")
    mocker.patch("app.utils.invoice_parser.parser.extrair_contribuinte", return_value="111111111")
    mocker.patch("app.utils.invoice_parser.parser.extrair_valor_total_da_fatura", return_value=99.99)
    mocker.patch("app.utils.invoice_parser.parser.process_amount_to_pay", return_value=99.99)
    mocker.patch("app.utils.invoice_parser.parser.verificar_conta", return_value=(True, "55555"))
    mocker.patch("app.utils.invoice_parser.parser.extract_client_by_coordinates", return_value="Marinha Portuguesa")
    mocker.patch("app.utils.invoice_parser.parser.extract_address_by_coordinates", return_value="Rua do Arsenal, Lisboa")

    # Mock compatível com re.Match
    mock_match = mocker.MagicMock()
    mock_match.group.return_value = "55555"
    mocker.patch("app.utils.invoice_parser.parser.extract_account", return_value=mock_match)

    data = parser.extract_invoice_data("fake.pdf")

    assert data["invoice_number"] == "4321"
    assert data["taxpayer_number"] == "111111111"
    assert data["amount_to_pay"] == pytest.approx(99.99)
    assert data["client"] == "Marinha Portuguesa"
    assert data["address"] == "Rua do Arsenal, Lisboa"
    assert data["address"] == "Rua do Arsenal, Lisboa"
 
