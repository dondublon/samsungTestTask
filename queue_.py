from types_ import Resources, Task


class TaskQueue:
    def add_task(self, task: Task):
        pass

    def get_task(self, available_resources: Resources) -> Task | None:
        """If there is no such task, we return None."""
        pass
