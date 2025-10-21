import pytest
from io import BytesIO
from app.utils import pdf_utils


@pytest.fixture
def fake_faturas():
    return [
        {
            "invoice_number": "FT-001",
            "account_number": "ACC-123",
            "invoice_period_month": "Janeiro",
            "invoice_period_year": "2025",
            "total_amount": "100.50",
        },
        {
            "invoice_number": "FT-002",
            "account_number": "ACC-456",
            "invoice_period_month": "Fevereiro",
            "invoice_period_year": "2025",
            "total_amount": "200.00",
        },
    ]


def test_generate_pdf_with_table_returns_bytes(monkeypatch, fake_faturas):
    """Garante que a função gera bytes válidos."""
    class DummyApp:
        static_folder = "static"

    monkeypatch.setattr(pdf_utils, "current_app", DummyApp())

    class DummyImage:
        """Mock completo para substituir reportlab.platypus.Image."""
        h_align = "CENTER"

        # Métodos esperados pelo engine de layout
        def wrap(self, *_, **__): return (0, 0)
        def draw_on(self, *_, **__):
            # Este método está intencionalmente vazio: é um no-op usado para
            # satisfazer o engine de layout do reportlab que espera chamar
            # drawOn; o DummyImage é usado apenas para testes e não precisa
            # realizar nenhuma operação de desenho.
            pass
        # Alias compatível com o nome esperado pelo reportlab será atribuído
        # externamente para evitar violações de estilo dentro da definição da classe.
        def get_keep_with_next(self): return 0
        def get_space_after(self): return 0
        def get_space_before(self): return 0
        def get_height(self): return 0
        def get_width(self): return 0

    # Atribui o alias esperado pelo reportlab sem declarar um atributo com letra
    # maiúscula dentro do corpo da classe (evita o erro de estilo de nomenclatura).
    DummyImage.drawOn = DummyImage.draw_on
    DummyImage.getKeepWithNext = DummyImage.get_keep_with_next
    DummyImage.getSpaceAfter = DummyImage.get_space_after
    DummyImage.getSpaceBefore = DummyImage.get_space_before
    DummyImage.getHeight = DummyImage.get_height
    DummyImage.getWidth = DummyImage.get_width

    monkeypatch.setattr(pdf_utils, "Image", lambda *_, **__: DummyImage())

    result = pdf_utils.generate_pdf_with_table(fake_faturas)
    assert isinstance(result, (bytes, bytearray))
    assert len(result) > 0


def test_generate_pdf_with_table_handles_invalid_image(monkeypatch, fake_faturas):
    """Simula falha ao criar imagem e verifica que uma exceção específica é lançada."""
    class DummyApp:
        static_folder = "static"

    monkeypatch.setattr(pdf_utils, "current_app", DummyApp())

    def raise_ioerror(*_, **__):
        raise IOError("invalid image")

    monkeypatch.setattr(pdf_utils, "Image", raise_ioerror)

    with pytest.raises(IOError):
        pdf_utils.generate_pdf_with_table(fake_faturas)