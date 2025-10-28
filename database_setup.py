"""
Database setup and connection utilities for the Electronics Store Q&A System
"""

import psycopg2
from sqlalchemy import create_engine, text
import pandas as pd
from config import DATABASE_CONFIG
from urllib.parse import quote_plus


def test_database_connection():
    """
    Test the database connection and return connection status
    """
    try:
        # Test with psycopg2
        conn = psycopg2.connect(**DATABASE_CONFIG)
        conn.close()

        # Test with SQLAlchemy
        password = quote_plus(DATABASE_CONFIG['password'])
        connection_string = f"postgresql://{DATABASE_CONFIG['user']}:{password}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
        engine = create_engine(connection_string)

        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()

        return True, "Database connection successful"
    except Exception as e:
        return False, f"Database connection failed: {str(e)}"


def get_database_info():
    """
    Get basic information about the database
    """
    try:
        password = quote_plus(DATABASE_CONFIG['password'])
        connection_string = f"postgresql://{DATABASE_CONFIG['user']}:{password}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
        engine = create_engine(connection_string)

        with engine.connect() as connection:
            # Get table information
            tables_query = """
            SELECT table_name, table_type 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
            """
            tables_result = connection.execute(text(tables_query))
            tables = tables_result.fetchall()

            # Get table row counts
            table_info = []
            for table_name, table_type in tables:
                count_query = f"SELECT COUNT(*) FROM {table_name};"
                count_result = connection.execute(text(count_query))
                row_count = count_result.fetchone()[0]
                table_info.append(
                    {
                        "table_name": table_name,
                        "table_type": table_type,
                        "row_count": row_count,
                    }
                )

            return table_info
    except Exception as e:
        return f"Error getting database info: {str(e)}"


def execute_sample_queries():
    """
    Execute some sample queries to test the database
    """
    try:
        password = quote_plus(DATABASE_CONFIG['password'])
        connection_string = f"postgresql://{DATABASE_CONFIG['user']}:{password}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
        engine = create_engine(connection_string)

        sample_queries = [
            "SELECT COUNT(*) as total_products FROM products;",
            "SELECT brand, COUNT(*) as count FROM products GROUP BY brand ORDER BY count DESC LIMIT 5;",
            "SELECT category, COUNT(*) as count FROM products GROUP BY category ORDER BY count DESC;",
        ]

        results = {}
        with engine.connect() as connection:
            for i, query in enumerate(sample_queries):
                result = connection.execute(text(query))
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
                results[f"query_{i + 1}"] = df

        return results
    except Exception as e:
        return f"Error executing sample queries: {str(e)}"


def main():
    """
    Main function to test database setup
    """
    print("🔧 Electronics Store Database Setup Test")
    print("=" * 50)

    # Test connection
    print("\n1. Testing database connection...")
    success, message = test_database_connection()
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
        print("\n💡 Make sure to:")
        print("   - Set up your database connection parameters in config.py")
        print("   - Create the electronics_store database")
        print("   - Run the SQL script from database/db_creation_electronics_store.sql")
        return

    # Get database info
    print("\n2. Getting database information...")
    table_info = get_database_info()
    if isinstance(table_info, str):
        print(f"❌ {table_info}")
    else:
        print("📊 Database Tables:")
        for table in table_info:
            print(f"   • {table['table_name']}: {table['row_count']} rows")

    # Execute sample queries
    print("\n3. Testing sample queries...")
    results = execute_sample_queries()
    if isinstance(results, str):
        print(f"❌ {results}")
    else:
        print("✅ Sample queries executed successfully!")
        for query_name, df in results.items():
            print(f"\n📋 {query_name}:")
            print(df.to_string(index=False))


if __name__ == "__main__":
    main()