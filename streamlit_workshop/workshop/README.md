# Streamlit for Data Professionals Workshop

A hands-on 3-hour workshop designed to teach data analysts and professionals how to build interactive data apps with Streamlit.

## Workshop Overview

This workshop is divided into 5 modules and a final project:

1. **Getting Started with Streamlit**: Layouts and basic widgets
2. **Working with Data**: DataFrames, data editors, and user inputs
3. **Performance with Caching**: Using `@st.cache_data` for efficient data loading
4. **State Management**: Using `st.session_state` for persistent interactions
5. **Visualization & Export**: Charts and downloading data
6. **Final Project**: Building a complete analytics dashboard

## Setup Instructions

### Prerequisites

- Python 3.7+ installed
- Basic Python knowledge (pandas, matplotlib/plotly helpful but not required)
- Code editor of your choice

### Installation

1. Create a virtual environment (recommended):
   ```
   python -m venv streamlit-workshop
   source streamlit-workshop/bin/activate  # On Windows: streamlit-workshop\Scripts\activate
   ```

2. Install required packages:
   ```
   pip install streamlit pandas numpy matplotlib plotly
   ```

3. Test your installation:
   ```
   streamlit hello
   ```

### Workshop Materials

Each module contains:
- `instructor_notes.md`: Teaching notes and explanations
- `exercise.py`: Starter code with TODOs for participants
- `solution.py`: Completed solution

The final project includes:
- `instructions.md`: Project requirements and guidelines
- `starter_template.py`: A template to start from with pre-initialized data
- `solution.py`: A complete implementation for reference

## Workshop Timeline

- **Module 1** (30 minutes): Intro & Widgets
- **Module 2** (30 minutes): Working with Data
- **Break** (10 minutes)
- **Module 3** (25 minutes): Caching & Performance
- **Module 4** (30 minutes): Session State
- **Break** (10 minutes)
- **Module 5** (25 minutes): Visualization & Export
- **Final Project** (20 minutes)

## Troubleshooting

Each module includes a troubleshooting section in the instructor notes with common errors and solutions. These can help both instructors and participants debug common issues.

## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [Streamlit Gallery](https://streamlit.io/gallery) 