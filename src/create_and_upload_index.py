import json
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = PROJECT_ROOT / "data" / "my_vector_schema_info.csv"
INDEX_PATH = PROJECT_ROOT / "data" / "schema_index.json"


def build_index():
    dataframe = pd.read_csv(SOURCE_PATH).fillna("")
    documents = []

    for _, row in dataframe.iterrows():
        documents.append(
            {
                "id": str(row["id"]),
                "type": str(row["type"]),
                "name": str(row["name"]),
                "description": str(row["description"]),
                "columns": str(row["columns"]),
            }
        )

    with INDEX_PATH.open("w", encoding="utf-8") as index_file:
        json.dump(documents, index_file, indent=2)

    return len(documents)


if __name__ == "__main__":
    document_count = build_index()
    print(f"[OK] Built local schema index with {document_count} documents: {INDEX_PATH}")
