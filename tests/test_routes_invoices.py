import io
import os
import pytest
from unittest.mock import patch, MagicMock
from flask import session
from app.routes.invoices import invoices_bp

def test_upload_faturas_no_files(client):
    """Testa upload sem arquivos."""
    with client.session_transaction() as sess:
        sess["username"] = "test"
    response = client.post("/invoices/upload", data={})
    assert response.status_code == 302
    assert "/invoices/" in response.location

def test_upload_faturas_invalid_file(client):
    """Testa upload com arquivo não PDF."""
    with client.session_transaction() as sess:
        sess["username"] = "test"
    data = {"faturas": (io.BytesIO(b"data"), "fake.txt")}
    response = client.post("/invoices/upload", data=data, content_type="multipart/form-data")
    assert response.status_code == 302
    assert "/invoices/" in response.location

def test_upload_faturas_valid_pdf_success(client, mocker, tmp_path):
    """Testa upload com PDF válido."""
    with client.session_transaction() as sess:
        sess["username"] = "test"
    dummy_pdf = tmp_path / "dummy.pdf"
    dummy_pdf.write_bytes(b"%PDF-1.4")
    data = {"faturas": (open(dummy_pdf, "rb"), "dummy.pdf")}
    
    # Mock verificar_conta para sucesso
    mocker.patch("app.routes.invoices.verificar_conta", return_value=(True, "ok"))
    # Mock shutil.copy
    mocker.patch("shutil.copy")
    
    response = client.post("/invoices/upload", data=data, content_type="multipart/form-data")
    assert response.status_code == 302
    assert "/invoices/" in response.location

def test_upload_faturas_valid_pdf_failure(client, mocker, tmp_path):
    """Testa upload com PDF inválido (verificar_conta falha)."""
    with client.session_transaction() as sess:
        sess["username"] = "test"
    dummy_pdf = tmp_path / "dummy.pdf"
    dummy_pdf.write_bytes(b"%PDF-1.4")
    data = {"faturas": (open(dummy_pdf, "rb"), "dummy.pdf")}
    
    # Mock verificar_conta para falha
    mocker.patch("app.routes.invoices.verificar_conta", return_value=(False, "invalid"))
    # Mock os.remove
    mocker.patch("os.remove")
    
    response = client.post("/invoices/upload", data=data, content_type="multipart/form-data")
    assert response.status_code == 302
    assert "/invoices/" in response.location

def test_process_invoices_empty_folder(client, mocker):
    """Testa process com pasta vazia."""
    with client.session_transaction() as sess:
        sess["username"] = "test"
    mocker.patch("os.listdir", return_value=[])
    response = client.get("/invoices/process")
    assert response.status_code == 200

def test_process_invoices_no_data(client, mocker, tmp_path):
    """Testa process com arquivo PDF mas sem dados extraídos."""
    with client.session_transaction() as sess:
        sess["username"] = "test"
    pdf_dir = tmp_path / "pdfs"
    pdf_dir.mkdir()
    (pdf_dir / "f1.pdf").write_bytes(b"%PDF-1.4")
    
    mocker.patch("os.listdir", return_value=["f1.pdf"])
    # extract_invoice_data retorna [] (sem dados)
    mocker.patch("app.routes.invoices.extract_invoice_data", return_value=[])
    
    response = client.get("/invoices/process")
    assert response.status_code == 200

def test_process_invoices_with_data(client, mocker, tmp_path):
    """Testa process com dados extraídos (cobre linhas 94-114)."""
    with client.session_transaction() as sess:
        sess["username"] = "test"
    pdf_dir = tmp_path / "pdfs"
    pdf_dir.mkdir()
    (pdf_dir / "f1.pdf").write_bytes(b"%PDF-1.4")
    
    mocker.patch("os.listdir", return_value=["f1.pdf"])
    mocker.patch("app.routes.invoices.extract_invoice_data", return_value={
        "invoice_type": "FT",
        "issue_date": "2023-10-01",
        "invoice_number": "12345",
        "client": "ClienteTeste",
        "invoice_period_year": "2023",
        "invoice_period_month": "10"
    })
    mocker.patch("os.makedirs")
    mocker.patch("os.path.exists", return_value=False)
    mocker.patch("shutil.move")
    
    response = client.get("/invoices/process")
    assert response.status_code == 200

def test_process_invoices_file_exists(client, mocker, tmp_path):
    """Testa process quando arquivo já existe (cobre os.remove)."""
    with client.session_transaction() as sess:
        sess["username"] = "test"
    pdf_dir = tmp_path / "pdfs"
    pdf_dir.mkdir()
    (pdf_dir / "f1.pdf").write_bytes(b"%PDF-1.4")
    
    mocker.patch("os.listdir", return_value=["f1.pdf"])
    mocker.patch("app.routes.invoices.extract_invoice_data", return_value={
        "invoice_type": "FT",
        "issue_date": "2023-10-01",
        "invoice_number": "12345",
        "client": "ClienteTeste",
        "invoice_period_year": "2023",
        "invoice_period_month": "10"
    })
    mocker.patch("os.makedirs")
    mocker.patch("os.path.exists", return_value=True)  # Arquivo existe
    mocker.patch("os.remove")
    mocker.patch("shutil.move")
    
    response = client.get("/invoices/process")
    assert response.status_code == 200

def test_get_faturas_success(client, mocker):
    """Testa GET /api/faturas sucesso."""
    with client.session_transaction() as sess:
        sess["username"] = "test"
    # Mock Invoice.query
    mock_invoice = MagicMock()
    mock_invoice.id = 1
    mock_invoice.invoice_type = "FT"
    mock_invoice.invoice_number = "123"
    mock_invoice.issue_date = "2023-01-01"
    mock_invoice.taxpayer_number = "123456"
    mock_invoice.account_number = "789"
    mock_invoice.client = "Test"
    mock_invoice.invoice_period_year = 2023
    mock_invoice.invoice_period_month = 10
    mock_invoice.amount_to_pay = 100.0
    mock_invoice.total_amount = 120.0
    mock_invoice.sent_validar = False
    mock_invoice.quitar = False
    mock_invoice.pdffile = "file.pdf"
    
    # Corrigir o mock para a cadeia de chamadas real: query.filter_by(...).all()
    mock_query = mocker.patch("app.routes.invoices.Invoice.query")
    mock_query.filter_by.return_value.all.return_value = [mock_invoice]
    
    response = client.get("/invoices/api/faturas")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["invoice_number"] == "123"

def test_get_faturas_db_error(client, mocker):
    """Testa GET /api/faturas erro de BD."""
    with client.session_transaction() as sess:
        sess["username"] = "test"
    from sqlalchemy.exc import SQLAlchemyError
    
    # Corrigir o mock para a cadeia de chamadas real e fazer com que .all() lance o erro
    mock_query = mocker.patch("app.routes.invoices.Invoice.query")
    mock_query.filter_by.return_value.all.side_effect = SQLAlchemyError("DB error")
    
    response = client.get("/invoices/api/faturas")
    assert response.status_code == 500
    data = response.get_json()
    assert "error" in data

def test_faturas_route(client):
    """Testa rota /faturas."""
    with client.session_transaction() as sess:
        sess["username"] = "test"
    response = client.get("/invoices/faturas")
    assert response.status_code == 200

def test_quitadas_route_success(client):
    """Testa rota /quitadas sucesso."""
    with client.session_transaction() as sess:
        sess["username"] = "test"
        sess["is_admin"] = True
    response = client.get("/invoices/quitadas")
    assert response.status_code == 200

def test_quitadas_route_error(client, mocker):
    """Testa rota /quitadas erro."""
    with client.session_transaction() as sess:
        sess["username"] = "test"
        sess["is_admin"] = True
    mocker.patch("app.routes.invoices.render_template", side_effect=Exception("Render error"))
    
    response = client.get("/invoices/quitadas")
    assert response.status_code == 302
    assert "/invoices/" in response.location