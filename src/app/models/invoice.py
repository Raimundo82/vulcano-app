import re

import fitz  # PyMuPDF
import mysql.connector

from app.db import get_connection

from ..config import Config


def process_amount_to_pay(amount_str):
    """Processa o valor de amount_to_pay e converte para float."""
    try:
        amount_str = (
            amount_str.replace("€", "").strip().replace(",", ".").replace(" ", "")
        )
        return float(amount_str)
    except ValueError as e:
        print(f"Erro ao converter amount_to_pay para float: {amount_str} - {e}")
        return None


def extrair_data_emissao(pdf_path):
    """Extrai a data de emissão do PDF."""
    documento = fitz.open(pdf_path)
    for pagina in documento:
        texto_procurado = "Data de emissão:"
        areas_encontradas = pagina.search_for(texto_procurado)
        if areas_encontradas:
            for area in areas_encontradas:
                x0, y0, x1, y1 = area
                area_valor = fitz.Rect(140, y0, 230, y1)
                issue_date = pagina.get_textbox(area_valor)
                return issue_date.strip()
    return None


def extrair_contribuinte(pdf_path):
    """Extrai o número do contribuinte do PDF."""
    documento = fitz.open(pdf_path)
    for pagina in documento:
        texto_procurado = "Nº Contribuinte:"
        areas_encontradas = pagina.search_for(texto_procurado)
        if areas_encontradas:
            for area in areas_encontradas:
                x0, y0, x1, y1 = area
                area_valor = fitz.Rect(140, y0, 230, y1)
                taxpayer_number = pagina.get_textbox(area_valor)
                return taxpayer_number.strip()
    return None


def extrair_valor_total_da_fatura(pdf_path):
    """Extrai o valor total da fatura do PDF e formata para float."""
    documento = fitz.open(pdf_path)
    for pagina in documento:
        texto_procurado = "Valor total da fatura"
        areas_encontradas = pagina.search_for(texto_procurado)
        if areas_encontradas:
            for area in areas_encontradas:
                x0, y0, x1, y1 = area
                area_valor = fitz.Rect(510, y0, 620, y1)
                texto_valor = pagina.get_textbox(area_valor)
                if texto_valor:
                    # Remove símbolos e espaços, substitui vírgulas por pontos
                    valor_limpo = (
                        texto_valor.strip()
                        .replace("€", "")
                        .replace(",", ".")
                        .replace(" ", "")
                    )
                    # Remove pontos extras que são separadores de milhar
                    if valor_limpo.count(".") > 1:
                        partes = valor_limpo.split(".")
                        valor_limpo = (
                            ".".join(partes[:-1]).replace(".", "") + "." + partes[-1]
                        )
                    return valor_limpo
    return None


def extract_client_by_coordinates(pdf_path, coordinates):
    """Extrai o cliente com base nas coordenadas da página."""
    try:
        doc = fitz.open(pdf_path)
        page = doc[0]
        address = page.get_textbox(coordinates)
        address = re.sub(r'[\\/:"*?<>|]+', "_", str(address))
        return address.strip() if address else None
    except Exception as e:
        print(f"Erro ao extrair cliente por coordenadas: {e}")
        return None


def extract_address_by_coordinates(pdf_path, coordinates):
    """Extrai o endereço com base nas coordenadas da página."""
    try:
        doc = fitz.open(pdf_path)
        page = doc[0]
        address = page.get_textbox(coordinates)
        return address.strip() if address else None
    except Exception as e:
        print(f"Erro ao extrair endereço por coordenadas: {e}")
        return None


def extract_account(text):
    return re.search(r"Nº Conta:\s*(\d+)", text)


def extract_invoice_data(pdf_path):
    """Extrai todos os dados da fatura do PDF."""
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text("text") for page in doc])

        conta_inf = verificar_conta(pdf_path, Config.BLM_CONTRACT_NUMBERS)
        if conta_inf[0]:
            invoice_type = "BLM"
        else:
            conta_inf = verificar_conta(pdf_path, Config.VOZ_CONTRACT_NUMBERS)
            if conta_inf[0]:
                invoice_type = "VOZ"
            else:
                invoice_type = "None"

        invoice_number = re.search(r"FT MV/(\d+)", text)
        reference_number = re.search(r"Nº de Referência :\s*(\d+)", text)
        issue_date = extrair_data_emissao(pdf_path)
        taxpayer_number = extrair_contribuinte(pdf_path)
        account_number = extract_account(text)
        client = extract_client_by_coordinates(pdf_path, fitz.Rect(310, 160, 550, 165))
        address = extract_address_by_coordinates(
            pdf_path, fitz.Rect(310, 170, 550, 230)
        )
        cvp = re.search(r"CVP:\s*(\d{12})", text)
        invoice_period = re.search(
            r"Fatura de:\s*([a-zç]+ \d{4})|Fatura de:\s*\n\s*([a-zç]+ \d{4})",
            text,
            re.IGNORECASE,
        )
        amount_to_pay_rec = extract_address_by_coordinates(
            pdf_path, fitz.Rect(510, 255, 580, 265)
        )
        total_amount = extrair_valor_total_da_fatura(pdf_path)

        amount_to_pay = (
            process_amount_to_pay(amount_to_pay_rec) if amount_to_pay_rec else None
        )

        return {
            "invoice_type": invoice_type,
            "invoice_number": invoice_number.group(1) if invoice_number else None,
            "reference_number": reference_number.group(1) if reference_number else None,
            "issue_date": issue_date,
            "taxpayer_number": taxpayer_number,
            "account_number": account_number.group(1) if account_number else None,
            "client": client.replace("\n", "<br>") if client else None,
            "address": address.replace("\n", "<br>") if address else None,
            "cvp": cvp.group(1) if cvp else None,
            "invoice_period_month": (
                invoice_period.group(1).split()[0]
                if invoice_period and invoice_period.group(1)
                else None
            ),
            "invoice_period_year": (
                invoice_period.group(1).split()[1]
                if invoice_period and invoice_period.group(1)
                else None
            ),
            "amount_to_pay": amount_to_pay,
            "total_amount": total_amount,  # Já está formatado corretamente
            "sent_validar": False,
            "quitar": False,
        }
    except Exception as e:
        print(f"Erro ao processar {pdf_path}: {e}")
        return None


def verificar_tarifario(pdf_path, tarifario=Config.TARIFARIO):
    """Verifica se o tarifário especificado está presente no PDF."""
    try:
        documento = fitz.open(pdf_path)
        for pagina in documento:
            texto = pagina.get_text("text")
            if tarifario in texto:
                return True
        return False
    except Exception as e:
        print(f"Erro ao verificar tarifário no arquivo {pdf_path}: {e}")
        return False


def verificar_conta(
    pdf_path, contas=Config.BLM_CONTRACT_NUMBERS + Config.VOZ_CONTRACT_NUMBERS
):
    """Verifica se a conta especificada está presente no PDF."""
    try:
        documento = fitz.open(pdf_path)
        for pagina in documento:
            texto = pagina.get_text("text")

            conta_extr = extract_account(texto)
            for conta in contas:  # percorre a lista de contas
                if conta in texto:
                    return True, conta
        return False, conta_extr

    except Exception as e:
        print(f"Erro ao verificar conta no arquivo {pdf_path}: {e}")
        return False


def save_to_database(data):
    """Salva os dados extraídos no banco de dados."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        check_query = """
        SELECT id FROM invoices
        WHERE invoice_number = %s
        """
        cursor.execute(check_query, (data["invoice_number"],))
        existing_invoice = cursor.fetchone()

        if existing_invoice:
            update_query = """
            UPDATE invoices
            SET invoice_type = %s,issue_date = %s, taxpayer_number = %s, account_number = %s, client = %s, address = %s, cvp = %s,
                invoice_period_month = %s, invoice_period_year = %s, total_amount = %s, amount_to_pay = %s,
                sent_validar = %s, quitar = %s, pdffile = %s
            WHERE invoice_number = %s
            """
            cursor.execute(
                update_query,
                (
                    data["invoice_type"],
                    data["issue_date"],
                    data["taxpayer_number"],
                    data["account_number"],
                    data["client"],
                    data["address"],
                    data["cvp"],
                    data["invoice_period_month"],
                    data["invoice_period_year"],
                    data["total_amount"],
                    data["amount_to_pay"],
                    data.get("sent_validar", False),
                    data.get("quitar", False),
                    data.get("pdffile"),
                    data["invoice_number"],
                ),
            )
        else:
            insert_query = """
            INSERT INTO invoices (invoice_type, invoice_number, issue_date, taxpayer_number, account_number, client, address, cvp, invoice_period_month, invoice_period_year, total_amount, amount_to_pay, sent_validar, quitar, pdffile)
            VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                insert_query,
                (
                    data["invoice_type"],
                    data["invoice_number"],
                    data["issue_date"],
                    data["taxpayer_number"],
                    data["account_number"],
                    data["client"],
                    data["address"],
                    data["cvp"],
                    data["invoice_period_month"],
                    data["invoice_period_year"],
                    data["total_amount"],
                    data["amount_to_pay"],
                    data.get("sent_validar", False),
                    data.get("quitar", False),
                    data.get("pdffile"),
                ),
            )

        conn.commit()
        cursor.close()
        conn.close()
        print(f"Dados salvos no banco de dados: {data}")
    except mysql.connector.Error as err:
        print(f"Erro ao salvar no banco de dados: {err}")
