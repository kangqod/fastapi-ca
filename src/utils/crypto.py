import bcrypt


class Crypto:
    def encrypt(self, password: str):
        # Hash a password using bcrypt
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password

    def verify(self, plain_password, hashed_password):
        # Check if the provided password matches the stored password (hashed)
        password_byte_enc = plain_password.encode("utf-8")
        # 해시된 비밀번호는 이미 바이트여야 하지만, 문자열로 되어 있을 경우 바이트로 변환

        hashed_password_byte_enc = hashed_password.encode("utf-8") if isinstance(hashed_password, str) else hashed_password

        # bcrypt로 비밀번호 확인
        return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password_byte_enc)
