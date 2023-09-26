from datetime import datetime

import databases
import sqlalchemy
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, ForeignKey

DATABASE_URL = 'sqlite:///task6/db6.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
db6 = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()
default_date = datetime.now

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(20)),
    sqlalchemy.Column("l_name", sqlalchemy.String(20)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(128)),
)

items = sqlalchemy.Table(
    "items",
    metadata,
    sqlalchemy.Column("item_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(50)),
    sqlalchemy.Column("description", sqlalchemy.String(256)),
    sqlalchemy.Column("price", sqlalchemy.Integer),
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("order_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, ForeignKey('users.user_id')),
    sqlalchemy.Column("item_id", sqlalchemy.Integer, ForeignKey('items.item_id')),
    sqlalchemy.Column("order_date", sqlalchemy.String(128), default=default_date),
    sqlalchemy.Column("status", sqlalchemy.String),
)


class Users(BaseModel):
    user_id: int
    name: str = Field(title="Name", min_length=2, max_length=20)
    l_name: str = Field(title="Last name", min_length=2, max_length=20)
    email: str = Field(title="Email", max_length=128)
    password: str = Field(title="Password", max_length=128)


class Items(BaseModel):
    item_id: int
    title: str = Field(title="Title", min_length=2, max_length=50)
    description: str = Field(title="Description", max_length=256)
    price: float = Field(title="Price", default=0)


class Orders(BaseModel):
    order_id: int
    user_id: int
    item_id: int
    order_date: str = Field(title="Order date")
    status: str = Field(title="Status")