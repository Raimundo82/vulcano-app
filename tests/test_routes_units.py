import pytest
from flask import session
from app.app import create_app
from app.models.unit import Unit

def test_list_units_renders_template(client, mocker):
    """Verifica se /units/ renderiza corretamente a lista (usando BD de teste vazia)."""
    # Configura sessão para simular utilizador logado
    with client.session_transaction() as sess:
        sess["username"] = "admin"
        sess["display_name"] = "Administrador"
        sess["is_admin"] = True
    render_mock = mocker.patch("app.routes.units.render_template", return_value="OK")
    # A rota correta é /units/ (com a barra no final)
    response = client.get("/units/")
    assert response.status_code == 200
    render_mock.assert_called_once()
    _, kwargs = render_mock.call_args
    assert "units" in kwargs and isinstance(kwargs["units"], list)
    assert kwargs["units"] == []  # A BD está vazia, então lista vazia

def test_add_unit_redirects_with_flash(client):
    """Verifica se /units/add redireciona corretamente."""
    # Configura sessão para simular utilizador logado e admin
    with client.session_transaction() as sess:
        sess["username"] = "admin"
        sess["display_name"] = "Administrador"
        sess["is_admin"] = True
    response = client.post("/units/add", follow_redirects=False)
    assert response.status_code == 302
    # O redirecionamento deve ser para /units/
    assert "/units/" in response.location

def test_edit_unit_redirects_with_flash(client):
    """Verifica se /units/edit/<id> redireciona corretamente."""
    # Configura sessão para simular utilizador logado e admin
    with client.session_transaction() as sess:
        sess["username"] = "admin"
        sess["display_name"] = "Administrador"
        sess["is_admin"] = True
    response = client.post("/units/edit/7", follow_redirects=False)
    assert response.status_code == 302
    # O redirecionamento deve ser para /units/
    assert "/units/" in response.location

def test_delete_unit_redirects_with_flash(client):
    """Verifica se /units/delete/<id> redireciona corretamente."""
    # Configura sessão para simular utilizador logado e admin
    with client.session_transaction() as sess:
        sess["username"] = "admin"
        sess["display_name"] = "Administrador"
        sess["is_admin"] = True
    response = client.post("/units/delete/7", follow_redirects=False)
    assert response.status_code == 302
    # O redirecionamento deve ser para /units/
    assert "/units/" in response.location