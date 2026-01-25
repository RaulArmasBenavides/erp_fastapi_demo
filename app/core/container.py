from app.application.services.purchase_request_service import PurchaseRequestService
from app.infrastructure.repository.database import Database
from app.infrastructure.repository.purchase_request_repository import (
    PurchaseRequestRepository,
)
from dependency_injector import containers, providers
from app.core.models.config import configs
from app.infrastructure.schema.entry_schema import EntrySchema

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.endpoints.supplier",
            "app.api.v1.endpoints.purchase_requests",
            "app.core.dependencies",
        ]
    )

    # for sqlachemy
    db = providers.Singleton(Database, db_url=configs.DATABASE_URI)
    entry_repository = providers.Factory(EntryRepository, db=db)
    entry_service = providers.Factory(EntryService, entry_repository=entry_repository)
    purchase_repository = providers.Factory(PurchaseRequestRepository, db=db)
    purchase_request_service = providers.Factory(
        PurchaseRequestService, purchase_repository=purchase_repository
    )
