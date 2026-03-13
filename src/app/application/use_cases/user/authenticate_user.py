from typing import Optional

from ....domain.entities.user import User
from ....domain.repositories.user_repository import UserRepository
from ...ports.user_authenticator_port import UserAuthenticatorPort


class AuthenticateUserUseCase:
    """
    Authenticate a user against the external identity provider and verify
    they exist in the local database.

    Returns the :class:`~domain.entities.user.User` entity on success, or
    ``None`` when the credentials are invalid or the user is not registered.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        authenticator: UserAuthenticatorPort,
    ) -> None:
        self._repo = user_repository
        self._authenticator = authenticator

    def execute(self, username: str, password: str) -> Optional[User]:
        """
        Validate *username* / *password* via the injected authenticator.

        The user must also be present in the local ``users`` table.  Returns a
        :class:`User` populated with the provider's ``display_name`` and the
        local ``is_admin`` flag, or ``None`` on failure.
        """
        result = self._authenticator.authenticate(username, password)
        if not result:
            return None

        user = self._repo.get_by_username(username)
        if not user:
            return None

        user.display_name = result.get("display_name", username)
        return user
