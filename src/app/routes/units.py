import mysql.connector
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

from ..db import get_connection
from ..utils.auth_decorators import admin_required, login_required

units_bp = Blueprint("units", __name__)


@units_bp.route("/units")
@login_required
def list_units():
    try:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    """
                    SELECT id, num_cliente, unidade, poc, email_poc
                    FROM unidades
                    ORDER BY num_cliente ASC, unidade ASC
                """
                )
                units = cursor.fetchall()

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

        # Basic validation
        if not all([num_cliente, unidade]):
            flash("Número de cliente e unidade são obrigatórios", "warning")
            return redirect(url_for("units.list_units"))

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO unidades (num_cliente, unidade, poc, email_poc)
                    VALUES (%s, %s, %s, %s)
                """,
                    (num_cliente, unidade, poc, email_poc),
                )
                conn.commit()

        flash("Unidade adicionada com sucesso!", "success")
        return redirect(url_for("units.list_units"))

    except mysql.connector.IntegrityError:
        flash("Unidade já existe para este cliente", "danger")
    except mysql.connector.Error as err:
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

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE unidades
                    SET num_cliente = %s, unidade = %s,
                        poc = %s, email_poc = %s
                    WHERE id = %s
                """,
                    (num_cliente, unidade, poc, email_poc, unit_id),
                )
                conn.commit()

        flash("Unidade atualizada com sucesso!", "success")
        return redirect(url_for("units.list_units"))

    except mysql.connector.IntegrityError:
        flash("Unidade já existe para este cliente", "danger")
    except mysql.connector.Error as err:
        current_app.logger.error(f"Database error in edit_unit: {err}")
        flash("Erro ao atualizar unidade", "danger")

    return redirect(url_for("units.list_units"))


@units_bp.route("/units/delete/<int:unit_id>", methods=["POST"])
@admin_required
def delete_unit(unit_id):
    """Delete unit (admin only)"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM unidades WHERE id = %s", (unit_id,))
                conn.commit()

        flash("Unidade apagada com sucesso!", "success")
    except mysql.connector.Error as err:
        current_app.logger.error(f"Database error in delete_unit: {err}")
        flash("Erro ao apagar unidade", "danger")

    return redirect(url_for("units.list_units"))
