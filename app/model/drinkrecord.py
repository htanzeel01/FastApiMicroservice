# app/models/drinkrecord.py
import uuid

from pydantic import BaseModel, Field, validator
from uuid import uuid4, UUID
from datetime import datetime, date
from typing import Optional
import uuid

class DrinkRecord(BaseModel):
    Id: str = Field(default_factory=lambda: str(uuid4()), alias="id")
    patient_id: str
    amount_ml: float
    date = date.today()


    @validator('amount_ml')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('amount_ml must be a positive number')
        return v

        # Validator to ensure the date field gets formatted correctly as a string
        @validator("date", pre=True, always=True)
        def format_date(cls, v):
            if isinstance(v, date):
                return v.isoformat()  # Convert date to "YYYY-MM-DD"
            return v

        class Config:
            # Pydantic configuration to serialize date objects as strings
            json_encoders = {
                date: lambda v: v.isoformat(),  # Ensures date is serialized as string
            }
            orm_mode = True


