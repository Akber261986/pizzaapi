from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

app = FastAPI(title="🍕 Pizza Delivery API")

class PizzaOrder(BaseModel):
    size: str  # "small", "medium", "large"
    toppings: List[str]
    crust: str  # "thin", "thick", "stuffed"
    customer_name: str
    delivery_address: str
    phone: str

orders_db = {}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Pizza Delivery API! 🍕"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "pizza-api"}

@app.post("/orders")
def create_order(order: PizzaOrder):
    order_id = str(uuid.uuid4())[:8]
    order_data = {
        "order_id": order_id,
        **order.dict(),
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "estimated_delivery": "30-45 minutes"
    }
    orders_db[order_id] = order_data
    return order_data

@app.get("/orders")
def list_orders():
    return list(orders_db.values())

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]

@app.get("/menu")
def get_menu():
    return {
        "sizes": {
            "small": {"price": 599, "slices": 6},
            "medium": {"price": 899, "slices": 8},
            "large": {"price": 1299, "slices": 12}
        },
        "toppings": ["pepperoni", "mushrooms", "onions", "sausage", "bacon"],
        "crusts": ["thin", "thick", "stuffed", "gluten-free"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
