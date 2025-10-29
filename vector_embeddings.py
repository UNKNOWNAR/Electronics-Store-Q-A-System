import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import json
from few_shots import few_shots
import os

# Import from your config file
from config import VECTOR_DB_CONFIG, SIMILARITY_CONFIG


class VectorEmbeddingManager:
    def __init__(self):
        """
        Initialize the vector embedding manager with Chroma database
        (NOW USES CONFIG)
        """
        self.db_path = VECTOR_DB_CONFIG["db_path"]
        self.collection_name = VECTOR_DB_CONFIG["collection_name"]
        self.model_name = SIMILARITY_CONFIG["embedding_model"]

        # Initialize sentence transformer model for embeddings
        self.embedding_model = SentenceTransformer(self.model_name)

        # Initialize Chroma client
        self.client = chromadb.PersistentClient(
            path=self.db_path,
            settings=Settings(anonymized_telemetry=False, allow_reset=True),
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name, metadata={"hnsw:space": "cosine"}
        )

    def create_embeddings_from_few_shots(self):
        """
        Create vector embeddings from few shots data and store in Chroma database
        """
        print("Creating embeddings from few shots data...")

        # Prepare data for embedding
        documents = []
        metadatas = []
        ids = []

        for i, shot in enumerate(few_shots):
            # The document we embed should *only* be the question
            # to match what the user will search for.
            documents.append(shot["Question"])

            # Create metadata with all information
            metadata = {
                "question": shot["Question"],
                "sql_query": shot["SQLQuery"],
                "sql_result": shot["SQLResult"],
                "answer": shot["Answer"],
                "index": i,
            }
            metadatas.append(metadata)

            # Create unique ID
            ids.append(f"few_shot_{i}")

        # Generate embeddings
        print(f"Generating embeddings using '{self.model_name}'...")
        embeddings = self.embedding_model.encode(documents).tolist()

        # Add to Chroma collection
        print("Storing embeddings in Chroma database...")
        self.collection.add(
            embeddings=embeddings, documents=documents, metadatas=metadatas, ids=ids
        )

        print(f"Successfully stored {len(documents)} embeddings in Chroma database")
        return len(documents)

    def search_similar_questions(self, query, n_results=None):
        """
        Search for similar questions in the database

        Args:
            query (str): The question to search for
            n_results (int): Number of similar results to return.
                             Defaults to value from config.

        Returns:
            list: List of similar questions with metadata
        """
        if n_results is None:
            n_results = SIMILARITY_CONFIG["max_results"]

        # Generate embedding for the query
        query_embedding = self.embedding_model.encode([query]).tolist()

        # Search in Chroma database
        results = self.collection.query(
            query_embeddings=query_embedding, n_results=n_results
        )

        return results

    def get_collection_info(self):
        """
        Get information about the collection
        """
        count = self.collection.count()
        return {
            "collection_name": self.collection_name,
            "total_documents": count,
            "db_path": self.db_path,
        }

    def reset_collection(self):
        """
        Reset the collection (delete all data)
        """
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name, metadata={"hnsw:space": "cosine"}
        )
        print(f"Collection '{self.collection_name}' has been reset")


def main():
    """
    Main function to create and test the vector embeddings
    """
    # Initialize the vector embedding manager
    embedding_manager = VectorEmbeddingManager()

    # Reset collection for a clean start (optional)
    # embedding_manager.reset_collection()

    # Create embeddings from few shots data
    num_embeddings = embedding_manager.create_embeddings_from_few_shots()

    # Get collection info
    info = embedding_manager.get_collection_info()
    print(f"\nCollection Info:")
    print(f"Name: {info['collection_name']}")
    print(f"Total documents: {info['total_documents']}")
    print(f"Database path: {info['db_path']}")

    # Test search functionality
    print("\n" + "=" * 50)
    print("Testing search functionality:")
    print("=" * 50)

    test_queries = [
        "How many Samsung phones are available?",
        "What is the total value of laptops?",
        "Which products have discounts?",
        "How much revenue from Apple products?",
    ]

    # Use default n_results from config
    n_results = SIMILARITY_CONFIG["max_results"]

    for query in test_queries:
        print(f"\nQuery: {query}")
        results = embedding_manager.search_similar_questions(query, n_results=n_results)

        if results["documents"] and results["documents"][0]:
            for i, (doc, metadata, distance) in enumerate(
                zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0],
                )
            ):
                print(f"  Result {i + 1} (similarity: {1 - distance:.3f}):")
                print(f"    Question: {metadata['question']}")
                print(f"    Answer: {metadata['answer']}")
                print(f"    SQL: {metadata['sql_query'][:100]}...")
                print()


if __name__ == "__main__":
    main()