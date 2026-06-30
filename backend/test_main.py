import os
from datetime import datetime, timedelta, timezone

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from pymongo import AsyncMongoClient

import crud
from database import get_database
from main import app
from schemas import TrainerBase, TrainingSlotBase


TEST_MONGODB_URI = os.getenv(
    "TEST_MONGODB_URI",
    os.getenv("MONGODB_URI", "mongodb://localhost:27017"),
)

TEST_MONGO_DB_NAME = os.getenv(
    "TEST_MONGO_DB_NAME",
    "fitbook_test_db",
)


@pytest_asyncio.fixture
async def test_db():
    """
    Create a clean MongoDB database for every test.
    """

    client = AsyncMongoClient(
        TEST_MONGODB_URI,
        serverSelectionTimeoutMS=5000,
    )

    await client.admin.command("ping")

    await client.drop_database(TEST_MONGO_DB_NAME)

    database = client[TEST_MONGO_DB_NAME]

    await crud.create_indexes(database)

    try:
        yield database
    finally:
        await client.drop_database(TEST_MONGO_DB_NAME)
        await client.close()


@pytest_asyncio.fixture
async def api_client(test_db):
    """
    Override the application's MongoDB dependency with the test database.
    """

    def override_get_database():
        return test_db

    app.dependency_overrides[get_database] = override_get_database

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()


async def insert_trainer(test_db):
    trainer = {
        "name": "Test Trainer",
        "specialization": "Strength Training",
    }

    result = await test_db.trainers.insert_one(trainer)

    trainer["_id"] = result.inserted_id

    return trainer


async def insert_training_slot(test_db, trainer_id):
    slot = {
        "trainer_id": trainer_id,
        "training_date": (
            datetime.now(timezone.utc)
            + timedelta(days=1)
        ),
        "is_available": True,
    }

    result = await test_db.training_slots.insert_one(slot)

    slot["_id"] = result.inserted_id

    return slot


@pytest.mark.asyncio
async def test_health_endpoint(api_client):
    response = await api_client.get("/api/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["database"] == "mongodb"
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_empty_trainers(api_client):
    response = await api_client.get("/api/trainers")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_and_get_trainer(test_db):
    created = await crud.create_trainer(
        test_db,
        TrainerBase(
            name="Ana Petrova",
            specialization="Yoga",
        ),
    )

    assert created["name"] == "Ana Petrova"
    assert created["specialization"] == "Yoga"
    assert isinstance(created["id"], str)

    trainers = await crud.get_trainers(test_db)

    assert len(trainers) == 1
    assert trainers[0]["id"] == created["id"]


@pytest.mark.asyncio
async def test_create_training_slot(test_db):
    trainer = await crud.create_trainer(
        test_db,
        TrainerBase(
            name="Marko Markov",
            specialization="CrossFit",
        ),
    )

    slot = await crud.create_training_slot(
        test_db,
        TrainingSlotBase(
            trainer_id=trainer["id"],
            training_date=(
                datetime.now(timezone.utc)
                + timedelta(days=1)
            ),
            is_available=True,
        ),
    )

    assert slot is not None
    assert isinstance(slot["id"], str)
    assert slot["trainer_id"] == trainer["id"]
    assert slot["is_available"] is True
    assert slot["trainer"]["name"] == "Marko Markov"


@pytest.mark.asyncio
async def test_get_available_slots(api_client, test_db):
    trainer = await insert_trainer(test_db)
    slot = await insert_training_slot(
        test_db,
        trainer["_id"],
    )

    response = await api_client.get(
        "/api/slots/available"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == str(slot["_id"])
    assert data[0]["is_available"] is True
    assert data[0]["trainer"]["name"] == "Test Trainer"


@pytest.mark.asyncio
async def test_successful_booking(api_client, test_db):
    trainer = await insert_trainer(test_db)
    slot = await insert_training_slot(
        test_db,
        trainer["_id"],
    )

    response = await api_client.post(
        "/api/bookings",
        json={
            "client_name": "Nena Test",
            "training_slot_id": str(slot["_id"]),
        },
    )

    assert response.status_code == 201

    booking = response.json()

    assert isinstance(booking["id"], str)
    assert booking["client_name"] == "Nena Test"
    assert booking["training_slot_id"] == str(slot["_id"])
    assert booking["training_slot"]["trainer"]["name"] == (
        "Test Trainer"
    )

    stored_slot = await test_db.training_slots.find_one(
        {"_id": slot["_id"]}
    )

    assert stored_slot["is_available"] is False


@pytest.mark.asyncio
async def test_second_booking_is_rejected(
    api_client,
    test_db,
):
    trainer = await insert_trainer(test_db)
    slot = await insert_training_slot(
        test_db,
        trainer["_id"],
    )

    first_response = await api_client.post(
        "/api/bookings",
        json={
            "client_name": "First Client",
            "training_slot_id": str(slot["_id"]),
        },
    )

    second_response = await api_client.post(
        "/api/bookings",
        json={
            "client_name": "Second Client",
            "training_slot_id": str(slot["_id"]),
        },
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409

    bookings_count = await test_db.bookings.count_documents({})

    assert bookings_count == 1


@pytest.mark.asyncio
async def test_get_bookings(api_client, test_db):
    trainer = await insert_trainer(test_db)
    slot = await insert_training_slot(
        test_db,
        trainer["_id"],
    )

    create_response = await api_client.post(
        "/api/bookings",
        json={
            "client_name": "Booking Client",
            "training_slot_id": str(slot["_id"]),
        },
    )

    assert create_response.status_code == 201

    response = await api_client.get("/api/bookings")

    assert response.status_code == 200

    bookings = response.json()

    assert len(bookings) == 1
    assert bookings[0]["client_name"] == "Booking Client"
    assert bookings[0]["training_slot"]["trainer"]["name"] == (
        "Test Trainer"
    )


@pytest.mark.asyncio
async def test_cancel_booking(api_client, test_db):
    trainer = await insert_trainer(test_db)
    slot = await insert_training_slot(
        test_db,
        trainer["_id"],
    )

    create_response = await api_client.post(
        "/api/bookings",
        json={
            "client_name": "Cancellation Client",
            "training_slot_id": str(slot["_id"]),
        },
    )

    booking_id = create_response.json()["id"]

    delete_response = await api_client.delete(
        f"/api/bookings/{booking_id}"
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["detail"] == (
        "Booking cancelled successfully"
    )

    bookings_count = await test_db.bookings.count_documents({})

    assert bookings_count == 0

    stored_slot = await test_db.training_slots.find_one(
        {"_id": slot["_id"]}
    )

    assert stored_slot["is_available"] is True


@pytest.mark.asyncio
async def test_invalid_booking_id_returns_404(api_client):
    response = await api_client.delete(
        "/api/bookings/not-a-valid-object-id"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Booking not found"


@pytest.mark.asyncio
async def test_missing_slot_booking_returns_409(api_client):
    response = await api_client.post(
        "/api/bookings",
        json={
            "client_name": "Missing Slot Client",
            "training_slot_id": "507f1f77bcf86cd799439011",
        },
    )

    assert response.status_code == 409