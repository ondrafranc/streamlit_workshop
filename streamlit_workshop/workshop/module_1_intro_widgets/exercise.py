import streamlit as st
import pandas as pd

# ☕ Cafe Order App - Exercise
# In this exercise, you'll build a simple coffee shop ordering system
# using Streamlit widgets and layouts

# TODO: Add a title for the app with an emoji
# Hint: Use st.title()


# TODO: Create a sidebar for the order customization
# Hint: Use 'with st.sidebar:'


# TODO: In the sidebar, add:
# 1. A selectbox for coffee type (Options: Espresso, Latte, Cappuccino, Americano, Mocha)
# 2. A slider for coffee size (Range: 8-20 oz, Step: 2, Default: 12)
# 3. A checkbox for 'Add whipped cream?'
# 4. A checkbox for 'Make it iced?'
# Hint: Use st.selectbox(), st.slider(), st.checkbox()


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

# TODO: Create two columns for the main content
# Hint: Use st.columns()


# MINI-EXERCISE: Create an interactive tip calculator
# Educational purpose: Practice using widgets and basic calculations
st.subheader("Tip Calculator")

# TODO: Create a slider for selecting tip percentage (10-30%, step 1, default 15%)
# TODO: Create a numeric input for the bill amount (default 50)
# TODO: Display the calculated tip amount and total bill
# HINT: Total = Bill + (Bill * Tip%)
pass


# TODO: In the first column, display an order summary including:
# - Coffee type and size
# - Whether it includes whipped cream
# - Whether it's iced
# - The total price (base coffee price + size adjustment + 0.50 for whipped cream)
# Hint: Use col1.subheader() and col1.write()


# TODO: In the second column, add a image placeholder and an "Order Now" button
# Hint: Use col2.image() with a URL of a coffee image
# For the button, use col2.button()


# TODO: Add an expander section at the bottom called "Nutrition Information"
# Inside the expander, create a simple dataframe with nutritional info and display it
# Hint: Use st.expander() and st.dataframe() 