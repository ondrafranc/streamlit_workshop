# Module 2: Working with Data in Streamlit

## Teaching Objectives
- Learn to display static and interactive data tables with `st.dataframe()`
- Master editable tables using `st.data_editor()`
- Understand how to create forms for structured user input
- Explore data filtering and searching techniques

## Key Talking Points

### Data Display Options (5 minutes)
- Static tables with `st.table()` vs interactive tables with `st.dataframe()`
- Control over column formatting with `column_config`
- Best practices for displaying large datasets
- Demonstration: Loading and displaying different data types

### Editable Data with `st.data_editor()` (10 minutes)
- Introduction to `st.data_editor()` for creating editable tables
- Column configuration for different data types
- Making specific columns editable
- Using the editor for data collection and modification
- Demonstration: Creating a simple data entry form with editable tables

### Forms and User Input Collection (10 minutes)
- Using `st.form()` to group inputs and reduce rerunning
- The importance of `st.form_submit_button()`
- Combining forms with data display
- Demonstration: Build a data collection form that updates a table

### Filtering and Searching Data (5 minutes)
- Implementing search functionality
- Using widgets to filter dataframes
- Pattern for interactive data exploration
- Demonstration: Create a searchable/filterable table

## Live Coding Demo
Walk through building the customer survey app (solution.py) step by step:
1. Setup the basic data structure
2. Create the survey form
3. Implement the data table display with formatting
4. Add filtering and searching
5. Show how to export data

## Exercise Instructions
- Direct participants to open exercise.py
- Explain the TODOs and what they need to complete
- Give them 10 minutes to work on it
- Walk around and assist as needed
- Review the solution together afterward

## Common Issues & Tips
- Remember that edits in `st.data_editor()` need to be captured and stored
- Forms prevent reruns until the submit button is clicked
- For large datasets, consider implementing pagination or search
- Use appropriate column types in data editor for better UX

## Quiz Questions
1. What's the main difference between `st.dataframe()` and `st.data_editor()`?
   - Answer: `st.data_editor()` allows users to edit the data while `st.dataframe()` is for display only

2. When using `st.form()`, when does the app rerun?
   - Answer: Only when the form's submit button is clicked

3. How can you make only certain columns editable in `st.data_editor()`?
   - Answer: By specifying the `disabled` parameter with a list of column names to be non-editable 