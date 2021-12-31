from fastapi import APIRouter
from src.api.apis.flow_map import flow_map_router
from src.api.apis.flow_control import flow_control_router

router = APIRouter()
router.include_router(
    flow_map_router,
    prefix='/v1/flow-map',
    tags=['flow-map']
)

router.include_router(
    flow_control_router,
    prefix='/v1/flow-control',
    tags=['flow-control']
)