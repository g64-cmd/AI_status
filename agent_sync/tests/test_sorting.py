"""
Critical tests for the 3-tier sorting logic in manager.py.
"""
import unittest
import time
# Assuming the project structure allows this import
from ..src import manager
from ..src import models


class TestSorting(unittest.TestCase):
    """
    Test suite for the sorting logic.
    """

    def test_sorting_logic(self):
        """
        Tests the 3-tier sorting: Status -> Priority -> Timestamp.
        """
        # Create mixed-up log entries
        logs = [
            models.LogEntry(
                id="1", creator="user1", creator_role="engineer",
                created_timestamp=1000, description="Completed tier2",
                priority="tier2", status="completed",
                completer="user2", completer_role="engineer",
                completion_timestamp=2000
            ),
            models.LogEntry(
                id="2", creator="user1", creator_role="engineer",
                created_timestamp=500, description="Pending tier1 newer",
                priority="tier1", status="pending"
            ),
            models.LogEntry(
                id="3", creator="user1", creator_role="engineer",
                created_timestamp=300, description="Pending tier0",
                priority="tier0", status="pending"
            ),
            models.LogEntry(
                id="4", creator="user1", creator_role="engineer",
                created_timestamp=200, description="Pending tier1 older",
                priority="tier1", status="pending"
            ),
            models.LogEntry(
                id="5", creator="user1", creator_role="engineer",
                created_timestamp=100, description="Completed tier0",
                priority="tier0", status="completed",
                completer="user2", completer_role="engineer",
                completion_timestamp=1500
            ),
        ]
        
        sorted_logs = manager.sort_logs(logs)
        
        # Expected order: pending tier0, pending tier1 (older), pending tier1 (newer),
        # completed tier0, completed tier2
        self.assertEqual(sorted_logs[0].id, "3")  # pending tier0
        self.assertEqual(sorted_logs[1].id, "4")  # pending tier1 (timestamp 200)
        self.assertEqual(sorted_logs[2].id, "2")  # pending tier1 (timestamp 500)
        self.assertEqual(sorted_logs[3].id, "5")  # completed tier0
        self.assertEqual(sorted_logs[4].id, "1")  # completed tier2

    def test_sort_pending_only(self):
        """
        Tests sorting when all entries are pending.
        """
        logs = [
            models.LogEntry(
                id="1", creator="user1", creator_role="engineer",
                created_timestamp=300, description="tier2",
                priority="tier2", status="pending"
            ),
            models.LogEntry(
                id="2", creator="user1", creator_role="engineer",
                created_timestamp=100, description="tier0",
                priority="tier0", status="pending"
            ),
            models.LogEntry(
                id="3", creator="user1", creator_role="engineer",
                created_timestamp=200, description="tier1",
                priority="tier1", status="pending"
            ),
        ]
        
        sorted_logs = manager.sort_logs(logs)
        
        # All pending, sorted by priority then timestamp
        self.assertEqual(sorted_logs[0].id, "2")  # tier0
        self.assertEqual(sorted_logs[1].id, "3")  # tier1
        self.assertEqual(sorted_logs[2].id, "1")  # tier2

    def test_sort_completed_only(self):
        """
        Tests sorting when all entries are completed.
        """
        logs = [
            models.LogEntry(
                id="1", creator="user1", creator_role="engineer",
                created_timestamp=300, description="tier2",
                priority="tier2", status="completed",
                completer="user2", completer_role="engineer",
                completion_timestamp=1000
            ),
            models.LogEntry(
                id="2", creator="user1", creator_role="engineer",
                created_timestamp=100, description="tier0",
                priority="tier0", status="completed",
                completer="user2", completer_role="engineer",
                completion_timestamp=1000
            ),
            models.LogEntry(
                id="3", creator="user1", creator_role="engineer",
                created_timestamp=200, description="tier1",
                priority="tier1", status="completed",
                completer="user2", completer_role="engineer",
                completion_timestamp=1000
            ),
        ]
        
        sorted_logs = manager.sort_logs(logs)
        
        # All completed, sorted by priority then timestamp
        self.assertEqual(sorted_logs[0].id, "2")  # tier0
        self.assertEqual(sorted_logs[1].id, "3")  # tier1
        self.assertEqual(sorted_logs[2].id, "1")  # tier2


if __name__ == '__main__':
    unittest.main()
