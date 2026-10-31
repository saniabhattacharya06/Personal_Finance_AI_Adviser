import streamlit as st
import pandas as pd
from modules.categorizer import categorize

st.set_page_config(
    page_title="Personal Finance AI Advisor",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Personal Finance AI Advisor")

st.header("Upload Your Expense File")

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully!")

    st.subheader("Expense Data")

    st.dataframe(df)

    st.subheader("Quick Summary")

    st.write(f"Total Transactions: {len(df)}")

    st.write(f"Total Spending: ₹{df['Amount'].sum():,.2f}")

    # Categorize the transactions based on the description
    df["Category"] = df["Description"].apply(categorize)
    st.dataframe(df)
    st.subheader("Categorized Expenses")
    st.dataframe(df)

    st.subheader("Category Wise Spending")
    category_summary = (
        df.groupby("Category")["Amount"]
        .sum()
        .reset_index()
        )
    st.dataframe(category_summary)