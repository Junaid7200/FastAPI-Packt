from contextlib import asynccontextmanager

from fastapi import FastAPI
from rich import panel, print
from scalar_fastapi import get_scalar_api_reference

from api.router import router
from database.session import create_db_tables


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("Server is started", border_style="green"))
    await create_db_tables()
    yield
    print(panel.Panel("Server stopped", border_style="red"))


app = FastAPI(lifespan=lifespan_handler)

app.include_router(router)


# route ordering matters, define static routes before dynamic routes
# documentation route
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url, title="JJ API Documentation"
    )


# default route
# @app.get("/shipment")
# def get_shipment():
#     return db[12701]

# put removes existing data and replaces it with given data
# @app.put("/shipment")
# def shipment_put(id: int, content: Optional[str], weight: Optional[float], status: Optional[str]) -> dict[str, Any]:
#     db[id] = {"content": content, "weight": weight, "status": status}
#     return db[id]


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


# @app.patch("/shipment")
# def shipment_patch(id: int, body: Shipment) -> dict[str, Any]:
#     shipment = db[id]
#     shipment.update(body)
#     return db[id]


# simple static route
# @app.get("/shipment/latest")
# def get_latest_shipment():
#     return db[max(db.keys())]


# parameterized route
# @app.get("/shipment/latest/{x}-{y}")
# def get_shipments_in_range(x: int, y: int):
#     return list(db.items())[x:y]


# another parameterized route
# @app.get("/shipment/{id}")
# def get_shipment_by_id(id: int):
#     return db[id]


# route accepting optional query params
# @app.get("/shipment/first")
# def get_shipment_or_first(id: int | None = None):
#     if id:
#         if id not in db:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Given id does not exist")
#         return db[id]
#     return db[min(db.keys())]
