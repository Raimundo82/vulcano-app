# src/app/routes/invoices.py
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    flash,
    send_from_directory,
    make_response,
    session,
    current_app,
)
from datetime import datetime
import os
import shutil
import tempfile
# from ..models.invoice import (
#     extract_invoice_data,
#     save_to_database,
#     verificar_tarifario,
#     verificar_conta,
#     extract_account,
# )
from ..utils.pdf_utils import generate_pdf_with_table
from ..config import Config
# from src.app.db_legacy import get_connection  # ❌ Disabled during SQLAlchemy migration
from ..utils.auth_decorators import login_required

invoices_bp = Blueprint("invoices", __name__)

# 🧠 Reminder: All DB logic below will be refactored to ORM later
# For now, we neutralize legacy DB connections so the app can import.


@invoices_bp.route("/")
def index():
    return render_template("index.html")


@invoices_bp.route("/upload", methods=["POST"])
@login_required
def upload_faturas():
    # This function only handles files, safe to keep active.
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
                file_path = os.path.join("pdfs", file.filename)
                shutil.copy(temp_path, file_path)
                uploaded_count += 1
                flash(f"Fatura {file.filename} carregada com sucesso!", "success")
            else:
                flash(
                    f"Fatura {file.filename} não carregada (conta {conta_inf[1]}).",
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
    pdf_folder = "pdfs"
    processed_folder = "processed"
    invoices_data = []

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            data = [] # extract_invoice_data(pdf_path)

            if data:
                year = data.get("invoice_period_year", "unknown")
                month = data.get("invoice_period_month", "unknown")
                destination_folder = os.path.join(processed_folder, year, month)
                os.makedirs(destination_folder, exist_ok=True)

                new_filename = f"{data['invoice_type']}_{data['issue_date']}_FT_{data['invoice_number']}_{data['client']}.pdf"
                destination_path = os.path.join(destination_folder, new_filename)
                data["pdffile"] = new_filename
                if os.path.exists(destination_path):
                    os.remove(destination_path)

                shutil.move(pdf_path, destination_path)
                
                #save_to_database(data)  # still works since it's self-contained
                invoices_data.append(data)

    flash(f"Processamento concluído. {len(invoices_data)} faturas processadas.")
    return render_template("processar.html", invoices=invoices_data)


# ❌ TEMPORARILY DISABLE ALL ROUTES THAT USE get_connection()
# @invoices_bp.route("/api/faturas", methods=["GET"])
# @login_required
# def get_faturas():
#     return jsonify([])

# @invoices_bp.route("/api/faturas/<invoice_number>/quitar", methods=["PUT"])
# @login_required
# def update_quitar(invoice_number):
#     return jsonify({"success": True})

# @invoices_bp.route("/api/faturas/eliminar", methods=["POST"])
# @login_required
# def eliminar_faturas():
#     return jsonify({"success": True})

# @invoices_bp.route("/api/quitadas", methods=["GET"])
# @login_required
# def get_quitadas():
#     return jsonify([])

# @invoices_bp.route("/api/faturas/quitar-marcadas", methods=["POST"])
# @login_required
# def quitar_faturas_marcadas():
#     return jsonify({"success": True})

# @invoices_bp.route("/account/<account_number>")
# @login_required
# def account_details(account_number):
#     return render_template("account_details.html")

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