"""Holds the user-buy data model """
import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class UserBuyModel(BaseModel):
    '''Defining the user-buy data model'''
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    username: str = Field(...)
    userid: str = Field(...)
    price: int = Field(...)
    timestamp: datetime = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

    class Config:
        '''Additional configuration and documentation for the model'''
        # Allows creating instances from dictionaries
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "exampleID",
                "username": "exampleUser",
                "userid": "exampleuserid",
                "price": 15,
                "timestamp": "2023-07-29T15:46:58.123456Z"
            }
        }
