import databases
import sqlalchemy
from pydantic import BaseModel, Field
from sqlalchemy import create_engine


DATABASE_URL = 'sqlite:///task1/db1.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
db1 = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(50)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(128)),
)


class Users(BaseModel):
    user_id: int
    username: str = Field(title="Name", min_length=2, max_length=50)
    email: str = Field(title="Email", max_length=128,
                       pattern='([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    password: str = Field(title="Password", min_length=8, max_length=128, pattern='(.*[a-z])||(.*[0-9])')
