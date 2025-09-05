import json
import os
import glob
from typing import List, Dict

from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from chromadb.utils import embedding_functions

class VectorStoreClient:
    """
    A client to handle all vector database interactions for the chatbot.
    """
    
    def __init__(self, db_path: str = "./knowledge/vector_db"):
        """Initializes the vector database client and embedding model."""
        try:
            print("Initializing SentenceTransformer model...")
            self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
            self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )

            print("Initializing ChromaDB persistent client...")
            self.client = PersistentClient(path=db_path)
            
            # The collection is created or retrieved here
            self.collection = self.client.get_or_create_collection(
                name="products_and_faqs",
                embedding_function=self.embedding_function
            )
            print(f"Vector store collection '{self.collection.name}' is ready.")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize VectorStoreClient: {e}")

    def _process_document(self, file_path: str) -> List[Dict]:
        """
        Processes documents from a given file path, supporting JSON and other formats.
        Returns a list of dictionaries with 'id', 'document', and 'metadata'.
        """
        documents_to_ingest = []
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for doc in data:
                doc_type = doc.get("type", "unknown")
                text_content = ""
                metadata = {}
                
                if doc_type == "product":
                    text_content = (
                        f"Product Name: {doc.get('name', '')}. "
                        f"Description: {doc.get('description', '')}. "
                        f"Attributes: {json.dumps(doc.get('attributes', {}))}"
                    )
                    metadata = {
                        "source": "product",
                        "name": doc.get('name', ''),
                        "category": doc.get('category', 'General'),
                        "id": doc.get('id', '')
                    }
                elif doc_type == "faq":
                    text_content = f"Question: {doc.get('question', '')}. Answer: {doc.get('answer', '')}"
                    metadata = {
                        "source": "faq",
                        "category": doc.get('category', 'General'),
                        "id": doc.get('id', '')
                    }
                
                if text_content and doc.get("id"):
                    documents_to_ingest.append({
                        "id": str(doc["id"]),
                        "document": text_content,
                        "metadata": metadata,
                    })
        else:
            print(f"Warning: Unsupported file type '{file_extension}'. Skipping {file_path}")
            
        return documents_to_ingest

    def ingest_data(self, knowledge_dir: str):
        """Loads and ingests all supported documents from a directory into the vector store."""
        print(f"Starting data ingestion from directory: {knowledge_dir}")

        # Delete all documents in the collection before a fresh ingestion
        print("Clearing existing data from the vector store...")
        try:
            # The empty `where` clause tells ChromaDB to delete everything.
            self.collection.delete(where={})
            print("Successfully cleared all existing data.")
        except Exception as e:
            print(f"Failed to clear existing data: {e}. Attempting to proceed with ingestion.")
        
        all_documents = []
        for file_path in glob.glob(os.path.join(knowledge_dir, "**/*"), recursive=True):
            if os.path.isfile(file_path):
                all_documents.extend(self._process_document(file_path))

        if not all_documents:
            print("No documents found to ingest.")
            return

        print(f"Processing and preparing {len(all_documents)} documents for ingestion...")
        
        ids = [doc['id'] for doc in all_documents]
        documents = [doc['document'] for doc in all_documents]
        metadatas = [doc['metadata'] for doc in all_documents]

        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Successfully ingested {len(ids)} documents into the vector store.")

    def query(self, query_text: str, n_results: int = 5, where_filter: dict = None) -> List[Dict]:
        """
        Queries the vector store for similar documents with optional metadata filtering.
        """
        print(f"Querying vector store for: '{query_text}' with filter: {where_filter}")
        
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=where_filter
            )
            
            # Format the output for easier use by the agents
            formatted_results = []
            for i, doc in enumerate(results["documents"][0]):
                formatted_results.append({
                    "id": results["ids"][0][i],
                    "document": doc,
                    "metadata": results["metadatas"][0][i],
                    "score": results["distances"][0][i]
                })
            
            return formatted_results
        
        except Exception as e:
            print(f"An error occurred during vector store query: {e}")
            return []

# Example usage:
if __name__ == "__main__":
    try:
        client = VectorStoreClient()
        knowledge_dir = "./knowledge"
        
        # Ingest data from the knowledge directory
        client.ingest_data(knowledge_dir)
        
        # Example 1: Query for product information
        product_results = client.query("velvet armchair dimensions")
        print("\nProduct Query Results:")
        for result in product_results:
            print(f"- [Score: {result['score']:.2f}] Document: {result['document'][:70]}... ID: {result['id']}")
            
        # Example 2: Query for FAQs using a metadata filter
        faq_results = client.query("how do I clean my new sofa?", where_filter={"source": "faq"})
        print("\nFAQ Query Results:")
        for result in faq_results:
            print(f"- [Score: {result['score']:.2f}] Document: {result['document'][:70]}... ID: {result['id']}")

    except Exception as e:
        print(f"A fatal error occurred: {e}")