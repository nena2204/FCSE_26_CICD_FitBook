from datetime import datetime, timezone
from typing import Optional, Union

from bson import ObjectId
from pymongo import ASCENDING, DESCENDING, ReturnDocument
from pymongo.errors import DuplicateKeyError

from models import (
    serialize_booking,
    serialize_trainer,
    serialize_training_slot,
)
from schemas import BookingBase, TrainerBase, TrainingSlotBase


class SlotUnavailableError(Exception):
    """Raised when a training slot cannot be booked."""


def to_object_id(value: Union[str, ObjectId]) -> Optional[ObjectId]:
    """Safely convert a string into a MongoDB ObjectId."""

    if isinstance(value, ObjectId):
        return value

    if not ObjectId.is_valid(value):
        return None

    return ObjectId(value)


async def create_indexes(db) -> None:
    """Create MongoDB indexes if they do not already exist."""

    await db.trainers.create_index(
        [("name", ASCENDING)],
        name="idx_trainers_name",
    )

    await db.training_slots.create_index(
        [("trainer_id", ASCENDING)],
        name="idx_slots_trainer_id",
    )

    await db.training_slots.create_index(
        [("training_date", ASCENDING)],
        name="idx_slots_training_date",
    )

    await db.training_slots.create_index(
        [("is_available", ASCENDING)],
        name="idx_slots_available",
    )

    await db.bookings.create_index(
        [("training_slot_id", ASCENDING)],
        unique=True,
        name="idx_bookings_unique_slot",
    )

    await db.bookings.create_index(
        [("client_name", ASCENDING)],
        name="idx_bookings_client_name",
    )


# -------------------------------------------------------------------
# Trainer operations
# -------------------------------------------------------------------

async def get_trainers(db, skip: int = 0, limit: int = 100):
    cursor = (
        db.trainers
        .find({})
        .sort("name", ASCENDING)
        .skip(skip)
        .limit(limit)
    )

    documents = await cursor.to_list(length=limit)

    return [serialize_trainer(document) for document in documents]


async def get_trainer(db, trainer_id: str):
    object_id = to_object_id(trainer_id)

    if object_id is None:
        return None

    document = await db.trainers.find_one({"_id": object_id})

    return serialize_trainer(document)


async def create_trainer(db, trainer: TrainerBase):
    document = trainer.model_dump()

    result = await db.trainers.insert_one(document)
    document["_id"] = result.inserted_id

    return serialize_trainer(document)


# -------------------------------------------------------------------
# Training-slot operations
# -------------------------------------------------------------------

async def build_training_slot_response(db, document):
    if document is None:
        return None

    trainer = await db.trainers.find_one(
        {"_id": document["trainer_id"]}
    )

    return serialize_training_slot(document, trainer)


async def get_training_slots(db, skip: int = 0, limit: int = 100):
    cursor = (
        db.training_slots
        .find({})
        .sort("training_date", ASCENDING)
        .skip(skip)
        .limit(limit)
    )

    documents = await cursor.to_list(length=limit)

    return [
        await build_training_slot_response(db, document)
        for document in documents
    ]


async def get_available_training_slots(db):
    cursor = (
        db.training_slots
        .find({"is_available": True})
        .sort("training_date", ASCENDING)
    )

    documents = await cursor.to_list(length=None)

    return [
        await build_training_slot_response(db, document)
        for document in documents
    ]


async def get_training_slot(db, slot_id: str):
    object_id = to_object_id(slot_id)

    if object_id is None:
        return None

    document = await db.training_slots.find_one({"_id": object_id})

    return await build_training_slot_response(db, document)


async def create_training_slot(db, slot: TrainingSlotBase):
    trainer_id = to_object_id(slot.trainer_id)

    if trainer_id is None:
        return None

    trainer = await db.trainers.find_one({"_id": trainer_id})

    if trainer is None:
        return None

    document = slot.model_dump()
    document["trainer_id"] = trainer_id

    result = await db.training_slots.insert_one(document)
    document["_id"] = result.inserted_id

    return serialize_training_slot(document, trainer)


async def update_slot_availability(
    db,
    slot_id: str,
    is_available: bool,
):
    object_id = to_object_id(slot_id)

    if object_id is None:
        return None

    document = await db.training_slots.find_one_and_update(
        {"_id": object_id},
        {"$set": {"is_available": is_available}},
        return_document=ReturnDocument.AFTER,
    )

    return await build_training_slot_response(db, document)


# -------------------------------------------------------------------
# Booking operations
# -------------------------------------------------------------------

async def build_booking_response(db, document):
    if document is None:
        return None

    training_slot = await db.training_slots.find_one(
        {"_id": document["training_slot_id"]}
    )

    trainer = None

    if training_slot is not None:
        trainer = await db.trainers.find_one(
            {"_id": training_slot["trainer_id"]}
        )

    return serialize_booking(
        document=document,
        training_slot=training_slot,
        trainer=trainer,
    )


async def get_bookings(db, skip: int = 0, limit: int = 100):
    cursor = (
        db.bookings
        .find({})
        .sort("created_at", DESCENDING)
        .skip(skip)
        .limit(limit)
    )

    documents = await cursor.to_list(length=limit)

    return [
        await build_booking_response(db, document)
        for document in documents
    ]


async def get_booking(db, booking_id: str):
    object_id = to_object_id(booking_id)

    if object_id is None:
        return None

    document = await db.bookings.find_one({"_id": object_id})

    return await build_booking_response(db, document)


async def create_booking(db, booking: BookingBase):
    slot_id = to_object_id(booking.training_slot_id)

    if slot_id is None:
        return None

    booking_document = {
        "_id": ObjectId(),
        "client_name": booking.client_name,
        "training_slot_id": slot_id,
        "created_at": datetime.now(timezone.utc),
    }

    async def booking_transaction(session):
        slot = await db.training_slots.find_one_and_update(
            {
                "_id": slot_id,
                "is_available": True,
            },
            {
                "$set": {
                    "is_available": False,
                }
            },
            return_document=ReturnDocument.AFTER,
            session=session,
        )

        if slot is None:
            raise SlotUnavailableError()

        await db.bookings.insert_one(
            booking_document,
            session=session,
        )

    try:
        async with db.client.start_session() as session:
            await session.with_transaction(booking_transaction)

    except (SlotUnavailableError, DuplicateKeyError):
        return None

    return await get_booking(
        db,
        str(booking_document["_id"]),
    )


async def delete_booking(db, booking_id: str) -> bool:
    object_id = to_object_id(booking_id)

    if object_id is None:
        return False

    async def cancellation_transaction(session):
        booking = await db.bookings.find_one(
            {"_id": object_id},
            session=session,
        )

        if booking is None:
            return False

        await db.bookings.delete_one(
            {"_id": object_id},
            session=session,
        )

        await db.training_slots.update_one(
            {"_id": booking["training_slot_id"]},
            {
                "$set": {
                    "is_available": True,
                }
            },
            session=session,
        )

        return True

    async with db.client.start_session() as session:
        deleted = await session.with_transaction(
            cancellation_transaction
        )

    return bool(deleted)