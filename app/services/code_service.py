from fastapi import HTTPException

from config import schemas
from config.database import collection
from repositories.repository import CodeRepository, GameRepository

game_repository = GameRepository(collection)
code_repository = CodeRepository(collection)


class CodeService:
    """Класс для работы с кодами активации игр"""

    @staticmethod
    async def get_codes(game_id: str) -> schemas.ActivationCodesOut:
        codes_data = await code_repository.get_activation_codes(game_id)
        if codes_data is None:
            raise HTTPException(status_code=404, detail="Game not found")
        return codes_data

    @staticmethod
    async def delete_code(game_id: str, code_index: int) -> bool:
        """Удаление кода активации игры"""
        result = await code_repository.delete_activation_code(game_id, code_index)
        return result

    @staticmethod
    async def update_codes(game_id: str, codes: list[str]) -> bool:
        # Здесь нет необходимости в блоке try-except, если вы не обрабатываете конкретные исключения
        return await code_repository.update_activation_codes(game_id, codes)

