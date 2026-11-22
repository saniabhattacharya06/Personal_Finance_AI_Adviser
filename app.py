import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules.ai_advisor import get_savings_advice
from modules.budget_analyzer import analyze_budget
from modules.categorizer import categorize
from modules.database import create_table, fetch_expenses, insert_expense

create_table()

#Set up the Streamlit app configuration
st.set_page_config(
    page_title="Personal Finance AI Advisor",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Personal Finance AI Advisor")

st.caption(
    "AI-powered expense analysis, budgeting and savings recommendations"
)

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

    #Monthly Income Input Section
    st.header("Financial Information")
    monthly_income = st.number_input(
         "Monthly Income (₹)",
    min_value=1,
    value=50000
    )
    total_spending = df["Amount"].sum() #to calculate total spending from the uploaded data
    savings = monthly_income - total_spending #to calculate savings based on income and spending
    savings_rate = (savings / monthly_income) * 100 #to calculate savings rate as a percentage

    #Creating Financial Health Score.
    if savings_rate >= 30:
         health_score = 100
    elif savings_rate >= 20:
         health_score = 80
    elif savings_rate >= 10:
         health_score = 60
    else:
         health_score = 40

    #Displaying Metrics.
    st.header("Financial Health")
    col1, col2, col3 = st.columns(3)
    col1.metric(
         "Income",
         f"₹{monthly_income:,.0f}"
         )

    col2.metric(
        "Savings",
        f"₹{savings:,.0f}"
        )
    col3.metric(
         "Health Score",
         f"{health_score}/100"
         )
    #Health Status based on the health score.
    if health_score >= 80:
         st.success("Excellent Financial Health ✅")

    elif health_score >= 60:
         st.warning("Moderate Financial Health ⚠️")

    else:
         st.error("Needs Improvement ❌")

    #Adding Spending Breakdown Section.
    st.subheader("Spending Percentage")
    spending_percentage = (
         total_spending / monthly_income
         ) * 100

    st.write(
         f"You spend {spending_percentage:.2f}% of your monthly income."
         )
    #Improving sidebars.
    st.sidebar.header("Financial Inputs")
    monthly_income = st.sidebar.number_input(
        "Monthly Income",
        min_value=1,
        value=50000
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

    #Adding overspending alerts
    st.subheader("Overspending Alerts")
    overspending_found = False
    for _, row in budget_df.iterrows():
        if row["Remaining"] < 0:
            overspending_found = True
            st.error(
                f"You exceeded the {row['Category']} budget by ₹{abs(row['Remaining'])}"
                    )

            if not overspending_found:
                st.info("No category is currently overspending your budget.")

    #Add Sidebar API Key Input
    st.sidebar.header("AI Settings")
    api_key = st.sidebar.text_input(
                "Enter Gemini API Key",
                type="password"
            )

    #Creating Spending Summary.
    summary = ""
    for _, row in budget_df.iterrows():
                summary += (
                    f"{row['Category']}: "
                    f"Budget={row['Budget']}, "
                    f"Spent={row['Spent']}, "
                    f"Remaining={row['Remaining']}\n"
                )

    # Display summary
    st.subheader("Spending Summary")
    st.text(summary)

    # AI section
    st.header("🤖 AI Finance Advisor")
    if st.button("Generate Savings Suggestions", key="generate_savings_suggestions"):
          if api_key:
                    with st.spinner("Analyzing your finances..."):
                        advice = get_savings_advice(summary, api_key)
                        if advice and advice != "No response received from Gemini.":
                            st.markdown(advice)
                        else:
                            st.warning(f"The AI advisor returned no usable content: {advice}")
    else:
         st.warning("Please enter Gemini API key.")

# For historical transaction data.
st.header("Transaction History")
history_df = fetch_expenses()
st.dataframe(history_df)

# Displaying Database Metrics.
st.subheader("Database Statistics")

st.write(
    f"Total Saved Transactions: {len(history_df)}"
)

#For downloading Report Features..
csv = history_df.to_csv(index=False)
st.download_button(
    label="Download Transactions",
    data=csv,
    file_name="finance_report.csv",
    mime="text/csv"
)

#Saving button to save the expenses to the database.
if st.button("Save Expenses to Database"):

    for _, row in df.iterrows():

        insert_expense(
            row["Date"],
            row["Description"],
            row["Amount"],
            row["Category"]
        )

    st.success("Expenses saved successfully!")

