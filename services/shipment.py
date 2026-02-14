from fastapi import HTTPException
from api.schemas.shipment import ShipmentCreate, ShipmentUpdateModel
from database.models import Shipment
from sqlalchemy.ext.asyncio import AsyncSession


class ShipmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Shipment:
        shipment = await self.session.get(Shipment, id)
        if shipment is None:
            raise HTTPException(
                status_code=404,
                detail=f"The record for the given id {id} does not exist",
            )
        return shipment

    async def add(self, shipment_create: ShipmentCreate) -> Shipment:
        new_shipment = Shipment(**shipment_create.model_dump())
        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)
        return new_shipment

    async def update(self, id: int, shipment_update: ShipmentUpdateModel) -> Shipment:
        shipment = await self.get(id)
        if shipment is None:
            raise HTTPException(
                status_code=404, detail="Could not find the record you want to UDPATE"
            )
        shipment.sqlmodel_update(shipment_update.model_dump(exclude_none=True))
        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)
        return shipment

    async def delete(self, id: int) -> None:
        await self.session.delete(await self.get(id))
        await self.session.commit()
