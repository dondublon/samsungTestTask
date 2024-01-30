from src.types_ import Resources, Task


class TaskQueue:
    def add_task(self, task: Task):
        pass

    def get_task(self, available_resources: Resources) -> Task | None:
        """If there is no such task, we return None."""
        pass

    # region Additional methods for testing:
    def clear(self):
        """Clears all the queue, be careful!"""
        pass

    def get_all(self, available_resources: Resources) -> list[Task]:
        """Just for control, not for production using."""
        pass
    # endregion
