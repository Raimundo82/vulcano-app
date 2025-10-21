import pytest
from unittest.mock import patch, MagicMock
from app.utils import ldap_auth


@pytest.fixture
def mock_ldap(monkeypatch):
    """Cria mocks para Server e Connection do ldap3."""
    mock_server = MagicMock(name="Server")
    mock_conn = MagicMock(name="Connection")

    # Simula comportamento do ldap3
    monkeypatch.setattr(ldap_auth, "Server", lambda *_, **__: mock_server)
    monkeypatch.setattr(ldap_auth, "Connection", lambda *_, **__: mock_conn)

    return mock_server, mock_conn


def test_authenticate_user_success(mock_ldap):
    """Deve autenticar com sucesso e devolver dicionário com utilizador."""
    _, mock_conn = mock_ldap
    mock_conn.bind.return_value = True
    mock_entry = MagicMock()
    mock_entry.displayName = "John Doe"
    mock_entry.__contains__.side_effect = lambda k: k == "displayName"
    mock_conn.entries = [mock_entry]

    result = ldap_auth.authenticate_user("john", "password123")

    assert result is not None
    assert result["username"] == "john"
    assert "display_name" in result
    assert result["display_name"] == "John Doe"
    assert "is_admin" in result


def test_authenticate_user_not_found(mock_ldap):
    """Quando o utilizador não existe no LDAP deve retornar None."""
    _, mock_conn = mock_ldap
    mock_conn.bind.return_value = True
    mock_conn.entries = []

    result = ldap_auth.authenticate_user("unknown", "password123")
    assert result is None


def test_authenticate_user_bind_fails(mock_ldap):
    """Quando a ligação LDAP falha, retorna None."""
    _, mock_conn = mock_ldap
    mock_conn.bind.return_value = False

    result = ldap_auth.authenticate_user("john", "wrongpass")
    assert result is None


def test_authenticate_user_raises_exception(monkeypatch):
    """Quando ocorre exceção, retorna None."""
    def raise_error(*_, **__):
        raise RuntimeError("Connection error")

    monkeypatch.setattr(ldap_auth, "Connection", raise_error)

    result = ldap_auth.authenticate_user("john", "password123")
    assert result is None