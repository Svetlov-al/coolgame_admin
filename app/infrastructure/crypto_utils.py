import base64
import binascii
import re

from cryptography.fernet import Fernet

from config import schemas
from config.schemas import GameOut
from config.settings import settings


class PasswordCipher:
    """Класс шифрования пароля для обеспечения безопасности хранения в базе и передачи"""

    def __init__(self, key: str):
        self.cipher_suite = Fernet(key.encode())

    def encrypt_password(self, plain_password: str) -> str:
        """
        Шифрует переданный пароль.

        Аргументы:
            plain_password (str): Пароль, который необходимо зашифровать.

        Возвращает:
            bytes: Зашифрованный пароль.
        """
        encrypted_password = self.cipher_suite.encrypt(plain_password.encode())
        return base64.urlsafe_b64encode(encrypted_password).decode('utf-8')

    def decrypt_password(self, encrypted_password: str) -> str:
        """
        Расшифровывает переданный зашифрованный пароль.

        Аргументы:
            encrypted_password (bytes): Зашифрованный пароль для расшифровки.

        Возвращает:
            str: Расшифрованный пароль.
        """
        if not self.is_encrypted(encrypted_password):
            return encrypted_password  # Если пароль не зашифрован, возвращаем его как есть

        try:
            encrypted_password_bytes = base64.urlsafe_b64decode(encrypted_password.encode('utf-8'))
            return self.cipher_suite.decrypt(encrypted_password_bytes).decode()
        except (binascii.Error, ValueError):
            print("Ошибка декодирования Base64 или шифрования")
            return encrypted_password

    def is_encrypted(self, password: str) -> bool:
        # Простая проверка, что строка соответствует формату Base64
        return re.match(r'^[A-Za-z0-9+/=]+\Z', password) is not None


    def decrypt_game_passwords(self, game_data):
        # Расшифровка пароля email аккаунта
        if game_data.get('emailAccount') and game_data['emailAccount'].get('password'):
            decrypted_email_password = encryptor.decrypt_password(game_data['emailAccount']['password'])
            game_data['emailAccount']['password'] = decrypted_email_password

        # Расшифровка пароля PSN аккаунта
        if game_data.get('psnAccount') and game_data['psnAccount'].get('password'):
            decrypted_psn_password = encryptor.decrypt_password(game_data['psnAccount']['password'])
            game_data['psnAccount']['password'] = decrypted_psn_password

        return game_data

    def decrypt_game_passwords_in_list(self, games_list: list[GameOut]):
        decrypted_games = []
        for game in games_list:
            game_dict = game.model_dump()
            decrypted_game_dict = self.decrypt_game_passwords(game_dict)
            decrypted_game = GameOut(**decrypted_game_dict)  # Создание объекта Pydantic из словаря
            decrypted_games.append(decrypted_game)
        return decrypted_games

encryptor = PasswordCipher(settings.encryption_key)
