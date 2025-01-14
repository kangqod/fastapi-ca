from datetime import datetime

from database import SessionLocal
from user.infra.schema.user import User
from utils.crypto import Crypto

with SessionLocal() as db:
    for i in range(50):
        user = User(
            id=f"UserID-{str(i).zfill(2)}",
            name=f"TestUser{i}",
            email=f"test-user{i}@test.com",
            password=Crypto().encrypt("test").decode("utf-8"),
            memo=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        db.add(user)
    db.commit()
