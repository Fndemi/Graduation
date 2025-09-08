import os
from crewai.tools import BaseTool
from services.api_client import EcommerceAPIClient

# Initialize the API client once at the top level
api_client = EcommerceAPIClient(base_url="http://127.0.0.1:8001")

class OrderApiTool(BaseTool):
    name: str = "Order Tracking Tool"
    description: str = (
        "Useful for tracking the status of a customer's order. "
        "The input to this tool must be a string representing the order ID, "
        "for example 'ORD-87654'."
    )

    def _run(self, order_id: str) -> str:
        """
        Fetches the order status from the E-commerce API.
        The order ID can be any valid order number, for example: '12345' or '67890'.
        
        Args:
            order_id (str): The unique identifier of the order.
            
        Returns:
            str: A formatted string containing the order status details.
        """
        response = api_client.get_order_status(order_id)
        
        if response and response.get("status") == "error":
            return response.get("message", "Could not retrieve order details.")
        
        status = response.get("status", "N/A")
        tracking = response.get("tracking_number", "N/A")
        carrier = response.get("carrier", "N/A")
        delivery = response.get("estimated_delivery", "N/A")
        
        return (
            f"Order Status: {status}\n"
            f"Carrier: {carrier}\n"
            f"Tracking Number: {tracking}\n"
            f"Estimated Delivery: {delivery}"
        )

# Example of how the tool can be used, for testing purposes.
if __name__ == '__main__':
    tool = OrderApiTool()
    # Test a valid order ID from your db.json
    print("Testing with a valid order ID:")
    result = tool.run("12345")
    print(result)

    print("\nTesting with an invalid order ID:")
    result_invalid = tool.run("INVALID-ID")
    print(result_invalid)