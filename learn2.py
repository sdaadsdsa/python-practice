from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Category(BaseModel):
    id: int
    name: str


class Service(BaseModel):
    id: int
    name: str
    category_id: int


categories = [
    Category(id=1, name="Стрижки и укладки"),
    Category(id=2, name="Маникюр и педикюр"),
    Category(id=3, name="Брови и ресницы"),
    Category(id=4, name="Спа-процедуры"),
]

services = [
    Service(id=1, name="Стрижка женская", category_id=1),
    Service(id=2, name="Стрижка мужская", category_id=1),
    Service(id=3, name="Укладка", category_id=1),
    Service(id=4, name="Окрашивание", category_id=1),
    Service(id=5, name="Ботокс волос", category_id=1),
    Service(id=6, name="Маникюр", category_id=2),
    Service(id=7, name="Педикюр", category_id=2),
    Service(id=8, name="Наращивание ногтей", category_id=2),
    Service(id=9, name="Дизайн ногтей", category_id=2),
    Service(id=10, name="Покрытие гель-лаком", category_id=2),
    Service(id=11, name="Коррекция бровей", category_id=3),
    Service(id=12, name="Окрашивание бровей", category_id=3),
    Service(id=13, name="Наращивание ресниц", category_id=3),
    Service(id=14, name="Ламинирование ресниц", category_id=3),
    Service(id=15, name="Спа-уход за лицом", category_id=4),
    Service(id=16, name="Спа-уход за телом", category_id=4),
    Service(id=17, name="Массаж", category_id=4),
    Service(id=18, name="Обёртывание", category_id=4),
]


@app.get("/categories")
def get_categories():
    result = []
    for category in categories:
        count = sum(1 for s in services if s.category_id == category.id)
        result.append({
            "id": category.id,
            "name": category.name,
            "servicesCount": count,
        })
    return result


@app.get("/categories/{category_id}")
def get_category(category_id: int):
    category = next((c for c in categories if c.id == category_id), None)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    count = sum(1 for s in services if s.category_id == category.id)
    return {
        "id": category.id,
        "name": category.name,
        "servicesCount": count,
    }