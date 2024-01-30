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
    # For option 1 (see explanation in README.md):
    cursor.execute('CREATE INDEX ix_priority_resources ON tasks (priority DESC, cpu_cores DESC , gpu_count DESC , ram DESC)')
    # For option 2 (see explanation in README.md):
    cursor.execute('CREATE INDEX ix_resources_priority ON tasks (cpu_cores DESC , gpu_count DESC , ram DESC , priority DESC)')

    connection.commit()

    return connection
