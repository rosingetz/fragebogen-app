import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "responses.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS vorarbeiter (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL DEFAULT (datetime('now','localtime')),
            profile_name TEXT DEFAULT '',
            answers TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS bewerber (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL DEFAULT (datetime('now','localtime')),
            answers TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_vorarbeiter(answers_dict, profile_name=""):
    conn = get_connection()
    conn.execute(
        "INSERT INTO vorarbeiter (profile_name, answers) VALUES (?, ?)",
        (profile_name, json.dumps(answers_dict))
    )
    conn.commit()
    conn.close()

def save_bewerber(answers_dict):
    conn = get_connection()
    conn.execute(
        "INSERT INTO bewerber (answers) VALUES (?)",
        (json.dumps(answers_dict),)
    )
    conn.commit()
    conn.close()

def get_all_vorarbeiter():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM vorarbeiter ORDER BY id").fetchall()
    conn.close()
    return rows

def get_all_bewerber():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM bewerber ORDER BY id DESC").fetchall()
    conn.close()
    return rows

def delete_vorarbeiter(record_id):
    conn = get_connection()
    conn.execute("DELETE FROM vorarbeiter WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()

def delete_bewerber(record_id):
    conn = get_connection()
    conn.execute("DELETE FROM bewerber WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()

def reset_all():
    conn = get_connection()
    conn.execute("DELETE FROM vorarbeiter")
    conn.execute("DELETE FROM bewerber")
    conn.commit()
    conn.close()
