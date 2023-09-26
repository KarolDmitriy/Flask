from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, Field

DATABASE_URL = "sqlite:///database.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Определение таблиц для товаров, заказов и пользователей
products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(100)),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("price", sqlalchemy.Float),
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("product_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id")),
    sqlalchemy.Column("status", sqlalchemy.String(20)),
)

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String(50)),
    sqlalchemy.Column("last_name", sqlalchemy.String(50)),
    sqlalchemy.Column("email", sqlalchemy.String(100)),
    sqlalchemy.Column("password", sqlalchemy.String(100)),
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

app = FastAPI()

class ProductBase(BaseModel):
    name: str
    description: str
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

class OrderBase(BaseModel):
    user_id: int
    product_id: int
    status: str

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

# Маршруты для управления товарами
@app.post("/products/", response_model=Product)
async def create_product(product: ProductCreate):
    query = products.insert().values(**product.dict())
    last_record_id = await database.execute(query)
    return {**product.dict(), "id": last_record_id}

@app.get("/products/", response_model=List[Product])
async def read_products():
    query = products.select()
    return await database.fetch_all(query)

@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)

@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, new_product: ProductCreate):
    query = products.update().where(products.c.id == product_id).values(**new_product.dict())
    await database.execute(query)
    return {**new_product.dict(), "id": product_id}

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {'message': 'Product deleted'}

# Маршруты для управления заказами
@app.post("/orders/", response_model=Order)
async def create_order(order: OrderCreate):
    query = orders.insert().values(**order.dict())
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}

@app.get("/orders/", response_model=List[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)

@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)

@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderCreate):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), "id": order_id}

@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}

# Маршруты для управления пользователями
@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    query = users.insert().values(**user.dict())
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}

@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserCreate):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
