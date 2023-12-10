from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from starlette.responses import JSONResponse

from config import schemas
from config.schemas import ClientInfo, ClientUpdate
from services.activation_service import ActivationService


router = APIRouter(
    prefix='/activation',
    tags=['ActivationInfo']
)
activation_service = ActivationService


@router.get("/{game_id}",
            response_model=schemas.ActivationInfo,
            status_code=status.HTTP_200_OK
            )
async def get_activation_info(game_id: str):
    return await activation_service.get_activation_info(game_id)


@router.post("/{game_id}")
async def add_client_to_activation(game_id: str, client_info: ClientInfo, activation_type: str = Query(...)):
    await activation_service.add_client_to_activation(game_id, client_info.model_dump(), activation_type)
    return {"message": "Client added successfully"}


@router.put("/{game_id}/{activation_type}/{client_index}")
async def update_client_info(game_id: str, activation_type: str, client_index: int, client_update: ClientUpdate):
    success = await activation_service.update_client_info(game_id, activation_type, client_index, client_update)
    if not success:
        raise HTTPException(status_code=404, detail="Client not found or update failed")
    return {"message": "Client info updated successfully"}


@router.delete("/{game_id}/{activation_type}/{client_index}")
async def delete_client_info(game_id: str, activation_type: str, client_index: int):
    success = await activation_service.remove_client_from_activation(game_id, activation_type, client_index)
    if not success:
        raise HTTPException(status_code=404, detail="Client not found or deletion failed")
    return {"message": "Client removed from activation successfully"}
