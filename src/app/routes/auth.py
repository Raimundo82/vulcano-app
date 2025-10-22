# src/app/routes/auth.py
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    current_app,
)
from ..utils.ldap_auth import authenticate_user

auth_bp = Blueprint("auth", __name__)


# 🔒 GET = apenas mostrar o formulário
@auth_bp.route("/login", methods=["GET"], endpoint="login")
def login_get():
    """
    Renders the login form.
    CSRF protection is automatically applied via Flask-WTF.
    """
    return render_template("login.html")


# 🔒 POST = processar autenticação
@auth_bp.route("/login", methods=["POST"], endpoint="login_post")
def login_post():
    """
    Processes login form submission.
    CSRF protection is active by default (Flask-WTF).
    """
    username = request.form.get("username")
    password = request.form.get("password")

    # Autenticação via LDAP
    user = authenticate_user(username, password)

    if user:
        current_app.logger.info(f"User {username} authenticated via LDAP")

        # Guarda dados de sessão
        session["username"] = user["username"]
        session["display_name"] = user["display_name"]
        session["is_admin"] = user["is_admin"]

        return redirect(url_for("invoices.index"))

    flash("Credenciais inválidas", "error")
    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    """Ends session and redirects to login."""
    session.pop("username", None)
    session.pop("display_name", None)
    session.pop("is_admin", None)
    flash("Você foi desconectado com sucesso.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/check_session")
def check_session():
    """Simple route to test if user is authenticated."""
    if "username" in session:
        return f"Utilizador autenticado: {session['username']}"
    return "Utilizador não autenticado."