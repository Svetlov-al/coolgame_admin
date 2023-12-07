from config.database import collection
from config.schemas import ClientUpdate
from repositories.repository import ActivationRepository

activation_repository = ActivationRepository(collection)


class ActivationService:
    """Сервис для работы с активациями"""

    @staticmethod
    async def get_activation_info(game_id: str) -> dict:
        """Сервис для получения информации об активации"""
        return await activation_repository.get_activation_info(game_id)

    @staticmethod
    async def add_client_to_activation(game_id: str, client_info: dict, activation_type: str):
        """Сервис для добавления клиента к активации"""
        await activation_repository.add_client_to_activation(game_id, client_info, activation_type)

    @staticmethod
    async def update_client_info(game_id: str, activation_type: str, client_index: int, client_update: ClientUpdate):
        return await activation_repository.update_client_info(game_id, activation_type, client_index, client_update.model_dump())

    @staticmethod
    async def remove_client_from_activation(game_id: str, activation_type: str, client_index: int):
        """Удаление клиента из активации"""
        return await activation_repository.remove_client_from_activation(game_id, activation_type, client_index)
