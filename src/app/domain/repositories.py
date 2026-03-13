from datetime import date, datetime, timedelta
from typing import Dict, List, Optional

from sqlalchemy import func, update

from ..db import db
from .models import Invoice, Unit, User


class UserRepository:
    """Data access layer for the User entity."""

    def get_all(self) -> List[User]:
        return db.session.execute(
            db.select(User).order_by(User.is_admin.desc(), User.username.asc())
        ).scalars().all()

    def get_by_username(self, username: str) -> Optional[User]:
        return db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()

    def get_by_id(self, user_id: int) -> Optional[User]:
        return db.session.get(User, user_id)

    def create(
        self,
        username: str,
        display_name: str,
        email: str,
        is_admin: bool = False,
    ) -> User:
        user = User(
            username=username,
            display_name=display_name,
            email=email,
            is_admin=is_admin,
        )
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, user_id: int, **kwargs) -> Optional[User]:
        user = db.session.get(User, user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            db.session.commit()
        return user

    def delete(self, user_id: int) -> bool:
        user = db.session.get(User, user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    def update_last_login(self, username: str) -> None:
        user = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()
        if user:
            user.last_login = datetime.now()
            db.session.commit()


class InvoiceRepository:
    """Data access layer for the Invoice entity."""

    def get_unpaid(self) -> List[Invoice]:
        return db.session.execute(
            db.select(Invoice).filter_by(quitar=False)
        ).scalars().all()

    def get_paid(self) -> List[Invoice]:
        return db.session.execute(
            db.select(Invoice).filter_by(quitar=True)
        ).scalars().all()

    def get_by_number(self, invoice_number: str) -> Optional[Invoice]:
        return db.session.execute(
            db.select(Invoice).filter_by(invoice_number=invoice_number)
        ).scalar_one_or_none()

    def get_by_account(
        self, account_number: str, limit: Optional[int] = None
    ) -> List[Invoice]:
        query = (
            db.select(Invoice)
            .filter_by(account_number=account_number)
            .order_by(Invoice.issue_date.desc())
        )
        if limit:
            query = query.limit(limit)
        return db.session.execute(query).scalars().all()

    def get_latest_by_account(self, account_number: str) -> Optional[Invoice]:
        return db.session.execute(
            db.select(Invoice)
            .filter_by(account_number=account_number)
            .order_by(Invoice.issue_date.desc())
            .limit(1)
        ).scalar_one_or_none()

    def get_12month_average(self, account_number: str) -> float:
        cutoff = date.today() - timedelta(days=365)
        result = db.session.execute(
            db.select(func.avg(Invoice.total_amount)).where(
                Invoice.account_number == account_number,
                Invoice.issue_date >= cutoff,
            )
        ).scalar()
        return float(result) if result else 0.0

    def get_by_numbers(self, invoice_numbers: List[str]) -> List[Invoice]:
        return db.session.execute(
            db.select(Invoice).where(Invoice.invoice_number.in_(invoice_numbers))
        ).scalars().all()

    def save(self, data: Dict) -> Invoice:
        """Insert or update invoice identified by *invoice_number*."""
        if "total_amount" in data and isinstance(data["total_amount"], str):
            try:
                data = {**data, "total_amount": float(data["total_amount"])}
            except (ValueError, TypeError):
                data = {**data, "total_amount": None}

        invoice = db.session.execute(
            db.select(Invoice).filter_by(invoice_number=data["invoice_number"])
        ).scalar_one_or_none()

        if invoice:
            for key, value in data.items():
                if hasattr(Invoice, key):
                    setattr(invoice, key, value)
        else:
            invoice = Invoice(**{k: v for k, v in data.items() if hasattr(Invoice, k)})
            db.session.add(invoice)

        db.session.commit()
        return invoice

    def set_paid_status(self, invoice_number: str, quitar: bool) -> Optional[Invoice]:
        """Set the paid status of an invoice, recording quita_date when marking as paid."""
        invoice = db.session.execute(
            db.select(Invoice).filter_by(invoice_number=invoice_number)
        ).scalar_one_or_none()
        if invoice:
            invoice.quitar = quitar
            invoice.quita_date = datetime.now() if quitar else invoice.quita_date
            db.session.commit()
        return invoice

    def mark_paid(self, invoice_number: str) -> Optional[Invoice]:
        invoice = db.session.execute(
            db.select(Invoice).filter_by(invoice_number=invoice_number)
        ).scalar_one_or_none()
        if invoice:
            invoice.quitar = True
            invoice.quita_date = datetime.now()
            db.session.commit()
        return invoice

    def mark_paid_multiple(self, invoice_numbers: List[str]) -> int:
        quita_date = datetime.now()
        result = db.session.execute(
            update(Invoice)
            .where(Invoice.invoice_number.in_(invoice_numbers))
            .values(quitar=True, quita_date=quita_date)
        )
        db.session.commit()
        return result.rowcount

    def delete_by_number(self, invoice_number: str) -> Optional[str]:
        invoice = db.session.execute(
            db.select(Invoice).filter_by(invoice_number=invoice_number)
        ).scalar_one_or_none()
        if invoice:
            pdffile = invoice.pdffile
            db.session.delete(invoice)
            db.session.commit()
            return pdffile
        return None


class UnitRepository:
    """Data access layer for the Unit entity."""

    def get_all(self) -> List[Unit]:
        return db.session.execute(
            db.select(Unit).order_by(Unit.num_cliente.asc(), Unit.unidade.asc())
        ).scalars().all()

    def get_by_id(self, unit_id: int) -> Optional[Unit]:
        return db.session.get(Unit, unit_id)

    def create(
        self, num_cliente: str, unidade: str, poc: str, email_poc: str
    ) -> Unit:
        unit = Unit(
            num_cliente=num_cliente, unidade=unidade, poc=poc, email_poc=email_poc
        )
        db.session.add(unit)
        db.session.commit()
        return unit

    def update(self, unit_id: int, **kwargs) -> Optional[Unit]:
        unit = db.session.get(Unit, unit_id)
        if unit:
            for key, value in kwargs.items():
                setattr(unit, key, value)
            db.session.commit()
        return unit

    def delete(self, unit_id: int) -> bool:
        unit = db.session.get(Unit, unit_id)
        if unit:
            db.session.delete(unit)
            db.session.commit()
            return True
        return False
