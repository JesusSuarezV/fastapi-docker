from fastapi import FastAPI, Request
import json
import os
import psycopg2
from pydantic import BaseModel

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

app = FastAPI()

class Note(BaseModel):
    title: str
    content: str

@app.get("/")
async def root():
    return {
        "message": "Welcome to the FastAPI application! "
        "You can use this API to manage your notes."
    }

@app.get("/notes")
async def get_notes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, content FROM notes")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    notes = []
    for row in rows:
        notes.append({
            "id": row[0],
            "title": row[1],
            "content": row[2]
        })

    return {"notes": notes}


@app.post("/notes")
async def create_note(note: Note):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO notes (title, content) VALUES (%s, %s)",
    (note.title, note.content)
    )
    conn.commit()  
    print("Note save in DB")
    cur.close()
    conn.close()
    return {"message": "Note created successfully!"}