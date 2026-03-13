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

from ..domain.repositories import UnitRepository
from ..utils.auth_decorators import admin_required, login_required

units_bp = Blueprint("units", __name__)

_unit_repo = UnitRepository()


@units_bp.route("/units")
@login_required
def list_units():
    try:
        units = [u.to_dict() for u in _unit_repo.get_all()]
        return render_template(
            "units.html",
            units=units,
            username=session.get("username"),
            display_name=session.get("display_name"),
            is_admin=session.get("is_admin", False),
        )
    except Exception as e:
        current_app.logger.error(f"Units list error: {str(e)}")
        flash("Erro ao carregar lista de unidades", "danger")
        return redirect(url_for("invoices.index"))


@units_bp.route("/units/add", methods=["POST"])
@admin_required
def add_unit():
    """Add new unit (admin only)"""
    try:
        num_cliente = request.form.get("num_cliente", "").strip()
        unidade = request.form.get("unidade", "").strip()
        poc = request.form.get("poc", "").strip()
        email_poc = request.form.get("email_poc", "").strip().lower()

        if not all([num_cliente, unidade]):
            flash("Número de cliente e unidade são obrigatórios", "warning")
            return redirect(url_for("units.list_units"))

        _unit_repo.create(num_cliente, unidade, poc, email_poc)
        flash("Unidade adicionada com sucesso!", "success")
        return redirect(url_for("units.list_units"))

    except IntegrityError:
        flash("Unidade já existe para este cliente", "danger")
    except SQLAlchemyError as err:
        current_app.logger.error(f"Database error in add_unit: {err}")
        flash("Erro ao adicionar unidade", "danger")

    return redirect(url_for("units.list_units"))


@units_bp.route("/units/edit/<int:unit_id>", methods=["POST"])
@admin_required
def edit_unit(unit_id):
    """Edit existing unit (admin only)"""
    try:
        num_cliente = request.form.get("num_cliente", "").strip()
        unidade = request.form.get("unidade", "").strip()
        poc = request.form.get("poc", "").strip()
        email_poc = request.form.get("email_poc", "").strip().lower()

        if not all([num_cliente, unidade]):
            flash("Número de cliente e unidade são obrigatórios", "warning")
            return redirect(url_for("units.list_units"))

        _unit_repo.update(
            unit_id,
            num_cliente=num_cliente,
            unidade=unidade,
            poc=poc,
            email_poc=email_poc,
        )
        flash("Unidade atualizada com sucesso!", "success")
        return redirect(url_for("units.list_units"))

    except IntegrityError:
        flash("Unidade já existe para este cliente", "danger")
    except SQLAlchemyError as err:
        current_app.logger.error(f"Database error in edit_unit: {err}")
        flash("Erro ao atualizar unidade", "danger")

    return redirect(url_for("units.list_units"))


@units_bp.route("/units/delete/<int:unit_id>", methods=["POST"])
@admin_required
def delete_unit(unit_id):
    """Delete unit (admin only)"""
    try:
        _unit_repo.delete(unit_id)
        flash("Unidade apagada com sucesso!", "success")
    except SQLAlchemyError as err:
        current_app.logger.error(f"Database error in delete_unit: {err}")
        flash("Erro ao apagar unidade", "danger")

    return redirect(url_for("units.list_units"))
