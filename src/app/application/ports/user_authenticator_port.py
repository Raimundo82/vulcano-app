from abc import ABC, abstractmethod
from typing import Optional


class UserAuthenticatorPort(ABC):
    """
    Port (interface) for external user authentication.

    The concrete adapter that wraps LDAP lives in the infrastructure layer
    and is injected at runtime.  This keeps the application layer free of any
    dependency on LDAP libraries.
    """

    @abstractmethod
    def authenticate(self, username: str, password: str) -> Optional[dict]:
        """
        Validate *username* and *password* against the external identity provider.

        Returns a dictionary with at least ``username`` and ``display_name``
        keys on success, or ``None`` on failure.
        """
