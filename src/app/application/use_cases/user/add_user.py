from ....domain.entities.user import User
from ....domain.repositories.user_repository import UserRepository


class AddUserUseCase:
    """Add a new user to the system."""

    def __init__(self, user_repository: UserRepository) -> None:
        self._repo = user_repository

    def execute(
        self, username: str, display_name: str, email: str, is_admin: bool = False
    ) -> User:
        """
        Create and persist a new :class:`User`.

        Raises :class:`ValueError` when any of the required fields are blank.
        """
        username = username.strip()
        display_name = display_name.strip()
        email = email.strip().lower()

        if not all([username, display_name, email]):
            raise ValueError("username, display_name and email are required")

        user = User(
            username=username,
            display_name=display_name,
            email=email,
            is_admin=is_admin,
        )
        return self._repo.save(user)
