import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

# 📈 Market Data Explorer - Exercise
# In this exercise, you'll learn how to implement caching to improve 
# app performance when working with large datasets

st.title("📈 Market Data Explorer")
st.write("Analyze stock data with efficient data loading using caching")

# This function simulates loading large datasets with a delay
def load_stock_data(ticker, years=5):
    # Simulate data loading time
    time.sleep(2)  # This represents an expensive operation (API call, DB query, etc.)
    
    # Generate synthetic stock data
    dates = pd.date_range(end=pd.Timestamp.today(), periods=years*252, freq='B')
    np.random.seed(42)  # For reproducible results
    
    # Different price ranges based on ticker
    if ticker == "TECH":
        start_price = 150
        volatility = 2
    elif ticker == "RETAIL":
        start_price = 75
        volatility = 1.5
    elif ticker == "ENERGY":
        start_price = 50
        volatility = 1.8
    else:
        start_price = 100
        volatility = 1.2
    
    # Generate a random walk for the stock price
    price_changes = np.random.normal(0.0005, 0.015, len(dates)) * volatility
    prices = start_price * (1 + np.cumsum(price_changes))
    
    # Create dataframe
    df = pd.DataFrame({
        'Date': dates,
        'Price': prices,
        'Volume': np.random.randint(100000, 10000000, len(dates))
    })
    
    st.write(f"Data loaded for {ticker} with {len(df)} rows")
    return df

# TODO: Implement caching for the load_stock_data function
# Hint: Use @st.cache_data decorator with ttl parameter of 3600 seconds


# Sidebar controls
st.sidebar.header("Data Controls")

# Select stock
ticker = st.sidebar.selectbox(
    "Select Stock",
    options=["TECH", "RETAIL", "ENERGY", "FINANCE"]
)

# Years of data
years = st.sidebar.slider("Years of Data", 1, 10, 5)

# Load data button
if st.sidebar.button("Load Data"):
    # Data loading process
    with st.spinner("Loading data..."):
        start_time = time.time()
        data = load_stock_data(ticker, years)
        end_time = time.time()
        
        # Display loading time
        loading_time = end_time - start_time
        st.sidebar.info(f"Data loaded in {loading_time:.2f} seconds")
    
    # Display data summary
    st.subheader("Data Summary")
    st.write(f"Stock: {ticker}")
    st.write(f"Time Period: {data['Date'].min().date()} to {data['Date'].max().date()}")
    st.write(f"Number of trading days: {len(data)}")
    
    # Display recent data
    st.subheader("Recent Price Data")
    st.dataframe(data.tail())
    
    # Create a simple plot
    st.subheader("Price Chart")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data['Date'], data['Price'])
    ax.set_title(f"{ticker} Stock Price")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price ($)")
    st.pyplot(fig)
    
    # TODO: Add a second call to load_stock_data with the same parameters
    # This will demonstrate the caching in action - it should be much faster the second time
    # Hint: Add another button and time the second data load
    pass
    
    # MINI-EXERCISE: Compare performance of cached vs non-cached function
    # Educational purpose: Demonstrate the speed difference with caching
    st.subheader("Caching Performance Test")
    
    # TODO: Create a non-cached version of a slow function (e.g., one that does heavy computation)
    # TODO: Create a cached version of the same function
    # TODO: Add a button to run both and compare execution times
    # HINT: Use time.time() before and after each function call to measure execution time
    pass

# TODO: Add a way to clear the cache
# Hint: Use st.cache_data.clear()
    