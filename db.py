import os
import sqlite3

DATABASE_FILE = "db.sqlite3"

def initialize_database():
    if os.path.exists(DATABASE_FILE):
        print("Database already exists. Skipping initialization.")
        return
    else:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Notes(
                    id UUID PRIMARY KEY,
                    title VARCHAR(255),
                    content TEXT
                )
                """
            )
            conn.commit()
            print("Database initialized successfully.")
        except sqlite3.Error as e:
            print("Error creating table:", e)
        finally:
            conn.close()

