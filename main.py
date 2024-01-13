from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import sqlite3

con = sqlite3.connect('database.db', check_same_thread=False)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(id, username, email)")

class User(BaseModel):
    id: int
    username: str
    email: str

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    res = cur.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
    return res.fetchone()

@app.get("/users")
def get_users():
    res = cur.execute("SELECT * FROM users")
    return res.fetchall()

@app.post("/create_user")
def create_user(user: User):
    id_check = cur.execute(f"SELECT * FROM users WHERE id = '{user.id}'")
    ids_not_available = cur.execute("SELECT id FROM users")
    if id_check.fetchone() is not None:
        raise HTTPException(status_code=400, detail=f"ID already exists. Id's not available: {ids_not_available.fetchone()}")
    else:
        cur.execute(f"INSERT INTO users VALUES ({user.id}, '{user.username}', '{user.email}')")
        con.commit()
        return "Created"
