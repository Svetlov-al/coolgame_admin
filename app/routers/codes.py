from typing import Any

from fastapi import APIRouter, HTTPException, Response, status

from config import schemas
from services.code_service import CodeService
from services.game_service import GameService

router = APIRouter(
    prefix='/codes',
    tags=['Codes']
)

code_service = CodeService()
game_service = GameService()


@router.get("/{game_id}",
            status_code=status.HTTP_200_OK,
            description="Получение кодов по ID игры",
            response_model=schemas.ActivationCodesOut)
async def get_codes(game_id: str):
    return await code_service.get_codes(game_id)


@router.put("/{game_id}",
            status_code=status.HTTP_200_OK,
            description="Обновление кодов активации игры",
            response_model=schemas.GameOut)
async def update_codes(game_id: str, codes_update: schemas.ActivationCodes):
    existing_game = await game_service.find_game_by_id(game_id)
    if not existing_game:
        raise HTTPException(status_code=404, detail="Game not found")

    updated_game = await code_service.update_codes(game_id, codes_update.codes)
    return updated_game


@router.delete("/{game_id}/{code_index}")
async def delete_code(game_id: str, code_index: int):
    await code_service.delete_code(game_id, code_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
