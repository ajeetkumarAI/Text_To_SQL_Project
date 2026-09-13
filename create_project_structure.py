import logging
import os
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

list_of_files = [
    "src/__init__.py",
    "src/templates.py",
    "src/database.py",
    "src/text_to_sql.py",
    "src/create_and_upload_index.py",
    "data/schema_index.json",
    "assets/.gitkeep",
    "app.py",
    "README.md",
    ".env",
    ".gitignore",
    "requirements.txt",
]

file_contents = {
    "src/templates.py": '''SQL_SYSTEM_PROMPT = """You are an assistant that converts natural language business questions into SQL queries.
Available table names: customers, suppliers, products, orders, order_details.
Use the following database schema context to help you:
{schema_context}
Return only the SQL query. Do not explain anything."""
''',
}


def create_project_structure():
    for filepath_text in list_of_files:
        filepath = Path(filepath_text)
        try:
            if filepath.parent != Path("."):
                filepath.parent.mkdir(parents=True, exist_ok=True)
                logging.info("Created directory: %s", filepath.parent)

            if not filepath.exists() or filepath.stat().st_size == 0:
                filepath.write_text(
                    file_contents.get(filepath_text, ""),
                    encoding="utf-8",
                )
                logging.info("Created file: %s", filepath)
            else:
                logging.info("File already exists: %s", filepath)
        except OSError as error:
            logging.error("Error creating %s: %s", filepath, error)


if __name__ == "__main__":
    create_project_structure()
