from typing import Optional

from bson import ObjectId
from fastapi import HTTPException

from config.database import collection
from config.schemas import GameOut, SaleStatus
from repositories.repository import GameRepository

game_repository = GameRepository(collection)


class GameService:
    """Класс сервиснгого слоя для работы с играми"""

    @staticmethod
    async def add_game(game_data: dict) -> str:
        """Метод добавления игры в базу данных"""

        return await game_repository.add_game(game_data)

    @staticmethod
    async def get_games(skip: int = 0, limit: int = 10):
        """Метод получения списка игр"""
        games = await game_repository.get_games(skip, limit)
        return [GameOut(**game) for game in games]

    @staticmethod
    async def find_game(game_name: str):
        """Метод поиска игры по названию"""
        return await game_repository.get_game_by_name(game_name)

    @staticmethod
    async def search_games(search_query: str):
        """Метод поиска игр по разным полям"""
        return await game_repository.search_games(search_query)

    @staticmethod
    async def find_game_by_id(game_id: str) -> Optional[GameOut]:
        """Метод поиска игры по ID"""
        game = await game_repository.get_game_by_id(game_id)
        if game:
            return GameOut(**game)
        return None

    @staticmethod
    async def update_game(game_id: str, update_data: dict):
        updated = await game_repository.update_game(game_id, update_data)
        return updated

    async def update_sale_status(self, game_id: str, sale_status: SaleStatus) -> str:
        existing_game = await self.find_game_by_id(game_id)
        if not existing_game:
            raise ValueError("Game not found")

        # Если статус уже установлен в нужное значение, возвращаем "success"
        if existing_game.saleStatus == sale_status:
            return "success"

        update_result = await game_repository.update_sale_status(game_id, sale_status)
        if update_result:
            return "success"
        else:
            raise HTTPException(status_code=404, detail="Game not found or unable to update")

    @staticmethod
    async def delete_game(game_id: ObjectId):
        """Метод удаления игры по идентификатору"""
        return await game_repository.delete_game(game_id)
