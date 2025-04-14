import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io

# 📊 Sales Dashboard - Solution

st.title("📊 Sales Dashboard")
st.write("Analyze sales data with interactive visualizations and export options")

# Generate synthetic sales data
@st.cache_data
def generate_sales_data():
    # Create date range for the past year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Generate random sales data
    np.random.seed(42)  # For reproducible results
    
    # Product categories
    categories = ['Electronics', 'Clothing', 'Home Goods', 'Sports', 'Books']
    
    # Generate sales records
    data = []
    for date in date_range:
        # Add random sales for each category on each day
        for category in categories:
            # More sales on weekends
            weekend_boost = 1.5 if date.dayofweek >= 5 else 1.0
            # Seasonal variation (higher in Dec, lower in Jan)
            month_factor = 1.3 if date.month == 12 else 0.8 if date.month == 1 else 1.0
            
            # Base sales vary by category
            if category == 'Electronics':
                base_sales = np.random.normal(5000, 1500)
            elif category == 'Clothing':
                base_sales = np.random.normal(3000, 1000)
            elif category == 'Home Goods':
                base_sales = np.random.normal(2500, 800)
            elif category == 'Sports':
                base_sales = np.random.normal(2000, 600)
            else:  # Books
                base_sales = np.random.normal(1500, 400)
            
            # Calculate daily sales
            daily_sales = abs(base_sales * weekend_boost * month_factor)
            units_sold = int(daily_sales / (base_sales / 100))  # Roughly scale to reasonable units
            
            # Add some randomness to profit margin (between 15-40%)
            profit_margin = np.random.uniform(0.15, 0.40)
            profit = daily_sales * profit_margin
            
            data.append({
                'Date': date,
                'Category': category,
                'Sales': daily_sales,
                'Units': units_sold,
                'Profit': profit
            })
    
    # Convert to DataFrame
    return pd.DataFrame(data)

# Load data
sales_data = generate_sales_data()

# Sidebar - Date Range Filter
st.sidebar.header("Filters")

# Date range selector
min_date = sales_data['Date'].min().date()
max_date = sales_data['Date'].max().date()

start_date = st.sidebar.date_input(
    "Start Date",
    min_date,
    min_value=min_date,
    max_value=max_date
)

end_date = st.sidebar.date_input(
    "End Date",
    max_date,
    min_value=start_date,
    max_value=max_date
)

# Category filter
all_categories = sales_data['Category'].unique().tolist()
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=all_categories,
    default=all_categories
)

# Filtering data based on selections
filtered_data = sales_data[
    (sales_data['Date'].dt.date >= start_date) & 
    (sales_data['Date'].dt.date <= end_date) &
    (sales_data['Category'].isin(selected_categories))
]

# Chart display options
st.sidebar.header("Chart Options")
chart_type = st.sidebar.selectbox(
    "Time Series Chart Type",
    options=["Line Chart", "Area Chart", "Bar Chart"]
)

show_trendline = st.sidebar.checkbox("Show Trend Line", value=False)

# Metrics calculation
total_sales = filtered_data['Sales'].sum()
total_units = filtered_data['Units'].sum()
total_profit = filtered_data['Profit'].sum()

# Calculate period-over-period comparison (last 30 days vs previous 30 days)
last_30_days = filtered_data[filtered_data['Date'] >= (max(filtered_data['Date']) - timedelta(days=30))]
previous_30_days = filtered_data[
    (filtered_data['Date'] < (max(filtered_data['Date']) - timedelta(days=30))) & 
    (filtered_data['Date'] >= (max(filtered_data['Date']) - timedelta(days=60)))
]

sales_delta = None
units_delta = None
profit_delta = None

if not last_30_days.empty and not previous_30_days.empty:
    last_30_sales = last_30_days['Sales'].sum()
    prev_30_sales = previous_30_days['Sales'].sum()
    sales_delta = (last_30_sales - prev_30_sales) / prev_30_sales * 100 if prev_30_sales > 0 else 0
    
    last_30_units = last_30_days['Units'].sum()
    prev_30_units = previous_30_days['Units'].sum()
    units_delta = (last_30_units - prev_30_units) / prev_30_units * 100 if prev_30_units > 0 else 0
    
    last_30_profit = last_30_days['Profit'].sum()
    prev_30_profit = previous_30_days['Profit'].sum()
    profit_delta = (last_30_profit - prev_30_profit) / prev_30_profit * 100 if prev_30_profit > 0 else 0

# Display metrics
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Sales",
        f"${total_sales:,.2f}",
        f"{sales_delta:.1f}%" if sales_delta is not None else None
    )

with col2:
    st.metric(
        "Total Units Sold",
        f"{total_units:,}",
        f"{units_delta:.1f}%" if units_delta is not None else None
    )

with col3:
    st.metric(
        "Total Profit",
        f"${total_profit:,.2f}",
        f"{profit_delta:.1f}%" if profit_delta is not None else None
    )

# Time series chart
st.subheader("Sales Over Time")

# Group by date and calculate daily totals
daily_sales = filtered_data.groupby('Date').agg({
    'Sales': 'sum',
    'Units': 'sum',
    'Profit': 'sum'
}).reset_index()

if chart_type == "Line Chart":
    fig = px.line(
        daily_sales,
        x='Date',
        y='Sales',
        title='Daily Sales',
        labels={'Sales': 'Sales ($)', 'Date': 'Date'},
        trendline='ols' if show_trendline else None
    )
elif chart_type == "Area Chart":
    fig = px.area(
        daily_sales,
        x='Date',
        y='Sales',
        title='Daily Sales',
        labels={'Sales': 'Sales ($)', 'Date': 'Date'}
    )
else:  # Bar Chart
    fig = px.bar(
        daily_sales,
        x='Date',
        y='Sales',
        title='Daily Sales',
        labels={'Sales': 'Sales ($)', 'Date': 'Date'}
    )

fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

# Category comparison chart
st.subheader("Sales by Category")

# Group by category
category_data = filtered_data.groupby('Category').agg({
    'Sales': 'sum',
    'Profit': 'sum'
}).reset_index()

# Create bar chart
fig2 = px.bar(
    category_data,
    x='Category',
    y=['Sales', 'Profit'],
    title='Sales and Profit by Category',
    barmode='group',
    labels={'value': 'Amount ($)', 'variable': 'Metric'},
    color_discrete_map={'Sales': '#1f77b4', 'Profit': '#2ca02c'}
)

st.plotly_chart(fig2, use_container_width=True)

# MINI-EXERCISE: Customizable Chart
st.subheader("Customizable Chart")

# User customization controls
col_controls1, col_controls2 = st.columns(2)

with col_controls1:
    # Color picker for chart
    chart_color = st.color_picker("Choose chart color", "#1f77b4")
    # Category selection for single-category view
    chart_category = st.selectbox("Select category to visualize", all_categories)

with col_controls2:
    # Show/hide gridlines
    show_grid = st.checkbox("Show gridlines", True)
    # Chart type selection
    custom_chart_type = st.radio("Chart type", ["Line", "Area", "Bar"], horizontal=True)

# Get data for selected category
category_sales = filtered_data[filtered_data['Category'] == chart_category]

# Group by month for a cleaner visualization
category_sales['Month'] = category_sales['Date'].dt.strftime('%b %Y')
monthly_category_sales = category_sales.groupby('Month').agg({
    'Sales': 'sum',
    'Profit': 'sum'
}).reset_index()

# Sort chronologically
month_order = pd.to_datetime(category_sales['Date'].dt.strftime('%Y-%m-01')).dt.strftime('%b %Y').unique()
monthly_category_sales['Month'] = pd.Categorical(monthly_category_sales['Month'], categories=month_order, ordered=True)
monthly_category_sales = monthly_category_sales.sort_values('Month')

# Create customized chart
if not monthly_category_sales.empty:
    custom_fig = None
    if custom_chart_type == "Line":
        custom_fig = px.line(monthly_category_sales, x='Month', y='Sales')
    elif custom_chart_type == "Area":
        custom_fig = px.area(monthly_category_sales, x='Month', y='Sales')
    else:  # Bar
        custom_fig = px.bar(monthly_category_sales, x='Month', y='Sales')
    
    # Apply custom styling
    custom_fig.update_traces(line_color=chart_color, marker_color=chart_color, fill='tozeroy')
    
    # Update layout based on user preferences
    custom_fig.update_layout(
        title=f"{chart_category} Monthly Sales",
        showlegend=False,
        xaxis=dict(showgrid=show_grid, title="Month"),
        yaxis=dict(showgrid=show_grid, title="Sales ($)"),
        height=400
    )
    
    st.plotly_chart(custom_fig, use_container_width=True)
    
    # Show a summary of the selected category
    total_cat_sales = monthly_category_sales['Sales'].sum()
    avg_monthly_sales = monthly_category_sales['Sales'].mean()
    
    summary_col1, summary_col2 = st.columns(2)
    with summary_col1:
        st.metric(f"Total {chart_category} Sales", f"${total_cat_sales:,.2f}")
    with summary_col2:
        st.metric(f"Avg. Monthly {chart_category} Sales", f"${avg_monthly_sales:,.2f}")
else:
    st.info(f"No data available for {chart_category} in the selected date range")

# NEW: Category Pie Chart
st.subheader("Category Distribution")

# Create two columns for different pie charts
col1, col2 = st.columns(2)

with col1:
    # Sales distribution pie chart
    fig_pie_sales = px.pie(
        category_data,
        values='Sales',
        names='Category',
        title='Sales Distribution by Category',
        hole=0.4,  # Donut chart
        color_discrete_sequence=px.colors.sequential.Plasma_r
    )
    fig_pie_sales.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie_sales, use_container_width=True)

with col2:
    # Profit distribution pie chart
    fig_pie_profit = px.pie(
        category_data,
        values='Profit',
        names='Category',
        title='Profit Distribution by Category',
        color_discrete_sequence=px.colors.sequential.Viridis_r
    )
    fig_pie_profit.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie_profit, use_container_width=True)

# Monthly trend chart
st.subheader("Monthly Sales Trend")

# Group by month
filtered_data['Month'] = filtered_data['Date'].dt.strftime('%b %Y')
monthly_data = filtered_data.groupby('Month').agg({
    'Sales': 'sum',
    'Profit': 'sum'
}).reset_index()

# Sort by date (not alphabetically)
month_order = pd.to_datetime(filtered_data['Date'].dt.strftime('%Y-%m-01')).dt.strftime('%b %Y').unique()
monthly_data['Month'] = pd.Categorical(monthly_data['Month'], categories=month_order, ordered=True)
monthly_data = monthly_data.sort_values('Month')

# Create line chart with markers
fig3 = px.line(
    monthly_data,
    x='Month',
    y=['Sales', 'Profit'],
    title='Monthly Sales and Profit Trend',
    labels={'value': 'Amount ($)', 'variable': 'Metric'},
    markers=True,
    color_discrete_map={'Sales': '#1f77b4', 'Profit': '#2ca02c'}
)

st.plotly_chart(fig3, use_container_width=True)

# Data Export Section
st.subheader("Export Data")
col1, col2 = st.columns(2)

# CSV Export
with col1:
    csv = filtered_data.to_csv(index=False)
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name=f"sales_data_{start_date}_to_{end_date}.csv",
        mime="text/csv"
    )

# Excel Export
with col2:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        filtered_data.to_excel(writer, sheet_name='Sales Data', index=False)
        # Add summary sheet
        summary_data = pd.DataFrame({
            'Metric': ['Total Sales', 'Total Units', 'Total Profit', 'Date Range', 'Categories'],
            'Value': [
                f"${total_sales:,.2f}",
                f"{total_units:,}",
                f"${total_profit:,.2f}",
                f"{start_date} to {end_date}",
                ", ".join(selected_categories)
            ]
        })
        summary_data.to_excel(writer, sheet_name='Summary', index=False)
    
    excel_data = buffer.getvalue()
    st.download_button(
        label="Download as Excel",
        data=excel_data,
        file_name=f"sales_data_{start_date}_to_{end_date}.xlsx",
        mime="application/vnd.ms-excel"
    ) 