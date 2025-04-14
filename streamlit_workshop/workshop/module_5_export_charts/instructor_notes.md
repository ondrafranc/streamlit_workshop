# Module 5: Data Visualization and Export

## Teaching Objectives
- Master Streamlit's built-in charting capabilities
- Learn to integrate external visualization libraries (Matplotlib, Plotly)
- Implement data export functionality with `st.download_button`
- Create professional data dashboards

## Key Talking Points

### Streamlit's Charting Capabilities (5 minutes)
- Overview of built-in chart types
- Using `st.line_chart()`, `st.bar_chart()`, and `st.area_chart()`
- Best practices for data formatting and preprocessing 
- Demonstration: Create simple charts from dataframes

### Integrating External Charting Libraries (10 minutes)
- Using Matplotlib with `st.pyplot()`
- Creating interactive Plotly charts with `st.plotly_chart()`
- Customizing charts for better user experience
- Chart responsiveness and layout considerations
- Demonstration: Create a dashboard with multiple chart types

### Data Export Options (5 minutes)
- Using `st.download_button()` for data export
- File format options (CSV, Excel, JSON, etc.)
- Creating downloadable visualizations
- Best practices for large data exports
- Demonstration: Add export functionality to a data app

### Building an End-to-End Dashboard (5 minutes)
- Combining all concepts: data loading, caching, interactivity, visualization, and export
- Layout optimization for dashboards
- User experience considerations
- Performance tips for complex dashboards
- Demonstration: Create a complete analytics dashboard

## Live Coding Demo
Walk through building the sales dashboard app (solution.py) step by step:
1. Set up the data loading with caching
2. Create basic data filters and summaries
3. Build visualizations with Plotly
4. Implement CSV and Excel export options
5. Add chart customization options

## Exercise Instructions
- Direct participants to open exercise.py
- Explain the TODOs and what they need to complete
- Give them 10 minutes to work on it
- Walk around and assist as needed
- Review the solution together afterward

## Common Issues & Tips
- Make sure to handle empty data gracefully in charts
- Chart sizes may need adjustment for different screens
- Remember to format numeric data appropriately for charts
- Use color schemes consistently for better visualization
- Test download functionality with different data sizes

## Troubleshooting Common Visualization and Export Errors

### 1. Charts Not Displaying or Empty
**Solution**: Check for:
- Empty dataframes or null values (validate with `df.empty` or `df.isna().sum()`)
- Incorrect column names in chart settings
- Column types not suitable for visualization (e.g., string where number needed)
- Add debug print statements to check data before visualization:
```python
st.write("Debug data:", data.head())
st.write("Data shape:", data.shape)
```

### 2. "ValueError: DataFrame has no numeric columns" 
**Solution**:
- Make sure your data columns are the correct types (use `df['column'] = df['column'].astype('float')`)
- For built-in charts like `st.line_chart()`, check that your dataframe has numeric columns
- For Plotly charts, ensure that column names match what's specified in the plot settings

### 3. Download Button Not Working
**Solution**:
- Verify that the `data` parameter contains the actual data, not just a filename
- For CSV, use `df.to_csv(index=False)` to convert to string first
- For Excel or binary formats, use BytesIO buffer:
```python
buffer = io.BytesIO()
df.to_excel(buffer, index=False)
excel_data = buffer.getvalue()
```
- Ensure you set the correct `mime` type in the download button

### 4. Plotly Chart Responsiveness Issues
**Solution**:
- Use `use_container_width=True` in `st.plotly_chart()`
- Set a reasonable height in the figure layout: `fig.update_layout(height=500)`
- Use `st.columns()` with appropriate widths for multi-chart layouts
- Test your app at different screen sizes

### 5. Memory Issues with Large Dataset Exports
**Solution**:
- Consider filtering or aggregating data before export
- Use caching for the export data preparation
- For very large exports, implement pagination or chunking
- Add a status indicator for large exports: `with st.spinner("Preparing download...")`

### 6. Date Formatting Issues in Charts or Exports
**Solution**:
- For charts, format dates before plotting: `df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')`
- For exports, use the `date_format` parameter in Excel writers
- For Plotly, set date formats in axis properties: `xaxis=dict(tickformat='%b %Y')`

## Quiz Questions
1. Which Streamlit function allows users to download data as a file?
   - Answer: `st.download_button()`

2. What's an advantage of using Plotly over Matplotlib in Streamlit apps?
   - Answer: Plotly creates interactive charts that users can zoom, pan, and hover over for details

3. When creating a download button for a DataFrame as CSV, what format should the data be in?
   - Answer: A string containing the CSV data, typically created using `df.to_csv(index=False)` 