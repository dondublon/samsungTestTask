from unittest import TestCase

from prepare_db import prepare_db
from sqlite_queue import SQLiteQueue
from types_ import Task, Resources


class TestSQLite(TestCase):
    connection = None
    @classmethod
    def setUpClass(cls) -> None:
        connection = prepare_db()
        cls.connection = connection

    def test_one_task(self):
        queue = SQLiteQueue(self.connection)
        task = Task(None, 10, Resources(32, 3, 4), "content", "")
        queue.add_task(task)
        task_expected = queue.get_task(Resources(32, 3, 4))
        self.assertEqual(task.priority, task_expected.priority)
        self.assertEqual(task.resources, task_expected.resources)
        # self.assertEqual(task.content, task_expected.content)
