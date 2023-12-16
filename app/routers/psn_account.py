from fastapi import APIRouter, status
from starlette.responses import Response

from config import schemas
from infrastructure.crypto_utils import encryptor
from services.psn_service import PsnService

router = APIRouter(
    prefix='/psnaccount',
    tags=['PsnAccount']
)

psn_service = PsnService()


@router.get("/{game_id}",
            response_model=schemas.PSNAccountOut,
            status_code=status.HTTP_200_OK,
            description="Получение PSN аккаунта по ID игры"
            )
async def get_psn_account(game_id: str):
    return await psn_service.get_psn_account(game_id)


@router.post("/{game_id}",
             status_code=status.HTTP_201_CREATED,
             description="Добавление PSN аккаунта в игру",
             response_model=schemas.GameOut)
async def add_psn_account(game_id: str, psn_account: schemas.PSNAccount):
    new_psn_account =  await psn_service.add_psn_account(game_id, psn_account)
    return encryptor.decrypt_game_passwords(new_psn_account)


@router.put("/{game_id}",
            status_code=status.HTTP_200_OK,
            description='Обновление PSN аккаунта.',
            response_model=schemas.GameOut)
async def update_psn_account(game_id: str, psn_account_data: schemas.PSNAccountOut):
    updated_game = await psn_service.update_psn_account(game_id, psn_account_data)
    return encryptor.decrypt_game_passwords(updated_game)


@router.delete("/{game_id}")
async def delete_psn_account(game_id: str):
    await psn_service.delete_psn_account(game_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
