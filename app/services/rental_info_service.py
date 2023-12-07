from config.database import collection
from repositories.repository import RentalInfoRepository

rental_info_repository = RentalInfoRepository(collection)


class RentalInfoService:
    """Сервисный слой для работы со статусом аренды"""

    @staticmethod
    async def get_rental_info(game_id: str):
        return await rental_info_repository.get_rental_info(game_id)

    @staticmethod
    async def update_rental_info(game_id: str, rental_info_update):
        return await rental_info_repository.update_rental_info(game_id,
                                                               rental_info_update.dict(exclude_unset=True))
