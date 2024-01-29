from queue_ import TaskQueue
from types_ import Task, Resources


class SQLiteQueue(TaskQueue):
    def __init__(self, connection):
        self.connection = connection

    def add_task(self, task: Task):
        """task.id is ignored here"""
        cursor = self.connection.cursor()
        # noinspection SqlResolve
        cursor.execute(f"""INSERT INTO tasks(priority, ram, cpu_cores, gpu_count, content) """
                       f"""VALUES (?, ?, ?, ?, ?)""",
                       (task.priority, task.resources.ram, task.resources.cpu_cores,task.resources.gpu_count, task.content))
        self.connection.commit()

    def get_task(self, available_resources: Resources) -> Task | None:
        ar = available_resources
        cursor = self.connection.cursor()
        # noinspection SqlResolve
        cursor.execute(f"""SELECT id, priority, ram, cpu_cores, gpu_count, content, result """ 
                       f"""FROM tasks WHERE ram >= {ar.ram} AND cpu_cores >= {ar.cpu_cores} AND """
                       f"""gpu_count >= {ar.gpu_count} ORDER BY priority DESC LIMIT 1""")
        sql_result = cursor.fetchone()

        if sql_result is None:
            return None
        else:
            id_, priority, ram, cpu_cores, gpu_count, content, result = sql_result
            resources = Resources(ram, cpu_cores, gpu_count)
            task = Task(id_, priority, resources, content, result)
            return task



