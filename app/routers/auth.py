from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from starlette.requests import Request
from starlette.responses import JSONResponse

from config import schemas
from config.settings import settings
from infrastructure.utils import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

router = APIRouter(
    tags=['Authentication']
)

load_dotenv()

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
ADMIN_PASSWORD = settings.admin_password


@router.post("/token", response_model=schemas.Token)
def token_path(user_credentials: OAuth2PasswordRequestForm = Depends()):
    """Маршурт для создания токена."""
    username = user_credentials.username
    password = user_credentials.password
    verifyied_password = verify_password(password, ADMIN_PASSWORD)

    if username != "admin" or not verifyied_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = create_access_token(data={"username": username})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/verify-token")
async def verify_token(request: Request):
    """Маршрут верификации токена."""
    bearer_token = request.headers.get('Authorization')
    if not bearer_token:
        return JSONResponse(status_code=400, content={"message": "Токен не предоставлен"})
    try:
        token = bearer_token.split(' ')[1]
        verify_access_token(token, HTTPException(status_code=401, detail="Invalid token"))
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})

    return JSONResponse(status_code=200, content={"message": "success"})


def create_access_token(data: dict):
    """Функция создания токена."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    """Верификация токена."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username != "admin":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return {"username": username}
