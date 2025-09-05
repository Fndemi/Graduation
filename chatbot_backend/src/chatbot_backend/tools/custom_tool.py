from typing import Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

# Define the input schema for the tool
class CustomToolInput(BaseModel):
    query: str = Field(..., description="The query string for the tool to process.")

class CustomTool(BaseTool):
    """
    A versatile tool for performing custom actions.
    """
    name = "custom_tool"
    description = (
        "Useful for performing any custom, non-standard actions that are not handled by other tools. "
        "Input should be a detailed, natural language query."
    )
    
    args_schema: Type[BaseModel] = CustomToolInput

    def _run(self, query: str) -> str:
        """
        Executes a mock custom action based on the query.
        """
        try:
            # Here you would implement your custom logic, such as calling an external API,
            # performing a unique calculation, or interacting with a new service.
            
            # This is a placeholder for your custom functionality.
            if "check stock" in query.lower():
                return "The product is in stock and ready to ship."
            if "find nearest store" in query.lower():
                return "The nearest store is located at 1234 Main Street, Anytown, USA."
            
            return f"The custom tool processed the query: '{query}' and returned a generic response."

        except Exception as e:
            return f"An error occurred while using the custom tool: {e}"

if __name__ == '__main__':
    # This block demonstrates how the tool works independently
    tool = CustomTool()
    
    # Test case for a stock check
    stock_query = "check stock for the vintage bookshelf"
    results_stock = tool.run(query=stock_query)
    print(f"Tool execution for query: '{stock_query}'\n")
    print("Results:")
    print(results_stock)
    
    print("\n---\n")
    
    # Test case for finding a store
    store_query = "find nearest store"
    results_store = tool.run(query=store_query)
    print(f"Tool execution for query: '{store_query}'\n")
    print("Results:")
    print(results_store)
