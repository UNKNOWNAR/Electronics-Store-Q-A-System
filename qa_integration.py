from vector_embeddings import VectorEmbeddingManager
import json


class ElectronicsQA:
    def __init__(self):
        """
        Initialize the Electronics Q&A system with vector embeddings
        """
        self.embedding_manager = VectorEmbeddingManager()

        # Check if we have embeddings, if not create them
        info = self.embedding_manager.get_collection_info()
        if info["total_documents"] == 0:
            print("Creating embeddings from few shots data...")
            self.embedding_manager.create_embeddings_from_few_shots()

    def find_similar_questions(self, user_question, top_k=3):
        """
        Find similar questions from the few shots data

        Args:
            user_question (str): The user's question
            top_k (int): Number of similar questions to return

        Returns:
            list: List of similar questions with metadata
        """
        results = self.embedding_manager.search_similar_questions(
            user_question, n_results=top_k
        )

        similar_questions = []
        if results["documents"] and results["documents"][0]:
            for i, (doc, metadata, distance) in enumerate(
                zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0],
                )
            ):
                similarity_score = 1 - distance
                similar_questions.append(
                    {
                        "question": metadata["question"],
                        "sql_query": metadata["sql_query"],
                        "answer": metadata["answer"],
                        "similarity_score": similarity_score,
                        "index": metadata["index"],
                    }
                )

        return similar_questions

    def get_best_match(self, user_question, threshold=0.5):
        """
        Get the best matching question if similarity is above threshold

        Args:
            user_question (str): The user's question
            threshold (float): Minimum similarity threshold (0-1)

        Returns:
            dict or None: Best match if above threshold, None otherwise
        """
        similar_questions = self.find_similar_questions(user_question, top_k=1)

        if similar_questions and similar_questions[0]["similarity_score"] >= threshold:
            return similar_questions[0]

        return None

    def suggest_sql_query(self, user_question):
        """
        Suggest a SQL query based on similar questions

        Args:
            user_question (str): The user's question

        Returns:
            dict: Contains suggested SQL query and confidence score
        """
        best_match = self.get_best_match(user_question, threshold=0.5)

        if best_match:
            return {
                "suggested_sql": best_match["sql_query"],
                "confidence": best_match["similarity_score"],
                "source_question": best_match["question"],
                "expected_answer": best_match["answer"],
            }

        return {
            "suggested_sql": None,
            "confidence": 0.0,
            "message": "No similar questions found. Consider adding more examples to few_shots.py",
        }


def demo_integration():
    """
    Demonstrate how to integrate the vector embeddings with your Q&A system
    """
    print("🔧 Electronics Store Q&A Integration Demo")
    print("=" * 50)

    # Initialize the Q&A system
    qa_system = ElectronicsQA()

    # Test questions
    test_questions = [
        "How many Samsung phones are in stock?",
        "What's the total value of all laptops?",
        "Show me products with big discounts",
        "How much money can we make from Apple products?",
        "What's the average price of smartwatches?",
        "How many headphones do we have?",
        "What's our total inventory worth?",
        "How many Dell laptops can we sell?",
    ]

    for question in test_questions:
        print(f"\n❓ User Question: '{question}'")
        print("-" * 60)

        # Get SQL suggestion
        suggestion = qa_system.suggest_sql_query(question)

        if suggestion["suggested_sql"]:
            print(
                f"✅ Suggested SQL Query (Confidence: {suggestion['confidence']:.3f}):"
            )
            print(f"   {suggestion['suggested_sql']}")
            print(f"📋 Based on: '{suggestion['source_question']}'")
            print(f"🎯 Expected Answer: {suggestion['expected_answer']}")
        else:
            print(f"❌ {suggestion['message']}")

        # Show similar questions
        similar = qa_system.find_similar_questions(question, top_k=2)
        if similar:
            print(f"\n🔍 Similar Questions Found:")
            for i, sim in enumerate(similar, 1):
                print(
                    f"   {i}. {sim['question']} (Similarity: {sim['similarity_score']:.3f})"
                )


def interactive_demo():
    """
    Interactive demo where user can ask questions
    """
    print("\n🎮 Interactive Demo - Ask your own questions!")
    print("Type 'quit' to exit")
    print("=" * 50)

    qa_system = ElectronicsQA()

    while True:
        user_input = input("\n❓ Enter your question: ").strip()

        if user_input.lower() in ["quit", "exit", "q"]:
            print("👋 Goodbye!")
            break

        if not user_input:
            continue

        print(f"\n🔍 Searching for similar questions...")
        suggestion = qa_system.suggest_sql_query(user_input)

        if suggestion["suggested_sql"]:
            print(f"\n✅ Found a match! (Confidence: {suggestion['confidence']:.3f})")
            print(f"📝 Suggested SQL:")
            print(f"   {suggestion['suggested_sql']}")
            print(f"📋 Based on: '{suggestion['source_question']}'")
            print(f"🎯 Expected Answer: {suggestion['expected_answer']}")
        else:
            print(f"\n❌ {suggestion['message']}")

            # Show similar questions anyway
            similar = qa_system.find_similar_questions(user_input, top_k=3)
            if similar:
                print(f"\n🔍 Here are some similar questions:")
                for i, sim in enumerate(similar, 1):
                    print(
                        f"   {i}. {sim['question']} (Similarity: {sim['similarity_score']:.3f})"
                    )


if __name__ == "__main__":
    # Run the integration demo
    demo_integration()

    # Ask if user wants to try interactive mode
    print("\n" + "=" * 50)
    try_interactive = (
        input("Would you like to try the interactive demo? (y/n): ").strip().lower()
    )

    if try_interactive in ["y", "yes"]:
        interactive_demo()
    else:
        print("👋 Demo completed!")