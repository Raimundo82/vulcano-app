import os
import shutil
import tempfile
import zipfile
from datetime import datetime
from io import BytesIO

import mysql.connector
from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    send_from_directory,
    session,
    url_for,
)

from app.db import get_connection

from ..config import Config
from ..models.invoice import extract_invoice_data, save_to_database, verificar_conta
from ..utils.auth_decorators import login_required
from ..utils.pdf_utils import generate_pdf_with_table
from ..utils.word_utils import generate_word_with_table

invoices_bp = Blueprint("invoices", __name__)


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

                # data["sent_validar"] = data.get("sent_validar", False)
                # data["quitar"] = data.get("quitar", False)

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
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                invoice_type,
                invoice_number,
                issue_date,
                taxpayer_number,
                account_number,
                client,
                invoice_period_year,
                invoice_period_month,
                amount_to_pay,
                total_amount,
                balance,
                irregular,
                quitar,
                meo_estado,
                obs,
                pdffile
            FROM invoices
            WHERE quitar = 0
        """
        )
        faturas = cursor.fetchall()

        for fatura in faturas:
            account_number = fatura["account_number"]
            cursor.execute(
                """
                SELECT AVG(total_amount) AS media
                FROM invoices
                WHERE account_number = %s
                AND issue_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
            """,
                (account_number,),
            )
            resultado = cursor.fetchone()
            fatura["media"] = resultado["media"] if resultado["media"] else 0.0

        cursor.close()
        conn.close()
        return jsonify(faturas)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@invoices_bp.route("/api/faturas/<invoice_number>/quitar", methods=["PUT"])
@login_required
def update_quitar(invoice_number):
    if not session.get("is_admin"):
        return (
            jsonify(
                {
                    "error": "Acesso negado — apenas administradores podem quitar facturas."
                }
            ),
            403,
        )
    try:
        data = request.get_json()
        quitar = data.get("quitar", False)
        quita_date = datetime.now()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE invoices
            SET quitar = %s, quita_date = %s
            WHERE invoice_number = %s
        """,
            (quitar, quita_date, invoice_number),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@invoices_bp.route("/api/faturas/<invoice_number>/irregular", methods=["PUT"])
@login_required
def update_irregular(invoice_number):
    if not session.get("is_admin"):
        return (
            jsonify(
                {
                    "error": "Acesso negado — apenas administradores podem marcar facturas como irregulares."
                }
            ),
            403,
        )
    try:
        data = request.get_json()
        irregular = data.get("irregular", False)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE invoices
            SET irregular = %s
            WHERE invoice_number = %s
        """,
            (irregular, invoice_number),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True})
    except mysql.connector.Error as err:
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

        conn = get_connection()
        cursor = conn.cursor()

        for invoice in invoices_to_delete:
            cursor.execute(
                "DELETE FROM invoices WHERE invoice_number = %s",
                (invoice["invoiceNumber"],),
            )
            conn.commit()

            pdf_path = os.path.join(
                Config.PROCESSED_DIR,
                str(invoice["invoiceYear"]),
                str(invoice["invoiceMonth"]),
                invoice["pdfFile"],
            )
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

        cursor.close()
        conn.close()
        return jsonify({"success": True, "message": "Faturas eliminadas com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@invoices_bp.route("/api/quitadas/<invoice_number>/obs", methods=["PUT"])
@login_required
def update_obs_quitadas(invoice_number):
    if not session.get("is_admin"):
        return (
            jsonify(
                {"error": "Acesso negado — apenas administradores podem editar OBS."}
            ),
            403,
        )

    try:
        # Lê o JSON enviado pelo frontend
        data = request.get_json()
        new_obs = data.get("obs", "")

        updated_invoice = update_invoice_obs(invoice_number, new_obs)

        return jsonify(
            {
                "status": "ok",
                "message": "OBS atualizada com sucesso.",
                "invoice": updated_invoice,
            }
        )

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@invoices_bp.route("/api/quitadas/<invoice_number>/meo_estado", methods=["PUT"])
@login_required
def update_meo_estado_quitadas(invoice_number):
    if not session.get("is_admin"):
        return (
            jsonify(
                {
                    "error": "Acesso negado — apenas administradores podem editar MEO estado."
                }
            ),
            403,
        )

    try:
        # Lê o JSON enviado pelo frontend
        data = request.get_json()
        new_obs = data.get("meo_estado", "")
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            UPDATE invoices
            SET meo_estado = %s
            WHERE invoice_number = %s
            """,
            (new_obs, invoice_number),
        )
        conn.commit()

        # Buscar o registro atualizado
        cursor.execute(
            "SELECT * FROM invoices WHERE invoice_number = %s", (invoice_number,)
        )
        updated_invoice = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify(
            {
                "status": "ok",
                "message": "Meo_estado atualizada com sucesso.",
                "invoice": updated_invoice,
            }
        )

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@invoices_bp.route("/api/faturas/<invoice_number>/meo_estado", methods=["PUT"])
@login_required
def update_meo_estado_faturas(invoice_number):
    if not session.get("is_admin"):
        return (
            jsonify(
                {
                    "error": "Acesso negado — apenas administradores podem editar MEO estado."
                }
            ),
            403,
        )

    try:
        # Lê o JSON enviado pelo frontend
        data = request.get_json()
        new_obs = data.get("meo_estado", "")
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            UPDATE invoices
            SET meo_estado = %s
            WHERE invoice_number = %s
            """,
            (new_obs, invoice_number),
        )
        conn.commit()

        # Buscar o registro atualizado
        cursor.execute(
            "SELECT * FROM invoices WHERE invoice_number = %s", (invoice_number,)
        )
        updated_invoice = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify(
            {
                "status": "ok",
                "message": "Meo_estado atualizada com sucesso.",
                "invoice": updated_invoice,
            }
        )

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@invoices_bp.route("/api/quitadas/<invoice_number>/pap", methods=["PUT"])
@login_required
def update_pap_quitadas(invoice_number):
    if not session.get("is_admin"):
        return (
            jsonify(
                {
                    "error": "Acesso negado — apenas administradores podem editar MEO estado."
                }
            ),
            403,
        )

    try:
        # Lê o JSON enviado pelo frontend
        data = request.get_json()
        new_pap = data.get("pap", "")
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            UPDATE invoices
            SET pap = %s
            WHERE invoice_number = %s
            """,
            (new_pap, invoice_number),
        )
        conn.commit()

        # Buscar o registro atualizado
        cursor.execute(
            "SELECT * FROM invoices WHERE invoice_number = %s", (invoice_number,)
        )
        updated_invoice = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify(
            {
                "status": "ok",
                "message": "PAP atualizada com sucesso.",
                "invoice": updated_invoice,
            }
        )

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@invoices_bp.route("/api/<invoice_number>/balance", methods=["PUT"])
@login_required
def update_balance(invoice_number):
    if not session.get("is_admin"):
        return (
            jsonify(
                {
                    "error": "Acesso negado — apenas administradores podem editar MEO estado."
                }
            ),
            403,
        )
    print(invoice_number)
    try:
        # Lê o JSON enviado pelo frontend
        data = request.get_json()
        new_balance = data.get("balance", "")
        print(new_balance)
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            UPDATE invoices
            SET balance = %s
            WHERE invoice_number = %s
            """,
            (new_balance, invoice_number),
        )
        conn.commit()

        # Buscar o registro atualizado
        cursor.execute(
            "SELECT * FROM invoices WHERE invoice_number = %s", (invoice_number,)
        )
        updated_invoice = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify(
            {
                "status": "ok",
                "message": "balance atualizada com sucesso.",
                "invoice": updated_invoice,
            }
        )

    except mysql.connector.Error as err:
        print("ERRO MYSQL:", err)
        return jsonify({"error": str(err)}), 500


@invoices_bp.route("/api/quitadas/<invoice_number>/invoiced", methods=["PUT"])
@login_required
def update_invoiced_quitadas(invoice_number):
    if not session.get("is_admin"):
        return (
            jsonify(
                {
                    "error": "Acesso negado — apenas administradores podem editar MEO estado."
                }
            ),
            403,
        )
    print(invoice_number)
    try:
        # Lê o JSON enviado pelo frontend
        data = request.get_json()
        new_invoiced = data.get("invoiced", "")
        print(new_invoiced)
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            UPDATE invoices
            SET invoiced = %s
            WHERE invoice_number = %s
            """,
            (new_invoiced, invoice_number),
        )
        conn.commit()

        # Buscar o registro atualizado
        cursor.execute(
            "SELECT * FROM invoices WHERE invoice_number = %s", (invoice_number,)
        )
        updated_invoice = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify(
            {
                "status": "ok",
                "message": "invoiced atualizada com sucesso.",
                "invoice": updated_invoice,
            }
        )

    except mysql.connector.Error as err:
        print("ERRO MYSQL:", err)
        return jsonify({"error": str(err)}), 500


@invoices_bp.route("/api/faturas/<invoice_number>/obs", methods=["PUT"])
@login_required
def update_obs_(invoice_number):
    if not session.get("is_admin"):
        return (
            jsonify(
                {"error": "Acesso negado — apenas administradores podem editar OBS."}
            ),
            403,
        )

    try:
        # Lê o JSON enviado pelo frontend
        data = request.get_json()
        new_obs = data.get("obs", "")

        updated_invoice = update_invoice_obs(invoice_number, new_obs)

        return jsonify(
            {
                "status": "ok",
                "message": "OBS atualizada com sucesso.",
                "invoice": updated_invoice,
            }
        )

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@invoices_bp.route("/api/quitadas", methods=["GET"])
@login_required
def get_quitadas():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                invoice_type,
                invoice_number,
                issue_date,
                taxpayer_number,
                account_number,
                client,
                invoice_period_year,
                invoice_period_month,
                amount_to_pay,
                total_amount,
                balance,
                quitar,
                quita_date,
                pap,
                invoiced,
                meo_estado,
                obs,
                pdffile
            FROM invoices
            WHERE quitar = 1
        """
        )
        faturas = cursor.fetchall()

        for fatura in faturas:
            account_number = fatura["account_number"]
            cursor.execute(
                """
                SELECT AVG(total_amount) AS media
                FROM invoices
                WHERE account_number = %s
                AND issue_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
            """,
                (account_number,),
            )
            resultado = cursor.fetchone()
            fatura["media"] = resultado["media"] if resultado["media"] else 0.0

        cursor.close()
        conn.close()
        return jsonify(faturas)
    except mysql.connector.Error as err:
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

            # Use context manager for database connection
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    placeholders = ",".join(["%s"] * len(faturas_marcadas))
                    query = f"""
                        SELECT account_number, invoice_number,
                            invoice_period_month, invoice_period_year,
                            total_amount, amount_to_pay
                        FROM invoices
                        WHERE invoice_number IN ({placeholders})
                    """
                    cursor.execute(query, faturas_marcadas)
                    faturas = cursor.fetchall()

            # Generate documents only if we got results
            if not faturas:
                return jsonify({"error": "Nenhuma fatura encontrada"}), 404

            pdf_content = generate_pdf_with_table(faturas)
            word_content = generate_word_with_table(faturas)

            # Criar ZIP em memória
            zip_buffer = BytesIO()

            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr(
                    "aammdd_Centralizacao_SMT_OCC_126_2024_TTT_Quitacao_mes.pdf",
                    pdf_content,
                )
                zip_file.writestr(
                    "aammdd_Centralizacao_SMT_OCC_126_2024_TTT_Quitacao_mes.docx",
                    word_content,
                )

            zip_buffer.seek(0)

            return send_file(
                zip_buffer,
                as_attachment=True,
                download_name="quitacao_faturas.zip",
                mimetype="application/zip",
            )

        except Exception as err:  # Catch all exceptions
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

        conn = get_connection()
        cursor = conn.cursor()
        quita_date = datetime.now()

        for invoice_number in faturas_marcadas:
            cursor.execute(
                """
                UPDATE invoices
                SET quitar = 1, quita_date = %s
                WHERE invoice_number = %s
            """,
                (quita_date, invoice_number),
            )

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(
            {
                "success": True,
                "message": f"{len(faturas_marcadas)} faturas quitadas com sucesso.",
            }
        )
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@invoices_bp.route("/account/<account_number>")
@login_required  # Uncomment when authentication is ready
def account_details(account_number):
    try:
        # Use your existing get_connection() function or direct mysql.connection
        conn = get_connection()  # Or: conn = mysql.connection
        cursor = conn.cursor(dictionary=True)

        # Get client name and most recent invoice
        cursor.execute(
            """
            SELECT invoice_number, issue_date, total_amount, client
            FROM invoices
            WHERE account_number = %s
            ORDER BY issue_date DESC
            LIMIT 1
        """,
            (account_number,),
        )

        invoice_data = cursor.fetchone()
        client_name = (
            invoice_data["client"] if invoice_data else "Cliente não encontrado"
        )

        # Get last 24 invoices for the chart
        cursor.execute(
            """
            SELECT invoice_number, issue_date, total_amount, amount_to_pay, meo_estado, pap,balance,irregular,quitar,obs,invoiced
            FROM invoices
            WHERE account_number = %s
            ORDER BY issue_date DESC
            LIMIT 24
        """,
            (account_number,),
        )

        invoices = cursor.fetchall()

        # Calculate 24-month average
        cursor.execute(
            """
            SELECT AVG(total_amount) as average_value
            FROM invoices
            WHERE account_number = %s
            AND issue_date >= DATE_SUB(CURDATE(), INTERVAL 24 MONTH)
        """,
            (account_number,),
        )

        average_result = cursor.fetchone()
        average_value = (
            float(average_result["average_value"])
            if average_result["average_value"]
            else 0
        )

        cursor.close()
        conn.close()

        # Prepare chart data (reversed for chronological order)
        invoices.reverse()
        labels = [invoice["issue_date"].strftime("%Y-%m") for invoice in invoices]
        amounts = [float(invoice["total_amount"]) for invoice in invoices]
        amounts_to_pay = [(invoice["amount_to_pay"]) for invoice in invoices]
        meo_estados = [(invoice["meo_estado"]) for invoice in invoices]
        paps = [(invoice["pap"]) for invoice in invoices]
        irregulares = [(invoice["irregular"]) for invoice in invoices]
        balances = [(invoice["balance"]) for invoice in invoices]
        quitadas = [(invoice["quitar"]) for invoice in invoices]
        obse = [(invoice["obs"]) for invoice in invoices]
        invoiceds = [(invoice["invoiced"]) for invoice in invoices]

        return render_template(
            "account_details.html",
            account_number=account_number,
            client=client_name,
            labels=labels,
            amounts=amounts,
            amounts_to_pay=amounts_to_pay,
            average_value=round(average_value, 2),
            meo_estados=meo_estados,
            paps=paps,
            balances=balances,
            irregulares=irregulares,
            quitadas=quitadas,
            obse=obse,
            invoiceds=invoiceds,
        )

    except Exception as err:
        current_app.logger.error(f"Account details error: {str(err)}")
        return jsonify({"error": "Erro ao carregar detalhes da conta"}), 500


@invoices_bp.route("/faturas")
@login_required
def faturas():
    try:
        is_admin = session.get("is_admin", 0)
        return render_template(
            "faturas.html", is_admin=is_admin, contas_blm=Config.BLM_CONTRACT_NUMBERS
        )
    except Exception as e:
        flash(f"Error accessing page: {str(e)}", "error")
        return redirect(url_for("invoices.index"))


@invoices_bp.route("/quitadas")
@login_required
def quitadas():
    try:
        is_admin = session.get("is_admin", 0)  # Now properly imported
        return render_template(
            "quitadas.html", is_admin=is_admin, contas_blm=Config.BLM_CONTRACT_NUMBERS
        )
    except Exception as e:
        flash(f"Error accessing page: {str(e)}", "error")
        return redirect(url_for("invoices.index"))


# funçoes auxiliares


def update_invoice_obs(invoice_number, new_obs):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        UPDATE invoices
        SET obs = %s
        WHERE invoice_number = %s
        """,
        (new_obs, invoice_number),
    )
    conn.commit()

    # Buscar o registro atualizado
    cursor.execute(
        "SELECT * FROM invoices WHERE invoice_number = %s", (invoice_number,)
    )
    updated_invoice = cursor.fetchone()

    cursor.close()
    conn.close()

    return updated_invoice
