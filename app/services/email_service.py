from typing import Optional
from config import schemas

from config.database import collection
from repositories.repository import EmailAccountRepository

email_repository = EmailAccountRepository(collection)


class EmailService:
    """Сервисный слой для работы с аккаунтом от почты"""
    @staticmethod
    async def get_email_account(game_id: str) -> Optional[schemas.EmailAccountOut]:
        return await email_repository.get_email_account(game_id)

    @staticmethod
    async def add_email_account(game_id: str, email_account: schemas.EmailAccount):
        return await email_repository.add_email_account(game_id, email_account)

    @staticmethod
    async def update_email_account(game_id: str, email_account: schemas.EmailAccountOut):
        return await email_repository.update_email_account(game_id, email_account)

    @staticmethod
    async def delete_email_account(game_id: str):
        return await email_repository.delete_email_account(game_id)
