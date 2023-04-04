import bcrypt


def hash_password(password: str | bytes) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_password(password: str | bytes, password_hash: str | bytes) -> bool:
    return bcrypt.checkpw(
        password.encode('utf-8'),
        password_hash.encode('utf-8')
    )
