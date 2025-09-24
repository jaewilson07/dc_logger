import re
from typing import Optional

from .client.models import Entity


def extract_entity_from_args(args, kwargs) -> Optional[Entity]:
    """Extract entity information from function arguments"""
    # First, check if any argument is a DomoEntity object
    for arg in args:
        if hasattr(arg, "id") and hasattr(arg, "auth"):
            # This looks like a DomoEntity
            return Entity.from_domo_entity(arg)

    # Check for entity ID parameters in kwargs
    entity_id = None
    entity_type = None

    # Common entity ID parameter patterns
    for param_name in [
        "dataset_id",
        "user_id",
        "group_id",
        "card_id",
        "page_id",
        "dataflow_id",
    ]:
        if param_name in kwargs:
            entity_id = kwargs[param_name]
            entity_type = param_name.replace("_id", "")
            break

    # Try to extract from URL if available
    url = kwargs.get("url", "")
    if not entity_type and url:
        if "/datasets/" in url:
            dataset_match = re.search(r"/datasets/([a-zA-Z0-9\-]+)", url)
            if dataset_match:
                entity_id = dataset_match.group(1)
                entity_type = "dataset"
        elif "/cards/" in url:
            card_match = re.search(r"/cards/([a-zA-Z0-9\-]+)", url)
            if card_match:
                entity_id = card_match.group(1)
                entity_type = "card"
        elif "/users/" in url:
            user_match = re.search(r"/users/([a-zA-Z0-9\-]+)", url)
            if user_match:
                entity_id = user_match.group(1)
                entity_type = "user"
        elif "/pages/" in url:
            page_match = re.search(r"/pages/([a-zA-Z0-9\-]+)", url)
            if page_match:
                entity_id = page_match.group(1)
                entity_type = "page"

    if entity_type and entity_id:
        # Try to get entity name from self object if available
        entity_name = None
        if args and hasattr(args[0], "name"):
            entity_name = getattr(args[0], "name", None)

        return Entity(type=entity_type, id=entity_id, name=entity_name)

    return None
