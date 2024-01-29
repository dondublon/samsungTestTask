import sqlite3

# Connect to the in-memory SQLite database
connection = sqlite3.connect(':memory:')

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Create a table with two integer fields
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

# Create an index on the two integer fields
cursor.execute('CREATE INDEX ix_resources_priority ON tasks (cpu_cores, gpu_count, ram, priority)')

# Commit the changes
connection.commit()

# Close the connection
connection.close()
