from datetime import datetime

from dependency_injector.wiring import inject
from fastapi import HTTPException
from ulid import ULID

from user.domain.repository.user_repo import IUserRepository
from user.domain.user import User
from utils.crypto import Crypto


class UserService:
    @inject
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo
        self.ulid = ULID()
        self.crypto = Crypto()

    def create_user(
        self,
        name: str,
        email: str,
        password: str,
        memo: str | None = None,
    ):
        _user = None

        try:
            _user = self.user_repo.find_by_email(email)
        except HTTPException as e:
            if e.status_code != 422:
                raise e

        if _user:
            raise HTTPException(status_code=422, detail="User already exists")

        now = datetime.now()
        encrypted_password = self.crypto.encrypt(password).decode("utf-8")
        user: User = User(id=self.ulid.generate(), name=name, email=email, password=encrypted_password, memo=memo, created_at=now, updated_at=now)
        self.user_repo.save(user)
        return user

    def get_users(self):
        return self.user_repo.find_all()

    def update_user(self, user_id: str, name: str | None = None, password: str | None = None):
        user = self.user_repo.find_by_id(user_id)

        if name:
            user.name = name
        if password:
            user.password = self.crypto.encrypt(password).decode("utf-8")
        user.updated_at = datetime.now()

        self.user_repo.update(user)
        return user
