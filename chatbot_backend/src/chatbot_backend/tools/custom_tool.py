import random
import requests
from crewai.tools import BaseTool
from typing import Optional, Type, Any
from pydantic import BaseModel, Field

# --- Input Schemas ---
class OrderTrackingInput(BaseModel):
    """Input schema for Order Tracking Tool."""
    order_id: str = Field(..., description="The order ID to track")

class StyleAdvisorInput(BaseModel):
    """Input schema for Style Advisor Tool."""
    query: str = Field(..., description="Style preferences or room description")

class ReturnsInput(BaseModel):
    """Input schema for Returns Tool."""
    query: str = Field(..., description="Product or order information for return")

class ProductInfoInput(BaseModel):
    """Input schema for Product Info Tool."""
    product_name: str = Field(..., description="The name of the product to get information for.")


# --- Tools ---
class OrderTrackingTool(BaseTool):
    name: str = "Order Tracking Tool"
    description: str = "A tool to track the status of an order using an external API."
    args_schema: Type[BaseModel] = OrderTrackingInput
    
    def _run(self, order_id: str, run_manager: Optional[Any] = None) -> str:
        """
        Retrieves real-time order status from a local mock API.
        """
        if not order_id:
            return "Please provide a valid order ID."

        API_ENDPOINT = f"http://localhost:3000/orders/{order_id}"
        
        try:
            response = requests.get(API_ENDPOINT)
            response.raise_for_status()

            tracking_data = response.json()
            
            if not tracking_data:
                return f"Order '{order_id}' not found."

            status = tracking_data.get("status", "Unknown")
            carrier = tracking_data.get("carrier", "N/A")
            tracking_number = tracking_data.get("tracking_number", "N/A")
            estimated_delivery = tracking_data.get("estimated_delivery", "N/A")

            return (
                f"Order {order_id} status: {status}. "
                f"Shipping carrier: {carrier}. "
                f"Tracking number: {tracking_number}. "
                f"Estimated delivery: {estimated_delivery}."
            )

        except requests.exceptions.RequestException as e:
            return f"Error retrieving order data for {order_id}: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"


class StyleAdvisorTool(BaseTool):
    name: str = "Style Advisor Tool"
    description: str = "A tool to provide product recommendations based on user style and preferences. Pass the query as a simple string containing customer preferences."
    args_schema: Type[BaseModel] = StyleAdvisorInput
    
    def _run(self, query: str = None, description: str = None, run_manager: Optional[Any] = None, **kwargs) -> str:
        """
        Provides detailed style recommendations based on a user query.
        Handles multiple input formats for compatibility.
        """
        actual_query = query or description or "general home decor recommendations"
        
        if "living room" in actual_query.lower():
            return "Based on your living room preferences, I recommend the 'Copenhagen' sectional sofa in slate gray, paired with a 'Nordic' coffee table and a 'Plush' area rug in off-white."
        elif "minimalist" in actual_query.lower():
            return "For a minimalist style, I recommend a 'Luna' floor lamp, a set of three 'Zen' floating shelves in natural wood, and the 'Elegance' minimalist desk."
        elif "modern" in actual_query.lower():
            return "For modern home decor, consider these stylish items: 1) Sleek geometric coffee table in walnut, 2) Abstract canvas wall art in neutral tones, 3) Contemporary floor lamp with brass accents, 4) Minimalist bookshelf with clean lines, 5) Modern accent chair in deep blue velvet."
        else:
            recommendations = [
                "For a classic look, consider a white sectional sofa with navy throw pillows and a glass coffee table.",
                "If you prefer contemporary style, try a leather accent chair with a geometric area rug and modern lighting.",
                "For a cozy atmosphere, layer different textures with throw blankets, wooden furniture, and warm lighting."
            ]
            return f"Based on your preferences: {actual_query}. " + random.choice(recommendations)

class ReturnsTool(BaseTool):
    name: str = "Returns Tool"
    description: str = "A tool to initiate a return process for a product."
    args_schema: Type[BaseModel] = ReturnsInput
    
    def _run(self, query: str, run_manager: Optional[Any] = None) -> str:
        """
        Initiates a return process and provides detailed instructions.
        """
        if "damaged" in query.lower():
            return f"Return process for '{query}' has been initiated. A shipping label has been sent to your email. Please use a padded box and mark it as 'Damaged - Do Not Resell'."
        else:
            return f"Return process for '{query}' has been initiated. A shipping label has been sent to your email. Your refund will be processed within 5-7 business days after we receive and inspect the item."

class ProductInfoTool(BaseTool):
    name: str = "Product Info Tool"
    description: str = "A tool to get specific details (dimensions, materials, weight) for a given product."
    args_schema: Type[BaseModel] = ProductInfoInput

    def _run(self, product_name: str, run_manager: Optional[Any] = None) -> str:
        """
        Simulates retrieving detailed product information from a database.
        """
        product_database = {
            "Oslo Sofa": {
                "dimensions": "85 inches (W) x 35 inches (D) x 30 inches (H)",
                "materials": "Solid oak frame, velvet upholstery",
                "weight": "150 lbs",
                "color": "Slate gray"
            },
            "Nordic Coffee Table": {
                "dimensions": "48 inches (W) x 24 inches (D) x 18 inches (H)",
                "materials": "Walnut wood, tempered glass top",
                "weight": "45 lbs",
                "color": "Natural wood"
            },
            "Minimalist Floor Lamp": {
                "dimensions": "72 inches (H) x 12 inches (W) base",
                "materials": "Brushed brass, steel",
                "weight": "15 lbs",
                "color": "Brass"
            }
        }

        product_info = product_database.get(product_name)
        if product_info:
            details = [f"{key.capitalize()}: {value}" for key, value in product_info.items()]
            return f"Product details for {product_name}:\n" + "\n".join(details)
        else:
            return f"Product '{product_name}' not found. Please provide a valid product name."