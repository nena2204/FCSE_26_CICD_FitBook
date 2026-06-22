from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class TrainerBase(BaseModel):
    name: str
    specialization: str


class TrainerResponse(TrainerBase):
    id: int

    class Config:
        from_attributes = True


class TrainingSlotBase(BaseModel):
    trainer_id: int
    training_date: datetime
    is_available: bool = True


class TrainingSlotResponse(TrainingSlotBase):
    id: int
    trainer: Optional[TrainerResponse] = None

    class Config:
        from_attributes = True


class BookingBase(BaseModel):
    client_name: str
    training_slot_id: int


class BookingResponse(BookingBase):
    id: int
    created_at: datetime
    training_slot: Optional[TrainingSlotResponse] = None

    class Config:
        from_attributes = True

