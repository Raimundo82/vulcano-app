# src/app/routes/units.py
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

units_bp = Blueprint("units", __name__)

UNITS_INDEX_LIST = "units.list_units"

# 🧩 Note:
# All DB logic temporarily disabled to allow Alembic to import models.
# After migration succeeds, we’ll replace with SQLAlchemy ORM calls.


@units_bp.route("/units")
@login_required
def list_units():
    # Placeholder version for migration
    dummy_units = [
        {"id": 1, "num_cliente": "123", "unidade": "Base Naval", "poc": "João", "email_poc": "joao@example.com"},
        {"id": 2, "num_cliente": "456", "unidade": "Centro Técnico", "poc": "Maria", "email_poc": "maria@example.com"},
    ]

    return render_template(
        "units.html",
        units=dummy_units,
        username=session.get("username"),
        display_name=session.get("display_name"),
        is_admin=session.get("is_admin", False),
    )


@units_bp.route("/units/add", methods=["POST"])
@admin_required
def add_unit():
    """Temporarily disabled DB logic (migration phase)"""
    flash("Unidade adicionada (modo simulado).", "success")
    return redirect(url_for(UNITS_INDEX_LIST))


@units_bp.route("/units/edit/<int:unit_id>", methods=["POST"])
@admin_required
def edit_unit(unit_id):
    """Temporarily disabled DB logic (migration phase)"""
    flash(f"Unidade {unit_id} atualizada (modo simulado).", "success")
    return redirect(url_for(UNITS_INDEX_LIST))


@units_bp.route("/units/delete/<int:unit_id>", methods=["POST"])
@admin_required
def delete_unit(unit_id):
    """Temporarily disabled DB logic (migration phase)"""
    flash(f"Unidade {unit_id} apagada (modo simulado).", "success")
    return redirect(url_for(UNITS_INDEX_LIST))