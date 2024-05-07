import sqlite3

# Connect to SQLite database
# If the file doesn't exist, it will be created in the current directory.
conn = sqlite3.connect('valplayers.db')

# Create a cursor object
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    kills INTEGER DEFAULT 0,
    deaths INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
);
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")
