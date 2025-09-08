import requests
from typing import List, Dict

class EcommerceAPIClient:
    """
    A client to interact with the e-commerce API.
    This class handles all HTTP requests to an external service,
    encapsulating the logic for fetching and sending data.
    """

    def __init__(self, base_url: str):
        """Initializes the API client with a base URL."""
        self.base_url = base_url
        print(f"EcommerceAPIClient initialized for URL: {self.base_url}")

    def get_order_status(self, order_id: str) -> Dict:
        """
        Fetches the status of a specific order from the e-commerce API.
        
        Args:
            order_id (str): The unique identifier for the order.
            
        Returns:
            Dict: A dictionary containing the order status details.
        """
        url = f"{self.base_url}/orders/{order_id}/status"
        print(f"Calling API to get status for order ID: {order_id} at {url}")
        
        try:
            response = requests.get(url)
            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()  
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching order status: {e}")
            return {"status": "error", "message": "Failed to fetch order status."}

    def add_to_cart(self, product_id: str, quantity: int) -> str:
        """
        Adds a product to the user's cart via the API.
        
        Args:
            product_id (str): The unique identifier for the product.
            quantity (int): The number of units to add.
            
        Returns:
            str: A confirmation message.
        """
        url = f"{self.base_url}/cart/add"
        payload = {"product_id": product_id, "quantity": quantity}
        print(f"Calling API to add product {product_id} (x{quantity}) to cart at {url}")
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error adding to cart: {e}")
            return "Failed to add product to cart."

    def initiate_return(self, order_id: str) -> str:
        """
        Initiates a return for a specific order via the API.
        
        Args:
            order_id (str): The unique identifier for the order.
            
        Returns:
            str: A confirmation message for the return request.
        """
        url = f"{self.base_url}/returns/initiate"
        payload = {"order_id": order_id}
        print(f"Calling API to initiate return for order ID: {order_id} at {url}")
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return f"Return for order '{order_id}' has been initiated."
        except requests.exceptions.RequestException as e:
            print(f"Error initiating return: {e}")
            return "Failed to initiate return."
    
    def search_products(self, query: str) -> List[Dict]:
        """
        Searches for products based on a query.
        
        Args:
            query (str): The search query.
            
        Returns:
            List[Dict]: A list of product dictionaries matching the query.
        """
        url = f"{self.base_url}/products/search"
        params = {"q": query}
        print(f"Calling API to search for products with query: {query} at {url}")
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching for products: {e}")
            return []

if __name__ == "__main__":
    
    client = EcommerceAPIClient(base_url="http://127.0.0.1:8001")
    
    print("\n--- Testing get_order_status ---")
    order_status = client.get_order_status(order_id="12345")
    print(f"Order Status: {order_status}")
    
    print("\n--- Testing add_to_cart ---")
    cart_status = client.add_to_cart(product_id="p-001", quantity=2)
    print(f"Add to Cart Status: {cart_status}")
    
    print("\n--- Testing initiate_return ---")
    return_status = client.initiate_return(order_id="12345")
    print(f"Return Status: {return_status}")
    
    print("\n--- Testing search_products ---")
    search_results = client.search_products("sofa")
    print(f"Search Results: {search_results}")