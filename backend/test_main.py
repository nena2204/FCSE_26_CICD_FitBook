import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

import sys
sys.path.insert(0, '/app/backend')

from main import app, get_db
from database import Base
import crud
import schemas
import models

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_trainers_empty():
    """Test getting trainers when none exist"""
    response = client.get("/api/trainers")
    assert response.status_code == 200
    assert response.json() == []


def test_create_and_get_trainer(db):
    """Test creating and retrieving a trainer"""
    trainer_data = {"name": "John Doe", "specialization": "Yoga"}
    trainer = crud.create_trainer(db, schemas.TrainerBase(**trainer_data))
    
    assert trainer.id is not None
    assert trainer.name == "John Doe"
    assert trainer.specialization == "Yoga"


def test_create_booking_success(db):
    """Test creating a booking successfully"""
    # Create trainer
    trainer = crud.create_trainer(db, schemas.TrainerBase(
        name="Jane Smith",
        specialization="Pilates"
    ))
    
    # Create training slot
    slot_date = datetime.utcnow() + timedelta(days=7)
    slot = crud.create_training_slot(db, schemas.TrainingSlotBase(
        trainer_id=trainer.id,
        training_date=slot_date,
        is_available=True
    ))
    
    # Create booking
    booking = crud.create_booking(db, schemas.BookingBase(
        client_name="Alice",
        training_slot_id=slot.id
    ))
    
    assert booking is not None
    assert booking.client_name == "Alice"
    
    # Check that slot is no longer available
    updated_slot = crud.get_training_slot(db, slot.id)
    assert updated_slot.is_available == False


def test_cancel_booking(db):
    """Test cancelling a booking"""
    # Create trainer and slot
    trainer = crud.create_trainer(db, schemas.TrainerBase(
        name="Bob",
        specialization="CrossFit"
    ))
    
    slot_date = datetime.utcnow() + timedelta(days=1)
    slot = crud.create_training_slot(db, schemas.TrainingSlotBase(
        trainer_id=trainer.id,
        training_date=slot_date,
        is_available=True
    ))
    
    # Create booking
    booking = crud.create_booking(db, schemas.BookingBase(
        client_name="Charlie",
        training_slot_id=slot.id
    ))
    
    # Slot should be unavailable
    assert crud.get_training_slot(db, slot.id).is_available == False
    
    # Cancel booking
    success = crud.delete_booking(db, booking.id)
    assert success == True
    
    # Slot should be available again
    assert crud.get_training_slot(db, slot.id).is_available == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

