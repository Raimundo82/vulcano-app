from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from ..domain.repositories import UserRepository
from ..utils.ldap_auth import authenticate_user

auth_bp = Blueprint("auth", __name__)

_user_repo = UserRepository()


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = authenticate_user(username, password)
        if user:
            try:
                _user_repo.update_last_login(username)
                current_app.logger.info(f"Last_login updated for user {username}")
            except Exception as e:
                current_app.logger.error(
                    f"Error updating last_login: {str(e)}", exc_info=True
                )
                flash("Aviso: Não foi possível registar a hora de login", "warning")

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
    session.pop("username", None)
    session.pop("display_name", None)
    session.pop("is_admin", None)
    flash("Você foi desconectado com sucesso.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/check_session")
def check_session():
    if "username" in session:
        return f"Utilizador autenticado: {session['username']}"
    return "Utilizador não autenticado."
