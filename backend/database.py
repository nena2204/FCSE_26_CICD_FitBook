from typing import Optional

from pymongo import AsyncMongoClient

from config import MONGODB_URI, MONGO_DB_NAME


mongo_client: Optional[AsyncMongoClient] = None
mongo_database = None


async def connect_to_mongo() -> None:
    """
    Connects the FastAPI application to MongoDB.
    """

    global mongo_client, mongo_database

    mongo_client = AsyncMongoClient(
        MONGODB_URI,
        serverSelectionTimeoutMS=5000,
    )

    # Verify that MongoDB is reachable.
    await mongo_client.admin.command("ping")

    mongo_database = mongo_client[MONGO_DB_NAME]

    print(f"Connected to MongoDB database: {MONGO_DB_NAME}")


async def close_mongo_connection() -> None:
    """
    Closes the MongoDB connection.
    """

    global mongo_client, mongo_database

    if mongo_client is not None:
        await mongo_client.close()

    mongo_client = None
    mongo_database = None

    print("MongoDB connection closed")


def get_database():
    if mongo_database is None:
        raise RuntimeError("MongoDB connection has not been initialized")

    return mongo_database