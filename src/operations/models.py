from sqlalchemy import Column, Integer, String, TIMESTAMP
from db import Base


class Operation(Base):
    __tablename__ = "operation"

    id = Column(Integer, primary_key=True)
    quantity = Column(String)
    figi = Column(String)
    instrument_type = Column(String, nullable=True)
    date = Column(TIMESTAMP)
    type = Column(String)
