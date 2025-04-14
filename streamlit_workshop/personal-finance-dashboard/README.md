# 💰 Personal Finance Dashboard

A Streamlit-powered personal finance dashboard that helps you track your income, expenses, and budget in an interactive web application.

## 🌟 Features

- **Interactive Dashboard**: Visualize your financial data with charts and metrics
- **Transaction Management**: Add, edit, and filter your financial transactions
- **Budget Tracking**: Set monthly budgets and track your spending against them
- **Data Import/Export**: Import your own data or export for offline analysis

## 🚀 Getting Started

### Prerequisites

- Python 3.7+ installed
- pip (Python package manager)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/personal-finance-dashboard.git
   cd personal-finance-dashboard
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

This repository contains two versions of the app:

### Lite Version (Starter Template)

A basic template with TODO comments to help you implement features step by step:

```bash
streamlit run lite_version/app.py
```

### Full Version (Complete Solution)

The complete dashboard with all features implemented:

```bash
streamlit run full_version/app.py
```

## 📊 App Structure

The dashboard consists of four main views:

1. **Dashboard**: Summary metrics and visualizations
2. **Transactions**: Manage your financial transactions
3. **Budgets**: Set and track monthly spending limits
4. **Settings**: Configure app settings and manage data

## 📚 Learning Objectives

By working with this app, you'll learn:

- Building interactive web applications with Streamlit
- Creating data visualizations with Plotly
- Managing application state with Streamlit's session state
- Implementing data filtering and manipulation with Pandas
- Designing intuitive user interfaces for data applications

## 🧩 Project Structure

```
personal-finance-dashboard/
├── README.md               # Project overview, setup, usage
├── requirements.txt        # Required Python packages
├── lite_version/
│   └── app.py              # Starter version with TODOs
├── full_version/
│   └── app.py              # Complete Streamlit solution
├── data/
│   └── sample_transactions.csv  # Sample data for import
└── docs/
    └── architecture.md     # Explains structure and key components
```

## 🔍 Next Steps

After mastering the basics, try implementing some of the bonus challenges:
- Add a monthly summary view
- Implement recurring transactions
- Create expense forecasting

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 