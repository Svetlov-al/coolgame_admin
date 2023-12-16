from fastapi import APIRouter, HTTPException, status

from config import schemas
from infrastructure.crypto_utils import encryptor
from services.email_service import EmailService

router = APIRouter(
    prefix='/emailaccount',
    tags=['EmailAccount']
)

email_service = EmailService()


@router.get("/{game_id}",
            response_model=schemas.EmailAccountOut,
            status_code=status.HTTP_200_OK,
            description="Получение Email аккаунта по ID игры")
async def get_email_account(game_id: str):
    game_email_account =  await email_service.get_email_account(game_id)
    return encryptor.decrypt_game_passwords(game_email_account)


@router.post("/{game_id}", status_code=status.HTTP_201_CREATED, description="Добавление Email аккаунта в игру")
async def add_email_account(game_id: str, email_account: schemas.EmailAccount):
    await email_service.add_email_account(game_id, email_account)
    return {"message": "Email account added successfully"}


@router.put("/{game_id}",
            status_code=status.HTTP_200_OK,
            description="Обновление Email аккаунта в игре",
            response_model=schemas.GameOut)
async def update_email_account(game_id: str, email_account: schemas.EmailAccountOut):
    updated_game = await email_service.update_email_account(game_id, email_account)
    return encryptor.decrypt_game_passwords(updated_game)

@router.delete("/{game_id}", status_code=status.HTTP_200_OK, description="Удаление Email аккаунта из игры")
async def delete_email_account(game_id: str):
    success = await email_service.delete_email_account(game_id)
    if success:
        return {"message": "Email account deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Email account not found")
