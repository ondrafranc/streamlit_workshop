import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

# ✅ Task Manager App - Exercise
# In this exercise, you'll learn how to use session state to build a full-featured
# task management application with persistence between reruns

st.title("✅ Task Manager App")
st.write("Keep track of your tasks with full state management")

# TODO: Initialize session state for tasks if it doesn't exist
# The tasks should be stored as a list of dictionaries with the following keys:
# - id: A unique identifier for the task (use uuid.uuid4())
# - text: The task description
# - completed: Boolean indicating if the task is completed
# - created_at: Datetime when the task was created
# Hint: Check if 'tasks' exists in st.session_state before initializing
pass

# MINI-EXERCISE: Create a counter with multiple buttons
# Educational purpose: Practice updating session state with different callbacks
st.subheader("Counter Mini-Exercise")

# TODO: Initialize a counter in session state if it doesn't exist
# TODO: Create 3 buttons: "+1", "+5", and "Reset"
# TODO: Implement callback functions for each button to update the counter
# TODO: Display the current counter value
# HINT: Define separate functions for each operation
pass

# Task creation form
st.subheader("Add a New Task")

# TODO: Create a form for adding a new task
# The form should have:
# 1. A text input for the task description
# 2. A submit button
# On submit, add the new task to the tasks list in session state
# Hint: Create a callback function to handle the form submission
pass

# Display tasks
st.subheader("Your Tasks")

# TODO: Create a filter for tasks (All, Active, Completed)
# Hint: Use st.radio() and filter the tasks list based on the selection
pass

# TODO: Display the filtered tasks with:
# 1. A checkbox to toggle completion status
# 2. The task text (strike through if completed)
# 3. A delete button for each task
# Hint: Use st.checkbox() with a key based on task ID for completion status,
# and add a delete button after each task
pass

# Task statistics
st.subheader("Task Statistics")

# TODO: Display stats about tasks:
# 1. Total number of tasks
# 2. Number of completed tasks
# 3. Number of active tasks
# Hint: Use len() and list comprehensions to calculate these statistics
pass

# Session state debugging
with st.expander("Debug: Session State"):
    # Display the current session state (useful for development)
    st.write(st.session_state)
    
    # TODO: Add a button to clear all tasks
    # Hint: Use st.button() and reset the tasks list when clicked
    pass 