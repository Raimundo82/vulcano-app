import os
import shutil
import tempfile
from datetime import datetime

from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from sqlalchemy.exc import SQLAlchemyError

from ..config import Config
from ..domain.repositories import InvoiceRepository
from ..models.invoice import extract_invoice_data, save_to_database, verificar_conta
from ..utils.auth_decorators import login_required
from ..utils.pdf_utils import generate_pdf_with_table

invoices_bp = Blueprint("invoices", __name__)

_invoice_repo = InvoiceRepository()


@invoices_bp.route("/")
def index():
    return render_template("index.html")


@invoices_bp.route("/upload", methods=["POST"])
@login_required
def upload_faturas():
    if "faturas" not in request.files:
        flash("Nenhum arquivo selecionado", "error")
        return redirect(url_for("invoices.index"))

    files = request.files.getlist("faturas")
    uploaded_count = 0

    for file in files:
        if file.filename.endswith(".pdf"):
            temp_path = os.path.join(tempfile.gettempdir(), file.filename)
            file.save(temp_path)
            conta_inf = verificar_conta(temp_path)
            if conta_inf[0]:
                file_path = os.path.join(Config.PDFS_DIR, file.filename)
                shutil.copy(temp_path, file_path)
                uploaded_count += 1
                flash(f"Fatura {file.filename} carregada com sucesso!", "success")
            else:
                flash(
                    f"Fatura {file.filename} não carregada numero de conta {conta_inf[1]}.",
                    "warning",
                )
                os.remove(temp_path)
        else:
            flash(f"Arquivo {file.filename} não é um PDF válido.", "error")

    if uploaded_count > 0:
        flash(f"{uploaded_count} faturas carregadas com sucesso!", "success")

    return redirect(url_for("invoices.index", uploaded=uploaded_count))


@invoices_bp.route("/process", methods=["GET"])
@login_required
def process_invoices():
    pdf_folder = Config.PDFS_DIR
    processed_folder = Config.PROCESSED_DIR
    invoices_data = []

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            data = extract_invoice_data(pdf_path)

            if data:
                if data["total_amount"]:
                    total_amount = float(data["total_amount"])
                else:
                    total_amount = 0.0

                data["sent_validar"] = data.get("sent_validar", False)
                data["quitar"] = data.get("quitar", False)

                year = (
                    data["invoice_period_year"]
                    if data["invoice_period_year"]
                    else "unknown"
                )
                month = (
                    data["invoice_period_month"]
                    if data["invoice_period_month"]
                    else "unknown"
                )
                destination_folder = os.path.join(processed_folder, year, month)
                os.makedirs(destination_folder, exist_ok=True)

                new_filename = f"{data["invoice_type"]}_{str(data["issue_date"])}_FT_{str(data["invoice_number"])}_{data["client"]}.pdf"
                destination_path = os.path.join(destination_folder, new_filename)
                data["pdffile"] = new_filename
                if os.path.exists(destination_path):
                    os.remove(destination_path)

                shutil.move(pdf_path, destination_path)
                save_to_database(data)
                invoices_data.append(data)

    flash(f"Processamento concluído. {len(invoices_data)} faturas processadas.")
    return render_template("processar.html", invoices=invoices_data)


@invoices_bp.route("/api/faturas", methods=["GET"])
@login_required
def get_faturas():
    try:
        faturas = []
        for invoice in _invoice_repo.get_unpaid():
            fatura = invoice.to_dict()
            fatura["media"] = _invoice_repo.get_12month_average(invoice.account_number)
            faturas.append(fatura)
        return jsonify(faturas)
    except SQLAlchemyError as err:
        return jsonify({"error": str(err)}), 500


@invoices_bp.route("/api/faturas/<invoice_number>/quitar", methods=["PUT"])
@login_required
def update_quitar(invoice_number):
    try:
        data = request.get_json()
        quitar = data.get("quitar", False)
        _invoice_repo.set_paid_status(invoice_number, quitar)
        return jsonify({"success": True})
    except SQLAlchemyError as err:
        return jsonify({"error": str(err)}), 500


@invoices_bp.route("/api/faturas/eliminar", methods=["POST"])
@login_required
def eliminar_faturas():
    try:
        if not session.get("is_admin"):
            return (
                jsonify(
                    {
                        "error": "Acesso negado. Apenas administradores podem eliminar faturas."
                    }
                ),
                403,
            )

        data = request.get_json()
        invoices_to_delete = data.get("invoices", [])

        for invoice in invoices_to_delete:
            _invoice_repo.delete_by_number(invoice["invoiceNumber"])

            pdf_path = os.path.join(
                Config.PROCESSED_DIR,
                str(invoice["invoiceYear"]),
                str(invoice["invoiceMonth"]),
                invoice["pdfFile"],
            )
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

        return jsonify({"success": True, "message": "Faturas eliminadas com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@invoices_bp.route("/api/quitadas", methods=["GET"])
@login_required
def get_quitadas():
    try:
        faturas = []
        for invoice in _invoice_repo.get_paid():
            fatura = invoice.to_dict()
            fatura["media"] = _invoice_repo.get_12month_average(invoice.account_number)
            faturas.append(fatura)
        return jsonify(faturas)
    except SQLAlchemyError as err:
        return jsonify({"error": str(err)}), 500


@invoices_bp.route("/processed/<path:filename>")
@login_required
def processed_files(filename):
    return send_from_directory(Config.PROCESSED_DIR, filename)


@invoices_bp.route("/quitar-faturas", methods=["GET", "POST"])
@login_required
def quitar_faturas():
    if request.method == "POST":
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Dados inválidos"}), 400

            faturas_marcadas = data.get("faturas", [])
            if not faturas_marcadas:
                return jsonify({"error": "Nenhuma fatura marcada."}), 400

            invoices = _invoice_repo.get_by_numbers(faturas_marcadas)
            faturas = [inv.to_dict() for inv in invoices]

            if not faturas:
                return jsonify({"error": "Nenhuma fatura encontrada"}), 404

            pdf_content = generate_pdf_with_table(faturas)
            response = make_response(pdf_content)
            response.headers["Content-Type"] = "application/pdf"
            response.headers["Content-Disposition"] = (
                "inline; filename=quitacao_faturas.pdf"
            )
            return response

        except Exception as err:
            current_app.logger.error(f"Error in quitar_faturas: {str(err)}")
            return jsonify({"error": "Erro interno no servidor"}), 500

    return redirect(url_for("invoices.index"))


@invoices_bp.route("/api/faturas/quitar-marcadas", methods=["POST"])
@login_required
def quitar_faturas_marcadas():
    try:
        data = request.get_json()
        faturas_marcadas = data.get("faturas", [])

        if not faturas_marcadas:
            return jsonify({"error": "Nenhuma fatura marcada."}), 400

        count = _invoice_repo.mark_paid_multiple(faturas_marcadas)
        return jsonify(
            {
                "success": True,
                "message": f"{count} faturas quitadas com sucesso.",
            }
        )
    except SQLAlchemyError as err:
        return jsonify({"error": str(err)}), 500


@invoices_bp.route("/account/<account_number>")
@login_required
def account_details(account_number):
    try:
        latest = _invoice_repo.get_latest_by_account(account_number)
        client_name = latest.client if latest else "Cliente não encontrado"

        invoices = _invoice_repo.get_by_account(account_number, limit=12)
        average_value = _invoice_repo.get_12month_average(account_number)

        invoices_list = [inv.to_dict() for inv in invoices]
        invoices_list.reverse()

        labels = [
            inv["issue_date"].strftime("%Y-%m")
            for inv in invoices_list
            if inv["issue_date"]
        ]
        amounts = [
            float(inv["total_amount"])
            for inv in invoices_list
            if inv["total_amount"] is not None
        ]

        return render_template(
            "account_details.html",
            account_number=account_number,
            client=client_name,
            labels=labels,
            amounts=amounts,
            average_value=round(average_value, 2),
        )

    except Exception as err:
        current_app.logger.error(f"Account details error: {str(err)}")
        return jsonify({"error": "Erro ao carregar detalhes da conta"}), 500


@invoices_bp.route("/faturas")
@login_required
def faturas():
    return render_template("faturas.html", contas_blm=Config.BLM_CONTRACT_NUMBERS)


@invoices_bp.route("/quitadas")
@login_required
def quitadas():
    try:
        is_admin = session.get("is_admin", 0)
        return render_template(
            "quitadas.html", is_admin=is_admin, contas_blm=Config.BLM_CONTRACT_NUMBERS
        )
    except Exception as e:
        flash(f"Error accessing page: {str(e)}", "error")
        return redirect(url_for("invoices.index"))
