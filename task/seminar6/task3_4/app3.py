# Задание №3
# Создать API для управления списком задач.
# Каждая задача должна содержать поля "название",
# "описание" и "статус" (выполнена/не выполнена).
# API должен позволять выполнять CRUD операции с
# задачами.
#
# Задание №4
# Напишите API для управления списком задач. Для этого создайте модель Task
# со следующими полями:
# ○ id: int (первичный ключ)
# ○ title: str (название задачи)
# ○ description: str (описание задачи)
# ○ done: bool (статус выполнения задачи)


import logging

from fastapi import FastAPI
from task3_4.models import Tasks, tasks, engine, metadata, db3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

metadata.create_all(engine)

app3 = FastAPI()


@app3.get("/tasks/")
async def read_root():
    logger.info('Отработал GET запрос.')
    query = tasks.select()
    return await db3.fetch_all(query)


@app3.get("/tasks/{task_id}", response_model=Tasks)
async def read_task(task_id: int):
    query = tasks.select().where(tasks.c.task_id == task_id)
    return await db3.fetch_one(query)


@app3.post("/tasks/", response_model=Tasks)
async def create_task(task: Tasks):
    query = tasks.insert().values(task_id=task.task_id, title=task.title, description=task.description,
                                  done=task.done)
    last_record_id = await db3.execute(query)
    return {**task.model_dump(), "id": last_record_id}


@app3.put("/tasks/{task_id}", response_model=Tasks)
async def update_task(task_id: int, new_task: Tasks):
    query = tasks.update().where(tasks.c.task_id == task_id).values(title=new_task.title, description=new_task.description,
                                                                    done=new_task.done)
    await db3.execute(query)
    return {**new_task.model_dump(), "id": task_id}


@app3.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    query = tasks.delete().where(tasks.c.task_id == task_id)
    await db3.execute(query)
    return {'message': 'Task deleted'}