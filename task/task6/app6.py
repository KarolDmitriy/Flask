import logging

from fastapi import FastAPI
from task6.models import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

metadata.create_all(engine)

app6 = FastAPI()


@app6.get("/users/")
async def read_users():
    logger.info('Отработал GET запрос.')
    query = users.select()
    return await db6.fetch_all(query)


@app6.get("/users/{user_id}", response_model=Users)
async def read_user(user_id: int):
    query = users.select().where(users.c.user_id == user_id)
    return await db6.fetch_one(query)


@app6.post("/users/", response_model=Users)
async def create_user(user: Users):
    query = users.insert().values(user_id=user.user_id, name=user.name, l_name=user.l_name, email=user.email,
                                  password=user.password)
    last_record_id = await db6.execute(query)
    return {**user.model_dump(), "id": last_record_id}


@app6.put("/users/{user_id}", response_model=Users)
async def update_user(user_id: int, new_user: Users):
    query = users.update().where(users.c.user_id == user_id).values(user_id=new_user.user_id, name=new_user.name,
                                                                    l_name=new_user.l_name, email=new_user.email,
                                                                    password=new_user.password)
    await db6.execute(query)
    return {**new_user.model_dump(), "id": user_id}


@app6.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.user_id == user_id)
    await db6.execute(query)
    return {'message': 'User deleted'}




@app6.get("/items/")
async def read_items():
    logger.info('Отработал GET запрос.')
    query = items.select()
    return await db6.fetch_all(query)


@app6.get("/items/{item_id}", response_model=Items)
async def read_item(item_id: int):
    query = items.select().where(items.c.item_id == item_id)
    return await db6.fetch_one(query)


@app6.post("/items/", response_model=Items)
async def create_item(item: Items):
    query = items.insert().values(item_id=item.item_id, title=item.title, description=item.description, price=item.price)
    last_record_id = await db6.execute(query)
    return {**item.model_dump(), "id": last_record_id}


@app6.put("/items/{item_id}", response_model=Items)
async def update_item(item_id: int, new_item: Items):
    query = items.update().where(items.c.item_id == item_id).values(item_id=new_item.item_id, title=new_item.title,
                                                                    description=new_item.description, price=new_item.price)
    await db6.execute(query)
    return {**new_item.model_dump(), "id": item_id}


@app6.delete("/items/{item_id}")
async def delete_item(item_id: int):
    query = items.delete().where(items.c.item_id == item_id)
    await db6.execute(query)
    return {'message': 'Item deleted'}



@app6.get("/orders/")
async def read_orders():
    logger.info('Отработал GET запрос.')
    query = orders.select()
    return await db6.fetch_all(query)


@app6.get("/orders/{order_id}", response_model=Orders)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.order_id == order_id)
    return await db6.fetch_one(query)


@app6.post("/orders/", response_model=Orders)
async def create_order(order: Orders):
    query = orders.insert().values(order_id=order.order_id, user_id=order.user_id, item_id=order.item_id,
                                   order_date=order.order_date, status=order.status)
    last_record_id = await db6.execute(query)
    return {**order.model_dump(), "id": last_record_id}


@app6.put("/orders/{order_id}", response_model=Orders)
async def update_order(order_id: int, new_order: Orders):
    query = orders.update().where(orders.c.order_id == order_id).values(order_id=new_order.order_id,
                                                                        user_id=new_order.user_id,
                                                                        item_id=new_order.item_id,
                                                                        order_date=new_order.order_date,
                                                                        status=new_order.status)
    await db6.execute(query)
    return {**new_order.model_dump(), "id": order_id}


@app6.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.order_id == order_id)
    await db6.execute(query)
    return {'message': 'Order deleted'}