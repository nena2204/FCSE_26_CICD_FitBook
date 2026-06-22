"""
FitBook Database Sample Data Initialization

This script can be run to populate the database with sample data for testing.
Usage: python init_sample_data.py
"""

from datetime import datetime, timedelta
from database import SessionLocal, engine, Base
import models
import crud
import schemas

# Create tables
Base.metadata.create_all(bind=engine)

def init_sample_data():
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_trainers = db.query(models.Trainer).count()
        if existing_trainers > 0:
            print("Sample data already exists. Skipping initialization.")
            return
        
        print("Initializing sample data...")
        
        # Create trainers
        trainers_data = [
            {"name": "John Smith", "specialization": "Yoga"},
            {"name": "Sarah Johnson", "specialization": "Pilates"},
            {"name": "Mike Davis", "specialization": "CrossFit"},
            {"name": "Emma Wilson", "specialization": "Boxing"},
            {"name": "Alex Chen", "specialization": "Personal Training"},
        ]
        
        trainers = []
        for trainer_data in trainers_data:
            trainer = crud.create_trainer(db, schemas.TrainerBase(**trainer_data))
            trainers.append(trainer)
            print(f"✓ Created trainer: {trainer.name}")
        
        # Create training slots
        base_date = datetime.utcnow() + timedelta(days=1)
        
        for i, trainer in enumerate(trainers):
            # Each trainer has 5 slots over the next 2 weeks
            for day_offset in range(1, 6):
                for hour in [9, 14, 18]:
                    slot_date = base_date + timedelta(days=day_offset * 2, hours=hour)
                    slot = crud.create_training_slot(
                        db,
                        schemas.TrainingSlotBase(
                            trainer_id=trainer.id,
                            training_date=slot_date,
                            is_available=True
                        )
                    )
                    print(f"✓ Created slot for {trainer.name} at {slot_date}")
        
        print("\n" + "="*50)
        print("Sample data initialization complete!")
        print("="*50)
        print(f"Created {len(trainers)} trainers")
        print("Created multiple training slots")
        print("\nYou can now:")
        print("1. Access the API at http://localhost:8000/api/docs")
        print("2. View trainers: GET /api/trainers")
        print("3. View slots: GET /api/slots/available")
        print("4. Create booking: POST /api/bookings")
        
    except Exception as e:
        print(f"❌ Error initializing data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_sample_data()

