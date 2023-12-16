from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """Верификация пароля"""
    return pwd_context.verify(plain_password, hashed_password)

if __name__ == "__main__":
    pass
    # password = hash_password('admin')
    # print(f"Hashed password - {password}")
    # verifyed_password = verify_password('admin', password)
    # print(f"{verifyed_password}")
