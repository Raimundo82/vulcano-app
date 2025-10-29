import pytest
from flask import session
from unittest.mock import patch

def test_login_get_renders_form(client):
    """Deve devolver o formulário de login (GET)."""
    # A rota agora é /auth/login
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert b"username" in response.data  # Verifica se o formulário foi renderizado

def test_login_post_valid_credentials(client, mocker):
    """Deve redirecionar para a página inicial com credenciais válidas."""
    # Mock da função authenticate_user para simular um login bem-sucedido.
    # O patch é feito em 'app.routes.auth' porque é nesse módulo que a função é importada e usada.
    mocker.patch('app.routes.auth.authenticate_user', return_value={
        'username': 'testuser',
        'display_name': 'Test User',
        'is_admin': True  # Simula um admin para cobertura completa
    })

    # A rota agora é /auth/login
    response = client.post("/auth/login", data={
        'username': 'testuser',
        'password': 'password'
    }, follow_redirects=True)

    assert response.status_code == 200
    # Após o login, a sessão deve conter o username.
    with client.session_transaction() as sess:
        assert sess.get("username") == "testuser"
        assert sess.get("is_admin") is True

def test_login_post_invalid_credentials(client, mocker):
    """Deve mostrar uma mensagem de erro com credenciais inválidas."""
    # Mock da função authenticate_user para simular uma falha de login (retorna None).
    mocker.patch('app.routes.auth.authenticate_user', return_value=None)

    # A rota agora é /auth/login
    response = client.post("/auth/login", data={
        'username': 'testuser',
        'password': 'wrongpassword'
    })

    assert response.status_code == 200  # A página de login é renderizada novamente
    assert b"Credenciais inv\xc3\xa1lidas" in response.data  # "Credenciais inválidas"

def test_logout_clears_session_and_redirects(client):
    """Deve limpar a sessão e redirecionar para a página de login."""
    # Primeiro, simula um login para criar a sessão
    with client.session_transaction() as sess:
        sess["username"] = "testuser"
        sess["is_admin"] = True

    # A rota agora é /auth/logout
    response = client.get("/auth/logout")

    # Verifica o redirecionamento
    assert response.status_code == 302
    assert "/auth/login" in response.location

    # Verifica se a sessão foi limpa
    with client.session_transaction() as sess:
        assert "username" not in sess
        assert "is_admin" not in sess