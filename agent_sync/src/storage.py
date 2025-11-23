"""
Handles reading from and writing to the status_log.json file.
"""
import json
import os
import tempfile
from typing import List
from .models import LogEntry


def load_logs(filepath: str) -> List[dict]:
    """
    Reads the JSON file. If the file doesn't exist, returns an empty list.

    Args:
        filepath: The path to the JSON file.

    Returns:
        A list of log entries as dictionaries.
    """
    if not os.path.exists(filepath):
        return []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_logs(filepath: str, logs: List[dict]) -> None:
    """
    Atomic write operation. Writes to a temporary file and renames it
    to prevent data corruption.

    This ensures that if the program crashes during writing, the original
    file remains intact.

    Args:
        filepath: The path to the destination JSON file.
        logs: A list of log entries as dictionaries to save.
    """
    # Get directory of target file
    directory = os.path.dirname(filepath) or '.'
    
    # Create temp file in same directory for atomic rename
    # We use mkstemp to ensure a unique filename
    fd, temp_path = tempfile.mkstemp(dir=directory, suffix='.json.tmp')
    
    try:
        # Write to temp file first
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        
        # Atomic rename: This operation is atomic on POSIX and Windows (Python 3.3+)
        # It replaces the target file with the temp file in one go.
        os.replace(temp_path, filepath)
    except Exception:
        # Clean up temp file on error to avoid clutter
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise
