from typing import List

from ....domain.entities.user import User
from ....domain.repositories.user_repository import UserRepository


class ListUsersUseCase:
    """Return all users ordered by role then username."""

    def __init__(self, user_repository: UserRepository) -> None:
        self._repo = user_repository

    def execute(self) -> List[User]:
        return self._repo.get_all()
