from typing import Any, Dict, Optional


def serialize_trainer(document: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Convert a MongoDB trainer document into an API response."""

    if document is None:
        return None

    return {
        "id": str(document["_id"]),
        "name": document["name"],
        "specialization": document["specialization"],
    }


def serialize_training_slot(
    document: Optional[Dict[str, Any]],
    trainer: Optional[Dict[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    """Convert a MongoDB training-slot document into an API response."""

    if document is None:
        return None

    return {
        "id": str(document["_id"]),
        "trainer_id": str(document["trainer_id"]),
        "training_date": document["training_date"],
        "is_available": document.get("is_available", True),
        "trainer": serialize_trainer(trainer),
    }


def serialize_booking(
    document: Optional[Dict[str, Any]],
    training_slot: Optional[Dict[str, Any]] = None,
    trainer: Optional[Dict[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    """Convert a MongoDB booking document into an API response."""

    if document is None:
        return None

    return {
        "id": str(document["_id"]),
        "client_name": document["client_name"],
        "training_slot_id": str(document["training_slot_id"]),
        "created_at": document["created_at"],
        "training_slot": serialize_training_slot(training_slot, trainer),
    }