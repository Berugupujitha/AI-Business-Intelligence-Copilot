from google import genai
import streamlit as st
import sqlite3
import pandas as pd
from schema_utils import get_schema

# Gemini Client
client = genai.Client(
    api_key="API_KEY"
)

st.title("AI Business Intelligence Copilot")

st.write("Ask business questions in plain English.")

question = st.text_input("Ask a business question")

if st.button("Generate Insight"):

    schema = get_schema()

    prompt = f"""
You are an expert SQLite SQL generator.

Database Schema:
{schema}

Rules:
1. Return ONLY SQL
2. No markdown
3. No explanation
4. First word must be SELECT

Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    sql_query = response.text.strip()

    # Clean Gemini response
    sql_query = sql_query.replace("```sql", "")
    sql_query = sql_query.replace("```", "")
    sql_query = sql_query.strip()

    select_pos = sql_query.upper().find("SELECT")

    if select_pos != -1:
        sql_query = sql_query[select_pos:]

    st.subheader("Generated SQL")
    st.code(sql_query)

    conn = sqlite3.connect("database/ecommerce.db")

    try:
        df = pd.read_sql_query(sql_query, conn)

        st.subheader("Results")
        st.dataframe(df)

        # Automatic Chart
        if len(df.columns) >= 2 and len(df) > 0:

            first_col = df.columns[0]
            second_col = df.columns[1]

            try:
                chart_df = df[[first_col, second_col]]

                chart_df = chart_df.set_index(first_col)

                st.subheader("Visualization")

                st.bar_chart(chart_df)

            except Exception:
                pass

    except Exception as e:
        st.error(f"SQL Error: {e}")

    finally:
        conn.close()