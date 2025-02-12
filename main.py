from fastapi import FastAPI

from products.router import router_products
from general.router import router_general

app = FastAPI()
app.include_router(router_general)
app.include_router(router_products)


@app.get("/")
async def root():
    return {"message": "Методы работы с WB"}





