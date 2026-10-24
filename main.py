from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.api.handlers.user.user_route_handler import UserAPIRouteHandler
from app.infrastructure.database.sqlite.database import (
    close_db,
    init_db,
    alchemy,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title='A Mão API',
    description='API de assistente pessoal que responde perguntas com base nos **seus próprios arquivos**.',
    version='0.1.0',
    contact={
        'name': 'Arthur',
        'email': 'arthurfranca.dev@gmail.com',
    },
    license_info={
        'name': 'MIT',
        'url': 'https://opensource.org/licenses/MIT',
    },
    root_path='/api/v1',
)
alchemy.init_app(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/health', tags=['Health'])
async def health_check():
    return {'status': 'ok'}


user_route_handler = UserAPIRouteHandler()


user_route_handler.register_route(app)
