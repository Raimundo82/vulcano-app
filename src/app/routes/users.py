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
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..domain.repositories import UserRepository
from ..utils.auth_decorators import admin_required

users_bp = Blueprint("users", __name__)

_user_repo = UserRepository()


@users_bp.route("/users")
# @login_required
@admin_required
def list_users():
    try:
        users = [u.to_dict() for u in _user_repo.get_all()]
        return render_template(
            "users.html",
            users=users,
            username=session.get("username"),
            display_name=session.get("display_name"),
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

        if not all([username, display_name, email]):
            flash("Todos os campos são obrigatórios", "warning")
            return redirect(url_for("users.list_users"))

        _user_repo.create(username, display_name, email, is_admin)
        flash("Utilizador adicionado com sucesso!", "success")
        return redirect(url_for("users.list_users"))

    except IntegrityError:
        flash("Username ou email já existente", "danger")
    except SQLAlchemyError as err:
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

        _user_repo.update(
            user_id,
            username=username,
            display_name=display_name,
            email=email,
            is_admin=is_admin,
        )
        flash("Utilizador atualizado com sucesso!", "success")
        return redirect(url_for("users.list_users"))

    except IntegrityError:
        flash("Username ou email já existente", "danger")
    except SQLAlchemyError as err:
        current_app.logger.error(f"Database error in edit_user: {err}")
        flash("Erro ao atualizar utilizador", "danger")

    return redirect(url_for("users.list_users"))


@users_bp.route("/users/delete/<int:user_id>", methods=["POST"])
@admin_required
def delete_user(user_id):
    """Delete user (admin only)"""
    try:
        if user_id == session.get("user_id"):
            flash("Não pode apagar a sua própria conta", "danger")
            return redirect(url_for("users.list_users"))

        _user_repo.delete(user_id)
        flash("Utilizador apagado com sucesso!", "success")

    except SQLAlchemyError as err:
        current_app.logger.error(f"Database error in delete_user: {err}")
        flash("Erro ao apagar utilizador", "danger")

    return redirect(url_for("users.list_users"))
