from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pymongo.errors import PyMongoError

import crud
import schemas
from database import (
    close_mongo_connection,
    connect_to_mongo,
    get_database,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Connect to MongoDB when FastAPI starts and close the connection
    when the application stops.
    """

    await connect_to_mongo()

    database = get_database()
    await crud.create_indexes(database)

    try:
        yield
    finally:
        await close_mongo_connection()


app = FastAPI(
    title="FitBook API",
    version="2.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check(db=Depends(get_database)):
    """
    Verify that the backend and MongoDB connection are working.
    """

    try:
        await db.command("ping")

        return {
            "status": "healthy",
            "database": "mongodb",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="MongoDB is unavailable",
        ) from exc


@app.get(
    "/api/trainers",
    response_model=list[schemas.TrainerResponse],
)
async def get_trainers(
    skip: int = 0,
    limit: int = 100,
    db=Depends(get_database),
):
    return await crud.get_trainers(
        db,
        skip=skip,
        limit=limit,
    )


@app.get(
    "/api/slots",
    response_model=list[schemas.TrainingSlotResponse],
)
async def get_slots(
    skip: int = 0,
    limit: int = 100,
    db=Depends(get_database),
):
    return await crud.get_training_slots(
        db,
        skip=skip,
        limit=limit,
    )


@app.get(
    "/api/slots/available",
    response_model=list[schemas.TrainingSlotResponse],
)
async def get_available_slots(db=Depends(get_database)):
    return await crud.get_available_training_slots(db)


@app.post(
    "/api/bookings",
    response_model=schemas.BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_booking(
    booking: schemas.BookingBase,
    db=Depends(get_database),
):
    created_booking = await crud.create_booking(
        db,
        booking,
    )

    if created_booking is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Training slot is unavailable or does not exist",
        )

    return created_booking


@app.get(
    "/api/bookings",
    response_model=list[schemas.BookingResponse],
)
async def get_bookings(
    skip: int = 0,
    limit: int = 100,
    db=Depends(get_database),
):
    return await crud.get_bookings(
        db,
        skip=skip,
        limit=limit,
    )


@app.delete("/api/bookings/{booking_id}")
async def delete_booking(
    booking_id: str,
    db=Depends(get_database),
):
    success = await crud.delete_booking(
        db,
        booking_id,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    return {
        "detail": "Booking cancelled successfully",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )