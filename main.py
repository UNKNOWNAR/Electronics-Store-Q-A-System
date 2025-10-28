import streamlit as st
import pandas as pd
from qa_integration import ElectronicsQA
import psycopg2
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import sys
from urllib.parse import quote_plus

# Load environment variables
load_dotenv()

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        "streamlit",
        "pandas",
        "chromadb",
        "sentence_transformers",
        "psycopg2",
        "sqlalchemy",
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        st.error("❌ Missing required packages:")
        for package in missing_packages:
            st.error(f"   • {package}")
        st.info("💡 Install missing packages with:")
        st.code("pip install -r requirements.txt")
        return False

    return True

# Page configuration
st.set_page_config(
    page_title="Electronics Store Q&A System",
    page_icon="🛒",
    layout="wide",
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
    return ElectronicsQA()


@st.cache_resource
def get_database_connection():
    """Get database connection with caching"""
    try:
        # Database connection parameters
        db_params = {
            "host": os.getenv("DB_HOST", "localhost"),
            "database": os.getenv("DB_NAME", "electronics_store"),
            "user": os.getenv("DB_USER", "postgres"),
            "password": os.getenv("DB_PASSWORD", "password"),
            "port": os.getenv("DB_PORT", "5432"),
        }

        # Create SQLAlchemy engine
        password = quote_plus(db_params['password'])
        connection_string = f"postgresql://{db_params['user']}:{password}@{db_params['host']}:{db_params['port']}/{db_params['database']}"
        engine = create_engine(connection_string)
        return engine
    except Exception as e:
        st.error(f"Database connection failed: {str(e)}")
        return None


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
    # Main header
    st.markdown(
        '<h1 class="main-header">🛒 Electronics Store Q&A System</h1>',
        unsafe_allow_html=True,
    )

    if not check_requirements():
        st.stop()

    # Initialize Q&A system
    with st.spinner("Initializing Q&A System..."):
        qa_system = initialize_qa_system()

    # Sidebar
    with st.sidebar:


        st.header("📊 Database Connection")
        engine = get_database_connection()
        if engine:
            st.success("✅ Database Connected")
        else:
            st.error("❌ Database Connection Failed")

        st.header("🎯 Similarity Threshold")
        threshold = st.slider(
            "Minimum similarity score",
            min_value=0.1,
            max_value=1.0,
            value=0.4,
            step=0.1,
            help="Higher values require more similar questions",
        )

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
                suggestion = qa_system.suggest_sql_query(user_question)

                # Find similar questions
                similar_questions = qa_system.find_similar_questions(
                    user_question, top_k=3
                )

    with col2:
        st.header("📈 Confidence Score")
        if user_question and "suggestion" in locals():
            if suggestion["suggested_sql"]:
                confidence = suggestion["confidence"]
                st.metric("Match Confidence", f"{confidence:.1%}")

                # Color-coded confidence indicator
                if confidence >= 0.7:
                    st.success("🟢 High Confidence")
                elif confidence >= 0.5:
                    st.warning("🟡 Medium Confidence")
                else:
                    st.error("🔴 Low Confidence")
            else:
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
            st.markdown(
                f"""
            <div class="sql-box">
                {suggestion["suggested_sql"]}
            </div>
            """,
                unsafe_allow_html=True,
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
                            engine, suggestion["suggested_sql"]
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
            st.markdown(
                """
            <div class="warning-box">
                <strong>⚠️ No similar questions found</strong><br>
                The system couldn't find a similar question in the database.
                Consider adding more examples to improve matching.
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