from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.routers import (activation_info, auth, codes, email_account, games, psn_account, rental_info)
from routers.auth import verify_access_token


class AuthTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        excluded_routes = ["/login", "/admin", "/admin/", "/token"]

        if request.url.path in excluded_routes:
            return await call_next(request)

        token = request.headers.get('Authorization')
        if not token:
            return JSONResponse(status_code=400, content={"message": "Токен не предоставлен"})

        try:
            token = token.split(' ')[1]
            verify_access_token(token, HTTPException(status_code=401, detail="Invalid token"))
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"message": e.detail})

        return await call_next(request)


app = FastAPI(
    title='База данных по играм',
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
    swagger_ui_oauth2_redirect_url=None,
)

templates = Jinja2Templates(directory="app/templates")

origins = ['*']

app.add_middleware(AuthTokenMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(games.router)
app.include_router(codes.router)
app.include_router(psn_account.router)
app.include_router(email_account.router)
app.include_router(activation_info.router)
app.include_router(rental_info.router)
app.include_router(auth.router)


@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/admin")
async def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)
