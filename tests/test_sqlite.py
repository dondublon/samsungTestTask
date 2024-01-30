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
        tasks_range = 1000
        max_priority = 100
        max_ram = 100
        max_cpu = 100
        max_gpu = 100
        for i in range(tasks_range):
            task = Task(None, randint(0, max_priority),
                        Resources(randint(0, max_ram), randint(0, max_cpu), randint(0, max_gpu)),
                        "", "")
            queue.add_task(task)

        got_tasks_count = 0
        for i in range(tasks_range):
            res_ram = randint(0, max_ram)
            res_cpu = randint(0, max_cpu)
            res_gpu = randint(0, max_gpu)
            res = Resources(res_ram, res_cpu, res_gpu)
            task_retrieved = queue.get_task(res)
            if task_retrieved:
                got_tasks_count += 1
            tasks_match = queue.get_all(res)
            if len(tasks_match):
                max_priority = task_retrieved.priority
                for itm in tasks_match:
                    self.assertLessEqual(itm.priority, max_priority)
                    self.assertLessEqual(itm.resources.ram, res_ram)
                    self.assertLessEqual(itm.resources.cpu_cores, res_cpu)
                    self.assertLessEqual(itm.resources.gpu_count, res_gpu)

            else:
                for itm in tasks_match:
                    self.assertGreater(itm.resources.ram, res_ram)
                    self.assertGreater(itm.resources.cpu_cores, res_cpu)
                    self.assertGreater(itm.resources.gpu_count, res_gpu)


        tasks_left = queue.get_all(Resources(max_ram, max_cpu, max_gpu))
        self.assertEqual(tasks_range-got_tasks_count, len(tasks_left))

        queue.clear()
