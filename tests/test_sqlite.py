from unittest import TestCase
from random import randint

from src.sqlite_queue.prepare_db import prepare_db
from src.sqlite_queue.sqlite_queue import SQLiteQueue
from src.types_ import Task, Resources
from tests.test_common import TestQueueCommon


class TestSQLite(TestQueueCommon):
    connection = None

    @classmethod
    def setUpClass(cls) -> None:
        connection = prepare_db()
        cls.connection = connection

    def get_queue(self):
        queue = SQLiteQueue(self.connection)
        return queue

    def test_random(self):
        """This test knows about the internal task storage and checks it."""
        queue = self.get_queue()
        TASKS_RANGE = 1000
        MAX_PRIORITY = 100
        MAX_RAM = 100
        MAX_CPU = 100
        MAX_GPU = 100
        for i in range(TASKS_RANGE):
            task = Task(None, randint(0, MAX_PRIORITY), Resources(randint(0, MAX_RAM), randint(0, MAX_CPU), randint(0, MAX_GPU)), "", "")
            queue.add_task(task)

        got_tasks_count = 0
        for i in range(TASKS_RANGE):
            res_ram = randint(0, MAX_RAM)
            res_cpu = randint(0, MAX_CPU)
            res_gpu = randint(0, MAX_GPU)
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
                for itm in tasks_match:
                    self.assertGreater(itm.resources.ram, res_ram)
                    self.assertGreater(itm.resources.cpu_cores, res_cpu)
                    self.assertGreater(itm.resources.gpu_count, res_gpu)
            queue.get_task(res)

        tasks_left = queue.get_all(Resources(MAX_RAM, MAX_CPU, MAX_GPU))
        self.assertEqual(TASKS_RANGE-got_tasks_count, len(tasks_left))

        queue.clear()

