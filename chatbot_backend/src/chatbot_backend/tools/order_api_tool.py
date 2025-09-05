#This tool provides an interface for AI agents to query a mock e-commerce API.
#It is designed to be used within a CrewAI or LangChain agentic framework.
from typing import Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

# Mock data to simulate an external API response
MOCK_ORDERS_DB = {
    "ORD-87654": {
        "status": "Shipped",
        "product_id": "PROD-203",
        "product_name": "Modern Leather Armchair",
        "shipping_carrier": "FedEx",
        "tracking_number": "1Z9999999999999999",
        "estimated_delivery": "2024-09-20"
    },
    "ORD-12345": {
        "status": "Delivered",
        "product_id": "PROD-101",
        "product_name": "Bohemian Jute & Wool Area Rug",
        "delivery_date": "2024-09-01"
    },
    "ORD-99887": {
        "status": "Processing",
        "product_id": "PROD-405",
        "product_name": "Vintage Industrial Bookshelf",
        "estimated_delivery": "2024-09-25"
    }
}

class OrderTrackingTool(BaseTool):
    """
    A tool for tracking the status of an e-commerce order.
    """
    name = "order_tracking"
    description = (
        "Useful for fetching the status and details of a customer's order. "
        "Input should be a valid order ID, e.g., 'ORD-87654'."
    )

    # Define the input schema for the tool
    class OrderTrackingToolInput(BaseModel):
        order_id: str = Field(..., description="The unique identifier for the order (e.g., 'ORD-12345').")

    args_schema: Type[BaseModel] = OrderTrackingToolInput

    def _run(self, order_id: str) -> str:
        """
        Retrieves order information from the mock database.
        """
        try:
            order_info = MOCK_ORDERS_DB.get(order_id.upper())
            if not order_info:
                return f"Order with ID '{order_id}' not found."

            # Format the order information for the agent
            formatted_info = f"Order ID: {order_id}\n"
            for key, value in order_info.items():
                formatted_info += f"{key.replace('_', ' ').title()}: {value}\n"
            
            return formatted_info.strip()

        except Exception as e:
            return f"An error occurred while fetching order details: {e}"


if __name__ == '__main__':
    # This block demonstrates how the tool works independently
    tool = OrderTrackingTool()
    
    # Test case for a valid order
    order_id_valid = "ORD-87654"
    results_valid = tool.run(order_id=order_id_valid)
    print(f"Tool execution for query: '{order_id_valid}'\n")
    print("Results:")
    print(results_valid)
    
    print("\n---\n")
    
    # Test case for a non-existent order
    order_id_invalid = "ORD-00000"
    results_invalid = tool.run(order_id=order_id_invalid)
    print(f"Tool execution for query: '{order_id_invalid}'\n")
    print("Results:")
    print(results_invalid)
