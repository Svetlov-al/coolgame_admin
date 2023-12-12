import re

from bson import ObjectId
from fastapi import HTTPException

from config import schemas
from config.schemas import ActivationCodesOut, EmailAccountOut, PSNAccountOut, SaleStatus


class GameRepository:
    def __init__(self, collection):
        self.collection = collection

    async def add_game(self, game_data: dict):
        """Метод добавления игры в базу данных"""
        result = await self.collection.insert_one(game_data)
        created_game = await self.collection.find_one(result.inserted_id)
        return created_game

    async def get_games(self, skip: int, limit: int):
        """Метод получения списка игр"""
        return await self.collection.find().skip(skip).limit(limit).to_list(length=limit)

    async def get_game_by_name(self, game_name: str) -> list[dict]:
        """Метод поиска игры по названию"""
        regex = re.compile(game_name, re.IGNORECASE)
        games = await self.collection.find({'gameName': regex}).to_list(None)
        return games

    async def search_games(self, search_query: str, skip: int, limit: int) -> list[dict]:
        """Метод поиска игр по разным полям"""
        regex = re.compile(search_query, re.IGNORECASE)
        query = {
            "$or": [
                {"gameName": regex},
                {"transactionNumber": regex},
                {"purchaseDate": {"$regex": search_query}},
                {"lastDeactivationDate": {"$regex": search_query}},
                {"additionalInfo": regex},
                {"saleStatus": regex},
                {"psnAccount.name": regex},
                {"psnAccount.networkID": regex},
                {"emailAccount.email": regex},
                {"activationInfo.ps4ActivationP1.name": regex},
                {"activationInfo.ps4ActivationP1.email": regex},
                {"activationInfo.ps4ActivationP1.vkLink": regex},
                {"activationInfo.ps4ActivationP1.tgLink": regex},
                {"activationInfo.ps5ActivationP1.name": regex},
                {"activationInfo.ps5ActivationP1.email": regex},
                {"activationInfo.ps5ActivationP1.vkLink": regex},
                {"activationInfo.ps5ActivationP1.tgLink": regex},
                {"activationInfo.ps4ActivationP3.name": regex},
                {"activationInfo.ps4ActivationP3.email": regex},
                {"activationInfo.ps4ActivationP3.vkLink": regex},
                {"activationInfo.ps4ActivationP3.tgLink": regex},
                {"activationInfo.ps5ActivationP3.name": regex},
                {"activationInfo.ps5ActivationP3.email": regex},
                {"activationInfo.ps5ActivationP3.vkLink": regex},
                {"activationInfo.ps5ActivationP3.tgLink": regex},
            ]
        }
        games = await self.collection.find(query).skip(skip).limit(limit).to_list(None)
        return games

    async def get_game_by_id(self, game_id: str) -> dict:
        """Метод поиска игры по ID"""
        return await self.collection.find_one({'_id': ObjectId(game_id)})

    async def update_game(self, game_id: str, game_data: dict):
        query = {'_id': ObjectId(game_id)}
        update_fields = {f"{key}": value for key, value in game_data.items() if value is not None}

        if not update_fields:
            return []

        result = await self.collection.update_one(query, {'$set': update_fields})

        if result.matched_count == 0:
            return []

        updated_game = await self.collection.find_one(query)
        return updated_game

    async def update_sale_status(self, game_id: str, sale_status: SaleStatus) -> bool:
        update_data = {'saleStatus': sale_status.value}

        update_result = await self.collection.update_one(
            {'_id': ObjectId(game_id)},
            {'$set': update_data}
        )

        return True

    async def delete_game(self, game_id: ObjectId):
        """Метод удаления игры по идентификатору"""
        await self.collection.delete_one({'_id': ObjectId(game_id)})


class CodeRepository:
    """Класс для работы с кодами активаций"""

    def __init__(self, collection):
        self.collection = collection

    async def get_activation_codes(self, game_id: str) -> ActivationCodesOut:
        game_data = await self.collection.find_one({'_id': ObjectId(game_id)}, {'activationCodes': 1})
        if game_data:
            return ActivationCodesOut(game_id=game_id, codes=game_data.get('activationCodes', []))
        else:
            # Если игра не найдена, возможно, стоит вернуть ошибку или пустой объект
            raise HTTPException(status_code=404, detail="Game not found")

    async def update_activation_codes(self, game_id: str, codes: list[str]):
        # Выполнение обновления
        await self.collection.update_one(
            {'_id': ObjectId(game_id)},
            {'$set': {'activationCodes': codes}}
        )

        # Получение и возврат обновленных данных об игре
        updated_game = await self.collection.find_one({'_id': ObjectId(game_id)})
        return updated_game

    async def delete_activation_code(self, game_id: str, code_index: int):
        """Удаление кода активации по индексу"""
        game_data = await self.collection.find_one({'_id': ObjectId(game_id)}, {'activationCodes': 1})
        if game_data and 'activationCodes' in game_data and len(game_data['activationCodes']) > code_index:
            # Удаление кода по индексу
            del game_data['activationCodes'][code_index]
            # Обновление списка активационных кодов в игре
            await self.update_activation_codes(game_id, game_data['activationCodes'])
            return True
        else:
            raise HTTPException(status_code=404, detail="Game not found or index out of range")


class ActivationRepository:
    def __init__(self, collection):
        self.collection = collection

    async def get_activation_info(self, game_id: str) -> dict:
        """Получение информации об активации по ID игры"""
        game_data = await self.collection.find_one({'_id': ObjectId(game_id)}, {'activationInfo': 1})
        if game_data:
            return game_data.get('activationInfo', {})
        else:
            raise HTTPException(status_code=404, detail="Game not found")

    async def add_client_to_activation(self, game_id: str, client_info: dict, activation_type: str):
        """Добавление клиента к определенному типу активации"""
        update_query = {'$push': {f'activationInfo.{activation_type}': client_info}}
        await self.collection.update_one({'_id': ObjectId(game_id)}, update_query)

    async def update_client_info(self, game_id: str, activation_type: str, client_index: int, client_update: dict):
        # Формирование запроса обновления только для указанных полей
        update_fields = {f"activationInfo.{activation_type}.{client_index}.{key}": value for key, value in
                         client_update.items() if value is not None}
        if not update_fields:
            return False

        query = {"_id": ObjectId(game_id)}
        update_data = {"$set": update_fields}

        result = await self.collection.update_one(query, update_data)
        return result.modified_count > 0

    async def remove_client_from_activation(self, game_id: str, activation_type: str, client_index: int):
        """Удаление клиента из активации"""
        update_query = {"$unset": {f"activationInfo.{activation_type}.{client_index}": ""}}

        result = await self.collection.update_one({"_id": ObjectId(game_id)}, update_query)

        # Чистка массива от "пустых" элементов
        await self.collection.update_one({"_id": ObjectId(game_id)},
                                         {"$pull": {f"activationInfo.{activation_type}": None}})

        return result.modified_count > 0


class RentalInfoRepository:
    """Класс для работы со статусом аренды"""
    def __init__(self, collection):
        self.collection = collection

    async def get_rental_info(self, game_id: str):
        """Метод для получения статуса аренды по текущей игре"""
        game_data = await self.collection.find_one({"_id": ObjectId(game_id)})
        print(game_data)
        if game_data and "rentalInfo" in game_data:
            return game_data["rentalInfo"]
        return None

    async def update_rental_info(self, game_id: str, rental_info_update):
        # Проверка на существование RentalInfo и инициализация, если необходимо
        await self.collection.update_one(
            {"_id": ObjectId(game_id), "rentalInfo": {"$exists": False}},
            {"$set": {"rentalInfo": {}}}
        )

        # Обновление полей в RentalInfo
        update_data = {"$set": {f"rentalInfo.{key}": value for key, value in rental_info_update.items()}}
        result = await self.collection.update_one({"_id": ObjectId(game_id)}, update_data)
        return result.modified_count > 0


class EmailAccountRepository:
    """Репозиторий для работы с почтовым аккаунтом"""
    def __init__(self, collection):
        self.collection = collection

    async def get_email_account(self, game_id: str) -> EmailAccountOut:
        game_data = await self.collection.find_one({'_id': ObjectId(game_id)}, {'emailAccount': 1})
        if game_data and 'emailAccount' in game_data and game_data['emailAccount']:
            return EmailAccountOut(**game_data['emailAccount'])
        else:
            raise HTTPException(status_code=404, detail="No data")

    async def add_email_account(self, game_id: str, email_account: schemas.EmailAccount):
        update_result = await self.collection.update_one(
            {'_id': ObjectId(game_id)},
            {'$set': {'emailAccount': email_account.model_dump()}}
        )
        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Game not found or Email account not added")

    async def update_email_account(self, game_id: str, email_account: schemas.EmailAccountOut):
        update_data = {f'emailAccount.{k}': v for k, v in email_account.model_dump(exclude_unset=True).items()}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        update_result = await self.collection.update_one(
            {'_id': ObjectId(game_id)},
            {'$set': update_data}
        )
        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Game not found or Email account not updated")

        updated_game = await self.collection.find_one({'_id': ObjectId(game_id)})
        return updated_game

    async def delete_email_account(self, game_id: str):
        update_result = await self.collection.update_one(
            {'_id': ObjectId(game_id)},
            {'$set': {'emailAccount': None}}
        )
        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Game not found or Email account not deleted")
        return True


class PSNAccountRepository:
    """Репозиторий для работы с аккаунтом ПСН"""
    def __init__(self, collection):
        self.collection = collection

    async def get_psn_account(self, game_id: str) -> PSNAccountOut:
        game_data = await self.collection.find_one({'_id': ObjectId(game_id)}, {'psnAccount': 1})
        if game_data and 'psnAccount' in game_data and game_data['psnAccount']:
            return PSNAccountOut(**game_data['psnAccount'])
        else:
            raise HTTPException(status_code=404, detail="No data")

    async def add_psn_account(self, game_id: str, psn_account: schemas.PSNAccount):
        update_result = await self.collection.update_one(
            {'_id': ObjectId(game_id)},
            {'$set': {'psnAccount': psn_account.model_dump()}}
        )
        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Game not found or psn account not added")
        updated_game = await self.collection.find_one({'_id': ObjectId(game_id)})
        return updated_game

    async def update_psn_account(self, game_id: str, psn_account: schemas.PSNAccountOut):
        update_data = {f'psnAccount.{k}': v for k, v in psn_account.model_dump(exclude_unset=True).items()}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        update_result = await self.collection.update_one(
            {'_id': ObjectId(game_id)},
            {'$set': update_data}
        )
        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Game not found or psn account not updated")

        updated_game = await self.collection.find_one({'_id': ObjectId(game_id)})
        return updated_game

    async def delete_psn_account(self, game_id: str):
        update_result = await self.collection.update_one(
            {'_id': ObjectId(game_id)},
            {'$set': {'psnAccount': None}}
        )
        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Game not found or psn account not deleted")
        return True
