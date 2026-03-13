from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """
    Domain entity representing an application user.

    Users are authenticated externally via LDAP.  The ``username`` maps to
    the LDAP ``sAMAccountName``.  The ``is_admin`` flag is stored locally
    and controls access to privileged operations.
    """

    username: str
    display_name: str
    email: str
    id: Optional[int] = None
    is_admin: bool = field(default=False)
    last_login: Optional[datetime] = None

    def can_administrate(self) -> bool:
        """Return True when the user holds the admin role."""
        return self.is_admin
