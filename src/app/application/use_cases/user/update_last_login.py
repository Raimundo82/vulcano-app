from ....domain.repositories.user_repository import UserRepository


class UpdateLastLoginUseCase:
    """Record the current timestamp as the last login time for a user."""

    def __init__(self, user_repository: UserRepository) -> None:
        self._repo = user_repository

    def execute(self, username: str) -> bool:
        """
        Update the ``last_login`` field for *username* to the current time.

        Returns True on success, False when the user was not found.
        """
        return self._repo.update_last_login(username)
