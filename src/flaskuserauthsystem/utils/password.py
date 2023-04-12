import bcrypt


def encode(string: str | bytes) -> bytes:
    return string.encode('utf-8') if isinstance(string, str) else string


def hash_password(password: str | bytes) -> bytes:
    return bcrypt.hashpw(encode(password), bcrypt.gensalt())


def check_password(password: str | bytes, password_hash: str | bytes) -> bool:
    return bcrypt.checkpw(
        encode(password),
        encode(password_hash),
    )
