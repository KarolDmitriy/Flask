# Задание №1
# Разработать API для управления списком пользователей с
# использованием базы данных SQLite. Для этого создайте
# модель User со следующими полями:
# ○ id: int (идентификатор пользователя, генерируется
# автоматически)
# ○ username: str (имя пользователя)
# ○ email: str (электронная почта пользователя)
# ○ password: str (пароль пользователя)

import logging

from fastapi import FastAPI
from werkzeug.security import generate_password_hash
from task1.models import Users, users, engine, metadata, db1

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

metadata.create_all(engine)

app1 = FastAPI()


@app1.get("/users/")
async def read_users():
    query = users.select()
    return await db1.fetch_all(query)


@app1.get("/users/{user_id}", response_model=Users)
async def read_user(user_id: int):
    query = users.select().where(users.c.user_id == user_id)
    return await db1.fetch_one(query)


@app1.post("/users/", response_model=Users)
async def create_user(user: Users):
    password_hash = generate_password_hash(str(user.password))
    query = users.insert().values(user_id=user.user_id, username=user.username, email=user.email,
                                  password=password_hash)
    last_record_id = await db1.execute(query)
    return {**user.model_dump(), "id": last_record_id}


@app1.put("/users/{user_id}", response_model=Users)
async def update_user(user_id: int, new_user: Users):
    password_hash = generate_password_hash(str(new_user.password))
    query = users.update().where(users.c.user_id == user_id).values(username=new_user.username, email=new_user.email,
                                                                    password=password_hash)
    await db1.execute(query)
    return {**new_user.model_dump(), "id": user_id}


@app1.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.user_id == user_id)
    await db1.execute(query)
    return {'message': 'User deleted'}
