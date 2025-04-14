# 🏆 Student Challenge Extensions

Here are several challenges to extend the starter template. These projects will help you practice your Streamlit skills and add valuable features to the personal finance dashboard.

## Challenge 1: Monthly Summary Dashboard

**Objective**: Create a new view that provides a monthly summary of your finances.

**Requirements**:
1. Add a "Monthly Summary" option to the navigation
2. Show month-by-month comparisons of:
   - Total income vs. expenses
   - Spending by category
   - Savings rate progression
3. Implement month selector (dropdown or date picker)
4. Create at least two visualizations (bar chart, line chart)
5. Add summary metrics comparing current month to previous month

**Tips**:
- Use `pd.Grouper(key='date', freq='M')` for monthly aggregation
- Consider implementing sparklines for trend visualization
- Add percentage change indicators for key metrics

## Challenge 2: Recurring Transactions

**Objective**: Implement a system to manage recurring transactions.

**Requirements**:
1. Create a "Recurring" view in the navigation
2. Build a form to create recurring transactions with:
   - Name/description
   - Amount
   - Category
   - Frequency (weekly, monthly, yearly)
   - Start date
   - End date (optional)
   - Status (active/paused)
3. Store recurring transactions in `st.session_state.recurring_transactions`
4. Add a button to generate all upcoming recurring transactions for the next 3 months
5. Show a table of upcoming generated transactions

**Tips**:
- Use `datetime` for date calculations
- Consider using `st.expander` to organize the interface
- Add validation to ensure logical start/end dates

## Challenge 3: Financial Goals Tracker

**Objective**: Add a goal-setting and tracking feature to help users reach financial targets.

**Requirements**:
1. Create a "Goals" view in the navigation
2. Implement goal creation form with:
   - Goal name
   - Target amount
   - Deadline date
   - Category (savings, debt repayment, etc.)
   - Initial amount (optional)
3. Display progress toward each goal with:
   - Progress bar visualization
   - Percentage complete
   - Amount needed to complete
   - Days remaining
4. Add ability to record contributions to goals
5. Create a projection chart showing when goals will be reached

**Tips**:
- Use `st.progress()` for visual progress indicators
- Store goals in `st.session_state.goals`
- Consider calculating required monthly contributions to reach goals

## Challenge 4: Data Visualization Enhancements

**Objective**: Enhance the dashboard with advanced visualizations.

**Requirements**:
1. Add a heat map showing spending patterns by day of week and category
2. Create an interactive scatter plot of transactions with size based on amount
3. Implement a sunburst chart showing hierarchical breakdown of expenses
4. Add trend lines and forecasting to time-series charts
5. Make at least two visualizations interactive with click events or hover information

**Tips**:
- Explore Plotly's advanced chart types
- Use `st.plotly_chart(fig, use_container_width=True)` for responsive layouts
- Add callbacks for interactive elements
- Consider using color scales to enhance information density 