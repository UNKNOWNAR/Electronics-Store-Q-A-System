import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
import textwrap  # Added this to clean up the prompt

from vector_embeddings import VectorEmbeddingManager
from few_shots import few_shots  # Import few_shots directly

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate  # Removed unused FewShotPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Import from your config file
from config import DATABASE_CONFIG, SIMILARITY_CONFIG


def getDatabaseConnection():
    """
    Check the database connection using settings from config.py
    """
    try:
        db_user = DATABASE_CONFIG["user"]
        db_password = quote_plus(DATABASE_CONFIG["password"])
        db_host = DATABASE_CONFIG["host"]
        db_port = DATABASE_CONFIG["port"]
        db_name = DATABASE_CONFIG["database"]

        db_uri = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        engine = SQLDatabase.from_uri(db_uri)
        return engine
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# --- CHANGE 1: Renamed class to match main.py ---
class ElectronicsQASystem:
    def __init__(self):
        """
        Initialize the Electronics Q&A system with vector embeddings and LangChain/Gemini
        """
        load_dotenv()  # Ensure environment variables are loaded

        # Initialize Vector Embedding Manager for similarity search
        self.embedding_manager = VectorEmbeddingManager()

        # Check if we have embeddings, if not create them
        info = self.embedding_manager.get_collection_info()
        if info["total_documents"] == 0:
            print("Creating embeddings from few shots data...")
            self.embedding_manager.create_embeddings_from_few_shots()

        # Initialize Google Gemini LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.0,
        )

        self.db = getDatabaseConnection()
        if self.db is None:
            raise Exception("Failed to initialize ElectronicsQA: Database connection failed.")

        # Define the example prompt for few-shot learning
        self.example_prompt = ChatPromptTemplate.from_template(
            "Question: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}"
        )

        # --- CHANGE 3: Cleaned up prompt indentation ---
        # Define the main prompt template for SQL generation
        system_prompt = textwrap.dedent(
            """You are an expert PostgreSQL assistant. Your goal is to write a single, syntactically correct PostgreSQL query to answer the user's question.

            Use the following database schema to construct your query:
            {schema}

            Here are some rules and best practices to follow:
            1.  **Only use tables and columns** that are explicitly listed in the schema.
            2.  Pay close attention to **which columns belong to which tables** to ensure correct JOINs.
            3.  For string comparisons (like brand names or categories), use `ILIKE` for case-insensitivity. For example: `WHERE brand ILIKE 'samsung'`.
            4.  If performing calculations, use `COALESCE` to handle potential `NULL` values (e.g., `COALESCE(discounts.pct_discount, 0)`).
            5.  **Do not** wrap your answer in markdown (e.g., ```sql ... ```).
            6.  **Only output the SQL query** and nothing else.

            Here are some examples of how to answer user questions:
            {few_shot_examples}
            """
        )
        self.sql_generation_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "Question: {question}"),
                ("ai", "SQL Query:"),  # This prompts the AI to respond
            ]
        )

        # Create the LangChain chain
        self.chain = self.sql_generation_prompt | self.llm | StrOutputParser()

    def find_similar_questions(self, user_question):
        """
        Find similar questions from the few shots data
        """
        top_k = SIMILARITY_CONFIG["max_results"]
        results = self.embedding_manager.search_similar_questions(
            user_question, n_results=top_k
        )
        # ... (rest of the function is correct) ...
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
                        "sql_result": metadata["sql_result"],  # Include SQLResult
                        "answer": metadata["answer"],
                        "similarity_score": similarity_score,
                        "index": metadata["index"],
                    }
                )
        return similar_questions

    def suggest_sql_query(self, user_question, threshold):
        """
        Suggest a SQL query using Google Gemini and LangChain,
        leveraging top_k similar questions as few-shot examples.
        """
        try:
            # 1. Find top_k similar questions using vector embeddings
            similar_examples = self.find_similar_questions(user_question)

            # 2. CHECK THE THRESHOLD (The "Garbage Filter" Logic)
            confidence = (
                similar_examples[0]["similarity_score"] if similar_examples else 0.0
            )

            if not similar_examples or confidence < threshold:
                # Confidence is too low, this is "garbage" or un-matchable
                return {
                    "suggested_sql": None,
                    "confidence": confidence,
                    "message": "Confidence below threshold. No similar question found.",
                    "source_question": None,
                    "expected_answer": None,
                }

            # 3. Format these similar questions as few-shot examples for the LLM
            formatted_few_shots = []
            for example in similar_examples:
                formatted_few_shots.append(
                    self.example_prompt.format(
                        Question=example["question"],
                        SQLQuery=example["sql_query"],
                        SQLResult=example["sql_result"],
                        Answer=example["answer"],
                    )
                )
            few_shot_examples_str = "\n\n".join(formatted_few_shots)

            # 4. Get database schema
            schema = self.db.get_table_info()

            # 5. Invoke the LLM chain to generate SQL
            generated_sql = self.chain.invoke(
                {
                    "schema": schema,
                    "few_shot_examples": few_shot_examples_str,
                    "question": user_question,
                }
            )

            # 6. Clean up the generated SQL
            if generated_sql.startswith("```sql"):
                generated_sql = (
                    generated_sql.replace("```sql", "").replace("```", "").strip()
                )

            # 7. Return the final suggestion
            return {
                "suggested_sql": generated_sql,
                "confidence": confidence,
                "source_question": similar_examples[0]["question"],
                "expected_answer": similar_examples[0]["answer"],
            }
        except Exception as e:
            return {
                "suggested_sql": None,
                "confidence": 0.0,
                "message": f"Error generating SQL: {e}",
            }