# main.py
from app.util.class_object import singleton
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.routes import routers as v1_routers
from app.core.container import Container
from app.core.models.config import configs
from app.infrastructure.schema.entry_schema import EntrySchema
from app.infrastructure.schema.db import db_proxy


@singleton
class AppCreator:
    def __init__(self):
        self.app = FastAPI(
            title=configs.PROJECT_NAME,
            openapi_url=f"{configs.API}/openapi.json",
            docs_url=f"{configs.API}/docs",
            redoc_url=f"{configs.API}/redoc",
            version="0.0.1",
        )

        self.container = Container()

        if configs.BACKEND_CORS_ORIGINS:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(o) for o in configs.BACKEND_CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        @self.app.get("/")
        def root():
            return "service is working"

        self.app.include_router(v1_routers, prefix=configs.API_V1_STR)

        @self.app.on_event("startup")
        def _startup() -> None:
            db = self.container.db()
            db.connect(reuse_if_open=True)
            db_proxy.initialize(db)
            db.create_tables([EntrySchema])

        @self.app.on_event("shutdown")
        def _shutdown() -> None:
            db = self.container.db()
            if not db.is_closed():
                db.close()


app_creator = AppCreator()
app = app_creator.app
container = app_creator.container
