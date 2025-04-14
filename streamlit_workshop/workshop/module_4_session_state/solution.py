import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

# ✅ Task Manager App - Solution

st.title("✅ Task Manager App")
st.write("Keep track of your tasks with full state management")

# Initialize session state for tasks if it doesn't exist
if 'tasks' not in st.session_state:
    st.session_state.tasks = [
        {
            'id': str(uuid.uuid4()),
            'text': 'Welcome to Task Manager!',
            'completed': False,
            'created_at': datetime.now()
        },
        {
            'id': str(uuid.uuid4()),
            'text': 'Check out this app tutorial',
            'completed': True,
            'created_at': datetime.now()
        }
    ]

# MINI-EXERCISE: Counter with multiple buttons
st.subheader("Counter Mini-Exercise")

# Initialize counter in session state
if 'mini_counter' not in st.session_state:
    st.session_state.mini_counter = 0

# Define callback functions for counter operations
def increment_by_one():
    st.session_state.mini_counter += 1

def increment_by_five():
    st.session_state.mini_counter += 5

def reset_counter():
    st.session_state.mini_counter = 0

# Create buttons with callbacks
col1, col2, col3 = st.columns(3)
col1.button("+1", on_click=increment_by_one, key="btn_plus_one")
col2.button("+5", on_click=increment_by_five, key="btn_plus_five")
col3.button("Reset", on_click=reset_counter, key="btn_reset")

# Display counter value with some styling
st.markdown(f"### Counter value: {st.session_state.mini_counter}")

# Add a divider to separate from the main app
st.divider()

# Callback function to add a new task
def add_task():
    if st.session_state.new_task.strip():  # Ensure task isn't empty
        new_task = {
            'id': str(uuid.uuid4()),
            'text': st.session_state.new_task,
            'completed': False,
            'created_at': datetime.now()
        }
        st.session_state.tasks.append(new_task)
        st.session_state.new_task = ""  # Clear the input
        
# Callback function to delete a task
def delete_task(task_id):
    st.session_state.tasks = [task for task in st.session_state.tasks if task['id'] != task_id]

# Callback function to toggle task completion
def toggle_task(task_id):
    for task in st.session_state.tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            break

# Task creation form
st.subheader("Add a New Task")
with st.form(key="add_task_form", clear_on_submit=True):
    st.text_input("Task Description", key="new_task")
    submit_button = st.form_submit_button("Add Task", on_click=add_task)

# Task filtering
st.subheader("Your Tasks")
task_filter = st.radio("Show", ["All Tasks", "Active Tasks", "Completed Tasks"], horizontal=True)

# Filter tasks based on selection
filtered_tasks = st.session_state.tasks
if task_filter == "Active Tasks":
    filtered_tasks = [task for task in st.session_state.tasks if not task['completed']]
elif task_filter == "Completed Tasks":
    filtered_tasks = [task for task in st.session_state.tasks if task['completed']]

# Sort tasks: completed at the bottom, then by creation time (newest first)
filtered_tasks = sorted(filtered_tasks, key=lambda x: (x['completed'], -x['created_at'].timestamp()))

# Display tasks
if not filtered_tasks:
    st.info(f"No {task_filter.lower()} to show")
else:
    for task in filtered_tasks:
        col1, col2, col3 = st.columns([0.05, 0.8, 0.15])
        
        # Task checkbox
        with col1:
            st.checkbox(
                "",
                value=task['completed'],
                key=f"check_{task['id']}",
                on_change=toggle_task,
                args=(task['id'],)
            )
        
        # Task text
        with col2:
            if task['completed']:
                st.markdown(f"~~{task['text']}~~")
            else:
                st.write(task['text'])
                
        # Delete button
        with col3:
            if st.button("Delete", key=f"delete_{task['id']}"):
                delete_task(task['id'])
                st.rerun()
        
        # Add a separator between tasks
        st.divider()

# Task statistics
st.subheader("Task Statistics")
col1, col2, col3 = st.columns(3)

# Calculate statistics
total_tasks = len(st.session_state.tasks)
completed_tasks = len([task for task in st.session_state.tasks if task['completed']])
active_tasks = total_tasks - completed_tasks

# Display metrics
with col1:
    st.metric("Total Tasks", total_tasks)
with col2:
    st.metric("Completed", completed_tasks)
with col3:
    st.metric("Active", active_tasks)

# Export as CSV button
if st.button("Export Tasks as CSV"):
    # Create a DataFrame from the tasks
    tasks_df = pd.DataFrame([
        {
            'Task': task['text'],
            'Status': 'Completed' if task['completed'] else 'Active',
            'Created': task['created_at'].strftime('%Y-%m-%d %H:%M')
        }
        for task in st.session_state.tasks
    ])
    
    # Create a download link
    csv = tasks_df.to_csv(index=False)
    st.download_button(
        "Download CSV",
        csv,
        "tasks.csv",
        "text/csv",
        key="download-csv"
    )

# Session state debugging
with st.expander("Debug: Session State"):
    # Display the current session state (useful for development)
    st.write(st.session_state)
    
    # Clear all tasks button
    if st.button("Clear All Tasks"):
        st.session_state.tasks = []
        st.success("All tasks cleared!")
        st.rerun() 