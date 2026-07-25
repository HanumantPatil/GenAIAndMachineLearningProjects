from fastapi import FastAPI
app = FastAPI()

# Use API_Model/run_dev.ps1 on Windows to avoid FastAPI CLI console encoding issues.
# .\API_Model\run_dev.ps1   
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/helloworld")
def read_helloworld():
    return {"Hello": "New World"}

@app.get("/hellow/{name}")
def read_helloworld(name: str):
    return {"Hello": f"New World, {name}"}
from enum import Enum

class AvailableCuisines(str, Enum):
    Italian = "Italian"
    Mexican = "Mexican"
    Japanese = "Japanese"
    Indian = "Indian"
@app.get("/get_items/{cuisine}")
def get_items(cuisine: AvailableCuisines):
    food_items = {
        "Italian": ["Pizza", "Pasta", "Lasagna"],
        "Mexican": ["Tacos", "Burritos", "Quesadillas"],
        "Japanese": ["Sushi", "Ramen", "Tempura"],
        "Indian": ["Butter Chicken", "Biryani", "Samosa"]
    }

    return {"Cuisine": cuisine.value, "Items": food_items.get(cuisine.value, [])}


coupon_codes = {
    1: "10%",
    2: "20%",
    3: "30%"
}

@app.get("/get_coupon/{coupon_id}")
def get_coupon(coupon_id: int):
    coupon = coupon_codes.get(coupon_id)
    if coupon:
        return {"Coupon ID": coupon_id, "Discount": coupon}
    else:
        return {"Error": "Coupon not found"}