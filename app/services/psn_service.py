from typing import Optional
from config import schemas

from config.database import collection
from repositories.repository import PSNAccountRepository

psn_repository = PSNAccountRepository(collection)


class PsnService:
    """Сервисный слой для работы с аккаунтом от почты"""
    @staticmethod
    async def get_psn_account(game_id: str) -> Optional[schemas.PSNAccountOut]:
        return await psn_repository.get_psn_account(game_id)

    @staticmethod
    async def add_psn_account(game_id: str, psn_account: schemas.PSNAccount):
        return await psn_repository.add_psn_account(game_id, psn_account)

    @staticmethod
    async def update_psn_account(game_id: str, psn_account: schemas.PSNAccountOut):
        return await psn_repository.update_psn_account(game_id, psn_account)

    @staticmethod
    async def delete_psn_account(game_id: str):
        return await psn_repository.delete_psn_account(game_id)
