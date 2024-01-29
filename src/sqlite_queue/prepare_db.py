import sqlite3
from typing import Any
from sqlite3 import Connection

def prepare_db() -> Connection:
    connection = sqlite3.connect(':memory:')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE tasks (
            id INTEGER,
            priority INTEGER,
            ram INTEGER, 
            cpu_cores INTEGER, 
            gpu_count INTEGER, 
            content VARCHAR,
            result VARCHAR,
            PRIMARY KEY (id)
        )
    ''')

    cursor.execute('CREATE INDEX ix_resources_priority ON tasks (cpu_cores, gpu_count, ram, priority)')

    connection.commit()

    return connection
