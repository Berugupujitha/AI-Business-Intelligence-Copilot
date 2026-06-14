import sqlite3

def get_schema(db_path="database/ecommerce.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    schema_text = ""

    cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table';
    """)

    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        column_names = [col[1] for col in columns]

        schema_text += f"{table_name}({', '.join(column_names)})\n\n"

    conn.close()

    return schema_text