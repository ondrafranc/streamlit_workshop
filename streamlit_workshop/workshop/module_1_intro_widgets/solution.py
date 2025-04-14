import streamlit as st
import pandas as pd

# ☕ Cafe Order App - Solution

# Set page title
st.title("☕ Cafe Order App")

# Create sidebar for order customization
with st.sidebar:
    st.header("Customize Your Order")
    
    # Coffee selection
    coffee_type = st.selectbox(
        "Select coffee type",
        options=["Espresso", "Latte", "Cappuccino", "Americano", "Mocha"]
    )
    
    # Size selection
    size = st.slider(
        "Select size (oz)",
        min_value=8,
        max_value=20,
        value=12,
        step=2
    )
    
    # Add-ons
    whipped_cream = st.checkbox("Add whipped cream?")
    iced = st.checkbox("Make it iced?")

# These dictionaries define the prices
coffee_prices = {
    "Espresso": 2.50,
    "Latte": 3.50, 
    "Cappuccino": 3.50,
    "Americano": 3.00,
    "Mocha": 4.00
}

size_price_adjustments = {
    8: -0.50,
    10: -0.25,
    12: 0.00,
    14: 0.25,
    16: 0.50,
    18: 0.75,
    20: 1.00
}

# Calculate price
base_price = coffee_prices[coffee_type]
size_adjustment = size_price_adjustments[size]
whipped_cream_price = 0.50 if whipped_cream else 0.00
total_price = base_price + size_adjustment + whipped_cream_price

# Create two columns for main content
col1, col2 = st.columns(2)

# MINI-EXERCISE: Interactive Tip Calculator
st.subheader("Tip Calculator")

# Tip calculator implementation
tip_percent = st.slider("Tip percentage", 10, 30, 15, 1)
bill_amount = st.number_input("Bill amount ($)", min_value=0.0, value=50.0, step=0.01)

# Calculate tip and total
tip_amount = bill_amount * (tip_percent / 100)
total_bill = bill_amount + tip_amount

# Display results
col_tip1, col_tip2 = st.columns(2)
with col_tip1:
    st.metric("Tip amount", f"${tip_amount:.2f}")
with col_tip2:
    st.metric("Total bill", f"${total_bill:.2f}")

st.divider()  # Add a visual separator

# First column: Order summary
with col1:
    st.subheader("Order Summary")
    st.write(f"**Coffee:** {coffee_type}")
    st.write(f"**Size:** {size} oz")
    st.write(f"**Whipped Cream:** {'Yes' if whipped_cream else 'No'}")
    st.write(f"**Iced:** {'Yes' if iced else 'No'}")
    
    st.subheader(f"Total: ${total_price:.2f}")
    st.write("*Price includes:*")
    st.write(f"- Base: ${base_price:.2f}")
    st.write(f"- Size adjustment: ${size_adjustment:.2f}")
    if whipped_cream:
        st.write(f"- Whipped cream: $0.50")

# Second column: Image and order button
with col2:
    # Display image based on coffee type (using placeholder URLs)
    if iced:
        st.image("https://images.unsplash.com/photo-1517701604599-bb29b565090c?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80", 
                 caption=f"Iced {coffee_type}")
    else:
        st.image("https://images.unsplash.com/photo-1572286258217-40156f34fa56?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80", 
                 caption=f"Hot {coffee_type}")
    
    # Order button
    if st.button("Order Now"):
        st.success(f"Your order of a {size}oz {coffee_type} has been placed! Please pay ${total_price:.2f} at the counter.")

# Nutrition information in an expander
with st.expander("Nutrition Information"):
    # Create a simple dataframe for nutritional info
    nutritional_info = pd.DataFrame({
        'Coffee Type': ["Espresso", "Latte", "Cappuccino", "Americano", "Mocha"],
        'Calories (8oz)': [5, 120, 110, 10, 170],
        'Fat (g)': [0, 4, 4, 0, 5],
        'Caffeine (mg)': [65, 55, 55, 65, 60]
    })
    st.dataframe(nutritional_info) 