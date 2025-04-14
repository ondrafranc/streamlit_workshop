# Module 4: State Management with Session State

## Teaching Objectives
- Understand the challenges of state persistence in Streamlit
- Learn how to use `st.session_state` for data persistence
- Master event-based callbacks for interaction handling
- Create interactive applications with complex state management

## Key Talking Points

### The Challenge of Statelessness (5 minutes)
- Streamlit's execution model and statelessness
- Problems with preserving user input across reruns
- The need for a state management solution
- Demonstration: Show a simple counter that doesn't work without session state

### Introducing Session State (10 minutes)
- Purpose and structure of `st.session_state`
- How to initialize, access, and modify session state variables
- Lifetime of session state (browser tab session)
- Best practices for session state keys
- Demonstration: Implementing a functional counter with session state

### Callbacks and Events (10 minutes)
- Using callbacks for event handling with `on_click`, `on_change`, etc.
- Implementing form submissions with state updates
- Widget states and form states
- Patterns for complex interactions with multiple steps
- Demonstration: Multi-step form with session state

### Complex State Management (5 minutes)
- Managing lists and dictionaries in session state
- Storing and updating dataframes
- State relationships and dependencies
- State resetting strategies
- Demonstration: Shopping cart implementation with session state

## Live Coding Demo
Walk through building the task management app (solution.py) step by step:
1. Set up the basic task list structure in session state
2. Create an input form for new tasks
3. Implement task completion toggling
4. Add task deletion functionality
5. Implement task editing
6. Add filtering and sorting of tasks

## Exercise Instructions
- Direct participants to open exercise.py
- Explain the TODOs and what they need to complete
- Give them 10 minutes to work on it
- Walk around and assist as needed
- Review the solution together afterward

## Common Issues & Tips
- Remember to initialize session state variables before accessing them
- Be careful with mutable objects (update references properly)
- Use prefixes for related state variables for better organization
- Debug session state with `st.write(st.session_state)`
- Avoid overly complex state management structures

## Troubleshooting Common Session State Errors

### 1. "KeyError: 'variable_name'"
**Solution**: This occurs when trying to access a key that doesn't exist in session state. Always initialize state variables before use:
```python
# Correct approach
if 'counter' not in st.session_state:
    st.session_state.counter = 0
    
# Then you can safely use it
st.session_state.counter += 1
```

### 2. State Updates Not Reflected in UI
**Solution**: If state changes don't seem to update the UI:
- Make sure you're updating the state variable correctly
- If updating complex objects (lists, dicts), assign the entire updated object, not just modify a property
- Use `st.rerun()` to force a rerun if needed after state changes

### 3. Callback Function Not Triggering
**Solution**: Check that:
- The callback function is defined before it's referenced
- The callback is properly connected to the widget with the `on_click`, `on_change`, etc. parameter
- Parameters are passed correctly using `args` or `kwargs` parameters
```python 
def increment():
    st.session_state.counter += 1

st.button("Increment", on_click=increment)  # Correct
# NOT: st.button("Increment", on_click=increment())  # Wrong - don't call the function!
```

### 4. State Reset Unexpectedly
**Solution**: This often happens because:
- Script logic is reinitializing variables on each rerun
- Widget keys are changing between runs
- You're using non-session state variables to control logic

### 5. Multiple Widgets Updating the Same State Variable
**Solution**: If multiple widgets need to update the same state:
- Use unique keys for each widget
- Use callback functions that check the source of the update
- Consider using a more structured state organization

### 6. Form Submission Not Updating State
**Solution**: Common issues include:
- Trying to access widget values outside the form
- Not using the form's submit button to trigger state updates
- Using `st.form_submit_button()` without a callback function

## Quiz Questions
1. Why is session state necessary in Streamlit applications?
   - Answer: To maintain state between reruns since Streamlit scripts rerun from top to bottom on each interaction

2. How long does session state persist in a Streamlit app?
   - Answer: For the duration of the browser tab session; it's cleared when the tab is closed or the server restarts

3. What's the difference between using a callback function and directly setting a state variable?
   - Answer: Callbacks provide more control and can perform operations before updating state, while direct assignment is simpler but less flexible