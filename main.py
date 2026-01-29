from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
app = FastAPI()

@app.get("/")
def get_shipment():
    return {"message": "Shipment service is running."}


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return(get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="JJ API Documentation"
    ))
