from fastapi import HTTPException

from database import SessionLocal
from user.domain.repository.user_repo import IUserRepository
from user.domain.user import User as UserVO
from user.infra.schema.user import User
from utils.db_utils import row_to_dict


class UserRepository(IUserRepository):
    def save(self, user: UserVO):
        new_user = User(
            id=user.id, name=user.name, email=user.email, password=user.password, memo=user.memo, created_at=user.created_at, updated_at=user.updated_at
        )

        with SessionLocal() as db:
            try:
                db.add(new_user)
                db.commit()
            finally:
                db.close()

    def find_by_email(self, email) -> UserVO:
        with SessionLocal() as db:
            user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(status_code=422)

        return UserVO(**row_to_dict(user))

    def find_all(self):
        with SessionLocal() as db:
            user = db.query(User).all()

            if not user:
                raise HTTPException(status_code=422)

        return user

    def find_by_id(self, user_id: str) -> UserVO:
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=422)

        return UserVO(**row_to_dict(user))

    def update(self, user_vo: UserVO):
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_vo.id).first()

            if not user:
                raise HTTPException(status_code=422)

            user.name = user_vo.name
            user.password = user_vo.password
            db.add(user)
            db.commit()

        return user