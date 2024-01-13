from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    email: str

users = [User(id=1, username="XXXX", email="john@example.com"),
        User(id=2, username="WWWW", email="jane@example.com")]

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = next((user for user in users if user_id == user_id), None)
    for user in users:
        if user.id == user_id:
            return user
        
@app.get("/users")
def get_users():
    return users

@app.post("/create_user")
def create_user(user: User):
    users.append(user)
    return user

