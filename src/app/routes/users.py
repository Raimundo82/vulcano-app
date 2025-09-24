import mysql.connector
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
    abort,
    current_app,
)
from ..utils.auth_decorators import login_required, admin_required
from ..config import Config
from ..db import get_connection

users_bp = Blueprint("users", __name__)


@users_bp.route("/users")
# @login_required
@admin_required
def list_users():
    try:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    """
                    SELECT id, username, display_name, email, is_admin, last_login
                    FROM users
                    ORDER BY is_admin DESC, username ASC
                """
                )
                users = cursor.fetchall()

        # Pass both users list and current username to template
        return render_template(
            "users.html",
            users=users,
            username=session.get("username"),
            display_name=session.get("display_name"),  # Add this
            is_admin=session.get("is_admin", False),
        )

    except Exception as e:
        current_app.logger.error(f"User list error: {str(e)}")
        flash("Erro ao carregar lista de usuários", "danger")
        return redirect(url_for("invoices.index"))


@users_bp.route("/users/add", methods=["POST"])
@admin_required
def add_user():
    """Add new user (admin only)"""
    try:
        username = request.form.get("username", "").strip()
        display_name = request.form.get("display_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        is_admin = "is_admin" in request.form

        # Basic validation
        if not all([username, display_name, email]):
            flash("Todos os campos são obrigatórios", "warning")
            return redirect(url_for("users.list_users"))

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (username, display_name, email, is_admin)
                    VALUES (%s, %s, %s, %s)
                """,
                    (username, display_name, email, is_admin),
                )
                conn.commit()

        flash("Utilizador adicionado com sucesso!", "success")
        return redirect(url_for("users.list_users"))

    except mysql.connector.IntegrityError:
        flash("Username ou email já existente", "danger")
    except mysql.connector.Error as err:
        current_app.logger.error(f"Database error in add_user: {err}")
        flash("Erro ao adicionar utilizador", "danger")

    return redirect(url_for("users.list_users"))


@users_bp.route("/users/edit/<int:user_id>", methods=["POST"])
@admin_required
def edit_user(user_id):
    """Edit existing user (admin only)"""
    try:
        username = request.form.get("username", "").strip()
        display_name = request.form.get("display_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        is_admin = "is_admin" in request.form

        if not all([username, display_name, email]):
            flash("Todos os campos são obrigatórios", "warning")
            return redirect(url_for("users.list_users"))

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users
                    SET username = %s, display_name = %s,
                        email = %s, is_admin = %s
                    WHERE id = %s
                """,
                    (username, display_name, email, is_admin, user_id),
                )
                conn.commit()

        flash("Utilizador atualizado com sucesso!", "success")
        return redirect(url_for("users.list_users"))

    except mysql.connector.IntegrityError:
        flash("Username ou email já existente", "danger")
    except mysql.connector.Error as err:
        current_app.logger.error(f"Database error in edit_user: {err}")
        flash("Erro ao atualizar utilizador", "danger")

    return redirect(url_for("users.list_users"))


@users_bp.route("/users/delete/<int:user_id>", methods=["POST"])
@admin_required
def delete_user(user_id):
    """Delete user (admin only)"""
    try:
        # Prevent self-deletion
        if user_id == session.get("user_id"):
            flash("Não pode apagar a sua própria conta", "danger")
            return redirect(url_for("users.list_users"))

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                conn.commit()

        flash("Utilizador apagado com sucesso!", "success")
    except mysql.connector.Error as err:
        current_app.logger.error(f"Database error in delete_user: {err}")
        flash("Erro ao apagar utilizador", "danger")

    return redirect(url_for("users.list_users"))
