from fastapi import APIRouter, HTTPException, status

from config import schemas
from services.game_service import GameService
from services.rental_info_service import RentalInfoService

router = APIRouter(
    prefix='/rentalinfo',
    tags=['RentalInfo']
)

game_service = GameService()
rental_info_service = RentalInfoService()


@router.get("/{game_id}",
            status_code=status.HTTP_200_OK,
            description="Получение статуса аренды по игре",
            response_model=schemas.RentalInfo)
async def get_rental_info(game_id: str):
    rental_info = await rental_info_service.get_rental_info(game_id)
    if rental_info is None:
        raise HTTPException(status_code=404, detail="Rental info is unfield")
    return rental_info


@router.put("/{game_id}",
            status_code=status.HTTP_200_OK,
            description="Обновление статуса аренды игры")
async def update_rental_info(game_id: str, rental_info_update: schemas.RentalInfo):
    existing_game = await game_service.find_game_by_id(game_id)
    if not existing_game:
        raise HTTPException(status_code=404, detail="Game not found")

    await rental_info_service.update_rental_info(game_id, rental_info_update)
    return {"message": "Rental info updated successfully"}
