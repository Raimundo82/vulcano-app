import pytest
from app.utils.invoice_parser.validators import verificar_tarifario


def test_verificar_tarifario_true(mocker):
    fake_page = mocker.MagicMock()
    fake_page.get_text.return_value = "Plano inclui TARIFARIO GOLD"
    fake_doc = [fake_page]
    mocker.patch("fitz.open", return_value=fake_doc)

    result = verificar_tarifario("fake.pdf", "TARIFARIO GOLD")
    assert result is True


def test_verificar_tarifario_false(mocker):
    fake_page = mocker.MagicMock()
    fake_page.get_text.return_value = "Sem tarifário"
    fake_doc = [fake_page]
    mocker.patch("fitz.open", return_value=fake_doc)

    result = verificar_tarifario("fake.pdf", "TARIFARIO GOLD")
    assert result is False


def test_verificar_tarifario_exception(mocker):
    mocker.patch("fitz.open", side_effect=Exception("Erro simulado"))
    result = verificar_tarifario("fake.pdf", "TARIFARIO GOLD")
    assert result is False