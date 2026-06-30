"""
Initialize FitBook MongoDB sample data.

Usage:
    python init_sample_data.py
"""

import asyncio
from datetime import datetime, timedelta, timezone

import crud
from database import (
    close_mongo_connection,
    connect_to_mongo,
    get_database,
)


async def init_sample_data() -> None:
    await connect_to_mongo()

    try:
        db = get_database()

        await crud.create_indexes(db)

        existing_trainers = await db.trainers.count_documents({})

        if existing_trainers > 0:
            print(
                "Sample data already exists. "
                "Skipping initialization."
            )
            return

        print("Initializing MongoDB sample data...")

        trainers_data = [
            {
                "name": "John Smith",
                "specialization": "Yoga",
            },
            {
                "name": "Sarah Johnson",
                "specialization": "Pilates",
            },
            {
                "name": "Mike Davis",
                "specialization": "CrossFit",
            },
            {
                "name": "Emma Wilson",
                "specialization": "Boxing",
            },
            {
                "name": "Alex Chen",
                "specialization": "Personal Training",
            },
        ]

        trainer_documents = []

        for trainer_data in trainers_data:
            result = await db.trainers.insert_one(
                trainer_data
            )

            trainer_documents.append(
                {
                    "_id": result.inserted_id,
                    **trainer_data,
                }
            )

            print(
                f"Created trainer: {trainer_data['name']}"
            )

        base_date = (
            datetime.now(timezone.utc)
            + timedelta(days=1)
        ).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        training_slots = []

        for trainer in trainer_documents:
            for day_offset in range(1, 6):
                training_day = (
                    base_date
                    + timedelta(days=day_offset * 2)
                )

                for hour in (9, 14, 18):
                    slot_date = training_day.replace(
                        hour=hour
                    )

                    training_slots.append(
                        {
                            "trainer_id": trainer["_id"],
                            "training_date": slot_date,
                            "is_available": True,
                        }
                    )

        result = await db.training_slots.insert_many(
            training_slots
        )

        print(
            f"Created {len(result.inserted_ids)} "
            "training slots."
        )

        print("MongoDB sample data initialized successfully.")

    finally:
        await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(init_sample_data())