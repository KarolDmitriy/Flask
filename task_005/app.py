from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


# Модель для описания задачи
class Task(BaseModel):
    task_id: int
    title: str
    description: str
    status: bool = False  # По умолчанию задача не выполнена


# Список задач (заглушка, можно использовать базу данных)
tasks = []


# Конечная точка для получения списка всех задач
@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return tasks


# Конечная точка для создания новой задачи
@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    tasks.append(task)
    return task


# Конечная точка для получения задачи по ID
@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]


# Конечная точка для обновления задачи по ID
@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")

    tasks[task_id] = updated_task
    return updated_task


# Конечная точка для удаления задачи по ID
@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")

    deleted_task = tasks.pop(task_id)
    return deleted_task


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
