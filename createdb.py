import pandas as pd
import sqlite3

# Create database
conn = sqlite3.connect("database/ecommerce.db")

# Load CSV files into database tables

pd.read_csv("data1/olist_customers_dataset.csv").to_sql(
    "customers", conn, if_exists="replace", index=False
)

pd.read_csv("data1/olist_orders_dataset.csv").to_sql(
    "orders", conn, if_exists="replace", index=False
)

pd.read_csv("data1/olist_order_items_dataset.csv").to_sql(
    "order_items", conn, if_exists="replace", index=False
)

pd.read_csv("data1/olist_order_payments_dataset.csv").to_sql(
    "payments", conn, if_exists="replace", index=False
)

pd.read_csv("data1/olist_products_dataset.csv").to_sql(
    "products", conn, if_exists="replace", index=False
)

pd.read_csv("data1/olist_sellers_dataset.csv").to_sql(
    "sellers", conn, if_exists="replace", index=False
)

pd.read_csv("data1/product_category_name_translation.csv").to_sql(
    "category_translation", conn, if_exists="replace", index=False
)

print("Database created successfully!")

conn.close()