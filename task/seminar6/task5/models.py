from pymongo import MongoClient
from pydantic import BaseModel, Field


md_client = MongoClient(f'mongodb://localhost:27017/')
cur = md_client.tasks.tasks_collection


class Tasks(BaseModel):
    task_id: int
    title: str = Field(title="Title", min_length=2, max_length=50)
    description: str = Field(title="Description", max_length=256)
    done: bool = Field(title="Done", default=False)