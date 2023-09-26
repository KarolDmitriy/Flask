# Задание №2
# Создать веб-приложение на FastAPI, которое будет предоставлять API для
# работы с базой данных пользователей. Пользователь должен иметь
# следующие поля:
# ○ ID (автоматически генерируется при создании пользователя)
# ○ Имя (строка, не менее 2 символов)
# ○ Фамилия (строка, не менее 2 символов)
# ○ Дата рождения (строка в формате "YYYY-MM-DD")
# ○ Email (строка, валидный email)
# ○ Адрес (строка, не менее 5 символов)
#
# 20:19
# Задание №2 (продолжение)
# API должен поддерживать следующие операции:
# ○ Добавление пользователя в базу данных
# ○ Получение списка всех пользователей в базе данных
# ○ Получение пользователя по ID
# ○ Обновление пользователя по ID
# ○ Удаление пользователя по ID
# Приложение должно использовать базу данных SQLite3 для хранения
# пользователей.

import databases
import sqlalchemy
from pydantic import BaseModel, Field
from sqlalchemy import create_engine


DATABASE_URL = 'sqlite:///task2/db2.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
db2 = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(50)),
    sqlalchemy.Column("email", sqlalchemy.String(50)),
    sqlalchemy.Column("birthday", sqlalchemy.String(10)),
    sqlalchemy.Column("password", sqlalchemy.String(128)),
    sqlalchemy.Column("address", sqlalchemy.String(128)),
)


class Users(BaseModel):
    user_id: int
    username: str = Field(title="Name", min_length=2, max_length=50)
    email: str = Field(title="Email", max_length=50,
                       pattern='([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    birthday: str = Field(title="Birthday", min_length=10, max_length=10,
                          pattern='(0?[1-9]|[12][0-9]|3[01])(\.)(0?[1-9]|1[012])(\.)((19|20)\d\d)')
    password: str = Field(title="Password", min_length=8, max_length=128, pattern='(.*[a-z])||(.*[0-9])')
    address: str = Field(title="Address", min_length=5, max_length=128)
