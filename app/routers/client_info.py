from fastapi import APIRouter, HTTPException, Response, status
from starlette.responses import JSONResponse

from config import schemas
from services.client_info import ClientService

router = APIRouter(
    prefix='/clientinfo',
    tags=['ClientInfo']
)

client_service = ClientService()


@router.get("/{game_id}",
            response_model=schemas.ActivationInfo,
            status_code=status.HTTP_200_OK,
            description="Получение информации об активации по ID игры")
async def get_activation_info(game_id: str):
    activation_info = await activation_service.get_activation_info(game_id)
    if not activation_info:
        raise HTTPException(status_code=404, detail="Game not found")
    return activation_info


@router.post("/{game_id}",
             status_code=status.HTTP_201_CREATED,
             description="Добавление информации о клиенте в игру"
             )
async def add_client_info(game_id: str, client_info: schemas.ClientInfo):
    new_client_info = await client_service.add_psn_account(game_id, client_info)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"id": new_client_info})


@router.put("/{game_id}/{client_info_id}")
async def update_code(game_id: str, client_info_data: schemas.PSNAccount):
    await client_service.update_psn_account(game_id, client_info_data)
    return JSONResponse(content={"message": "success"}, status_code=status.HTTP_200_OK)


@router.delete("/{game_id}/{client_info_id}")
async def delete_code(game_id: str, client_info_id: int):
    await client_service.delete_code(game_id, client_info_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
