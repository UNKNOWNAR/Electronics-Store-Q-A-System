import streamlit as st
import pandas as pd
from qa_integration import ElectronicsQASystem, getDatabaseConnection
from database_setup import get_sqlalchemy_engine
from sqlalchemy import text

# Import settings from config.py
from config import (
    STREAMLIT_CONFIG,
    SIMILARITY_CONFIG,
)


# Page configuration (now uses STREAMLIT_CONFIG)
st.set_page_config(
    **STREAMLIT_CONFIG,
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
        color: #000000;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }
    .sql-box {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        margin: 1rem 0;
        color: #000000;
    }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def initialize_qa_system():
    """Initialize the Q&A system with caching"""
    return ElectronicsQASystem()


@st.cache_resource
def get_cached_sqlalchemy_engine():
    """Get and cache the SQLAlchemy engine."""
    engine = get_sqlalchemy_engine()
    if engine is None:
        st.error("Failed to get SQLAlchemy engine.")
        return None
    return engine


def execute_sql_query(engine, query):
    """Execute SQL query and return results"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            columns = result.keys()
            data = result.fetchall()

            if data:
                df = pd.DataFrame(data, columns=columns)
                return df, None
            else:
                return (
                    pd.DataFrame(),
                    "Query executed successfully but returned no results.",
                )
    except Exception as e:
        return None, str(e)


def main():
    threshold = SIMILARITY_CONFIG["default_threshold"]
    # Main header
    st.markdown(
        '<h1 class="main-header">🛒 Electronics Store Q&A System</h1>',
        unsafe_allow_html=True,
    )

    # Initialize Q&A system
    with st.spinner("Initializing Q&A System..."):
        qa_system = initialize_qa_system()

    # Sidebar
    with st.sidebar:
        st.header("📊 Database Connection")
        engine = get_cached_sqlalchemy_engine()
        if engine:
            st.success("✅ Database Connected")
        else:
            st.error("❌ Database Connection Failed")


        st.header("📝 Example Questions")
        example_questions = [
            "How many Samsung phones do we have in stock?",
            "What's the total value of all laptops?",
            "Which products have discounts over 10%?",
            "How much revenue can we make from Apple products?",
            "What's the average price of smartwatches?",
            "How many headphones are in stock?",
            "What's our total inventory worth?",
        ]

        for i, example in enumerate(example_questions):
            if st.button(f"📌 {example[:50]}...", key=f"example_{i}"):
                st.session_state.user_question = example

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("💬 Ask a Question")

        # Question input
        user_question = st.text_input(
            "Enter your question about the electronics store:",
            value=st.session_state.get("user_question", ""),
            placeholder="e.g., How many Samsung phones do we have in stock?",
            key="question_input",
        )

        if user_question:
            st.markdown("---")

            # Process the question
            with st.spinner("🔍 Finding similar questions and generating SQL..."):
                # Get SQL suggestion
                # --- CHANGE ---
                # We now pass the threshold value from the slider
                suggestion = qa_system.suggest_sql_query(
                    user_question, threshold=threshold
                )
                # --- END CHANGE ---

    with col2:
        st.header("📈 Confidence Score")
        if user_question and "suggestion" in locals():
            # We can now display the confidence even if no SQL was suggested
            confidence = suggestion["confidence"]
            st.metric("Match Confidence", f"{confidence:.1%}")

            if suggestion["suggested_sql"]:
                # Color-coded confidence indicator
                if confidence >= 0.7:
                    st.success("🟢 High Confidence")
                elif confidence >= 0.5:
                    st.warning("🟡 Medium Confidence")
                else:
                    st.error("🔴 Low Confidence")
            else:
                # This branch now handles low-confidence "garbage" questions
                st.error("❌ No Match Found")

    # Display results
    if user_question and "suggestion" in locals():
        st.markdown("---")

        if suggestion["suggested_sql"]:
            # Display suggested SQL
            st.header("🔍 Found Similar Question")
            st.markdown(
                f"""
            <div class="success-box">
                <strong>Original Question:</strong> {suggestion["source_question"]}<br>
                <strong>Expected Answer:</strong> {suggestion["expected_answer"]}
            </div>
            """,
                unsafe_allow_html=True,
            )

            st.header("💻 Generated SQL Query")
            edited_sql = st.text_area(
                "You can edit the SQL query below:",
                value=suggestion["suggested_sql"],
                height=150,
            )

            # Execute SQL if database is connected
            if engine:
                st.header("📊 Query Results")

                col_execute, col_info = st.columns([1, 3])
                with col_execute:
                    execute_query = st.button("🚀 Execute Query", type="primary")

                with col_info:
                    st.info("💡 Click 'Execute Query' to run the SQL and see results")

                if execute_query:
                    with st.spinner("Executing SQL query..."):
                        df, error = execute_sql_query(
                            engine, edited_sql
                        )

                        if df is not None:
                            if not df.empty:
                                st.success("✅ Query executed successfully!")
                                st.dataframe(df, use_container_width=True)

                                # Show summary statistics
                                if len(df.columns) == 1 and df.iloc[0, 0] is not None:
                                    st.metric("Result", float(df.iloc[0, 0]))
                            else:
                                st.warning("⚠️ Query executed but returned no results")
                        else:
                            st.error(f"❌ Query execution failed: {error}")
            else:
                st.warning("⚠️ Database not connected. Cannot execute SQL queries.")

        else:
            # This message now appears when the confidence is below the threshold
            st.markdown(
                """
            <div class="warning-box">
                <strong>⚠️ No similar questions found</strong><br>
                The system couldn't find a similar question in the database,
                or the confidence was below the threshold.
            </div>
            """,
                unsafe_allow_html=True,
            )

    # Footer
    st.markdown("---")
    st.markdown(
        """
    <div style="text-align: center; color: #666; padding: 1rem;">
        🛒 Electronics Store Q&A System | Powered by Vector Embeddings & Chroma DB
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()