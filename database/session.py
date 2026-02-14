from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

engine = create_engine(
    url="sqlite:///shipmentdb.db",
    echo=True,
    connect_args={"check_same_thread": False}
)


def create_db_tables():
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    with Session(bind=engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# session = Session(bind=engine)
# session.get(
#     Shipment, 1
# )

# session.commit()
