from sqlalchemy.orm import Session
from models import Trainer, TrainingSlot, Booking
from schemas import TrainerBase, TrainingSlotBase, BookingBase
from datetime import datetime


# Trainer operations
def get_trainers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Trainer).offset(skip).limit(limit).all()


def get_trainer(db: Session, trainer_id: int):
    return db.query(Trainer).filter(Trainer.id == trainer_id).first()


def create_trainer(db: Session, trainer: TrainerBase):
    db_trainer = Trainer(**trainer.dict())
    db.add(db_trainer)
    db.commit()
    db.refresh(db_trainer)
    return db_trainer


# Training slots operations
def get_training_slots(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TrainingSlot).offset(skip).limit(limit).all()


def get_available_training_slots(db: Session):
    return db.query(TrainingSlot).filter(TrainingSlot.is_available == True).all()


def get_training_slot(db: Session, slot_id: int):
    return db.query(TrainingSlot).filter(TrainingSlot.id == slot_id).first()


def create_training_slot(db: Session, slot: TrainingSlotBase):
    db_slot = TrainingSlot(**slot.dict())
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot


def update_slot_availability(db: Session, slot_id: int, is_available: bool):
    slot = get_training_slot(db, slot_id)
    if slot:
        slot.is_available = is_available
        db.commit()
        db.refresh(slot)
    return slot


# Booking operations
def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Booking).offset(skip).limit(limit).all()


def get_booking(db: Session, booking_id: int):
    return db.query(Booking).filter(Booking.id == booking_id).first()


def create_booking(db: Session, booking: BookingBase):
    # Get the training slot
    slot = get_training_slot(db, booking.training_slot_id)
    if not slot or not slot.is_available:
        return None
    
    # Create booking
    db_booking = Booking(**booking.dict())
    db.add(db_booking)
    
    # Mark slot as unavailable
    update_slot_availability(db, booking.training_slot_id, False)
    
    db.commit()
    db.refresh(db_booking)
    return db_booking


def delete_booking(db: Session, booking_id: int):
    booking = get_booking(db, booking_id)
    if booking:
        # Make the slot available again
        update_slot_availability(db, booking.training_slot_id, True)
        
        db.delete(booking)
        db.commit()
        return True
    return False

