# Module 3: Performance and Caching in Streamlit

## Teaching Objectives
- Understand how Streamlit executes code with each interaction
- Learn the performance implications of loading data repeatedly
- Master the `@st.cache_data` decorator for efficient data loading
- Explore best practices for optimizing Streamlit app performance

## Key Talking Points

### Streamlit Execution Model (5 minutes)
- Streamlit reruns the entire script from top to bottom on each interaction
- Implications for performance, especially with data loading or complex calculations
- The need for caching to avoid expensive operations
- Demonstration: Show performance without caching

### Introducing Caching (5 minutes)
- Purpose of caching: avoid redundant operations
- Types of caching in Streamlit: `@st.cache_data` and `@st.cache_resource`
- How to implement the `@st.cache_data` decorator
- What operations should be cached
- Demonstration: Add caching and measure performance improvement

### Advanced Caching Features (10 minutes)
- Cache invalidation with TTL (Time To Live)
- Cache key management
- Handling dependencies between cached functions
- Limitations and gotchas of caching
- Demonstration: Different caching patterns and their use cases

### Best Practices for Performance (5 minutes)
- When to use caching vs. when not to
- Structuring your code for optimal caching
- Debugging caching issues
- Tips for profiling Streamlit app performance
- Demonstration: Compare different approaches to the same problem

## Live Coding Demo
Walk through building the stock price app (solution.py) step by step:
1. Start with a basic data loading function (expensive operation)
2. Show performance issues without caching
3. Implement basic caching with `@st.cache_data`
4. Add TTL and caching parameters
5. Demonstrate how to debug caching issues

## Exercise Instructions
- Direct participants to open exercise.py
- Explain the TODOs and what they need to complete
- Give them 7-10 minutes to work on it
- Walk around and assist as needed
- Review the solution together afterward

## Common Issues & Tips
- Be careful with mutable objects (like dataframes) in cached functions
- Remember that changing the function's code will invalidate the cache
- Use `clear_cache()` during development to test functionality
- Adding cache parameters can help with debugging and control

## Troubleshooting Common Caching Errors

### 1. Cache Not Working (Function Still Running Slowly)
**Solution**: Check the following:
- Make sure the decorator is placed **before** the function definition
- Verify no random/unpredictable elements exist in the function (e.g., `random.random()` without a seed)
- Ensure you're not modifying cached objects in-place after they're returned

### 2. "TypeError: the 'parameter' object is not callable"
**Solution**: This often happens with incorrect decorator syntax. The correct format is:
```python
@st.cache_data
def my_function():
    # function code

# With parameters:
@st.cache_data(ttl=3600, max_entries=100)
def my_function():
    # function code
```

### 3. Cache Invalidating Too Frequently
**Solution**: Check if you're:
- Passing unhashable objects as parameters (like dictionaries or lists) - convert to tuples or strings
- Using the current time/date as a parameter without rounding to appropriate units
- Inadvertently changing function code (even spacing or comments) during development

### 4. Memory Issues with Large Cached Data
**Solution**: 
- Use the `max_entries` parameter to limit cache size
- Consider caching smaller processed results instead of large raw datasets
- Use `ttl` to expire old entries: `@st.cache_data(ttl=3600)`  # 1 hour

### 5. Different Results for the Same Parameters
**Solution**: This can happen if:
- Your function has external dependencies not captured in parameters
- You're modifying the returned object after caching
- The function relies on global/external state

## Quiz Questions
1. Why is caching important in Streamlit applications?
   - Answer: Because Streamlit reruns the entire script on each interaction, so caching prevents expensive operations from running repeatedly

2. What type of operations should be cached with `@st.cache_data`?
   - Answer: Data loading, data processing, and other expensive operations that return data but don't have side effects

3. What happens when you change the code inside a cached function?
   - Answer: The cache is invalidated and the function will run again the next time it's called 