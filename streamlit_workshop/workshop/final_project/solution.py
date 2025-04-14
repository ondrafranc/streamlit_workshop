import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import uuid
import base64

# 💰 Personal Finance Dashboard - Final Project Solution

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
        'id': [str(uuid.uuid4()) for _ in range(20)],
        'date': pd.date_range(end=datetime.now(), periods=20, freq='D'),
        'amount': np.random.normal(100, 50, 20).round(2) * np.random.choice([-1, 1], size=20, p=[0.7, 0.3]),
        'category': np.random.choice(['Groceries', 'Dining', 'Transportation', 'Utilities', 'Entertainment', 'Salary'], 20, p=[0.3, 0.2, 0.15, 0.1, 0.15, 0.1]),
        'description': ['Supermarket', 'Restaurant', 'Gas', 'Electricity', 'Movies', 
                        'Paycheck', 'Groceries', 'Lunch', 'Uber', 'Internet', 
                        'Concert', 'Bonus', 'Food', 'Dinner', 'Bus', 
                        'Water', 'Netflix', 'Paycheck', 'Groceries', 'Coffee']
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

if 'view' not in st.session_state:
    st.session_state.view = "Dashboard"

# Function to load data from CSV
@st.cache_data
def load_csv(uploaded_file):
    df = pd.read_csv(uploaded_file)
    # Add ID column if not present
    if 'id' not in df.columns:
        df['id'] = [str(uuid.uuid4()) for _ in range(len(df))]
    # Convert date strings to datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    return df

# Function to filter transactions by date range
def filter_transactions(df, start_date, end_date, categories=None, transaction_type=None):
    filtered = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]
    
    if categories:
        filtered = filtered[filtered['category'].isin(categories)]
        
    if transaction_type == "Expenses":
        filtered = filtered[filtered['amount'] < 0]
    elif transaction_type == "Income":
        filtered = filtered[filtered['amount'] > 0]
        
    return filtered

# Function to calculate summary statistics
def get_summary_stats(df):
    income = df[df['amount'] > 0]['amount'].sum()
    expenses = abs(df[df['amount'] < 0]['amount'].sum())
    balance = income - expenses
    
    # Safe division to avoid divide by zero
    savings_rate = (income - expenses) / income * 100 if income > 0 else 0
    
    return {
        'income': income,
        'expenses': expenses,
        'balance': balance,
        'savings_rate': savings_rate
    }

# Function to get budget performance
def get_budget_performance(df, budgets):
    # Group expenses by category and sum
    category_spending = (
        df[df['amount'] < 0]
        .groupby('category')['amount']
        .sum()
        .abs()
        .reset_index()
    )
    
    # Calculate budget performance
    result = []
    for category, budget in budgets.items():
        spent = category_spending[category_spending['category'] == category]['amount'].sum()
        if pd.isna(spent):
            spent = 0
        
        result.append({
            'category': category,
            'budget': budget,
            'spent': spent,
            'remaining': budget - spent,
            'percent_used': min(100, (spent / budget * 100)) if budget > 0 else 0
        })
    
    return pd.DataFrame(result)

# Main app title
st.title("💰 Personal Finance Dashboard")

# Navigation tabs in sidebar
st.sidebar.title("Navigation")
view = st.sidebar.radio("Select View", ["Dashboard", "Transactions", "Budgets", "Settings"])
st.session_state.view = view

# File upload option
st.sidebar.header("Data Options")
uploaded_file = st.sidebar.file_uploader("Upload Transaction Data (CSV)", type="csv")

if uploaded_file is not None:
    try:
        upload_data = load_csv(uploaded_file)
        if st.sidebar.button("Replace current data with uploaded data"):
            st.session_state.transactions = upload_data
            st.success("Data loaded successfully!")
            st.rerun()
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

# Date filter (applies to all views)
st.sidebar.header("Date Filter")
all_dates = st.session_state.transactions['date']
min_date = all_dates.min().date()
max_date = all_dates.max().date()

default_start = max_date - timedelta(days=30)
start_date = st.sidebar.date_input("Start Date", default_start, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=start_date, max_value=max_date)

# Category filter
all_categories = sorted(st.session_state.transactions['category'].unique().tolist())
selected_categories = st.sidebar.multiselect("Filter Categories", all_categories, default=all_categories)

# Transaction type filter
transaction_type = st.sidebar.radio("Transaction Type", ["All", "Expenses", "Income"])

# Filter the data
filtered_data = filter_transactions(
    st.session_state.transactions, 
    start_date, 
    end_date, 
    selected_categories if selected_categories else None,
    transaction_type
)

# DASHBOARD VIEW
if st.session_state.view == "Dashboard":
    # Calculate summary statistics
    stats = get_summary_stats(filtered_data)
    
    # Summary metrics
    st.header("Financial Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Income", f"${stats['income']:.2f}")
    with col2:
        st.metric("Expenses", f"${stats['expenses']:.2f}")
    with col3:
        st.metric("Balance", f"${stats['balance']:.2f}", delta=f"{'+' if stats['balance'] > 0 else ''}{stats['balance']:.2f}")
    with col4:
        st.metric("Savings Rate", f"{stats['savings_rate']:.1f}%")
    
    # Expense breakdown by category
    st.header("Expense Breakdown")
    
    expense_data = filtered_data[filtered_data['amount'] < 0].copy()
    if not expense_data.empty:
        # Group by category
        expense_by_category = expense_data.groupby('category')['amount'].sum().abs().reset_index()
        expense_by_category = expense_by_category.sort_values('amount', ascending=False)
        
        # Create two columns for pie chart and bar chart
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart
            fig_pie = px.pie(
                expense_by_category,
                values='amount',
                names='category',
                title='Expense Distribution',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Bar chart
            fig_bar = px.bar(
                expense_by_category,
                x='category',
                y='amount',
                title='Expenses by Category',
                labels={'amount': 'Amount ($)', 'category': 'Category'},
                color='category',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No expense data available for the selected period.")
    
    # Time series of income/expenses
    st.header("Income & Expenses Over Time")
    
    # Group by date
    daily_totals = filtered_data.groupby(['date', 
                                         pd.Grouper(key='amount', 
                                         apply=lambda x: 'Income' if x > 0 else 'Expense')])['amount'].sum().reset_index()
    daily_totals['amount'] = daily_totals['amount'].abs()
    
    # Plot time series
    if not daily_totals.empty:
        fig_time = px.line(
            daily_totals,
            x='date',
            y='amount',
            color='amount',
            markers=True,
            labels={'date': 'Date', 'amount_y': 'Amount ($)', 'amount_color': 'Type'},
            title='Daily Financial Activity'
        )
        st.plotly_chart(fig_time, use_container_width=True)
    else:
        st.info("No transaction data available for the selected period.")
    
    # Budget performance
    st.header("Budget Performance")
    
    # Get budget performance
    budget_performance = get_budget_performance(filtered_data, st.session_state.budgets)
    
    # Horizontal bar chart for budget vs actual
    if not budget_performance.empty:
        fig_budget = go.Figure()
        
        # Add bars for budget
        fig_budget.add_trace(go.Bar(
            y=budget_performance['category'],
            x=budget_performance['budget'],
            name='Budget',
            orientation='h',
            marker=dict(color='rgba(58, 71, 80, 0.6)')
        ))
        
        # Add bars for amount spent
        fig_budget.add_trace(go.Bar(
            y=budget_performance['category'],
            x=budget_performance['spent'],
            name='Spent',
            orientation='h',
            marker=dict(color='rgba(246, 78, 139, 0.6)')
        ))
        
        fig_budget.update_layout(
            title='Budget vs. Actual Spending',
            barmode='group',
            xaxis_title='Amount ($)',
            yaxis_title='Category'
        )
        
        st.plotly_chart(fig_budget, use_container_width=True)
        
        # Budget progress
        st.subheader("Budget Progress")
        for i, row in budget_performance.iterrows():
            # Create a progress bar
            col1, col2 = st.columns([3, 1])
            with col1:
                progress_color = (
                    "red" if row['percent_used'] > 90 else 
                    "orange" if row['percent_used'] > 75 else 
                    "green"
                )
                st.progress(row['percent_used'] / 100)
            with col2:
                st.write(f"{row['category']}: ${row['spent']:.2f} / ${row['budget']:.2f}")
    else:
        st.info("No budget data available.")

# TRANSACTIONS VIEW
elif st.session_state.view == "Transactions":
    st.header("Transactions")
    
    # Form to add new transaction
    with st.expander("Add New Transaction"):
        with st.form("transaction_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                new_date = st.date_input("Date", datetime.now())
                new_amount = st.number_input("Amount", value=0.0, step=0.01)
            
            with col2:
                new_category = st.selectbox("Category", all_categories)
                new_type = st.radio("Type", ["Expense", "Income"])
            
            with col3:
                new_description = st.text_input("Description")
            
            submit_button = st.form_submit_button("Add Transaction")
            
            if submit_button:
                # Adjust sign based on transaction type
                adjusted_amount = abs(new_amount)
                if new_type == "Expense":
                    adjusted_amount = -adjusted_amount
                
                # Create new transaction
                new_transaction = {
                    'id': str(uuid.uuid4()),
                    'date': pd.to_datetime(new_date),
                    'amount': adjusted_amount,
                    'category': new_category,
                    'description': new_description
                }
                
                # Add to dataframe
                st.session_state.transactions = pd.concat([
                    st.session_state.transactions,
                    pd.DataFrame([new_transaction])
                ], ignore_index=True)
                
                st.success("Transaction added!")
                st.rerun()
    
    # Display all transactions
    st.subheader("Transaction List")
    
    # Create a copy for display with formatted amount
    display_data = filtered_data.copy()
    display_data['amount_formatted'] = display_data['amount'].apply(
        lambda x: f"${x:.2f}" if x > 0 else f"-${abs(x):.2f}"
    )
    
    # Use the data editor to allow editing
    edited_data = st.data_editor(
        display_data,
        column_config={
            "id": st.column_config.TextColumn(
                "ID",
                disabled=True,
                width="small"
            ),
            "date": st.column_config.DateColumn(
                "Date",
                width="medium"
            ),
            "amount": st.column_config.NumberColumn(
                "Amount",
                width="medium",
                format="%.2f"
            ),
            "amount_formatted": st.column_config.TextColumn(
                "Formatted Amount",
                disabled=True,
                width="small"
            ),
            "category": st.column_config.SelectboxColumn(
                "Category",
                options=all_categories,
                width="medium"
            ),
            "description": st.column_config.TextColumn(
                "Description",
                width="large"
            )
        },
        hide_index=True,
        num_rows="dynamic",
        key="transaction_editor"
    )
    
    # Update button
    if st.button("Update Transactions"):
        # Remove the display column and update the main dataframe
        if 'amount_formatted' in edited_data.columns:
            edited_data = edited_data.drop(columns=['amount_formatted'])
        
        # Update the main dataframe while preserving rows not in the filter
        for idx, row in edited_data.iterrows():
            transaction_id = row['id']
            # Find the corresponding row in the main dataframe
            main_idx = st.session_state.transactions[st.session_state.transactions['id'] == transaction_id].index
            if not main_idx.empty:
                # Update the row
                st.session_state.transactions.loc[main_idx, edited_data.columns] = row
        
        st.success("Transactions updated!")
        st.rerun()
    
    # Export options
    st.subheader("Export Options")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export as CSV"):
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"transactions_{start_date}_to_{end_date}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("Export as Excel"):
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                filtered_data.to_excel(writer, sheet_name='Transactions', index=False)
                
                # Add summary sheet
                stats = get_summary_stats(filtered_data)
                summary_df = pd.DataFrame({
                    'Metric': ['Income', 'Expenses', 'Balance', 'Savings Rate', 'Date Range'],
                    'Value': [
                        f"${stats['income']:.2f}",
                        f"${stats['expenses']:.2f}",
                        f"${stats['balance']:.2f}",
                        f"{stats['savings_rate']:.1f}%",
                        f"{start_date} to {end_date}"
                    ]
                })
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Add category breakdown
                if not filtered_data.empty:
                    expense_by_category = (filtered_data[filtered_data['amount'] < 0]
                                          .groupby('category')['amount'].sum().abs()
                                          .reset_index()
                                          .sort_values('amount', ascending=False))
                    expense_by_category.columns = ['Category', 'Amount']
                    expense_by_category.to_excel(writer, sheet_name='Expense Breakdown', index=False)
            
            excel_data = buffer.getvalue()
            st.download_button(
                label="Download Excel",
                data=excel_data,
                file_name=f"transactions_{start_date}_to_{end_date}.xlsx",
                mime="application/vnd.ms-excel"
            )

# BUDGET VIEW
elif st.session_state.view == "Budgets":
    st.header("Budget Settings")
    
    # Form to update budget
    with st.form("budget_form"):
        st.subheader("Set Monthly Budget Limits")
        
        # Create input fields for each category
        updated_budgets = {}
        cols = st.columns(3)
        
        for i, (category, amount) in enumerate(st.session_state.budgets.items()):
            col_idx = i % 3
            with cols[col_idx]:
                updated_budgets[category] = st.number_input(
                    f"{category} ($)",
                    min_value=0.0,
                    value=float(amount),
                    step=50.0
                )
        
        # Submit button
        if st.form_submit_button("Update Budgets"):
            st.session_state.budgets = updated_budgets
            st.success("Budgets updated!")
    
    # Display current budget vs actual
    st.header("Budget Performance")
    
    # Calculate budget performance for the current month
    current_month_start = datetime(datetime.now().year, datetime.now().month, 1).date()
    current_month_end = (datetime(datetime.now().year, datetime.now().month + 1, 1) - timedelta(days=1)).date()
    
    current_month_data = filter_transactions(
        st.session_state.transactions, 
        current_month_start, 
        current_month_end
    )
    
    budget_performance = get_budget_performance(current_month_data, st.session_state.budgets)
    
    # Display as a bar chart
    if not budget_performance.empty:
        fig = px.bar(
            budget_performance,
            x='category',
            y=['budget', 'spent'],
            title='Budget vs. Actual Spending (Current Month)',
            barmode='group',
            labels={'value': 'Amount ($)', 'variable': 'Type'},
            color_discrete_map={'budget': 'lightblue', 'spent': 'coral'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Budget progress table
        st.subheader("Budget Progress Details")
        
        # Format data for display
        display_df = budget_performance.copy()
        display_df['percent_used'] = display_df['percent_used'].round(1).astype(str) + '%'
        display_df['status'] = display_df.apply(
            lambda x: "❌ Over Budget" if x['spent'] > x['budget'] else
                      "⚠️ Warning" if x['spent'] / x['budget'] > 0.8 else
                      "✅ On Track",
            axis=1
        )
        
        # Rename columns for display
        display_df = display_df.rename(columns={
            'category': 'Category',
            'budget': 'Budget ($)',
            'spent': 'Spent ($)',
            'remaining': 'Remaining ($)',
            'percent_used': 'Used',
            'status': 'Status'
        })
        
        st.dataframe(
            display_df[['Category', 'Budget ($)', 'Spent ($)', 'Remaining ($)', 'Used', 'Status']],
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No transaction data available for the current month.")

# SETTINGS VIEW
else:  # Settings view
    st.header("Settings")
    
    # Clear data option
    st.subheader("Data Management")
    
    if st.button("Reset to Sample Data"):
        # Clear session state and rerun
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    # Export all data
    if st.button("Export All Data"):
        csv = st.session_state.transactions.to_csv(index=False)
        st.download_button(
            label="Download Complete Dataset (CSV)",
            data=csv,
            file_name="all_transactions.csv",
            mime="text/csv"
        )
    
    # Add new category
    st.subheader("Manage Categories")
    
    with st.form("category_form"):
        new_category = st.text_input("New Category Name")
        submitted = st.form_submit_button("Add Category")
        
        if submitted and new_category:
            # Add to budgets with default value
            if new_category not in st.session_state.budgets:
                st.session_state.budgets[new_category] = 0.0
                st.success(f"Added category: {new_category}")
                st.rerun()
            else:
                st.error("Category already exists!")
    
    # App information
    st.subheader("About")
    st.write("""
    📊 **Personal Finance Dashboard**  
    This application helps you track your personal finances, set budgets, 
    and analyze your spending patterns.
    
    Built with Streamlit as part of the Streamlit Workshop for Data Professionals.
    """)

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("© 2023 Streamlit Workshop")

# Add Debug Section in Settings
if st.session_state.view == "Settings":
    with st.expander("Debug Info"):
        st.write("Session State Variables:")
        for key, value in st.session_state.items():
            if key == 'transactions':
                st.write(f"transactions: DataFrame with {len(value)} rows")
            elif key == 'budgets':
                st.write("budgets:", value)
            else:
                st.write(f"{key}:", value) 