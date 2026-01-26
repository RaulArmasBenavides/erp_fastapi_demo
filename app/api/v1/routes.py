from fastapi import APIRouter

from app.api.v1.endpoints.supplier import router as supplier_router
from app.api.v1.endpoints.purchase_requests import router as purchase_requests_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.users import router as users_router

routers = APIRouter()

router_list = [supplier_router, purchase_requests_router, auth_router, users_router]

for router in router_list:
    routers.include_router(router)
