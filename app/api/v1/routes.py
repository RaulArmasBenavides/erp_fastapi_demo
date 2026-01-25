from fastapi import APIRouter

from app.api.v1.endpoints.supplier import router as supplier_router
 
routers = APIRouter(prefix="/api/v1")
router_list = [supplier_router]

for router in router_list:
    routers.include_router(router)