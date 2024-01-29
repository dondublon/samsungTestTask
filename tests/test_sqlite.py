from unittest import TestCase
from random import randint

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
        self.assertEqual(11, task_expected.priority)
        self.assertEqual("content2", task_expected.content)

        task_expected2 = queue.get_task(Resources(30, 3, 4))
        self.assertEqual(10, task_expected2.priority)
        self.assertEqual("content1", task_expected2.content)

        task_expected3 = queue.get_task(Resources(30, 3, 4))
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

    def test_random(self):
        queue = SQLiteQueue(self.connection)
        for i in range(1000):
            task = Task(None, randint(0, 100), Resources(randint(0, 100), randint(0, 100), randint(0, 100)), "", "")
            queue.add_task(task)

        got_tasks_count = 0
        for i in range(1000):
            res_ram = randint(0, 100)
            res_cpu = randint(0, 100)
            res_gpu = randint(0, 100)
            res = Resources(res_ram, res_cpu, res_gpu)
            tasks_match = queue.get_all(res)
            if len(tasks_match):
                max_priority = tasks_match[0].priority
                for itm in tasks_match:
                    self.assertLessEqual(itm.priority, max_priority)
                    self.assertLessEqual(itm.resources.ram, res_ram)
                    self.assertLessEqual(itm.resources.cpu_cores, res_cpu)
                    self.assertLessEqual(itm.resources.gpu_count, res_gpu)
                got_tasks_count += 1
            else:
                all_tasks = queue.get_all(res)
                for itm in all_tasks:
                    self.assertGreater(itm.resources.ram, res_ram)
                    self.assertGreater(itm.resources.cpu_cores, res_cpu)
                    self.assertGreater(itm.resources.gpu_count, res_gpu)
            queue.get_task(res)

        tasks_left = queue.get_all(Resources(100, 100, 100))
        self.assertEqual(1000-got_tasks_count, len(tasks_left))

        queue.clear()

