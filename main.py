import streamlit as st
from app.llm.tools.sql_tool import get_sql_tools
from langchain_openai import OpenAI

# Initialize LLM
model = OpenAI(model_name="gpt-4", api_key="YOUR_OPENAI_API_KEY")
tools = get_sql_tools(model)

# Streamlit page config
st.set_page_config(page_title="SmartShop Assistant", page_icon="🛍️", layout="wide")

st.title("SmartShop Assistant 🛍️")
st.write("Ask about t-shirt, food, or other products and see images directly!")

# Chat input
user_input = st.text_input("Ask me about products:")

if user_input:
    # Build SQL query dynamically (simple example)
    # In real agent, LangChain will pick this automatically
    import sqlite3
    conn = sqlite3.connect("app/db/smartshop_assistant.db")
    cursor = conn.cursor()

    # Example: parse query for category/color (very basic)
    category = None
    color = None
    if "sari" in user_input.lower():
        category = "sari"
    elif "food" in user_input.lower():
        category = "food"

    if "red" in user_input.lower():
        color = "red"

    sql = f"SELECT name, price, image_path FROM products WHERE 1=1"
    if category:
        sql += f" AND category='{category}'"
    if color:
        sql += f" AND color='{color}'"
    sql += " LIMIT 5"

    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()

    if results:
        st.write(f"Found {len(results)} items:")
        for name, price, img_path in results:
            st.image(img_path, caption=f"{name} - ${price}")
    else:
        st.write("No items found for your query.")
