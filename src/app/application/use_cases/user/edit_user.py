from ....domain.entities.user import User
from ....domain.repositories.user_repository import UserRepository


class EditUserUseCase:
    """Update an existing user's details."""

    def __init__(self, user_repository: UserRepository) -> None:
        self._repo = user_repository

    def execute(
        self,
        user_id: int,
        username: str,
        display_name: str,
        email: str,
        is_admin: bool = False,
    ) -> User:
        """
        Update the user identified by *user_id*.

        Raises :class:`ValueError` when any required field is blank.
        Raises :class:`LookupError` when the user is not found.
        """
        username = username.strip()
        display_name = display_name.strip()
        email = email.strip().lower()

        if not all([username, display_name, email]):
            raise ValueError("username, display_name and email are required")

        user = self._repo.get_by_id(user_id)
        if user is None:
            raise LookupError(f"User with id {user_id} not found")

        user.username = username
        user.display_name = display_name
        user.email = email
        user.is_admin = is_admin
        return self._repo.update(user)
