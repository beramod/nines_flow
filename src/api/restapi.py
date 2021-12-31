import logging
from src.api import config
from functools import lru_cache
from fastapi import FastAPI, Depends, APIRouter
from src.api.errors import http_422_error_handler, http_error_handler
from src.api.database.mongodb import set_db, close_db
from src.api.urls import router as api_router
from src.api import settings
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from src.api.interpreter import RequestHandlingMiddleware
from src.api.custom_route import CustomRoute

app = FastAPI(title="nines_flow")

app.add_middleware(RequestHandlingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", set_db)
app.add_event_handler("shutdown", close_db)

app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)
app.router.route_class = CustomRoute
app.include_router(
    api_router,
    prefix="/api",
    tags=["api"]
)

@lru_cache()
def get_settings():
    return config.Settings()

@app.get('/')
async def root(settings: config.Settings = Depends(get_settings)):
    env = settings.nines_flow_env
    print(env)
    return {"message": f"NINES Flow REST API, env:{env}"}