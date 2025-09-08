import json
import os
import uuid
from typing import Dict, List
from fastapi import FastAPI, HTTPException, status
import uvicorn
from pydantic import BaseModel

app = FastAPI(
    title="Luxe Mock E-commerce API",
    description="A mock backend to simulate order, cart, and product functionalities for the Luxe chatbot."
)

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db.json'))

def load_data():
    """Loads mock data from the db.json file."""
    try:
        with open(db_path, 'r') as f:
            data = json.load(f)
            print(f"✅ Successfully loaded data from {db_path}")
            return data
    except FileNotFoundError:
        print(f"❌ Error: The file {db_path} was not found.")
        return {"orders": []}
    except json.JSONDecodeError:
        print(f"❌ Error: Could not decode JSON from {db_path}.")
        return {"orders": []}

# Mock database class to handle data retrieval and operations
class MockDatabase:
    def __init__(self, initial_data: Dict):
        self.orders = {item['id']: item for item in initial_data.get("orders", [])}
        # Add a products dictionary to complete the mock DB
        self.products = {
            "p-001": {"id": "p-001", "name": "Velvet Armchair", "description": "Luxurious velvet armchair with gold-plated legs.", "price": 450.00, "stock": 10},
            "p-002": {"id": "p-002", "name": "Minimalist Coffee Table", "description": "Sleek coffee table with a matte black finish.", "price": 200.00, "stock": 5},
            "p-003": {"id": "p-003", "name": "Linen Sofa", "description": "Comfortable three-seater sofa with linen upholstery.", "price": 800.00, "stock": 3},
            "p-004": {"id": "p-004", "name": "Classic Dining Chair", "description": "A timeless wooden dining chair.", "price": 120.00, "stock": 25},
        }
        self.returns = {}
        
# Load initial data from the JSON file
initial_db_data = load_data()
db = MockDatabase(initial_db_data)

class AddToCartRequest(BaseModel):
    product_id: str
    quantity: int

class InitiateReturnRequest(BaseModel):
    order_id: str

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "ok"}

@app.get("/orders/{order_id}/status", status_code=status.HTTP_200_OK)
def get_order_status(order_id: str):
    """Fetches the status of a specific order from the e-commerce API."""
    order = db.orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    return order

@app.post("/cart/add", status_code=status.HTTP_200_OK)
def add_to_cart(request: AddToCartRequest):
    """Adds a product to the user's cart."""
    product = db.products.get(request.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    return {"message": f"Successfully added {request.quantity} of '{product['name']}' to the cart."}

@app.post("/returns/initiate", status_code=status.HTTP_200_OK)
def initiate_return(request: InitiateReturnRequest):
    """Initiates a return for a specific order."""
    order = db.orders.get(request.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    
    return_id = str(uuid.uuid4())
    db.returns[return_id] = {"order_id": request.order_id, "status": "Return initiated."}
    
    return {"message": f"Return for order '{request.order_id}' has been initiated successfully. Return ID: {return_id}"}

@app.get("/products/search", status_code=status.HTTP_200_OK)
def search_products(q: str):
    """Searches for products based on a query."""
    results = [
        product for product in db.products.values()
        if q.lower() in product['name'].lower() or q.lower() in product['description'].lower()
    ]
    if not results:
        raise HTTPException(status_code=404, detail="No products found matching the query.")
    return results

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)