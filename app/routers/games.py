from fastapi import APIRouter, HTTPException, Query, Response, status
from starlette.responses import JSONResponse

from config import schemas
from config.schemas import SaleStatusUpdate
from infrastructure.crypto_utils import encryptor
from services.game_service import GameService

game_service = GameService()

router = APIRouter(
    prefix='/games',
    tags=['Games']
)


@router.get("/", response_model=list[schemas.GameOut],
            status_code=status.HTTP_200_OK,
            description="Получение списка игр"
            )
async def get_games(skip: int = 0, limit: int = 50):
    games = await game_service.get_games(skip, limit)
    decrypted_games = encryptor.decrypt_game_passwords_in_list(games)
    return decrypted_games


@router.get("/find_game",
            response_model=list[schemas.GameOut],
            status_code=status.HTTP_200_OK,
            description="Поиск игры по названию")
async def find_game(gamename: str = Query(None)):
    games = await game_service.find_game(game_name=gamename)
    if games:
        decrypted_games = encryptor.decrypt_game_passwords_in_list(games)
        return decrypted_games
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")


@router.get("/search_games",
            response_model=list[schemas.GameOut],
            status_code=status.HTTP_200_OK,
            description="Поиск игры по разным полям")
async def search_games(query: str = Query(None), skip: int = 0, limit: int = 50):
    games = await game_service.search_games(search_query=query, skip=skip, limit=limit)
    if games:
        decrypted_games = encryptor.decrypt_game_passwords_in_list(games)
        return decrypted_games
    else:
        return []


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             description="Добавление игры",
             response_model=schemas.GameOut)
async def add_game(game: schemas.Game):
    new_game = await game_service.add_game(game_data=game.model_dump())
    return encryptor.decrypt_game_passwords(new_game)


@router.get("/{game_id}", response_model=schemas.GameOut)
async def get_game_by_id(game_id: str):
    game = await game_service.find_game_by_id(game_id)
    if game:
        return encryptor.decrypt_game_passwords(game)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")


@router.put("/{game_id}",
            status_code=status.HTTP_200_OK,
            description="Обновление игры по идентификатору",
            response_model=schemas.GameOut)
async def update_game(game_id: str, game_update: schemas.GameUpdate):
    update_data = game_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    updated_game = await game_service.update_game(game_id, update_data)
    if not updated_game:
        raise HTTPException(status_code=404, detail="Game not found")
    return encryptor.decrypt_game_passwords(updated_game)


@router.put("/{game_id}/sale-status",
            status_code=status.HTTP_200_OK,
            response_model=schemas.GameOut)
async def update_sale_status(game_id: str, sale_status_update: SaleStatusUpdate):
    game = await game_service.update_sale_status(game_id, sale_status_update.saleStatus)
    return encryptor.decrypt_game_passwords(game)


@router.delete("/{game_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               description="Удаление игры по идентификатору"
               )
async def delete_game(game_id: str):
    existing_game = await game_service.find_game_by_id(game_id)
    if not existing_game:
        raise HTTPException(status_code=404, detail="Game not found")

    await game_service.delete_game(existing_game.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
