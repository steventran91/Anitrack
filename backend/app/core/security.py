import bycrypt

def hash_password(password: str) -> str:
    salt = bycrypt.salt()
    hashed = bycrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bycrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
