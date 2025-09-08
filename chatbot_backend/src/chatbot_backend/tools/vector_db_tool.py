from typing import Type, Optional
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import sys
import os
import json

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)

from services.vector_store import VectorStoreClient

_shared_client = None

class VectorDBTool(BaseTool):
    """
    A tool for querying the vector database to find relevant documents.
    """
    name: str = "vector_db_query"
    description: str = (
        "Useful for answering questions about product information, specifications, "
        "and frequently asked questions (FAQs). "
        "Input should be a detailed, natural language query string."
        "The tool can also filter the search by document type (e.g., 'product' or 'faq')."
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global _shared_client
        if _shared_client is None:
            print("Initializing shared VectorStoreClient...")
            _shared_client = VectorStoreClient()
            try:
                knowledge_dir = os.path.join(project_root, 'knowledge')
                _shared_client.ingest_data(knowledge_dir)
            except Exception as e:
                print(f"Warning: Data ingestion failed during tool initialization. Vector store may be empty. Error: {e}")

    class VectorDBToolInput(BaseModel):
        query: str = Field(..., description="The natural language question or query to search for.")
        document_type: Optional[str] = Field(None, description="Optional filter to specify the type of document to search, e.g., 'product' or 'faq'.")
    
    args_schema: Type[BaseModel] = VectorDBToolInput

    def _run(self, query: str, document_type: Optional[str] = None) -> str:
        """
        Executes the vector database query and returns a formatted string of results.
        """
        try:
            global _shared_client
            
            where_filter = {"source": document_type} if document_type else None
            
            results = _shared_client.query(query, n_results=5, where_filter=where_filter)
            
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

if __name__ == '__main__':
    tool = VectorDBTool()
    
    # Example 1
    search_query = "What is the Bohemian Jute & Wool Area Rug made of and what does it cost?"
    results = tool._run(query=search_query)
    print(f"\nTool execution for query: '{search_query}'\n")
    print("Results:")
    print(results)
    
    print("\n---\n")
    
    # Example 2
    search_query_faq = "What is the return policy for orders?"
    results_faq = tool._run(query=search_query_faq, document_type="faq")
    print(f"\nTool execution for query: '{search_query_faq}' with filter 'faq'\n")
    print("Results:")
    print(results_faq)