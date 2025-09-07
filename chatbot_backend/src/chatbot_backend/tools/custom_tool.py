import random
import requests
import os
import json
import sys
from crewai.tools import BaseTool
from typing import Optional, Type, Any
from pydantic import BaseModel, Field

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)
from services.vector_store import VectorStoreClient

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
    product_name: str = Field(..., description="The name of the product or a description to get information for.")

# --- Tools ---
class OrderTrackingTool(BaseTool):
    name: str = "Order Tracking Tool"
    description: str = "A tool to track the status of an order using an external API."
    args_schema: Type[BaseModel] = OrderTrackingInput
    
    def _run(self, order_id: str, run_manager: Optional[Any] = None) -> str:
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
        if "damaged" in query.lower():
            return f"Return process for '{query}' has been initiated. A shipping label has been sent to your email. Please use a padded box and mark it as 'Damaged - Do Not Resell'."
        else:
            return f"Return process for '{query}' has been initiated. A shipping label has been sent to your email. Your refund will be processed within 5-7 business days after we receive and inspect the item."

class VectorDBTool(BaseTool):
    """
    A tool for querying the vector database to find relevant documents.
    """
    name: str = "Product Info Tool"
    description: str = (
        "Useful for answering questions about product information, specifications, "
        "and frequently asked questions (FAQs). "
        "Input should be a detailed, natural language query string."
        "The tool can also filter the search by document type (e.g., 'product' or 'faq')."
    )

    class VectorDBToolInput(BaseModel):
        query: str = Field(..., description="The natural language question or query to search for.")
        document_type: Optional[str] = Field(None, description="Optional filter to specify the type of document to search, e.g., 'product' or 'faq'.")
    
    args_schema: Type[BaseModel] = VectorDBToolInput

    def _run(self, query: str, document_type: Optional[str] = None) -> str:
        try:
            client = VectorStoreClient()
            
            where_filter = {"source": document_type} if document_type else None
            
            results = client.query(query, n_results=5, where_filter=where_filter)
            
            if not results:
                return "No relevant documents found in the vector database."
            
            formatted_results = ""
            for doc in results:
                source = doc['metadata'].get('source', 'unknown')
                
                if source == 'product':
                    name = doc['metadata'].get('name', 'N/A')
                    category = doc['metadata'].get('category', 'N/A')
                    price = doc['metadata'].get('price', 'N/A')
                    content = doc['document']
                    
                    formatted_results += (
                        f"--- Product Match ---\n"
                        f"Name: {name}\n"
                        f"Category: {category}\n"
                        f"Price: {price}\n"
                        f"Details: {content}\n\n"
                    )
                elif source == 'faq':
                    content = doc['document']
                    formatted_results += (
                        f"--- FAQ Match ---\n"
                        f"Content: {content}\n\n"
                    )
                else:
                    formatted_results += f"Source: {source}\nContent: {doc['document']}\n\n"
            
            return formatted_results.strip()
            
        except Exception as e:
            return f"An error occurred while querying the vector database: {e}"