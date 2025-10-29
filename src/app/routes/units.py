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


@units_bp.route("/")
@login_required
def list_units():
    """Lista todas as unidades existentes na base de dados"""

    from app.models.unit import Unit # Evita import circular

    units = Unit.query.order_by(Unit.id.asc()).all()

    return render_template(
        "units.html",
        units=units,
        username=session.get("username"),
        display_name=session.get("display_name"),
        is_admin=session.get("is_admin", False),
    )


@units_bp.route("/add", methods=["POST"])
@admin_required
def add_unit():
    """Temporarily disabled DB logic (migration phase)"""
    flash("Unidade adicionada (modo simulado).", "success")
    return redirect(url_for(UNITS_INDEX_LIST))


@units_bp.route("/edit/<int:unit_id>", methods=["POST"])
@admin_required
def edit_unit(unit_id):
    """Temporarily disabled DB logic (migration phase)"""
    flash(f"Unidade {unit_id} atualizada (modo simulado).", "success")
    return redirect(url_for(UNITS_INDEX_LIST))


@units_bp.route("/delete/<int:unit_id>", methods=["POST"])
@admin_required
def delete_unit(unit_id):
    """Temporarily disabled DB logic (migration phase)"""
    flash(f"Unidade {unit_id} apagada (modo simulado).", "success")
    return redirect(url_for(UNITS_INDEX_LIST))