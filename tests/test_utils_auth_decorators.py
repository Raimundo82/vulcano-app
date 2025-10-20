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