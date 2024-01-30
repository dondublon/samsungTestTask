from random import randint

from src.numpy_queue.numpy_queue import NumpyQueue
from src.types_ import Task, Resources
from tests.test_common import TestQueueCommon


class TestNumpy(TestQueueCommon):
    MAX_PRIORITY = 100
    MAX_RAM = 100
    MAX_CPU = 100
    MAX_GPU = 100

    def get_queue(self):
        queue = NumpyQueue(self.MAX_RAM, self.MAX_CPU, self.MAX_GPU)
        return queue

    def test_random(self):
        """This test knows about the internal task storage and checks it."""
        queue = self.get_queue()
        tasks_range = 1000

        for i in range(tasks_range):
            task = Task(None, randint(0, self.MAX_PRIORITY),
                        Resources(randint(0, self.MAX_RAM), randint(0, self.MAX_CPU), randint(0, self.MAX_GPU)),
                        "", "")
            queue.add_task(task)

        got_tasks_count = 0
        for i in range(tasks_range):
            res_ram = randint(0, self.MAX_RAM)
            res_cpu = randint(0, self.MAX_CPU)
            res_gpu = randint(0, self.MAX_GPU)
            res = Resources(res_ram, res_cpu, res_gpu)
            retrieved_task = queue.get_task(res)
            tasks_match = queue.get_all(res)
            if retrieved_task:
                max_priority = retrieved_task.priority
                # self.assertGreater(len(tasks_match), 0)
                for tasks_row in tasks_match:
                    for itm in tasks_row:
                        self.assertLessEqual(itm.priority, max_priority)
                        self.assertLessEqual(itm.resources.ram, res_ram)
                        self.assertLessEqual(itm.resources.cpu_cores, res_cpu)
                        self.assertLessEqual(itm.resources.gpu_count, res_gpu)
                got_tasks_count += 1
            else:
                self.assertEqual(len(tasks_match), 0)
                for tasks_row in tasks_match:
                    for itm in tasks_row:
                        self.assertGreater(itm.resources.ram, res_ram)
                        self.assertGreater(itm.resources.cpu_cores, res_cpu)
                        self.assertGreater(itm.resources.gpu_count, res_gpu)

        tasks_left = queue.get_all(Resources(self.MAX_RAM, self.MAX_CPU, self.MAX_GPU))
        self.assertEqual(tasks_range-got_tasks_count, len(tasks_left))

        queue.clear()
