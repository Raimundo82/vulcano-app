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
        yield client


def test_list_units_renders_template(client, mocker):
    """Verifica se /units renderiza corretamente a lista dummy."""
    render_mock = mocker.patch("app.routes.units.render_template", return_value="OK")
    response = client.get("/units")
    assert response.status_code == 200
    render_mock.assert_called_once()
    _, kwargs = render_mock.call_args
    assert "units" in kwargs and isinstance(kwargs["units"], list)


def test_add_unit_redirects_with_flash(client):
    """Verifica se /units/add redireciona corretamente."""
    response = client.post("/units/add", follow_redirects=False)
    assert response.status_code == 302
    assert "/units" in response.location


def test_edit_unit_redirects_with_flash(client):
    """Verifica se /units/edit/<id> redireciona corretamente."""
    response = client.post("/units/edit/7", follow_redirects=False)
    assert response.status_code == 302
    assert "/units" in response.location


def test_delete_unit_redirects_with_flash(client):
    """Verifica se /units/delete/<id> redireciona corretamente."""
    response = client.post("/units/delete/7", follow_redirects=False)
    assert response.status_code == 302
    assert "/units" in response.location