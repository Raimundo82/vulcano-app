from datetime import datetime
from app.extensions.db import db
from datetime import datetime
from typing import Dict, Any


class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)
    invoice_type = db.Column(db.String(50))
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    issue_date = db.Column(db.String(50))
    taxpayer_number = db.Column(db.String(50))
    account_number = db.Column(db.String(50))
    client = db.Column(db.Text)
    address = db.Column(db.Text)
    cvp = db.Column(db.String(20))
    invoice_period_month = db.Column(db.String(20))
    invoice_period_year = db.Column(db.String(10))
    total_amount = db.Column(db.Float)
    amount_to_pay = db.Column(db.Float)
    sent_validar = db.Column(db.Boolean, default=False)
    quitar = db.Column(db.Boolean, default=False)
    pdffile = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Invoice {self.invoice_number} - {self.client}>"
    
    @staticmethod
    def get_all_invoices():
        """Retorna todas as faturas."""
        return Invoice.query.all()



def save_to_database(data: Dict[str, Any]) -> None:
    """
    Guarda ou atualiza uma fatura no base de dados usando SQLAlchemy ORM.

    Args:
        data (Dict[str, Any]): Dicionário com os dados da fatura extraída.

    Returns:
        None
    """
    try:
        # Verifica se a fatura já existe
        existing_invoice = Invoice.query.filter_by(
            invoice_number=data["invoice_number"]
        ).first()

        if existing_invoice:
            # Atualiza os campos existentes
            for key, value in data.items():
                if hasattr(existing_invoice, key):
                    setattr(existing_invoice, key, value)
            print(f"📝 Fatura atualizada: {data['invoice_number']}")
        else:
            # Cria uma nova instância de fatura
            new_invoice = Invoice(**data)
            db.session.add(new_invoice)
            print(f"✅ Nova fatura adicionada: {data['invoice_number']}")

        db.session.commit()

    except Exception as err:
        db.session.rollback()
        print(f"⚠️ Erro ao guardar na base de dados: {err}")