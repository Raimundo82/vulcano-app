import os
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
)
from flask import current_app


def generate_pdf_with_table(faturas):
    """
    Gera um PDF com uma tabela de faturas.

    Args:
        faturas (list): Lista de dicionários contendo os dados das faturas.

    Returns:
        bytes: Conteúdo do PDF gerado.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=55,
        topMargin=40,
        bottomMargin=30,
    )
    styles = getSampleStyleSheet()
    elements = []

    # Adiciona a imagem "SI_faturas.png" centrada
    img_path = os.path.join(current_app.static_folder, "imgs", "SI_faturas.png")
    img = Image(img_path, width=67, height=70)
    img.hAlign = "CENTER"
    elements.append(img)
    elements.append(Spacer(1, 24))

    # Adiciona o cabeçalho
    elements.append(
        Paragraph("RELATÓRIO RECEPÇÃO DE MATERIAL/SERVIÇO", styles["Title"])
    )
    elements.append(Spacer(1, 12))

    # Adiciona a tabela de informações do processo e fornecedor
    info_data = [
        ["N.º PROCESSO DESPESA:", "FORNECEDOR:"],
        ["3024004501", "252525 - MEO - SERVIÇOS DE COMUNICAÇÕES E MULTIMÉDIA, S.A."],
    ]

    info_table = Table(info_data, colWidths=[150, 350])
    info_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, 1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )

    elements.append(info_table)
    elements.append(Spacer(1, 12))

    # Adiciona o texto introdutório
    elements.append(
        Paragraph(
            "Considera-se o serviço foi realizado de acordo com os termos e condições "
            "contratualizados, tendo sido efetuada uma análise à média dos consumos "
            "por cada conta (UEO), considerando-se que estão em condições para "
            "considerar cumpridos os parâmetros para a receção qualitativa e "
            "quantitativa das seguintes faturas:",
            styles["BodyText"],
        )
    )
    elements.append(Spacer(1, 12))

    # Adiciona a tabela de faturas
    fatura_data = [["Nº Fatura", "Nº Conta", "Mês", "Ano", "Valor a Pagar"]]
    total_amount = 0

    for fatura in faturas:
        amount = float(fatura["total_amount"])
        total_amount += amount
        fatura_data.append(
            [
                fatura["invoice_number"],
                fatura["account_number"],
                fatura["invoice_period_month"],
                fatura["invoice_period_year"],
                f"€ {amount:.2f}",
            ]
        )

    # Adiciona a linha de total
    fatura_data.append(["", "", "", "Total", f"€ {total_amount:.2f}"])

    # Define as larguras das colunas
    col_widths = [120, 120, 70, 70, 120]

    fatura_table = Table(fatura_data, colWidths=col_widths)
    fatura_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -2), colors.beige),
                ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )

    elements.append(fatura_table)
    elements.append(Spacer(1, 24))

    # Adiciona a linha "Superintendência da Informação, [data atual]"
    data_atual = datetime.now().strftime("%d/%m/%Y")
    elements.append(
        Paragraph(f"Superintendência da Informação, {data_atual},", styles["BodyText"])
    )
    elements.append(Spacer(1, 12))

    # Adiciona o rodapé com as assinaturas
    footer_data = [
        ["O Gestor do Contrato", "O Chefe de Divisão"],
        ["Ass: ___________________________", "Ass: ___________________________"],
    ]

    footer_table = Table(footer_data, colWidths=[250, 250])
    footer_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 42),
                ("LEADING", (0, 1), (-1, 1), 75),
                ("GRID", (0, 0), (-1, -1), 0, colors.white),
            ]
        )
    )

    elements.append(footer_table)

    # Constrói o PDF
    doc.build(elements)

    # Retorna o conteúdo do PDF
    buffer.seek(0)
    return buffer.getvalue()