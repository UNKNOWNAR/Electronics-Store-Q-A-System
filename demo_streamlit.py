"""
Demo script showing the key features of the Electronics Store Q&A Streamlit App
"""

import streamlit as st
from qa_integration import ElectronicsQA
import time


def demo_question_processing():
    """Demonstrate question processing workflow"""
    st.header("🔍 Question Processing Demo")

    # Initialize Q&A system
    with st.spinner("Initializing Q&A System..."):
        qa_system = ElectronicsQA()

    # Demo questions
    demo_questions = [
        "How many Samsung phones do we have in stock?",
        "What's the total value of all laptops?",
        "Which products have discounts over 10%?",
        "How much revenue can we make from Apple products?",
    ]

    selected_question = st.selectbox("Choose a demo question:", demo_questions)

    if st.button("🔍 Process Question"):
        with st.spinner("Processing..."):
            time.sleep(1)  # Simulate processing time

            # Get suggestion
            suggestion = qa_system.suggest_sql_query(selected_question)

            # Display results
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📊 Results")
                if suggestion["suggested_sql"]:
                    st.success(
                        f"✅ Match Found! (Confidence: {suggestion['confidence']:.1%})"
                    )
                    st.write(f"**Original Question:** {suggestion['source_question']}")
                    st.write(f"**Expected Answer:** {suggestion['expected_answer']}")
                else:
                    st.error("❌ No match found")

            with col2:
                st.subheader("💻 Generated SQL")
                if suggestion["suggested_sql"]:
                    st.code(suggestion["suggested_sql"], language="sql")
                else:
                    st.warning("No SQL generated")


def demo_similarity_search():
    """Demonstrate similarity search functionality"""
    st.header("🎯 Similarity Search Demo")

    qa_system = ElectronicsQA()

    user_input = st.text_input(
        "Enter your own question:",
        placeholder="e.g., How many headphones are available?",
    )

    if user_input:
        with st.spinner("Searching for similar questions..."):
            similar_questions = qa_system.find_similar_questions(user_input, top_k=3)

            if similar_questions:
                st.subheader("🔍 Similar Questions Found:")
                for i, sim in enumerate(similar_questions, 1):
                    with st.expander(
                        f"Match {i} (Similarity: {sim['similarity_score']:.1%})"
                    ):
                        st.write(f"**Question:** {sim['question']}")
                        st.write(f"**Answer:** {sim['answer']}")
                        st.code(sim["sql_query"], language="sql")
            else:
                st.warning("No similar questions found")


def demo_confidence_scoring():
    """Demonstrate confidence scoring system"""
    st.header("📈 Confidence Scoring Demo")

    qa_system = ElectronicsQA()

    # Test questions with different confidence levels
    test_cases = [
        ("How many Samsung phones do we have in stock?", "Exact match"),
        ("Samsung phone count", "Partial match"),
        ("What is the total inventory value?", "Good match"),
        ("Random unrelated question about weather", "No match"),
    ]

    for question, expected in test_cases:
        st.write(f"**Question:** {question}")
        st.write(f"**Expected:** {expected}")

        suggestion = qa_system.suggest_sql_query(question)

        if suggestion["suggested_sql"]:
            confidence = suggestion["confidence"]
            if confidence >= 0.7:
                st.success(f"🟢 High Confidence: {confidence:.1%}")
            elif confidence >= 0.5:
                st.warning(f"🟡 Medium Confidence: {confidence:.1%}")
            else:
                st.error(f"🔴 Low Confidence: {confidence:.1%}")
        else:
            st.error("❌ No match found")

        st.write("---")


def main():
    """Main demo function"""
    st.set_page_config(
        page_title="Electronics Store Q&A Demo", page_icon="🛒", layout="wide"
    )

    st.title("🛒 Electronics Store Q&A System Demo")
    st.markdown(
        "This demo showcases the key features of the vector embedding-powered Q&A system."
    )

    # Create tabs for different demos
    tab1, tab2, tab3 = st.tabs(
        ["🔍 Question Processing", "🎯 Similarity Search", "📈 Confidence Scoring"]
    )

    with tab1:
        demo_question_processing()

    with tab2:
        demo_similarity_search()

    with tab3:
        demo_confidence_scoring()

    # Footer
    st.markdown("---")
    st.markdown(
        """
    <div style="text-align: center; color: #666;">
        🛒 Electronics Store Q&A System Demo | Powered by Vector Embeddings
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
