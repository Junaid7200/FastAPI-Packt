from pydantic import BaseModel, Field


class shipment(BaseModel):
    content: str = Field(description="this field will describe the contents of the shipment in string", max_length=100)
    weight: float = Field(lt=25, ge=1)
    status: str
    destination: int | None = Field(default=None)