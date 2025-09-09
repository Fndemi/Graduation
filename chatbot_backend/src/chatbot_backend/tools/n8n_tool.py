import os
import json
import requests
from typing import Type
from langchain.tools import tool
from datetime import datetime

N8N_WEBHOOK_URL: str = "https://directedjeremiah.app.n8n.cloud/webhook/a62a7cb9-8b1d-4eab-8c26-0505bf3bc4c5"

@tool
def send_customer_details(name: str, phone: str, email: str, product: str, location: str) -> str:
    """
    Useful for sending customer and product details to an external workflow for follow-up.
    This is the only tool that can handle requests for sending information, like
    requesting a return, refund, or connecting with a representative.
    When using this tool, make sure to get the customer's name, email, phone,
    the product they're asking about, and their location before invoking it.
    
    Args:
        name: The customer's full name.
        phone: The customer's phone number.
        email: The customer's email address.
        product: The name of the product the customer is interested in.
        location: The customer's city or location.
    """
    payload = {
        "name": name,
        "phone": phone,
        "email": email,
        "product": product,
        "location": location,
        "date": datetime.now().isoformat()
    }
    
    try:
        print(f"Calling n8n webhook at {N8N_WEBHOOK_URL} with payload: {payload}")
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=5)
        response.raise_for_status()
        
        response_data = response.json()
        return f"Successfully sent customer details to workflow. N8n response: {json.dumps(response_data)}"
        
    except requests.exceptions.Timeout:
        return "Error: Request to n8n workflow timed out. The workflow may still be processing."
    except requests.exceptions.RequestException as e:
        return f"Error: Failed to send customer details to n8n workflow. Details: {e}"
    
N8N_PRODUCT_WEBHOOK_URL = "https://directedjeremiah.app.n8n.cloud/webhook/550cd07c-bd08-4733-98fa-ab0ba66fcda8"

@tool
def send_product_info(product_name: str, product_description: str) -> str:
    """
    Sends product information to a separate n8n workflow.

    Args:
        product_name: Name of the product.
        product_description: Description of the product.
    """
    payload = {
        "product_name": product_name,
        "product_description": product_description,
        "date": datetime.now().isoformat()
    }

    try:
        print(f"Sending payload to {N8N_PRODUCT_WEBHOOK_URL}: {payload}")
        response = requests.post(N8N_PRODUCT_WEBHOOK_URL, json=payload, timeout=5)
        response.raise_for_status()
        response_data = response.json()
        return f"Successfully sent product info. n8n response: {json.dumps(response_data)}"
    except requests.exceptions.Timeout:
        return "Error: Request timed out."
    except requests.exceptions.RequestException as e:
        return f"Error: Failed to send product info. Details: {e}"

if __name__ == '__main__':
    print("Testing sending customer details to workflow:")
    customer_data = {
        "name": "Alex Johnson",
        "phone": "555-555-5555",
        "email": "alex.johnson@example.com",
        "product": "Linen Sofa",
        "location": "Miami"
    }
    
    result = send_customer_details(**customer_data)
    print("Results:")
    print(result)

    print("\n---\n")
    
    # Test case with invalid data (the agent would be responsible for this validation)
    print("This is how the tool would handle an error:")
    try:
        invalid_data = {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "product": "Velvet Armchair",
            "location": "Los Angeles"
        }
        send_customer_details(**invalid_data)
    except Exception as e:
        print(f"Caught expected error: {e}")