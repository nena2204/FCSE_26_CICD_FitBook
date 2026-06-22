from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
import crud
import schemas
from datetime import datetime

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FitBook API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.get("/api/trainers", response_model=list[schemas.TrainerResponse])
def get_trainers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all trainers"""
    trainers = crud.get_trainers(db, skip=skip, limit=limit)
    return trainers


@app.get("/api/slots", response_model=list[schemas.TrainingSlotResponse])
def get_slots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all training slots"""
    slots = crud.get_training_slots(db, skip=skip, limit=limit)
    return slots


@app.get("/api/slots/available", response_model=list[schemas.TrainingSlotResponse])
def get_available_slots(db: Session = Depends(get_db)):
    """Get available training slots"""
    slots = crud.get_available_training_slots(db)
    return slots


@app.post("/api/bookings", response_model=schemas.BookingResponse)
def create_booking(booking: schemas.BookingBase, db: Session = Depends(get_db)):
    """Create a new booking"""
    db_booking = crud.create_booking(db, booking)
    if not db_booking:
        raise HTTPException(
            status_code=400,
            detail="Training slot is not available or does not exist"
        )
    return db_booking


@app.get("/api/bookings", response_model=list[schemas.BookingResponse])
def get_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all bookings"""
    bookings = crud.get_bookings(db, skip=skip, limit=limit)
    return bookings


@app.delete("/api/bookings/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    """Cancel a booking"""
    success = crud.delete_booking(db, booking_id)
    if not success:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"detail": "Booking cancelled successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

