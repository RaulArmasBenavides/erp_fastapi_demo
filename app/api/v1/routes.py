from fastapi import APIRouter

from app.api.v1.endpoints.entries import router as entries_router
 
routers = APIRouter(prefix="/api/v1")
router_list = [entries_router]

for router in router_list:
    routers.include_router(router)