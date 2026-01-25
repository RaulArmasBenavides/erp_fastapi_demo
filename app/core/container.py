from app.application.services.auth_service import AuthService
from app.application.services.purchase_request_service import PurchaseRequestService
from app.application.services.supplier_service import SupplierService
from app.infrastructure.repository.database import Database
from app.infrastructure.repository.purchase_request_repository import (
    PurchaseRequestRepository,
)
from app.infrastructure.repository.supplier_repository import SupplierRepository
from app.infrastructure.repository.user_repository import UserRepository
from dependency_injector import containers, providers
from app.core.models.config import configs


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.security.current_user",
            "app.api.security.roles",
            "app.api.v1.endpoints.supplier",
            "app.api.v1.endpoints.purchase_requests",
            "app.api.v1.endpoints.auth",
            "app.core.dependencies",
        ]
    )

    # for sqlachemy
    db = providers.Singleton(Database, db_url=configs.DATABASE_URI)
    supplier_repository = providers.Factory(SupplierRepository, db=db)
    supplier_service = providers.Factory(
        SupplierService, supplier_repository=supplier_repository
    )
    purchase_repository = providers.Factory(PurchaseRequestRepository, db=db)
    purchase_request_service = providers.Factory(
        PurchaseRequestService, purchase_repository=purchase_repository
    )
    user_repository = providers.Factory(UserRepository, db=db)
    auth_service = providers.Factory(AuthService, user_repository=UserRepository)
