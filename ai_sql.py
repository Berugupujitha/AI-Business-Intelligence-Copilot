from google import genai
import sqlite3
import pandas as pd

# ==========================
# Gemini API Key
# ==========================
client = genai.Client(
    api_key="API_KEY"
)

# ==========================
# Database Schema
# ==========================
schema = """
customers(customer_id, customer_unique_id, customer_city, customer_state)

orders(order_id, customer_id, order_status, order_purchase_timestamp)

order_items(order_id, product_id, seller_id, price)

payments(order_id, payment_type, payment_value)

products(product_id, product_category_name)

sellers(seller_id, seller_city, seller_state)

category_translation(product_category_name, product_category_name_english)
"""

# ==========================
# User Question
# ==========================
question = input("Ask a question: ")

# ==========================
# Prompt
# ==========================
prompt = f"""
You are an expert SQLite SQL generator.

Database Schema:
{schema}

Rules:
1. Return ONLY SQL.
2. Do NOT explain anything.
3. Do NOT use markdown.
4. First word must be SELECT.
5. Generate valid SQLite SQL only.

Question:
{question}
"""

# ==========================
# Gemini Response
# ==========================
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

sql_query = response.text.strip()

# Clean response
sql_query = sql_query.replace("```sql", "")
sql_query = sql_query.replace("```", "")
sql_query = sql_query.strip()

# Extract SQL from first SELECT
select_pos = sql_query.upper().find("SELECT")

if select_pos != -1:
    sql_query = sql_query[select_pos:]

print("\nGenerated SQL:")
print(sql_query)

# ==========================
# Execute SQL
# ==========================
conn = sqlite3.connect("database/ecommerce.db")

try:
    df = pd.read_sql_query(sql_query, conn)

    print("\nResult:")
    print(df)

except Exception as e:
    print("\nSQL Error:")
    print(e)

finally:
    conn.close()