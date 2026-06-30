from fastapi import FastAPI
from pydantic import BaseModel, Field

products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "is_active": True},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "is_active": True},
    {"id": 3, "code": "SP003", "name": "Monitor", "price": 2500000, "is_active": False},
]

app = FastAPI()


def get_product_by_id(id):
    for product in products:
        if id == product["id"]:
            return product

    return None


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    product = get_product_by_id(product_id)
    if not product:
        return {"detail": "Product not found"}
    if not product["is_active"]:
        return {"detail": "Product already inactive"}

    product["is_active"] = False
    return {"detail": "Ngừng kinh doanh thành công"}
