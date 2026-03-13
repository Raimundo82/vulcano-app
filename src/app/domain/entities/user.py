from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """Domain entity representing an application user."""

    username: str
    display_name: str
    email: str
    id: Optional[int] = None
    is_admin: bool = field(default=False)
    last_login: Optional[datetime] = None
