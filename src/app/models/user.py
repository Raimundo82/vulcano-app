from datetime import datetime
from app.extensions.db import db


class User(db.Model):
    """User model mapped to 'users' table."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    display_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, default=None)

    def __repr__(self):
        return f"<User {self.username}>"

    # --- Optional helpers for CRUD operations ---

    @classmethod
    def get_all(cls):
        """Return all users."""
        return cls.query.order_by(cls.is_admin.desc(), cls.username.asc()).all()

    @classmethod
    def get_by_id(cls, user_id):
        """Find a user by ID."""
        return cls.query.get(user_id)

    @classmethod
    def get_by_username(cls, username):
        """Find a user by username."""
        return cls.query.filter_by(username=username).first()

    def save(self):
        """Insert or update a user."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete a user."""
        db.session.delete(self)
        db.session.commit()