import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd

# Load environment variables from .env file
load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

def get_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )


def execute_query(query):
    conn = get_connection()

    try:
        df = pd.read_sql(query, conn)
    finally:
        conn.close()
    return df



if __name__ == "__main__":
    try:
        # Test query to select records from customers table
        test_query = "SELECT * FROM customers LIMIT 5;"
        df = execute_query(test_query)
        print("Sample records from customers table:")
        print(df)
    except Exception as e:
        print("Database connection or test query failed:", e)