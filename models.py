import sqlite3
from db import DATABASE_FILE


class Note:
    def __init__(self, id=None, title=None, content=None):
        self.id = id
        self.title = title
        self.content = content

    @staticmethod
    def connection():
        return sqlite3.connect(DATABASE_FILE)

    def save(self):
        conn = Note.connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO Notes (id, title, content) VALUES (?, ?, ?)",
                (self.id, self.title, self.content),
            )
            conn.commit()
            print("Note saved successfully.")
        except sqlite3.Error as e:
            print("Error saving note:", e)
        finally:
            conn.close()

    @staticmethod
    def all():
        conn = Note.connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Notes")
        return cursor.fetchall()

    @staticmethod
    def get_by_id(note_id):
        conn = Note.connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Notes WHERE id = ?", (note_id,))
        note = cursor.fetchone()
        if note:
            return note
        else:
            return "Note not found"

    def update(self, note_id):
        conn = Note.connection()
        cursor = conn.cursor()
        note = self.get_by_id(note_id=note_id)

        cursor.execute(
            f"UPDATE {note} SET title =?, content=? WHERE=?",
            (self.title, self.content, note_id),
        )
        conn.commit()

    def delete(self, note_id):
        conn = Note.connection()
        cursor = conn.cursor()
        note = self.get_by_id(note_id=note_id)
        cursor.execute(f"DELETE FROM Notes WHERE id = ?", (note_id,))
        conn.commit()
