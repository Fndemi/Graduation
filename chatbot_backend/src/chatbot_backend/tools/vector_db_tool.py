from typing import Type, Optional
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import sys
import os

# Add the project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, project_root)

from services.vector_store import VectorStoreClient

class VectorDBTool(BaseTool):
    """
    A tool for querying the vector database to find relevant documents.
    """
    name: str = "vector_db_query"
    description: str = (
        "Useful for answering questions about product information, specifications, "
        "and frequently asked questions (FAQs). "
        "Input should be a detailed, natural language question."
    )
    
    # Define the input schema for the tool
    class VectorDBToolInput(BaseModel):
        query: str = Field(..., description="The query string to search for in the vector database.")
        
    args_schema: Type[BaseModel] = VectorDBToolInput

    def _run(self, query: str, run_manager: Optional[any] = None) -> str:
        """
        Executes the vector database query and returns a formatted string of results.
        """
        try:
            vector_store_client = VectorStoreClient()
            results = vector_store_client.query(query)
            
            if not results or not results.get('documents') or not results['documents'][0]:
                return "No relevant documents found in the vector database."
            
            # Format results for the agent to use
            formatted_results = ""
            for i, doc in enumerate(results['documents'][0]):
                source = results['metadatas'][0][i].get('source', 'unknown')
                doc_id = results['metadatas'][0][i].get('id', 'unknown')
                
                formatted_results += f"Source: {source} (ID: {doc_id})\nContent: {doc}\n\n"
            
            return formatted_results.strip()
            
        except Exception as e:
            return f"An error occurred while querying the vector database: {e}"

if __name__ == '__main__':
    # This block demonstrates how the tool works independently
    tool = VectorDBTool()
    search_query = "What is the Bohemian Jute & Wool Area Rug made of?"
    results = tool.run({"query": search_query})
    print(f"Tool execution for query: '{search_query}'\n")
    print("Results:")
    print(results)
    
    print("\n---\n")
    
    search_query_faq = "What is the return policy for orders?"
    results_faq = tool.run({"query": search_query_faq})
    print(f"Tool execution for query: '{search_query_faq}'\n")
    print("Results:")
    print(results_faq)