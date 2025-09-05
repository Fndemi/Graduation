from typing import Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

# Mock data to simulate n8n workflow responses
MOCK_WORKFLOW_DB = {
    "initiate_return": {
        "success": True,
        "message": "Return workflow successfully initiated. A return label has been sent to the customer's email.",
        "return_id": "RET-09876"
    }
}

class N8NTool(BaseTool):
    """
    A tool for triggering external n8n workflows.
    """
    name = "n8n_workflow_trigger"
    description = (
        "Useful for initiating automated workflows for tasks like processing returns or refunds. "
        "Input should be the name of the workflow to trigger and any required data."
    )

    # Define the input schema for the tool
    class N8NToolInput(BaseModel):
        workflow_name: str = Field(..., description="The name of the n8n workflow to trigger (e.g., 'initiate_return').")
        data: dict = Field(..., description="A dictionary of data required for the workflow (e.g., {'order_id': 'ORD-12345'}).")

    args_schema: Type[BaseModel] = N8NToolInput

    def _run(self, workflow_name: str, data: dict) -> str:
        """
        Triggers a mock n8n workflow and returns a formatted response.
        """
        try:
            workflow_response = MOCK_WORKFLOW_DB.get(workflow_name)
            
            if not workflow_response:
                return f"Error: n8n workflow '{workflow_name}' not found."

            # Format the response for the agent
            formatted_response = f"n8n Workflow Triggered: '{workflow_name}'\n"
            formatted_response += f"Status: {'Success' if workflow_response['success'] else 'Failure'}\n"
            formatted_response += f"Message: {workflow_response['message']}\n"
            
            # Include specific data from the workflow response if available
            for key, value in workflow_response.items():
                if key not in ['success', 'message']:
                    formatted_response += f"{key.replace('_', ' ').title()}: {value}\n"
            
            return formatted_response.strip()

        except Exception as e:
            return f"An error occurred while triggering the n8n workflow: {e}"

if __name__ == '__main__':
    # This block demonstrates how the tool works independently
    tool = N8NTool()
    
    # Test case for a valid workflow trigger
    workflow_name_valid = "initiate_return"
    data_valid = {"order_id": "ORD-12345"}
    results_valid = tool.run(workflow_name=workflow_name_valid, data=data_valid)
    print(f"Tool execution for workflow: '{workflow_name_valid}' with data: {data_valid}\n")
    print("Results:")
    print(results_valid)
    
    print("\n---\n")
    
    # Test case for a non-existent workflow
    workflow_name_invalid = "process_refund"
    data_invalid = {"order_id": "ORD-67890"}
    results_invalid = tool.run(workflow_name=workflow_name_invalid, data=data_invalid)
    print(f"Tool execution for workflow: '{workflow_name_invalid}' with data: {data_invalid}\n")
    print("Results:")
    print(results_invalid)
