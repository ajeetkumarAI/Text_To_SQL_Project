import json
import os
import re
from pathlib import Path

import openai
from dotenv import load_dotenv

from src.templates import SQL_SYSTEM_PROMPT

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = PROJECT_ROOT / "data" / "schema_index.json"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

client = openai.OpenAI(api_key=OPENAI_API_KEY)


def _tokens(value):
    return set(re.findall(r"[a-z0-9_]+", value.lower()))


def _load_index():
    if not INDEX_PATH.exists():
        raise FileNotFoundError(
            f"Local schema index not found at {INDEX_PATH}. "
            "Run: python -m src.create_and_upload_index"
        )
    with INDEX_PATH.open(encoding="utf-8") as index_file:
        return json.load(index_file)


def search_index(query_text, top=3):
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
    search_results = search_index(question)
    context = "\n".join(build_schema_context(doc) for doc in search_results)

    system_prompt = SQL_SYSTEM_PROMPT.format(schema_context=context)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0,
        max_tokens=150,
    )
    return clean_sql(response.choices[0].message.content.strip())
