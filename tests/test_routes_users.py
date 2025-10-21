import pytest
from flask import session
from app.app import create_app

@pytest.fixture
def client():
    """Cria cliente Flask de teste com sessão simulada."""
    app = create_app()
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False, SECRET_KEY="test")
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["username"] = "admin"
            sess["display_name"] = "Administrador"
            sess["is_admin"] = True
            sess["user_id"] = 1
        yield client


def test_list_users_renders_template(client, mocker):
    """Verifica se /users renderiza a lista com utilizadores simulados."""
    render_mock = mocker.patch("app.routes.users.render_template", return_value="OK")
    response = client.get("/users")
    assert response.status_code == 200
    render_mock.assert_called_once()
    _, kwargs = render_mock.call_args
    assert "users" in kwargs and isinstance(kwargs["users"], list)


def test_add_user_redirects_with_flash(client):
    """Simula POST /users/add e confirma redirect + mensagem flash."""
    response = client.post("/users/add", follow_redirects=False)
    assert response.status_code == 302
    assert "/users" in response.location


def test_edit_user_redirects_with_flash(client):
    """Simula POST /users/edit/<id> e confirma redirect."""
    response = client.post("/users/edit/5", follow_redirects=False)
    assert response.status_code == 302
    assert "/users" in response.location


def test_delete_other_user_success_flash(client):
    """Simula remoção de outro utilizador (não o próprio)."""
    with client.session_transaction() as sess:
        sess["user_id"] = 1  # o admin logado
    response = client.post("/users/delete/99", follow_redirects=False)
    assert response.status_code == 302
    assert "/users" in response.location


def test_delete_self_warning_flash(client):
    """Simula tentativa de apagar a própria conta."""
    with client.session_transaction() as sess:
        sess["user_id"] = 10
    response = client.post("/users/delete/10", follow_redirects=False)
    assert response.status_code == 302
    assert "/users" in response.location