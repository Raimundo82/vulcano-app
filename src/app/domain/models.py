from datetime import datetime

from ..db import db


class User(db.Model):
    """ORM entity for the *users* table."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    display_name = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    last_login = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "display_name": self.display_name,
            "email": self.email,
            "is_admin": bool(self.is_admin),
            "last_login": self.last_login,
        }


class Invoice(db.Model):
    """ORM entity for the *invoices* table."""

    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)
    invoice_type = db.Column(db.String(10))
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    issue_date = db.Column(db.Date)
    taxpayer_number = db.Column(db.String(50))
    account_number = db.Column(db.String(50))
    client = db.Column(db.String(500))
    address = db.Column(db.String(1000))
    cvp = db.Column(db.String(50))
    invoice_period_month = db.Column(db.String(20))
    invoice_period_year = db.Column(db.String(4))
    amount_to_pay = db.Column(db.Float)
    total_amount = db.Column(db.Float)
    sent_validar = db.Column(db.Boolean, default=False)
    quitar = db.Column(db.Boolean, default=False)
    quita_date = db.Column(db.DateTime)
    pdffile = db.Column(db.String(500))

    def to_dict(self):
        return {
            "id": self.id,
            "invoice_type": self.invoice_type,
            "invoice_number": self.invoice_number,
            "issue_date": self.issue_date,
            "taxpayer_number": self.taxpayer_number,
            "account_number": self.account_number,
            "client": self.client,
            "address": self.address,
            "cvp": self.cvp,
            "invoice_period_month": self.invoice_period_month,
            "invoice_period_year": self.invoice_period_year,
            "amount_to_pay": self.amount_to_pay,
            "total_amount": self.total_amount,
            "sent_validar": bool(self.sent_validar),
            "quitar": bool(self.quitar),
            "quita_date": self.quita_date,
            "pdffile": self.pdffile,
        }


class Unit(db.Model):
    """ORM entity for the *unidades* table."""

    __tablename__ = "unidades"

    id = db.Column(db.Integer, primary_key=True)
    num_cliente = db.Column(db.String(50), nullable=False)
    unidade = db.Column(db.String(200), nullable=False)
    poc = db.Column(db.String(200))
    email_poc = db.Column(db.String(200))

    def to_dict(self):
        return {
            "id": self.id,
            "num_cliente": self.num_cliente,
            "unidade": self.unidade,
            "poc": self.poc,
            "email_poc": self.email_poc,
        }
