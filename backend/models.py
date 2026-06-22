from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Trainer(Base):
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    specialization = Column(String)

    training_slots = relationship("TrainingSlot", back_populates="trainer")


class TrainingSlot(Base):
    __tablename__ = "training_slots"

    id = Column(Integer, primary_key=True, index=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"))
    training_date = Column(DateTime, index=True)
    is_available = Column(Boolean, default=True)

    trainer = relationship("Trainer", back_populates="training_slots")
    bookings = relationship("Booking", back_populates="training_slot")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, index=True)
    training_slot_id = Column(Integer, ForeignKey("training_slots.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    training_slot = relationship("TrainingSlot", back_populates="bookings")

