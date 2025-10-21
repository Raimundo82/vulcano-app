import io
import os
import pytest
from flask import Flask
from app.routes.invoices import invoices_bp


@pytest.fixture
def client(monkeypatch, tmp_path):
    """Cria app Flask isolada para testar apenas o invoices_bp."""
    app = Flask(__name__)
    app.secret_key = "test"
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        PDF_FOLDER=str(tmp_path / "pdfs"),
        PROCESSED_FOLDER=str(tmp_path / "processed"),
    )

    # ✅ Mock do render_template no módulo correto (onde é importado)
    def fake_render_template(template_name, **kwargs):
        return f"rendered {template_name}".encode("utf-8")

    monkeypatch.setattr("app.routes.invoices.render_template", fake_render_template)

    app.register_blueprint(invoices_bp, url_prefix="/invoices")

    client = app.test_client()
    with client.session_transaction() as sess:
        sess["username"] = "john"
    return client

def test_index_route_renders_template(client):
    response = client.get("/invoices/")
    assert response.status_code == 200
    assert b"html" in response.data or b"<!DOCTYPE" in response.data


def test_upload_faturas_no_file(client):
    response = client.post("/invoices/upload", data={})
    assert response.status_code == 302
    assert "/invoices" in response.location


def test_upload_faturas_invalid_extension(client):
    data = {"faturas": (io.BytesIO(b"data"), "fake.txt")}
    response = client.post("/invoices/upload", data=data, content_type="multipart/form-data")
    assert response.status_code == 302
    assert "/invoices" in response.location


def test_upload_faturas_valid_pdf(monkeypatch, client, tmp_path):
    """Mock de file.save e verificar_conta"""
    dummy_pdf = tmp_path / "dummy.pdf"
    dummy_pdf.write_bytes(b"%PDF-1.4")
    data = {"faturas": (open(dummy_pdf, "rb"), "dummy.pdf")}

    monkeypatch.setattr("app.routes.invoices.verificar_conta", lambda path: (True, "ok"))
    monkeypatch.setattr("shutil.copy", lambda src, dst: None)

    response = client.post("/invoices/upload", data=data, content_type="multipart/form-data")
    assert response.status_code == 302
    assert "/invoices" in response.location


def test_process_invoices_empty_folder(monkeypatch, client):
    monkeypatch.setattr("os.listdir", lambda _: [])
    response = client.get("/invoices/process")
    assert response.status_code == 200
    # ✅ Ajustado para verificar o mock
    assert b"rendered processar.html" in response.data


def test_process_invoices_with_mocked_files(monkeypatch, client, tmp_path):
    pdf_dir = tmp_path / "pdfs"
    pdf_dir.mkdir()
    (pdf_dir / "f1.pdf").write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("os.listdir", lambda _: ["f1.pdf"])
    monkeypatch.setattr("shutil.move", lambda src, dst: None)
    monkeypatch.setattr("os.path.exists", lambda _: False)
    monkeypatch.setattr("os.makedirs", lambda *a, **kw: None)

    response = client.get("/invoices/process")
    assert response.status_code == 200
    # ✅ Ajustado para o mock também
    assert b"rendered processar.html" in response.data


def test_faturas_route(client):
    response = client.get("/invoices/faturas")
    assert response.status_code == 200


def test_quitadas_route_admin_and_error(monkeypatch, client):
    with client.session_transaction() as sess:
        sess["is_admin"] = True

    # ✅ primeira chamada deve renderizar sem erros
    response = client.get("/invoices/quitadas")
    assert response.status_code == 200
    assert b"rendered quitadas.html" in response.data

    # ✅ segunda chamada com exceção deve redirecionar
    def raise_error(*_, **__): raise RuntimeError("fail")
    monkeypatch.setattr("app.routes.invoices.render_template", raise_error)
    response = client.get("/invoices/quitadas")
    assert response.status_code == 302
    assert "/invoices" in response.location