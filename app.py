import streamlit as st
import pandas as pd
from modules.categorizer import categorize
import plotly.express as px
from modules.budget_analyzer import analyze_budget
import plotly.graph_objects as go

#Set up the Streamlit app configuration
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

    #Creating KPI Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Total Transactions",
        len(df)
        )
    col2.metric(
        "Total Spending",
        f"₹{df['Amount'].sum():,.0f}"
        )
    col3.metric(
        "Categories",
        df["Category"].nunique()
        )

    # Create Expense Distribution Pie Chart
    st.subheader("Expense Distribution")
    category_summary = (
        df.groupby("Category")["Amount"]
        .sum()
        .reset_index()
        )
    fig_pie = px.pie(
        category_summary,
        names="Category",
        values="Amount",
        hole=0.4,
        title="Expense Distribution by Category"
        )
    st.plotly_chart(
        fig_pie,
        use_container_width=True
        )
    # Create Category Spending Bar Chart
    st.subheader("Category Spending Comparison")
    fig_bar = px.bar(
        category_summary,
        x="Category",
        y="Amount",
        color="Category",
        text_auto=True,
        title="Amount Spent per Category"
        )
    st.plotly_chart(
        fig_bar,
        use_container_width=True
        )

    #Better Dashboard Layout.
    col1, col2 = st.columns(2)
    with col1:
        
        fig_pie = px.pie(
            category_summary,
            names="Category",
            values="Amount",
            hole=0.4
            )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
            )
        with col2:
            fig_bar = px.bar(
            category_summary,
            x="Category",
            y="Amount",
            color="Category"
            )
            st.plotly_chart(
                fig_bar,
                use_container_width=True
                )
            #Budget Input Section
            st.header("Monthly Budget Setup")
            food_budget = st.number_input(
                "Food Budget",
                min_value=0,
                value=5000
                )
            transport_budget = st.number_input(
                "Transport Budget",
                min_value=0,
                value=3000
                )
            shopping_budget = st.number_input(
                "Shopping Budget",
                min_value=0,
                value=4000
                )
            utilities_budget = st.number_input(
                "Utilities Budget",
                min_value=0,
                value=2500
                )
            #Budget Dictionary
            budgets = {
                "Food": food_budget,
                "Transport": transport_budget,
                "Shopping": shopping_budget,
                "Utilities": utilities_budget
                }

            #Generate Budget Analysis Report
            report = analyze_budget(df, budgets)
            budget_df = pd.DataFrame(report)

            # Display Budget Table
            st.subheader("Budget Analysis")
            st.dataframe(budget_df)

            #Adding overspending alerts
            st.subheader("Overspending Alerts")
            for _, row in budget_df.iterrows():
                if row["Remaining"] < 0:
                    st.error(
                        f"You exceeded the {row['Category']} budget by ₹{abs(row['Remaining'])}"
                        )

                    #Budget vs Spending Bar Chart
                    fig = go.Figure()
                    fig.add_bar(
                        name="Budget",
                        x=budget_df["Category"],
                        y=budget_df["Budget"]
                        )
                    fig.add_bar(
                        name="Spent",
                        x=budget_df["Category"],
                        y=budget_df["Spent"]
                        )
                    fig.update_layout(
                        barmode="group",
                        title="Budget vs Actual Spending"
                        )
                    st.plotly_chart(
                        fig,
                        use_container_width=True
                        )