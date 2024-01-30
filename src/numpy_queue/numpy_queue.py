import bisect
import numpy as np

from src.queue_ import TaskQueue
from src.types_ import Task, Resources


class NumpyQueue(TaskQueue):
    def __init__(self):
        self.arr = None
        self.clear()

    def clear(self):
        self.arr = np.empty((101, 101, 101), dtype=object)

    def add_task(self, task: Task):
        resource_point = self.arr[task.resources.ram, task.resources.cpu_cores, task.resources.gpu_count]
        if resource_point is None:
            self.arr[task.resources.ram, task.resources.cpu_cores, task.resources.gpu_count] = [task]
        else:
            bisect.insort(resource_point, task, key=lambda t: t.priority)

    def get_task(self, available_resources: Resources) -> Task | None:
        ar = available_resources
        tmp_max_priority = -1
        tmp_obj = None
        tmp_coords = None
        for ram_idx in range(ar.ram+1):
            for cpu_idx in range(ar.cpu_cores+1):
                for gpu_idx in range(ar.gpu_count+1):
                    if row := self.arr[ram_idx, cpu_idx, gpu_idx]:
                        if row[-1].priority > tmp_max_priority:
                            tmp_max_priority = row[-1].priority
                            tmp_obj = row[-1]
                            tmp_coords = (ram_idx, cpu_idx, gpu_idx)
        if tmp_obj:
            row = self.arr[tmp_coords]
            del row[-1]
        return tmp_obj