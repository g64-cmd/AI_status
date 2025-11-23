"""
Defines the data structures and type validation.
"""
import dataclasses
from typing import Optional

# Defines the priority mapping for sorting.
# Lower values indicate higher priority.
# This mapping is critical for the 3-tier sorting logic.
PRIORITY_MAP = {
    "tier0": 0,  # Critical - Must be addressed immediately
    "tier1": 1,  # Bug - Should be fixed soon
    "tier2": 2,  # TODO - Planned work
    "tier3": 3,  # Weak Warning - Low priority/Nice to have
}


@dataclasses.dataclass
class LogEntry:
    """
    A Dataclass representing a single row in the log.
    
    Attributes:
        id (str): Unique UUID for the entry.
        creator (str): Name of the user/agent who created the entry.
        creator_role (str): Role of the creator (planner, engineer, user).
        created_timestamp (int): Unix timestamp of creation.
        description (str): Text description of the task.
        priority (str): Priority tier (tier0-tier3).
        status (str): Current status ('pending' or 'completed').
        completer (Optional[str]): Name of user/agent who completed the task.
        completer_role (Optional[str]): Role of the completer.
        completion_timestamp (Optional[int]): Unix timestamp of completion.
    """
    id: str
    creator: str
    creator_role: str
    created_timestamp: int
    description: str
    priority: str
    status: str
    completer: Optional[str] = None
    completer_role: Optional[str] = None
    completion_timestamp: Optional[int] = None


def to_dict(entry: LogEntry) -> dict:
    """
    Serializes the LogEntry object for JSON storage.

    Args:
        entry: The LogEntry object to serialize.

    Returns:
        A dictionary representation of the LogEntry.
    """
    return dataclasses.asdict(entry)


def from_dict(data: dict) -> LogEntry:
    """
    Deserializes JSON data into a strictly typed LogEntry object.
    Handles missing optional fields.

    Args:
        data: The dictionary to deserialize.

    Returns:
        A LogEntry object.
    """
    return LogEntry(**data)
