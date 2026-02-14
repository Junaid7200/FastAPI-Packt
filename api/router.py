from fastapi import APIRouter
from rich import print

from api.dependencies import ServiceDep
from api.schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdateModel

router = APIRouter(prefix="/shipment", tags=["Shipment"])


@router.get("/{id}", response_model=ShipmentRead)
async def get_shipment(id: int, service: ServiceDep):
    print("GET query executed")
    result = await service.get(id)
    return result


@router.post("/", response_model=ShipmentRead, status_code=201)
async def submit_shipment(data: ShipmentCreate, service: ServiceDep):
    print("CREATE query executed")
    new_shipment = await service.add(data)
    print(f"New record created with the id: {new_shipment.id}")
    return new_shipment


@router.patch("/{id}", response_model=ShipmentRead)
async def patch_shipment(
    id: int, shipment_update: ShipmentUpdateModel, service: ServiceDep
):
    shipment = await service.update(id, shipment_update)
    return shipment


@router.delete("/{id}")
async def shipment_delete(id: int, service: ServiceDep):
    await service.delete(id)
    return {"deleted": True, "id": id}
