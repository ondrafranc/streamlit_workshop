import streamlit as st
import pandas as pd
import datetime

# 📊 Customer Feedback System - Exercise
# In this exercise, you'll build a customer feedback collection and viewing system
# using Streamlit's data input and display capabilities

st.title("📊 Customer Feedback System")
st.write("Collect and analyze customer feedback for your business")

# Initialize the feedback dataframe if it doesn't exist in session state
if 'feedback_data' not in st.session_state:
    # Starting with some sample feedback
    st.session_state.feedback_data = pd.DataFrame({
        'Date': [datetime.date(2023, 5, 15), datetime.date(2023, 5, 16), datetime.date(2023, 5, 17)],
        'Customer Name': ['John Doe', 'Jane Smith', 'Robert Johnson'],
        'Product': ['Coffee Maker', 'Blender', 'Toaster'],
        'Rating': [4, 5, 3],
        'Comments': ['Good product, but difficult to clean', 
                    'Excellent performance and durability', 
                    'Decent value for the price, but not exceptional']
    })

# Create tabs for different sections
tab1, tab2 = st.tabs(["Submit Feedback", "View Feedback"])

# Tab 1: Submit Feedback
with tab1:
    # TODO: Create a feedback submission form using st.form()
    # The form should include:
    # 1. Text input for customer name
    # 2. Selectbox for product (Options: Coffee Maker, Blender, Toaster, Microwave, Food Processor)
    # 3. Slider for rating (1-5)
    # 4. Text area for comments
    # 5. Submit button
    # When submitted, add the feedback to st.session_state.feedback_data
    # Hint: Remember to include the current date with the submission
    pass
    
# Tab 2: View Feedback
with tab2:
    st.header("Customer Feedback")
    
    # TODO: Add a search box to filter feedback by customer name
    # Hint: Use st.text_input() and filter the dataframe based on the input
    pass
    
    # TODO: Add a filter for product type using st.multiselect()
    # The multiselect should allow selecting multiple products to view
    # Hint: Use .isin() method to filter the DataFrame
    pass
    
    # MINI-EXERCISE: Create a simple text search filter for the feedback data
    # Educational purpose: Practice filtering dataframes based on text input
    st.subheader("Search Comments")
    
    # TODO: Add a text input widget for searching in the comments field
    # TODO: Filter the dataframe to only show rows where the comment contains the search text
    # TODO: Display the count of matching results
    # HINT: Use str.contains() method with case=False parameter
    pass
    
    # TODO: Display the filtered feedback using st.dataframe() or st.data_editor()
    # Include column configuration to:
    # 1. Format the date column
    # 2. Show the rating column as a number or bar chart
    # 3. Make the comments column wider
    # Hint: Use column_config parameter
    pass
    
    # TODO: Add a section showing average rating by product
    # Hint: Use DataFrame groupby and mean operations, then display as a dataframe
    pass 