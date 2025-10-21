import os
import pytest
from flask import Flask, session, Response
from app.utils.auth_decorators import login_required, admin_required

@pytest.fixture
def app():
    """Cria app Flask simples para testar decorators."""
    app = Flask(__name__)
    app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(24)

    # --- Rotas simuladas ---
    @app.route("/login")
    def login():
        return "login page"
    app.add_url_rule("/login", endpoint="auth.login", view_func=login)

    # ✅ Adiciona rota dummy para invoices.index (usada pelo admin_required)
    @app.route("/invoices")
    def invoices_index():
        return "invoices page"
    app.add_url_rule("/invoices", endpoint="invoices.index", view_func=invoices_index)

    # --- Rotas protegidas ---
    @app.route("/protected")
    @login_required
    def protected():
        return "protected"

    @app.route("/admin")
    @admin_required
    def admin():
        return "admin"

    return app

def test_login_required_redirects_when_not_logged_in(app):
    """Deve redirecionar para login quando o utilizador não está autenticado."""
    with app.test_client() as client:
        response = client.get("/protected")
        assert response.status_code == 302
        assert "/login" in response.location


def test_login_required_allows_access_when_logged_in(app):
    """Deve permitir acesso quando há utilizador autenticado (session['username'])."""
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["username"] = "john"
        response = client.get("/protected")
        assert response.status_code == 200
        assert b"protected" in response.data


def test_admin_required_redirects_if_not_admin(app):
    """Deve redirecionar para invoices.index quando não é admin."""
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["username"] = "john"
            sess["is_admin"] = False
        response = client.get("/admin")
        assert response.status_code == 302
        assert "/invoices" in response.location


def test_admin_required_allows_access_if_admin(app):
    """Deve permitir acesso quando é admin."""
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["username"] = "admin"
            sess["is_admin"] = True
        response = client.get("/admin")
        assert response.status_code == 200
        assert b"admin" in response.data

def test_login_required_redirects_if_no_username(app):
    """Deve redirecionar para login se não existir 'username' na sessão."""
    with app.test_client() as client:
        response = client.get("/protected")
        assert response.status_code == 302
        assert "/login" in response.location