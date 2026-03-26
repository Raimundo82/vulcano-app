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

from ..db import get_connection  # Adicionar esta importação
from ..utils.ldap_auth import authenticate_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = authenticate_user(username, password)
        if user:
            # Update last_login in database
            conn = None
            cursor = None
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET last_login = NOW() WHERE username = %s",
                    (username,),
                )
                conn.commit()
                current_app.logger.info(
                    f"Last_login updated for user {username}"
                )  # Log de confirmação
            except Exception as e:
                conn.rollback()  # Importante fazer rollback em caso de erro
                current_app.logger.error(
                    f"Error updating last_login: {str(e)}", exc_info=True
                )
                flash("Aviso: Não foi possível registar a hora de login", "warning")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

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
