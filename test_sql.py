import sqlite3
import pandas as pd

conn = sqlite3.connect("database/ecommerce.db")

query = """
SELECT COUNT(*) AS total_orders
FROM orders;
"""

df = pd.read_sql(query, conn)
print(df)

conn.close()