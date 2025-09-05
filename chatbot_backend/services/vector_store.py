import json
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from chromadb.utils import embedding_functions

class VectorStoreClient:
    """
    A client to handle all vector database interactions.
    """
    def __init__(self, db_path: str = "./knowledge/vector_db"):
        print("Initializing SentenceTransformer model...")
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        
        print("Initializing ChromaDB persistent client...")
        self.client = PersistentClient(path=db_path)
        
        print("Creating or getting 'products' collection...")
        self.collection = self.client.get_or_create_collection(
            name="products",
            embedding_function=self.embedding_function
        )
        
    def _process_document(self, doc: dict) -> dict:
        """Helper function to process and prepare a single document for ingestion."""
        text_content = ""
        metadata = {}
        
        doc_type = doc.get("type", "unknown")
        
        if doc_type == "product":
            text_content = f"Product Name: {doc.get('name', '')}. Description: {doc.get('description', '')}"
            for attr, value in doc.get("attributes", {}).items():
                text_content += f" {attr}: {value}."
            
            metadata = {
                "source": doc_type,
                "name": doc.get('name', ''),
                "category": doc.get('category', 'General'),
                "id": doc.get('id', '')
            }
        elif doc_type == "faq":
            text_content = f"Question: {doc.get('question', '')}. Answer: {doc.get('answer', '')}"
            metadata = {
                "source": doc_type,
                "category": doc.get('category', 'General'),
                "id": doc.get('id', '')
            }
        
        return {
            "id": doc.get("id"),
            "document": text_content,
            "metadata": metadata,
        }

    def ingest_data(self, file_path: str):
        """Loads and ingests data from a JSON file into the vector store."""
        print("Loading product data...")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        print("Processing and preparing data for ingestion...")
        documents_to_ingest = [self._process_document(doc) for doc in data]
        
        ids = [doc['id'] for doc in documents_to_ingest]
        documents = [doc['document'] for doc in documents_to_ingest]
        metadatas = [doc['metadata'] for doc in documents_to_ingest]
        
        # New: Check if the collection has any documents before attempting to delete.
        existing_ids = self.collection.get()["ids"]
        if existing_ids:
            self.collection.delete(ids=existing_ids)
            print(f"Deleted {len(existing_ids)} existing documents.")
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Ingested {len(ids)} documents into the vector store.")

    def query(self, query_text: str, n_results: int = 5) -> list:
        """Queries the vector store for similar documents."""
        print(f"Querying vector store for: '{query_text}'")
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results

# Example usage:
if __name__ == "__main__":
    try:
        client = VectorStoreClient()
        client.ingest_data("./knowledge/products.json")
        
        results = client.query("velvet armchair material and dimensions")
        print("\nQuery Results:")
        for result in results["documents"][0]:
            print(f"- {result}")
    except Exception as e:
        print(f"An error occurred: {e}")
