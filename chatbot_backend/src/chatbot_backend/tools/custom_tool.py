import os
import random
import requests
import json
import sys
from typing import Optional, Any
from langchain.tools import tool
from pydantic import BaseModel, Field

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)
from services.vector_store import VectorStoreClient
from services.api_client import EcommerceAPIClient

# Initialize the API client once at the top level for use in tools
api_client = EcommerceAPIClient(base_url="http://127.0.0.1:8001")


# --- Tools with the @tool decorator ---

@tool
def track_order(order_id: str) -> str:
    """
    A tool to track the status of an order using an external API.
    The order ID can be any valid order number, for example: '12345' or '67890'.
    """
    if not order_id:
        return "Please provide a valid order ID."
    
    response = api_client.get_order_status(order_id)
    
    if response and response.get("status") == "error":
        return response.get("message", "Could not retrieve order details.")
    
    status = response.get("status", "N/A")
    carrier = response.get("carrier", "N/A")
    tracking_number = response.get("tracking_number", "N/A")
    estimated_delivery = response.get("estimated_delivery", "N/A")
    
    return (
        f"Order Status: {status}\n"
        f"Carrier: {carrier}\n"
        f"Tracking Number: {tracking_number}\n"
        f"Estimated Delivery: {estimated_delivery}"
    )

@tool
def get_style_recommendations(query: str) -> str:
    """
    A tool to provide product recommendations based on user style and preferences.
    Pass the query as a simple string containing customer preferences.
    """
    actual_query = query or "general home decor recommendations"
    
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

@tool
def get_product_info(query: str) -> str:
    """
    Useful for answering questions about product information, specifications, 
    and frequently asked questions (FAQs).
    Input should be a detailed, natural language query string.
    """
    try:
        client = VectorStoreClient()
        
        # The tool now infers the document type based on the query if needed,
        # or can be explicitly called by the agent to search for 'product' or 'faq'
        # based on the prompt's instructions.
        where_filter = None 
        if "faq" in query.lower() or "question" in query.lower():
            where_filter = {"source": "faq"}
        elif "product" in query.lower() or "item" in query.lower():
            where_filter = {"source": "product"}
            
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


# Example of how the tools can be used for testing
if __name__ == '__main__':
    # Test the OrderTrackingTool with a valid order ID from your db.json
    print("--- Testing OrderTrackingTool with a valid order ID ---")
    print(track_order("12345"))

    print("\n--- Testing OrderTrackingTool with an invalid order ID ---")
    print(track_order("INVALID-ID"))