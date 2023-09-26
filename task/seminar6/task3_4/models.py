import databases
import sqlalchemy
from pydantic import BaseModel, Field
from sqlalchemy import create_engine


DATABASE_URL = 'sqlite:///task3_4/db3.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
db3 = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()


tasks = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("task_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(50)),
    sqlalchemy.Column("description", sqlalchemy.String(256)),
    sqlalchemy.Column("done", sqlalchemy.Boolean()),
)


class Tasks(BaseModel):
    task_id: int
    title: str = Field(title="Title", min_length=2, max_length=50)
    description: str = Field(title="Description", max_length=256)
    done: bool = Field(title="Done", default=False)
# done: Optional[bool] = False