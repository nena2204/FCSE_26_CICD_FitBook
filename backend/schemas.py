from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class FitBookSchema(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )


class TrainerBase(FitBookSchema):
    name: str = Field(min_length=1, max_length=100)
    specialization: str = Field(min_length=1, max_length=100)


class TrainerResponse(TrainerBase):
    id: str


class TrainingSlotBase(FitBookSchema):
    trainer_id: str
    training_date: datetime
    is_available: bool = True


class TrainingSlotResponse(TrainingSlotBase):
    id: str
    trainer: Optional[TrainerResponse] = None


class BookingBase(FitBookSchema):
    client_name: str = Field(min_length=1, max_length=100)
    training_slot_id: str


class BookingResponse(BookingBase):
    id: str
    created_at: datetime
    training_slot: Optional[TrainingSlotResponse] = None