from ..domain.repositories import UserRepository

_repo = UserRepository()


def register_user(username, display_name, email):
    return _repo.create(username, display_name, email)


def get_users():
    return [u.to_dict() for u in _repo.get_all()]


def add_user(username, display_name, email, is_admin):
    return _repo.create(username, display_name, email, is_admin)


def edit_user(user_id, username, display_name, email, is_admin):
    return _repo.update(
        user_id,
        username=username,
        display_name=display_name,
        email=email,
        is_admin=is_admin,
    )


def delete_user(user_id):
    return _repo.delete(user_id)
