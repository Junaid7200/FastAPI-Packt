from fastapi import FastAPI, HTTPException, status
from typing import Literal

sort_by_type = Literal["asc", "dsc"]

# some dummy data
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




app = FastAPI()

@app.get("/") 
def get_data():
    return {"hello there": "yo yo mate, whats popping. this is the default route"}

@app.get("/getdata")
def getdata():
    return {
        "id": 12705,
        "childName": "Junaid",
        "childHeartRate": 467
    }

@app.get("/getdata/anything")
def getdata_with_query_params(sort_by: str):
    if sort_by not in ("asc", "dsc"):
        raise HTTPException(status_code=400, detail="invalid sort order option selected")
    return {"sort by that was in the query params": sort_by}


@app.get("/getdata/{id}")
def getdata_by_id(id: int):
    # some code to fetch that exact child by id from the database. but since our "db" is just the dict above, we can do this:
    if id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id does not exist"
        )
    return db[id]


