import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io

# 📊 Sales Dashboard - Exercise
# In this exercise, you'll create an interactive sales dashboard with
# data visualizations and export functionality

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

# TODO: Create a sidebar with date range filter
# Use st.sidebar.date_input to create a date range selector
# Filter the sales_data DataFrame based on the selected date range
# Hint: Create two date inputs (start_date and end_date) and filter using
# sales_data[(sales_data['Date'] >= start_date) & (sales_data['Date'] <= end_date)]


# TODO: Add a category filter using multiselect
# Allow users to select one or more product categories to display
# Filter the data based on selected categories
# Hint: Use st.sidebar.multiselect() with the list of unique categories

# Calculate summary metrics from filtered data

# TODO: Create metrics row showing Total Sales, Total Units, and Profit
# Use st.columns to create 3 columns and st.metric in each column
# Display the sum of Sales, Units, and Profit from the filtered data
# Hint: Use col.metric("Label", value, delta=None)


# TODO: Create a sales over time chart using Plotly
# Group the filtered data by Date and sum the Sales
# Create a line chart showing Sales over time
# Hint: Use px.line() and st.plotly_chart()


# TODO: Create a category comparison chart
# Group the filtered data by Category and sum the Sales and Profit
# Create a bar chart showing Sales and Profit by Category
# Hint: Use px.bar() with barmode='group'


# MINI-EXERCISE: Create a customizable chart with user controls
# Educational purpose: Practice chart customization with user inputs
st.subheader("Customizable Chart")

# TODO: Add a color picker widget for selecting the chart color
# TODO: Add a checkbox for showing/hiding chart gridlines
# TODO: Add a radio button for choosing between line, area, and bar chart types
# TODO: Create a simple chart with a single data series using the selected options
# HINT: Get monthly sales for a single category and visualize with user's preferences


# NEW TODO: Create a pie chart showing category distribution
# Group the filtered data by Category and calculate the percentage of total sales
# Create a pie chart showing the distribution
# Hint: Use px.pie() with values and names parameters


# TODO: Add data export functionality
# Create a section with buttons to export the filtered data as CSV and Excel
# Hint: Use st.download_button() for each format type 