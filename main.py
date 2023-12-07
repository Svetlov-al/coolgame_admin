from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.routers import (
    games,
    codes,
    psn_account,
    email_account,
    client_info,
    activation_info,
    rental_info
)

app = FastAPI(
    title='База данных по играм'
)

templates = Jinja2Templates(directory="app/templates")

origins = ['*']

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
app.include_router(client_info.router)
app.include_router(activation_info.router)
app.include_router(rental_info.router)


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)
