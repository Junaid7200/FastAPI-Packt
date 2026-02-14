from datetime import datetime

from pydantic import BaseModel, Field

from database.models import ShipmentStatus


class ShipmentCreate(BaseModel):
    content: str = Field(max_length=100, description="Describes shipment content")
    weight: float = Field(gt=1, le=25)
    destination: int
    status: ShipmentStatus = ShipmentStatus.placed
    estimated_delivery: datetime = Field(default=datetime.now())


class ShipmentUpdateModel(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime = Field(default_factory=datetime.now)


class ShipmentRead(BaseModel):
    id: int
    content: str
    weight: float
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime
