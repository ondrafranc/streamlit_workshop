# Module 1: Getting Started with Streamlit

## Teaching Objectives
- Understand what Streamlit is and its benefits for data professionals
- Learn how to structure a basic Streamlit app
- Master page layouts (columns, containers, sidebar)
- Explore basic widgets for user interaction

## Key Talking Points

### Introduction (5 minutes)
- Streamlit is an open-source Python library for creating web apps with minimal effort
- Great for data professionals who want to showcase their work without web development expertise
- Everything is written in Python - no HTML, CSS, or JavaScript required
- Apps run top-to-bottom, like a script, and re-run when state changes

### Basic Structure (5 minutes)
- Every Streamlit app starts with `import streamlit as st`
- Page title and headers create hierarchy: `st.title()`, `st.header()`, `st.subheader()`
- Text display options: `st.write()`, `st.text()`, `st.markdown()`
- Demonstration: Show how simple it is to create a basic app

### Page Layout (10 minutes)
- Columns create horizontal layouts: `st.columns()`
- Containers group elements: `st.container()`
- Expanders hide content until needed: `st.expander()`
- Sidebar for controls: `st.sidebar`
- Demonstration: Show different layout options with examples

### Basic Widgets (10 minutes)
- Buttons: `st.button()`
- Text inputs: `st.text_input()`, `st.text_area()`
- Number inputs: `st.number_input()`, `st.slider()`
- Selection widgets: `st.selectbox()`, `st.multiselect()`, `st.radio()`, `st.checkbox()`
- Date and time inputs: `st.date_input()`, `st.time_input()`
- Demonstration: Create a simple form with various widgets

## Live Coding Demo
Walk through building the coffee order app (solution.py) step by step:
1. Start with the basic structure and title
2. Add sidebar for order customization
3. Create the main content with columns
4. Add interactive widgets for ordering
5. Show how app reacts to user inputs

## Exercise Instructions
- Direct participants to open exercise.py
- Explain the TODOs and what they need to complete
- Give them 7-10 minutes to work on it
- Walk around and assist as needed
- Review the solution together afterward

## Common Issues & Tips
- Ensure proper indentation when using columns and containers
- Remember that the app reruns from top to bottom on each interaction
- Use meaningful labels and help text for better UX
- When deploying, consider which variables should be reset on each rerun

## Troubleshooting Common Errors

### 1. "NameError: name 'st' is not defined"
**Solution**: Make sure to include `import streamlit as st` at the top of your script.

### 2. "IndentationError" when using columns or containers
**Solution**: Check that you're using proper indentation with the `with` statement. Example:
```python
col1, col2 = st.columns(2)
with col1:
    st.write("This is column 1")  # Correctly indented
```

### 3. Button click doesn't persist
**Solution**: Explain that button states don't persist between reruns. If you need to remember a button was clicked, store the result in session state (preview of Module 4).

### 4. Elements appearing in unexpected order
**Solution**: Streamlit executes top-to-bottom. If elements appear in an unexpected order, check your code order.

### 5. Changes to widgets don't update other widgets
**Solution**: When a widget changes, the entire script reruns. If you want a widget to affect other widgets, make sure the dependent widgets are below the controlling widget in your code.

## Quiz Questions
1. What happens when a user interacts with a widget in Streamlit?
   - Answer: The entire script reruns from top to bottom

2. How can you create a two-column layout in Streamlit?
   - Answer: Using `col1, col2 = st.columns(2)`

3. What's the difference between `st.write()` and `st.text()`?
   - Answer: `st.write()` can display various data types and supports markdown, while `st.text()` only displays plain text 