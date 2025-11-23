"""
Contains the core business logic, including CRUD operations and sorting.
"""
import uuid
import time
from typing import List
from .models import LogEntry, PRIORITY_MAP


def create_entry(description: str, priority: str, creator: str, role: str) -> LogEntry:
    """
    Generates a new LogEntry with a UUID, current timestamp, and 'pending' status.

    Args:
        description: The description of the log entry.
        priority: The priority tier of the entry.
        creator: The name of the person or agent creating the entry.
        role: The role of the creator.

    Returns:
        The newly created LogEntry object.
    """
    # Validate priority against the allowed keys in PRIORITY_MAP
    if priority not in PRIORITY_MAP:
        raise ValueError(f"Invalid priority: {priority}. Must be one of {list(PRIORITY_MAP.keys())}")
    
    return LogEntry(
        id=str(uuid.uuid4()),  # Generate a unique ID
        creator=creator,
        creator_role=role,
        created_timestamp=int(time.time()),  # Use Unix timestamp for easy sorting
        description=description,
        priority=priority,
        status='pending'
    )


def complete_entry(log_id: str, completer: str, role: str, logs: List[LogEntry]) -> List[LogEntry]:
    """
    Finds an entry by ID, updates its status to 'completed', and records
    completion details.

    Args:
        log_id: The ID of the log entry to complete.
        completer: The name of the person or agent completing the entry.
        role: The role of the completer.
        logs: The list of all log entries.

    Returns:
        The updated list of log entries.
    """
    # Find the entry by ID
    found = False
    for entry in logs:
        if entry.id == log_id:
            entry.status = 'completed'
            entry.completer = completer
            entry.completer_role = role
            entry.completion_timestamp = int(time.time())
            found = True
            break
    
    if not found:
        raise ValueError(f"Log entry with ID '{log_id}' not found")
    
    return logs


def sort_logs(logs: List[LogEntry]) -> List[LogEntry]:
    """
    Implements the 3-tier sorting logic on a list of log entries.
    Sorts by:
    1. Status (Pending first)
    2. Priority (Tier0 first)
    3. Creation time (Oldest first)

    Args:
        logs: The list of LogEntry objects to sort.

    Returns:
        The sorted list of LogEntry objects.
    """
    # The sorting key is a tuple, which Python compares element by element.
    return sorted(logs, key=lambda x: (
        0 if x.status == 'pending' else 1,  # Primary sort: Pending (0) before Completed (1)
        PRIORITY_MAP[x.priority],           # Secondary sort: Priority value (0=tier0, 3=tier3)
        x.created_timestamp                 # Tertiary sort: Creation time (ascending/oldest first)
    ))
