from pydantic import BaseModel, Field
from enum import Enum


class ShipmentStatus(str, Enum):
    placed= "placed"
    in_transit="in_transit"
    delivered="delivered"

class Shipment(BaseModel):
    content: str = Field(description="this field will describe the contents of the shipment in string", max_length=100)
    weight: float = Field(lt=25, ge=1)
    status: ShipmentStatus = Field(default=ShipmentStatus.placed)
    # destination: int | None = Field(default=None)

class ShipmentUpdateModel(BaseModel):
    status: ShipmentStatus = Field(default=ShipmentStatus.placed)