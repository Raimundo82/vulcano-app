from app.models.invoice import save_to_database, Invoice

def test_save_to_database_creates_new_invoice(app):
    """Verifica se uma fatura nova é criada corretamente."""
    data = {
        "invoice_type": "BLM",
        "invoice_number": "FT-001",
        "issue_date": "2025-01-01",
        "taxpayer_number": "123456789",
        "account_number": "998877",
        "client": "Marinha Portuguesa",
        "address": "Rua do Arsenal, Lisboa",
        "cvp": "123456789012",
        "invoice_period_month": "Janeiro",
        "invoice_period_year": "2025",
        "total_amount": 100.50,
        "amount_to_pay": 100.50,
    }

    save_to_database(data)
    invoice = Invoice.query.filter_by(invoice_number="FT-001").first()

    assert invoice is not None
    assert invoice.invoice_type == "BLM"
    assert invoice.client == "Marinha Portuguesa"


def test_save_to_database_updates_existing_invoice(app):
    """Verifica se uma fatura existente é atualizada corretamente."""
    initial = Invoice(invoice_number="FT-002", total_amount=100)
    from app.extensions.db import db
    db.session.add(initial)
    db.session.commit()

    data = {"invoice_number": "FT-002", "total_amount": 200}
    save_to_database(data)

    updated = Invoice.query.filter_by(invoice_number="FT-002").first()
    assert updated.total_amount == 200


def test_save_to_database_handles_db_error(app, mocker):
    """Garante que save_to_database() trata erros de base de dados sem crashar."""
    from app.models.invoice import save_to_database

    # Dados mínimos simulados
    data = {
        "invoice_number": "FT-999",
        "invoice_type": "VOZ",
        "issue_date": "2025-01-01",
        "taxpayer_number": "999999999",
        "account_number": "12345",
        "client": "Erro Simulado",
        "address": "Rua Teste 123",
        "cvp": "000000000000",
        "invoice_period_month": "Janeiro",
        "invoice_period_year": "2025",
        "total_amount": 10.0,
        "amount_to_pay": 10.0,
    }

    # Simula erro de commit na base de dados
    mocker.patch("app.models.invoice.db.session.commit", side_effect=Exception("DB Error"))

    # Executa dentro do contexto Flask
    with app.app_context():
        save_to_database(data)
    """Garante que save_to_database() trata erros de base de dados sem crashar."""
    # Dados de fatura mínimos
    data = {
        "invoice_number": "FT-999",
        "invoice_type": "VOZ",
        "issue_date": "2025-01-01",
        "taxpayer_number": "999999999",
        "account_number": "12345",
        "client": "Erro Simulado",
        "address": "Rua Teste 123",
        "cvp": "000000000000",
        "invoice_period_month": "Janeiro",
        "invoice_period_year": "2025",
        "total_amount": 10.0,
        "amount_to_pay": 10.0,
    }

    # Simula erro de base de dados (p.ex. conexão perdida)
    mocker.patch("app.models.invoice.db.session.commit", side_effect=Exception("DB Error"))

    # Chamada não deve lançar exceção
    save_to_database(data)