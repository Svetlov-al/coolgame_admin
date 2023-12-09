from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from enum import Enum


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *args, **kwargs):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema, **kwargs):
        field_schema.update(type='string')


class SaleStatus(str, Enum):
    FOR_SALE = "В продаже"
    SOLD = "Продано"
    PREORDER = "Прездаказ"
    FOR_SALE_PS5 = "В продаже PS5"
    FOR_SALE_PS4 = "В продаже PS4"
    PUSH_TO_SALE = "! На продажу"
    FOR_SALE_P1 = "В продаже П1"
    BLOCKED = "Заблокирован"
    RECOVER = "Восстановить"


class SaleStatusUpdate(BaseModel):
    saleStatus: SaleStatus


class RentalStatus(str, Enum):
    AVAILABLE = "ДА"
    NOT_AVAILIABLE = "НЕТ"


class ClientInfo(BaseModel):
    name: str
    email: Optional[str] = None
    vkLink: Optional[str] = None
    tgLink: Optional[str] = None


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    vkLink: Optional[str] = None
    tgLink: Optional[str] = None


class ActivationInfo(BaseModel):
    ps4ActivationP1: List[ClientInfo] = []
    ps5ActivationP1: List[ClientInfo] = []
    ps4ActivationP3: List[ClientInfo] = []
    ps5ActivationP3: List[ClientInfo] = []


class RentalInfo(BaseModel):
    isRented: Optional[RentalStatus] = None
    rentalPrice: Optional[float] = None
    rentalDate: Optional[str] = None


class PSNAccount(BaseModel):
    name: str
    password: str
    address: str
    birthDate: str
    networkID: str
    phoneNumbers: List[str]
    paymentMethod: Optional[str] = None
    secretQuestionAnswer: str


class PSNAccountOut(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    address: Optional[str] = None
    birthDate: Optional[str] = None
    networkID: Optional[str] = None
    phoneNumbers: Optional[List[str]] = []
    paymentMethod: Optional[str] = None
    secretQuestionAnswer: Optional[str] = None


class EmailAccountOut(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    birthDate: Optional[str] = None
    secretQuestionAnswer: Optional[str] = None


class EmailAccount(BaseModel):
    email: str
    password: str
    birthDate: str
    secretQuestionAnswer: Optional[str] = None


class ActivationCodes(BaseModel):
    codes: Optional[List[str]] = []


class ActivationCodesOut(BaseModel):
    game_id: PyObjectId
    codes: Optional[List[str]] = []

    class Config:
        json_encoders = {
            ObjectId: lambda oid: str(oid)
        }
        populate_by_name = True


class Game(BaseModel):
    account_number: int
    gameName: str
    transactionNumber: str
    price: float
    purchaseDate: str
    lastDeactivationDate: Optional[str] = None
    additionalInfo: Optional[str] = None
    comment: Optional[str] = None


class GameOut(Game):
    id: PyObjectId = Field(alias='_id')
    psnAccount: Optional[PSNAccount] = None
    emailAccount: Optional[EmailAccount] = None
    activationCodes: Optional[List[str]] = []
    activationInfo: Optional[List[str]] = []
    rentalInfo: Optional[RentalInfo] = None
    saleStatus: Optional[SaleStatus] = None

    class Config:
        json_encoders = {
            ObjectId: lambda oid: str(oid)
        }
        populate_by_name = True


class GameUpdate(BaseModel):
    account_number: Optional[int] = None
    gameName: Optional[str] = None
    transactionNumber: Optional[str] = None
    price: Optional[float] = None
    purchaseDate: Optional[str] = None
    lastDeactivationDate: Optional[str] = None
    additionalInfo: Optional[str] = None
    comment: Optional[str] = None
    rentalInfo: Optional[RentalInfo] = None
