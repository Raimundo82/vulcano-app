# src/app/routes/users.py
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

users_bp = Blueprint("users", __name__)

USERS_INDEX_LIST = "users.list_users"

# 🧩 Migration phase: all DB calls disabled so Alembic can import models
# After migration succeeds, these routes will be refactored to ORM-based versions.


@users_bp.route("/users")
@admin_required
def list_users():
    """List placeholder users (migration mode)"""
    dummy_users = [
        {"id": 1, "username": "admin", "display_name": "Administrador", "email": "admin@example.com", "is_admin": True},
        {"id": 2, "username": "john", "display_name": "John Doe", "email": "john@example.com", "is_admin": False},
    ]

    return render_template(
        "users.html",
        users=dummy_users,
        username=session.get("username"),
        display_name=session.get("display_name"),
        is_admin=session.get("is_admin", False),
    )


@users_bp.route("/users/add", methods=["POST"])
@admin_required
def add_user():
    """Temporarily disabled DB logic"""
    flash("Utilizador adicionado (modo simulado).", "success")
    return redirect(url_for(USERS_INDEX_LIST))


@users_bp.route("/users/edit/<int:user_id>", methods=["POST"])
@admin_required
def edit_user(user_id):
    """Temporarily disabled DB logic"""
    flash(f"Utilizador {user_id} atualizado (modo simulado).", "success")
    return redirect(url_for(USERS_INDEX_LIST))


@users_bp.route("/users/delete/<int:user_id>", methods=["POST"])
@admin_required
def delete_user(user_id):
    """Temporarily disabled DB logic"""
    if user_id == session.get("user_id"):
        flash("Não pode apagar a sua própria conta (modo simulado).", "warning")
    else:
        flash(f"Utilizador {user_id} apagado (modo simulado).", "success")
    return redirect(url_for(USERS_INDEX_LIST))