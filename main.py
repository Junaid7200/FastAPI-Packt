from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
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
@app.get("/")
def get_shipment():
    return {"message": "Shipment service is running."}


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
@app.get("/{id}")
def get_shipment_by_id(id: int):
    return {"message": f"Shipment service is running for the id: {id}."}


# route accepting optional query params
@app.get("/shipment/first")
def get_shipment_or_first(id : int | None = None):
    
    if (id):
        if id not in db:
            return {"Error": "Wrong Id"}
        return db[id]
    return db[min(db.keys())]
