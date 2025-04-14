import streamlit as st
import pandas as pd
import datetime

# 📊 Customer Feedback System - Solution

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
    st.header("Submit Your Feedback")
    
    # Create feedback form
    with st.form("feedback_form"):
        # Form inputs
        customer_name = st.text_input("Your Name")
        product = st.selectbox(
            "Product",
            options=["Coffee Maker", "Blender", "Toaster", "Microwave", "Food Processor"]
        )
        rating = st.slider("Rating", 1, 5, 3)
        comments = st.text_area("Comments")
        
        # Submit button
        submit_button = st.form_submit_button("Submit Feedback")
        
        # Process form submission
        if submit_button and customer_name:  # Basic validation
            # Create new feedback entry
            new_feedback = {
                'Date': datetime.date.today(),
                'Customer Name': customer_name,
                'Product': product,
                'Rating': rating,
                'Comments': comments
            }
            
            # Add to existing data
            st.session_state.feedback_data = pd.concat([
                st.session_state.feedback_data, 
                pd.DataFrame([new_feedback])
            ], ignore_index=True)
            
            st.success("Thank you for your feedback!")

# Tab 2: View Feedback
with tab2:
    st.header("Customer Feedback")
    
    # Search by customer name
    search_name = st.text_input("Search by Customer Name")
    
    # Filter by product
    all_products = st.session_state.feedback_data['Product'].unique().tolist()
    selected_products = st.multiselect(
        "Filter by Product",
        options=all_products,
        default=all_products
    )
    
    # MINI-EXERCISE: Text search in comments
    st.subheader("Search Comments")
    
    # Text search implementation
    search_text = st.text_input("Search in comments:")
    
    # Filter data based on search
    if search_text:
        comment_results = st.session_state.feedback_data[
            st.session_state.feedback_data['Comments'].str.contains(search_text, case=False)
        ]
        st.success(f"Found {len(comment_results)} matching comments")
        
        # Show the results in a simple table
        if not comment_results.empty:
            st.dataframe(
                comment_results[['Customer Name', 'Product', 'Comments']],
                use_container_width=True
            )
    
    st.divider()  # Add visual separator
    
    # Apply filters
    filtered_data = st.session_state.feedback_data.copy()
    
    # Filter by name (if search provided)
    if search_name:
        filtered_data = filtered_data[filtered_data['Customer Name'].str.contains(search_name, case=False)]
    
    # Filter by selected products
    if selected_products:
        filtered_data = filtered_data[filtered_data['Product'].isin(selected_products)]
    
    # Display filtered feedback with formatting
    st.subheader("Feedback Data")
    st.dataframe(
        filtered_data,
        column_config={
            "Date": st.column_config.DateColumn(
                "Date Submitted",
                format="MM/DD/YYYY",
            ),
            "Rating": st.column_config.ProgressColumn(
                "Rating",
                min_value=1,
                max_value=5,
                format="%d ⭐",
            ),
            "Comments": st.column_config.TextColumn(
                "Feedback Comments",
                width="large",
            ),
        },
        hide_index=True,
    )
    
    # Display editable version of the data
    st.subheader("Edit Feedback")
    edited_data = st.data_editor(
        filtered_data,
        column_config={
            "Date": st.column_config.DateColumn("Date Submitted"),
            "Rating": st.column_config.NumberColumn("Rating", min_value=1, max_value=5)
        },
        num_rows="dynamic",
        use_container_width=True,
    )
    
    # Update button to save changes
    if st.button("Update Feedback Data"):
        st.session_state.feedback_data = edited_data
        st.success("Feedback data updated!")
    
    # Show average rating by product
    st.subheader("Average Rating by Product")
    
    if not filtered_data.empty:
        avg_ratings = filtered_data.groupby('Product')['Rating'].mean().reset_index()
        avg_ratings['Rating'] = avg_ratings['Rating'].round(1)
        
        # Display as a dataframe
        st.dataframe(
            avg_ratings,
            column_config={
                "Rating": st.column_config.ProgressColumn(
                    "Avg. Rating",
                    min_value=1,
                    max_value=5,
                    format="%.1f ⭐",
                ),
            },
            hide_index=True,
        )
    else:
        st.info("No data available to calculate average ratings.") 