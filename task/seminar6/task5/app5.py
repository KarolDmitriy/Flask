# Задание №5*
# Разработать API для управления списком задач с использованием базы
# данных MongoDB. Для этого создайте модель Task со следующими полями:
# ○ id: str (идентификатор задачи, генерируется автоматически)
# ○ title: str (название задачи)
# ○ description: str (описание задачи)
# ○ done: bool (статус выполнения задачи)

# Задание №5* (продолжение)
# API должно поддерживать следующие операции:
# ○ Получение списка всех задач: GET /tasks/
# ○ Получение информации о конкретной задаче: GET /tasks/{task_id}/
# ○ Создание новой задачи: POST /tasks/
# ○ Обновление информации о задаче: PUT /tasks/{task_id}/
# ○ Удаление задачи: DELETE /tasks/{task_id}/
# Для валидации данных используйте параметры Field модели Task.
# Для работы с базой данных используйте PyMongo.


import logging
from fastapi import FastAPI
from task5.models import cur, Tasks

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app5 = FastAPI()


@app5.get("/tasks/")
async def read_all():
    res = []
    logger.info('Отработал GET запрос.')
    tasks = cur.find({})
    for task in tasks:
        res.append(task)
    return str(res)


@app5.get("/tasks/{task_id}")
async def read_task(task_id: int):
    logger.info('Отработал GET запрос.')
    return str(cur.find_one({'task_id': task_id}))


@app5.post("/tasks/")
async def create_task(task: Tasks):
    logger.info('Отработал POST запрос.')
    id = cur.insert_one(task.model_dump()).inserted_id
    return str(cur.find_one({"_id": id}))


@app5.put("/tasks/{task_id}")
async def upd_task(task_id: int, task: Tasks):
    logger.info('Отработал PUT запрос.')
    cur.update_one({'task_id': task_id}, {"$set": task.model_dump()})
    return str(cur.find_one({'task_id': task_id}))


@app5.delete("/tasks/{task_id}")
async def upd_task(task_id: int):
    logger.info('Отработал DEL запрос.')
    cur.delete_one({'task_id': task_id})
    return "Task deleted!"




