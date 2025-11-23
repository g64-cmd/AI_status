"""
Tests for the business logic in manager.py.
"""
import unittest
# Assuming the project structure allows this import
from ..src import manager
from ..src import models


class TestManager(unittest.TestCase):
    """
    Test suite for the manager module.
    """

    def test_create_entry(self):
        """
        Tests the creation of a new log entry.
        """
        entry = manager.create_entry(
            description="Test bug fix",
            priority="tier1",
            creator="gemini-cli",
            role="engineer"
        )
        
        # Assert basic properties
        self.assertIsNotNone(entry.id)
        self.assertEqual(entry.description, "Test bug fix")
        self.assertEqual(entry.priority, "tier1")
        self.assertEqual(entry.creator, "gemini-cli")
        self.assertEqual(entry.creator_role, "engineer")
        self.assertEqual(entry.status, "pending")
        self.assertIsNotNone(entry.created_timestamp)
        
        # Assert optional fields are None for pending entries
        self.assertIsNone(entry.completer)
        self.assertIsNone(entry.completer_role)
        self.assertIsNone(entry.completion_timestamp)

    def test_complete_entry(self):
        """
        Tests the completion of a log entry.
        """
        # Create sample log entries
        logs = [
            models.LogEntry(
                id="test-id-123",
                creator="user1",
                creator_role="planner",
                created_timestamp=1000,
                description="Fix memory leak",
                priority="tier0",
                status="pending"
            ),
            models.LogEntry(
                id="test-id-456",
                creator="user2",
                creator_role="engineer",
                created_timestamp=2000,
                description="Update docs",
                priority="tier2",
                status="pending"
            )
        ]
        
        # Complete the first entry
        updated_logs = manager.complete_entry(
            log_id="test-id-123",
            completer="claude-code",
            role="engineer",
            logs=logs
        )
        
        # Find the completed entry
        completed = None
        for entry in updated_logs:
            if entry.id == "test-id-123":
                completed = entry
                break
        
        self.assertIsNotNone(completed)
        self.assertEqual(completed.status, "completed")
        self.assertEqual(completed.completer, "claude-code")
        self.assertEqual(completed.completer_role, "engineer")
        self.assertIsNotNone(completed.completion_timestamp)

    def test_complete_nonexistent_entry(self):
        """
        Tests that completing a non-existent entry is handled correctly.
        """
        logs = [
            models.LogEntry(
                id="test-id-123",
                creator="user1",
                creator_role="planner",
                created_timestamp=1000,
                description="Fix memory leak",
                priority="tier0",
                status="pending"
            )
        ]
        
        # Attempt to complete a non-existent entry
        with self.assertRaises(ValueError) as context:
            manager.complete_entry(
                log_id="non-existent-id",
                completer="claude-code",
                role="engineer",
                logs=logs
            )
        
        self.assertIn("not found", str(context.exception).lower())


if __name__ == '__main__':
    unittest.main()
