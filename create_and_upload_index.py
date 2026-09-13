import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
SOURCE_PATH = BASE_DIR / "data" / "my_vector_schema_info.csv"
INDEX_PATH = BASE_DIR / "data" / "schema_index.json"

df = pd.read_csv(SOURCE_PATH).fillna("")

documents = []
for _, row in df.iterrows():
    doc = {
        "id": str(row["id"]),
        "type": str(row["type"]),
        "name": str(row["name"]),
        "description": str(row["description"]),
        "columns": str(row["columns"])
    }
    documents.append(doc)

with INDEX_PATH.open("w", encoding="utf-8") as index_file:
    json.dump(documents, index_file, indent=2)

print(f"[OK] Built local schema index with {len(documents)} documents: {INDEX_PATH}")