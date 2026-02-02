from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any, Optional
from schemas import shipment



app = FastAPI()



db = {
    12701: {
        "weight": 3.5,
        "content": "furniture",
        "status": "in transit"
    },
    12702: {
        "weight": 1.2,
        "content": "books",
        "status": "delivered"
    },
    12703: {
        "weight": 7.8,
        "content": "electronics",
        "status": "pending"
    },
    12704: {
        "weight": 2.0,
        "content": "clothes",
        "status": "in transit"
    },
    12705: {
        "weight": 5.5,
        "content": "appliances",
        "status": "shipped"
    },
    12706: {
        "weight": 0.9,
        "content": "toys",
        "status": "delivered"
    }
}


# default route
@app.get("/shipment")
def get_shipment():
    return db[12701]

@app.post("/shipment")
def submit_shipment(data: dict) -> dict[str, int]:
    content = data["content"]
    weight = data["weight"]
    if weight > 25:
        raise HTTPException(
            status_code=406,
            detail="Maximum weight limit is 25"
        )
    last_shipment_key = max(db.keys())
    db[last_shipment_key+1] = {"weight": weight,
        "content": content,
        }
    return {"id": last_shipment_key+1}


# put removes existing data and replaces it with given data
@app.put("/shipment")
def shipment_put(id: int, content: Optional[str], weight: Optional[float], status: Optional[str]) -> dict[str, Any]:
    db[id] = {
        "content": content,
        "weight": weight,
        "status": status
    }
    return db[id]








# patch is true partial updates
# @app.patch("/shipment")
# def shipment_patch(id: int, content: Optional[str] = None, weight: Optional[float] = None, status: Optional[str] = None) -> dict[str, Any]:
#     shipment = db[id]
#     if content:
#         shipment["content"] = content
#     if weight:
#         shipment["weight"] = weight
#     if status:
#         shipment["status"] = status
#     db[id] = shipment
#     return db[id]





@app.patch("/shipment")
def shipment_patch(id: int, body: shipment) -> dict[str, Any]:
    shipment = db[id]
    shipment.update(body)
    return db[id]


@app.delete("/shipment")
def shipment_delete(id: int):
    db.pop(id)
    return db


# route ordering matters, define static routes before dynamic routes
# documentation route
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return(get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="JJ API Documentation"
    ))

# simple static route
@app.get("/shipment/latest")
def get_latest_shipment():
    return db[max(db.keys())]


# parameterized route
@app.get("/shipment/latest/{x}-{y}")
def get_shipments_in_range(x: int, y: int):
    return list(db.items())[x:y]


# another parameterized route
@app.get("/shipment/{id}")
def get_shipment_by_id(id: int):
    return db[id]


# route accepting optional query params
@app.get("/shipment/first")
def get_shipment_or_first(id : int | None = None):
    
    if (id):
        if id not in db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Given id does not exist"
            )
        return db[id]
    return db[min(db.keys())]

