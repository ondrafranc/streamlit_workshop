# Streamlit Cheat Sheet

## Getting Started

```python
import streamlit as st

# Basic text elements
st.title("My Streamlit App")
st.header("A header")
st.subheader("A subheader")
st.write("Write displays text and other data types")
st.markdown("**Bold text** with *markdown*")
st.caption("This is a small caption")
st.code("def hello_world():", language="python")
```

## Layouts

```python
# Columns
col1, col2 = st.columns(2)  # Two equal columns
col1, col2, col3 = st.columns([1, 2, 1])  # Custom widths

with col1:
    st.write("This is column 1")
    
with col2:
    st.write("This is column 2")

# Containers
with st.container():
    st.write("Everything inside this container")
    
# Expandable sections
with st.expander("Click to expand"):
    st.write("Hidden content")

# Tabs
tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
with tab1:
    st.write("Content for tab 1")
```

## Widgets

```python
# Basic input widgets
name = st.text_input("Your name")
age = st.number_input("Your age", min_value=0, max_value=120, value=30)
comment = st.text_area("Comments")
date = st.date_input("Select date")
time = st.time_input("Select time")

# Selection widgets
option = st.selectbox("Choose one", ["Option 1", "Option 2", "Option 3"])
options = st.multiselect("Choose multiple", ["A", "B", "C", "D"])
radio = st.radio("Pick one", ["Cat", "Dog", "Fish"])

# Buttons and checkboxes
if st.button("Click me"):
    st.write("Button clicked!")
    
agree = st.checkbox("I agree")
if agree:
    st.write("You agreed!")

# Sliders
value = st.slider("Select value", 0, 100, 50)
range_values = st.slider("Select range", 0, 100, (25, 75))

# File uploader
uploaded_file = st.file_uploader("Upload a file", type=["csv", "txt"])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data)
```

## Data Display

```python
import pandas as pd
import numpy as np

# Sample data
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [24, 32, 18],
    'City': ['New York', 'Los Angeles', 'Chicago']
})

# Display data
st.dataframe(df)  # Interactive dataframe
st.table(df)      # Static table
st.json({'a': 1, 'b': 2})  # JSON

# Customizing dataframes
st.dataframe(
    df,
    column_config={
        "Name": st.column_config.TextColumn("Full Name", width="medium"),
        "Age": st.column_config.NumberColumn("Age (years)", format="%d"),
        "City": st.column_config.SelectboxColumn("Location", options=["New York", "Los Angeles", "Chicago"])
    },
    hide_index=True,
    use_container_width=True
)

# Editable dataframes
edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True
)
```

## Forms

```python
# Group inputs into a form to reduce reruns
with st.form("my_form"):
    name = st.text_input("Name")
    age = st.number_input("Age")
    
    # Add submit button (must be inside the form)
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write(f"Name: {name}, Age: {age}")
```

## Caching

```python
import time

# Cache expensive operations
@st.cache_data
def load_data(url):
    data = pd.read_csv(url)
    return data

# With time to live (TTL)
@st.cache_data(ttl=3600)  # Cache expires after 1 hour
def get_api_data():
    # Simulate API call with delay
    time.sleep(2)
    return {"result": "data"}

# Cache resources (connections, models)
@st.cache_resource
def get_database_connection():
    # Create connection (only once)
    return connection

# Clear cache
if st.button("Clear Cache"):
    st.cache_data.clear()
```

## Session State

```python
# Initialize session state variables
if 'counter' not in st.session_state:
    st.session_state.counter = 0

# Increment counter with callback function
def increment_counter():
    st.session_state.counter += 1

# Use the callback with a button
st.button("Increment", on_click=increment_counter)

# Display the counter value
st.write(f"Counter value: {st.session_state.counter}")

# Direct manipulation
if st.button("Reset"):
    st.session_state.counter = 0

# Using session_state with form inputs
st.text_input("Name", key="name_input")
st.write(f"Hello, {st.session_state.name_input}")
```

## Charts

```python
import matplotlib.pyplot as plt
import plotly.express as px

# Sample data
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C'])

# Built-in charts
st.line_chart(chart_data)
st.bar_chart(chart_data)
st.area_chart(chart_data)

# Matplotlib
fig, ax = plt.subplots()
ax.scatter([1, 2, 3], [1, 2, 3])
st.pyplot(fig)

# Plotly
fig = px.scatter(chart_data, x='A', y='B', color='C')
st.plotly_chart(fig, use_container_width=True)
```

## Metrics and Status Elements

```python
# Metrics (with optional delta)
st.metric("Temperature", "70 °F", delta="1.2 °F")
st.metric("Revenue", "$500", delta="-$10", delta_color="inverse")

# Status elements
st.success("This is a success message")
st.info("This is an info message")
st.warning("This is a warning message")
st.error("This is an error message")

# Progress and spinners
progress_bar = st.progress(0)
for i in range(100):
    progress_bar.progress(i + 1)
    
with st.spinner("Loading..."):
    time.sleep(1)
```

## Data Download

```python
import io

# CSV download
csv = df.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="data.csv",
    mime="text/csv"
)

# Excel download
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False)
excel_data = buffer.getvalue()
st.download_button(
    label="Download Excel",
    data=excel_data,
    file_name="data.xlsx",
    mime="application/vnd.ms-excel"
)

# Image download
from PIL import Image
img = Image.open("image.jpg")
buf = io.BytesIO()
img.save(buf, format="JPEG")
st.download_button(
    label="Download Image",
    data=buf.getvalue(),
    file_name="image.jpg",
    mime="image/jpeg"
)
```

## Page Configuration

```python
# Set at the beginning of your app
st.set_page_config(
    page_title="My App",
    page_icon="🧊",
    layout="wide",  # or "centered"
    initial_sidebar_state="expanded"  # or "collapsed"
)
```

## Common Patterns

```python
# Filter dataframe pattern
def filter_dataframe(df, column, value):
    return df[df[column] == value]

filter_option = st.selectbox("Filter by:", df.columns)
filter_value = st.selectbox("Value:", df[filter_option].unique())
filtered_df = filter_dataframe(df, filter_option, filter_value)
st.dataframe(filtered_df)

# Toggle section visibility
show_section = st.checkbox("Show advanced options")
if show_section:
    st.write("Advanced options here")

# Dynamic options in selectbox
option1 = st.selectbox("Choose category", ["Fruits", "Vegetables"])
if option1 == "Fruits":
    option2 = st.selectbox("Choose fruit", ["Apple", "Banana", "Orange"])
else:
    option2 = st.selectbox("Choose vegetable", ["Carrot", "Broccoli", "Spinach"])