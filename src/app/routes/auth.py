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
# from ..db_legacy import get_connection  # ❌ Legacy import (disabled — now using ORM soon)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Temporary migration-safe version:
    - Keeps LDAP authentication working.
    - Disables MySQL calls (until we migrate to SQLAlchemy).
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Authenticate via LDAP (this still works fine)
        user = authenticate_user(username, password)

        if user:
            # ✅ Temporarily skip DB updates for last_login
            # conn = get_connection()
            # cursor = conn.cursor()
            # cursor.execute(
            #     "UPDATE users SET last_login = NOW() WHERE username = %s",
            #     (username,),
            # )
            # conn.commit()

            current_app.logger.info(f"User {username} authenticated via LDAP")

            # Set session variables
            session["username"] = user["username"]
            session["display_name"] = user["display_name"]
            session["is_admin"] = user["is_admin"]

            return redirect(url_for("invoices.index"))

        else:
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