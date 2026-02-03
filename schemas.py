from pydantic import BaseModel, Field
from enum import Enum


class ShipmentStatus(str, Enum):
    placed= "placed"
    in_transit="in_transit"
    delivered="delivered"

class shipment(BaseModel):
    content: str = Field(description="this field will describe the contents of the shipment in string", max_length=100)
    weight: float = Field(lt=25, ge=1)
    status: ShipmentStatus
    destination: int | None = Field(default=None)