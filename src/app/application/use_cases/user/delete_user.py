from ....domain.repositories.user_repository import UserRepository


class DeleteUserUseCase:
    """Delete a user from the system."""

    def __init__(self, user_repository: UserRepository) -> None:
        self._repo = user_repository

    def execute(self, user_id: int, requesting_user_id: int) -> bool:
        """
        Delete the user identified by *user_id*.

        Raises :class:`PermissionError` when a user tries to delete themselves.
        Returns True on success, False when the user was not found.
        """
        if user_id == requesting_user_id:
            raise PermissionError("Users cannot delete their own account")

        return self._repo.delete(user_id)
