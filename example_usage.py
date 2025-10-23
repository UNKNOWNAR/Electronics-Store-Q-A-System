"""
Example usage of the Vector Embedding Manager for Electronics Store Q&A System
"""

from vector_embeddings import VectorEmbeddingManager


def demonstrate_vector_search():
    """
    Demonstrate how to use the vector embedding system for question similarity search
    """
    # Initialize the embedding manager
    print("Initializing Vector Embedding Manager...")
    embedding_manager = VectorEmbeddingManager()

    # Check if we have data in the collection
    info = embedding_manager.get_collection_info()
    print(f"Collection has {info['total_documents']} documents")

    # If no data, create embeddings from few shots
    if info["total_documents"] == 0:
        print("No data found. Creating embeddings from few shots...")
        embedding_manager.create_embeddings_from_few_shots()

    # Example queries to test similarity search
    test_queries = [
        "How many Samsung phones do we have?",
        "What's the total price of all laptops?",
        "Show me products with discounts over 10%",
        "How much money will we make from Apple products?",
        "What's the average price of smartwatches?",
        "How many headphones are in stock?",
        "What's the total inventory value?",
        "How many Dell laptops can we sell?",
    ]

    print("\n" + "=" * 80)
    print("SIMILARITY SEARCH RESULTS")
    print("=" * 80)

    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        print("-" * 60)

        # Search for similar questions
        results = embedding_manager.search_similar_questions(query, n_results=2)

        if results["documents"] and results["documents"][0]:
            for i, (doc, metadata, distance) in enumerate(
                zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0],
                )
            ):
                similarity_score = 1 - distance
                print(f"\n📋 Match {i + 1} (Similarity: {similarity_score:.3f})")
                print(f"   Original Question: {metadata['question']}")
                print(f"   Answer: {metadata['answer']}")
                print(f"   SQL Query: {metadata['sql_query']}")
        else:
            print("   No similar questions found.")


def demonstrate_metadata_retrieval():
    """
    Demonstrate how to retrieve specific metadata from the vector database
    """
    print("\n" + "=" * 80)
    print("METADATA RETRIEVAL DEMONSTRATION")
    print("=" * 80)

    embedding_manager = VectorEmbeddingManager()

    # Search for questions about specific brands
    brand_queries = ["Samsung", "Apple", "Dell"]

    for brand in brand_queries:
        print(f"\n🏷️  Searching for questions about {brand}:")
        results = embedding_manager.search_similar_questions(
            f"questions about {brand}", n_results=3
        )

        if results["documents"] and results["documents"][0]:
            for i, (doc, metadata, distance) in enumerate(
                zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0],
                )
            ):
                if (
                    brand.lower() in metadata["question"].lower()
                    or brand.lower() in metadata["sql_query"].lower()
                ):
                    print(f"   • {metadata['question']}")
                    print(f"     Answer: {metadata['answer']}")


if __name__ == "__main__":
    print("🚀 Electronics Store Q&A Vector Embedding System")
    print("=" * 50)

    # Run demonstrations
    demonstrate_vector_search()
    demonstrate_metadata_retrieval()

    print("\n✅ Demonstration completed!")
    print("\nTo use this system in your application:")
    print("1. Import VectorEmbeddingManager from vector_embeddings")
    print("2. Initialize: manager = VectorEmbeddingManager()")
    print("3. Search: results = manager.search_similar_questions('your question')")
    print("4. Access results: results['metadatas'][0] for metadata")
