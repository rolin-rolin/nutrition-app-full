from app.api.v1.endpoints import recommend, macro_target, health

from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(recommend.router, prefix="/recommend", tags=["recommendations"])
api_router.include_router(macro_target.router, prefix="/macro-targets", tags=["macro-targets"]) 