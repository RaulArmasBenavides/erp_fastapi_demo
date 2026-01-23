from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from app.application.services.EntryService import EntryService
from app.core.container import Container
from app.core.interfaces.IEntryService import IEntryService
from app.core.models.entry import EntryModel
from typing import List

router = APIRouter(
    prefix="/entries",
    tags=["entries"],
)
@router.get("/test")
@inject
async def read_root():
    return {"message": "Bienvenido a mi API construida con FastAPI!"}


@router.get("/", response_model=List[EntryModel])
@inject
def get_entries(service: IEntryService = Depends(Provide[Container.entry_service])):
    return service.view_entries()

@router.post("/", response_model=EntryModel)
@inject
def create_entry(
    body: EntryModel,
    service: IEntryService = Depends(Provide[Container.entry_service]),
):
    return service.add_entry(body)

@router.delete("/{entry_id}")
@inject
def delete_entry(
    entry_id: int,
    service: IEntryService = Depends(Provide[Container.entry_service]),
):
    service.delete_entry(entry_id)
    return {"message": "Entry deleted"}