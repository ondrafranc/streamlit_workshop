import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

# 📈 Market Data Explorer - Solution

st.title("📈 Market Data Explorer")
st.write("Analyze stock data with efficient data loading using caching")

# This function simulates loading large datasets with a delay
# Cached version with TTL of 1 hour (3600 seconds)
@st.cache_data(ttl=3600, show_spinner=False)
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

# For comparison, an uncached version of the function
def load_stock_data_uncached(ticker, years=5):
    # This function has the same implementation but without caching
    return load_stock_data(ticker, years)

# Sidebar controls
st.sidebar.header("Data Controls")

# Select stock
ticker = st.sidebar.selectbox(
    "Select Stock",
    options=["TECH", "RETAIL", "ENERGY", "FINANCE"]
)

# Years of data
years = st.sidebar.slider("Years of Data", 1, 10, 5)

# Choose between cached and uncached
use_cache = st.sidebar.checkbox("Use Caching", value=True)

# Load data button
if st.sidebar.button("Load Data"):
    # Determine which function to use based on checkbox
    loading_function = load_stock_data if use_cache else load_stock_data_uncached
    
    # Data loading process
    with st.spinner("Loading data..."):
        start_time = time.time()
        data = loading_function(ticker, years)
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
    
    # Add a section to demonstrate cache reuse
    st.subheader("Caching Demonstration")
    if st.button("Load Same Data Again"):
        with st.spinner("Loading data again..."):
            start_time = time.time()
            data = loading_function(ticker, years)
            end_time = time.time()
            second_loading_time = end_time - start_time
            
            st.info(f"Second load took {second_loading_time:.2f} seconds")
            st.write(f"Improvement: {loading_time/second_loading_time:.1f}x faster")
            
            if use_cache and second_loading_time < 0.1:
                st.success("The data was served from the cache!")
            elif not use_cache:
                st.warning("Without caching, the data had to be regenerated.")
    
    # MINI-EXERCISE: Caching Performance Comparison
    st.subheader("Caching Performance Test")
    
    # Define a slow calculation function without caching
    def slow_calculation_no_cache(n=1000000):
        """A deliberately slow function without caching"""
        time.sleep(1)  # Simulate a slow operation
        return sum(i**2 for i in range(n))
    
    # Same function but with caching
    @st.cache_data
    def slow_calculation_cached(n=1000000):
        """The same function with caching"""
        time.sleep(1)  # Simulate a slow operation
        return sum(i**2 for i in range(n))
    
    # Button to run comparison
    if st.button("Run Performance Test"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Without Caching**")
            # Run uncached version
            start_time = time.time()
            result1 = slow_calculation_no_cache()
            non_cached_time = time.time() - start_time
            st.metric("Execution time", f"{non_cached_time:.4f} sec")
            
            # Run uncached again
            start_time = time.time()
            result1_again = slow_calculation_no_cache()
            non_cached_time_again = time.time() - start_time
            st.metric("Second run time", f"{non_cached_time_again:.4f} sec")
        
        with col2:
            st.markdown("**With Caching**")
            # Run cached version
            start_time = time.time()
            result2 = slow_calculation_cached()
            cached_time = time.time() - start_time
            st.metric("First execution time", f"{cached_time:.4f} sec")
            
            # Run cached version again (should be near-instant)
            start_time = time.time()
            result2_again = slow_calculation_cached()
            cached_time_again = time.time() - start_time
            st.metric("Second run time", f"{cached_time_again:.4f} sec")
        
        # Show speedup statistics
        speedup = non_cached_time_again / cached_time_again
        st.success(f"Caching made the second run {speedup:.1f}x faster!")

# Cache management
st.sidebar.header("Cache Management")
if st.sidebar.button("Clear Cache"):
    st.cache_data.clear()
    st.sidebar.success("Cache cleared!")

# Display cache info
with st.sidebar.expander("Cache Information"):
    st.write("Caching is used to store the results of expensive operations like data loading.")
    st.write("When you load data with caching enabled, it's stored for reuse.")
    st.write("Try loading data, then change parameters and load again to see the difference.")
    st.write("The 'Clear Cache' button lets you reset all cached data.") 