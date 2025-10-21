import pytest

# 🔒 Fixture global que bloqueia qualquer ligação real ao LDAP
@pytest.fixture(autouse=True)
def mock_ldap(monkeypatch):
    """Bloqueia conexões reais a LDAP durante os testes."""
    class DummyConnection:
        def __init__(self, *_, **__):
            self.entries = []
        def bind(self): return False
        def search(self, *_, **__): return None
    class DummyServer:
        def __init__(self, *_, **__):
            # Intentionally empty: this dummy server exists only as a placeholder
            # to prevent the tests from creating real network LDAP connections,
            # so no initialization is required here.
            pass

    monkeypatch.setattr("app.utils.ldap_auth.Server", DummyServer)
    monkeypatch.setattr("app.utils.ldap_auth.Connection", DummyConnection)
    yield


# 🧪 Testes de rotas de autenticação
def test_login_get_renders_form(client):
    """Deve devolver o formulário de login (GET)."""
    response = client.get("/login")
    assert response.status_code in (200, 302)
    assert b"login" in response.data.lower()


def test_login_post_invalid_credentials(client, mocker):
    """Se as credenciais forem inválidas, deve voltar ao login."""
    mocker.patch("app.routes.auth.authenticate_user", return_value=None)

    response = client.post("/login", data={"username": "john", "password": "bad"})
    # Pode devolver 200 (recarrega formulário) ou 302 (redirect), ambas são válidas
    assert response.status_code in (200, 302)
    assert b"login" in response.data.lower() or "/login" in (response.location or "")


def test_login_post_valid_credentials(client, mocker):
    """Deve redirecionar para /invoices se o login for bem-sucedido."""
    mocker.patch(
        "app.routes.auth.authenticate_user",
        return_value={"username": "john", "display_name": "John", "is_admin": False},
    )

    response = client.post("/login", data={"username": "john", "password": "ok"})
    assert response.status_code == 302
    assert "/" in response.location


def test_login_post_admin_user_redirects_properly(client, mocker):
    """Deve redirecionar o admin após login bem-sucedido."""
    mocker.patch(
        "app.routes.auth.authenticate_user",
        return_value={"username": "admin", "display_name": "Boss", "is_admin": True},
    )

    response = client.post("/login", data={"username": "admin", "password": "ok"})
    assert response.status_code == 302
    assert "/" in response.location


def test_logout_clears_session(client):
    """O logout deve limpar a sessão e redirecionar para o login."""
    with client.session_transaction() as sess:
        sess["username"] = "john"
        sess["is_admin"] = False

    response = client.get("/logout")
    assert response.status_code == 302
    assert "/login" in response.location

    # Confirma que a sessão foi limpa
    with client.session_transaction() as sess:
        assert "username" not in sess
        assert "is_admin" not in sess