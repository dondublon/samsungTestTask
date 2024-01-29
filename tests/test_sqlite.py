from unittest import TestCase

from src.sqlite_queue.prepare_db import prepare_db
from src.sqlite_queue.sqlite_queue import SQLiteQueue
from src.types_ import Task, Resources


class TestSQLite(TestCase):
    connection = None

    @classmethod
    def setUpClass(cls) -> None:
        connection = prepare_db()
        cls.connection = connection

    def test_empty(self):
        queue = SQLiteQueue(self.connection)
        task = queue.get_task(Resources(32, 3, 4))
        self.assertIsNone(task)

    def test_one_task(self):
        queue = SQLiteQueue(self.connection)
        task = Task(None, 10, Resources(32, 3, 4), "content", "")
        queue.add_task(task)
        task_expected = queue.get_task(Resources(32, 3, 4))
        self.assertEqual(task.priority, task_expected.priority)
        self.assertEqual(task.resources, task_expected.resources)
        self.assertEqual(task.content, task_expected.content)
        queue.clear()

    def test_no_resources(self):
        queue = SQLiteQueue(self.connection)
        tasks = [Task(None, 10, Resources(32, 3, 4), "content", ""),
                 Task(None, 11, Resources(32, 3, 4), "content", ""),
                 Task(None, 12, Resources(32, 3, 4), "content", "")]
        for task in tasks:
            queue.add_task(task)
        task_expected = queue.get_task(Resources(31, 3, 4))
        self.assertIsNone(task_expected)
        queue.clear()

    def test_resources_lower(self):
        queue = SQLiteQueue(self.connection)
        tasks = [Task(None, 10, Resources(30, 3, 4), "content", ""),
                 Task(None, 11, Resources(32, 3, 4), "content", ""),
                 Task(None, 12, Resources(32, 3, 4), "content", ""),
                 Task(None, 11, Resources(32, 3, 4), "content", "")]
        for task in tasks:
            queue.add_task(task)
        task_expected = queue.get_task(Resources(32, 3, 4))
        self.assertIsNotNone(task_expected)
        self.assertEqual(12, task_expected.priority)
        queue.clear()

    def test_some_resources_out(self):
        queue = SQLiteQueue(self.connection)
        tasks = [Task(None, 10, Resources(30, 3, 4), "content1", ""),
                 Task(None, 11, Resources(30, 3, 4), "content2", ""),
                 Task(None, 11, Resources(32, 3, 4), "content3", ""),
                 Task(None, 12, Resources(32, 3, 4), "content4", ""),
                 Task(None, 11, Resources(32, 3, 4), "content5", "")]
        for task in tasks:
            queue.add_task(task)
        task_expected = queue.get_task(Resources(30, 3, 4))
        self.assertIsNotNone(task_expected)
        self.assertEqual(11, task_expected.priority)
        self.assertEqual(Resources(30, 3, 4), task_expected.resources)
        self.assertEqual("content2", task_expected.content)
        queue.clear()

    def test_some_resources_out_several_tasks(self):
        queue = SQLiteQueue(self.connection)
        tasks = [Task(None, 10, Resources(30, 3, 4), "content1", ""),
                 Task(None, 11, Resources(30, 3, 4), "content2", ""),
                 Task(None, 11, Resources(32, 3, 4), "content3", ""),
                 Task(None, 12, Resources(32, 3, 4), "content4", ""),
                 Task(None, 11, Resources(32, 3, 4), "content5", ""),
                 Task(None, 10, Resources(30, 2, 4), "content6", ""),
                 Task(None, 11, Resources(30, 4, 2), "content7", ""),
                 Task(None, 11, Resources(32, 3, 4), "content8", ""),
                 Task(None, 12, Resources(32, 3, 4), "content9", ""),
                 Task(None, 11, Resources(32, 3, 4), "content10", "")
                 ]
        for task in tasks:
            queue.add_task(task)
        task_expected = queue.get_task(Resources(30, 3, 4))
        self.assertIsNotNone(task_expected)
        self.assertEqual(11, task_expected.priority)
        self.assertEqual(Resources(30, 3, 4), task_expected.resources)
        self.assertEqual("content2", task_expected.content)

        task_expected2 = queue.get_task(Resources(30, 3, 4))
        self.assertEqual(10, task_expected2.priority)
        self.assertEqual(Resources(30, 3, 4), task_expected2.resources)
        self.assertEqual("content1", task_expected2.content)

        task_expected3 = queue.get_task(Resources(30, 3, 4))
        self.assertIsNotNone(task_expected3)
        self.assertEqual(10, task_expected3.priority)
        self.assertEqual(task_expected3.content, 'content6')

        task_expected4 = queue.get_task(Resources(32, 3, 4))
        self.assertEqual(12, task_expected4.priority)

        task_expected5 = queue.get_task(Resources(33, 3, 4))
        self.assertEqual(12, task_expected5.priority)

        task_expected5 = queue.get_task(Resources(33, 3, 4))
        self.assertEqual(11, task_expected5.priority)

        task_expected6 = queue.get_task(Resources(33, 3, 4))
        self.assertEqual(11, task_expected6.priority)

        task_expected7 = queue.get_task(Resources(33, 3, 4))
        self.assertEqual(11, task_expected7.priority)

        task_expected8 = queue.get_task(Resources(30, 3, 4))
        self.assertIsNone(task_expected8)

        task_expected9 = queue.get_task(Resources(30, 3, 4))
        self.assertIsNone(task_expected9)

        queue.clear()
