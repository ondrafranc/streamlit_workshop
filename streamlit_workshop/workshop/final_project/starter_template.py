import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import io
import uuid

# 💰 Personal Finance Dashboard - Starter Template

# Set page config
st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="💰",
    layout="wide"
)

# Initialize session state variables
if 'transactions' not in st.session_state:
    # Create sample transaction data
    st.session_state.transactions = pd.DataFrame({
        'id': [str(uuid.uuid4()) for _ in range(10)],
        'date': pd.date_range(end=datetime.now(), periods=10, freq='D'),
        'amount': np.random.normal(100, 50, 10).round(2) * np.random.choice([-1, 1], size=10, p=[0.7, 0.3]),
        'category': np.random.choice(['Groceries', 'Dining', 'Transportation', 'Utilities', 'Entertainment', 'Salary'], 10, p=[0.3, 0.2, 0.15, 0.1, 0.15, 0.1]),
        'description': ['Supermarket', 'Restaurant', 'Gas', 'Electricity', 'Movies', 
                        'Paycheck', 'Groceries', 'Lunch', 'Uber', 'Internet']
    })
    
    # Ensure expense amounts are negative and income amounts are positive
    for i, row in st.session_state.transactions.iterrows():
        if row['category'] in ['Salary'] and row['amount'] < 0:
            st.session_state.transactions.at[i, 'amount'] = abs(row['amount'])
        elif row['category'] not in ['Salary'] and row['amount'] > 0:
            st.session_state.transactions.at[i, 'amount'] = -abs(row['amount'])

if 'budgets' not in st.session_state:
    # Initialize budget settings
    st.session_state.budgets = {
        'Groceries': 500,
        'Dining': 300,
        'Transportation': 200,
        'Utilities': 350,
        'Entertainment': 150
    }

# Main app title
st.title("💰 Personal Finance Dashboard")

# TODO: Create a sidebar with navigation
# Hint: Use st.sidebar.radio() to create a navigation menu with options
# like "Dashboard", "Transactions", "Budgets", "Settings"


# TODO: Add date range selector in the sidebar
# Hint: Use st.sidebar.date_input() to select start and end dates


# TODO: Add category filter in the sidebar
# Hint: Get unique categories from transactions and use st.sidebar.multiselect()


# TODO: Implement a function to filter transactions by date and category
# Hint: Create a function that takes the transactions, date range, and categories
# and returns a filtered dataframe


# TODO: Create a dashboard view that shows:
# 1. Summary metrics (total income, expenses, balance)
# 2. Expense breakdown by category (consider a pie chart)
# 3. Income/expense trend over time (consider a line chart)
# Hint: Use st.columns() for layout and plotly for charts


# TODO: Implement a transaction management view that:
# 1. Shows a list of transactions in an editable table
# 2. Allows adding new transactions
# 3. Includes export functionality
# Hint: Use st.data_editor() for the table and st.download_button() for export


# TODO: Add a budget management view that:
# 1. Shows current budget settings
# 2. Allows updating budget amounts
# 3. Displays budget vs. actual spending
# Hint: Use a form for budget settings and charts to show performance


# Helper function for data download (already implemented)
def download_as_csv(df, filename):
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )

# For debugging - display session state (you can remove this later)
if st.checkbox("Show session state (Debug)"):
    st.write(st.session_state) 