import os
import json
import re
from pathlib import Path

from dotenv import load_dotenv
import openai


from database import execute_query

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent
INDEX_PATH = BASE_DIR / "data" / "schema_index.json"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

client = openai.OpenAI(
    api_key=OPENAI_API_KEY,
)


def _tokens(value):
    return set(re.findall(r"[a-z0-9_]+", value.lower()))


def _load_index():
    if not INDEX_PATH.exists():
        raise FileNotFoundError(
            f"Local schema index not found at {INDEX_PATH}. "
            "Run: python create_and_upload_index.py"
        )
    with INDEX_PATH.open(encoding="utf-8") as index_file:
        return json.load(index_file)

def search_index(query_text, top=1):
    query_tokens = _tokens(query_text)
    documents = _load_index()
    ranked = sorted(
        documents,
        key=lambda document: len(
            query_tokens
            & _tokens(" ".join(str(value) for value in document.values()))
        ),
        reverse=True,
    )
    return ranked[:top]

def build_schema_context(doc):
    return (
        f"Table: {doc.get('name', '')}\n"
        f"Description: {doc.get('description', '')}\n"
        f"Columns: {doc.get('columns', '')}\n"
    )

def clean_sql(sql: str):
    lines = sql.strip().splitlines()
    cleaned_lines = [line for line in lines if not line.strip().startswith("```")]
    return "\n".join(cleaned_lines).strip()
    


def question_to_sql(question: str):
    # Retrieve top search results for RAG context
    search_results = search_index(question, top=3)
    context = "\n".join(build_schema_context(doc) for doc in search_results)

    system_prompt = (
        "You are an assistant that converts natural language business questions "
        "into SQL queries.\n"
        "Available table names: customers, suppliers, products, orders, order_details.\n"
        "Use the following database schema context to help you:\n"
        f"{context}\n"
        "Return only the SQL query. Do not explain anything."
    )


    message = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages = message,
        temperature=0,
        max_tokens=150
    )
    sql = response.choices[0].message.content.strip()
    cln_sql = clean_sql(sql)
    return cln_sql


if __name__ == "__main__":
    question = "What is the total shipping cost of orders for each country?" 
    sql_query = question_to_sql(question)
    print("Generated SQL:\n", sql_query)

    # Execute the generated SQL query using the database connection
    try:
        results = execute_query(sql_query)
        print("Query Results:")
        print(results)
    except Exception as e:
        print("Error executing query:", e)

    
