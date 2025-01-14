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
        return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)
