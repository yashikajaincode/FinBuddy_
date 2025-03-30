import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import calculate_budget_summary, format_currency, get_llm_response
from gamification import award_badge, update_user_progress

def display_budget_planner():
    st.title("📊 Budget Planner")
    st.write("Track your income and expenses to create a smart budget plan with FinBuddy's recommendations.")
    
    # Initialize or get user budget from session state
    if "user_budget" not in st.session_state:
        st.session_state.user_budget = {
            "income": [],
            "expenses": []
        }
    
    # Create tabs for the budget planner
    tab1, tab2, tab3 = st.tabs(["Income", "Expenses", "Budget Summary"])
    
    # Income tab
    with tab1:
        st.subheader("Income Sources")
        
        # Display current income sources
        if st.session_state.user_budget["income"]:
            income_df = pd.DataFrame(st.session_state.user_budget["income"])
            st.dataframe(income_df, use_container_width=True)
            total_income = sum(item["amount"] for item in st.session_state.user_budget["income"])
            st.info(f"Total Income: {format_currency(total_income)}")
        else:
            st.info("No income sources added yet. Add your first income source below.")
        
        # Form to add new income source
        with st.form("add_income_form"):
            st.subheader("Add Income Source")
            income_name = st.text_input("Description (e.g., Salary, Part-time job)")
            income_amount = st.number_input("Monthly Amount ($)", min_value=0.0, step=100.0)
            
            submitted = st.form_submit_button("Add Income Source")
            if submitted and income_name and income_amount > 0:
                new_income = {
                    "name": income_name,
                    "amount": income_amount
                }
                st.session_state.user_budget["income"].append(new_income)
                st.success(f"Added {income_name}: {format_currency(income_amount)}")
                
                # Award badge for adding first income
                if len(st.session_state.user_budget["income"]) == 1:
                    award_badge("Income Tracker", "💵")
                    update_user_progress(0.1)
                
                st.rerun()
    
    # Expenses tab
    with tab2:
        st.subheader("Expenses")
        
        # Display current expenses
        if st.session_state.user_budget["expenses"]:
            expenses_df = pd.DataFrame(st.session_state.user_budget["expenses"])
            st.dataframe(expenses_df, use_container_width=True)
            total_expenses = sum(item["amount"] for item in st.session_state.user_budget["expenses"])
            st.info(f"Total Expenses: {format_currency(total_expenses)}")
        else:
            st.info("No expenses added yet. Add your first expense below.")
        
        # Form to add new expense
        with st.form("add_expense_form"):
            st.subheader("Add Expense")
            expense_name = st.text_input("Description (e.g., Rent, Groceries)")
            expense_category = st.selectbox(
                "Category",
                ["Housing", "Food", "Transportation", "Utilities", "Entertainment", 
                 "Education", "Healthcare", "Personal", "Debt", "Savings", "Other"]
            )
            expense_amount = st.number_input("Monthly Amount ($)", min_value=0.0, step=10.0)
            
            submitted = st.form_submit_button("Add Expense")
            if submitted and expense_name and expense_amount > 0:
                new_expense = {
                    "name": expense_name,
                    "category": expense_category,
                    "amount": expense_amount
                }
                st.session_state.user_budget["expenses"].append(new_expense)
                st.success(f"Added {expense_name}: {format_currency(expense_amount)}")
                
                # Award badge for adding first expense
                if len(st.session_state.user_budget["expenses"]) == 1:
                    award_badge("Expense Tracker", "📝")
                    update_user_progress(0.1)
                
                st.rerun()
    
    # Budget Summary tab
    with tab3:
        st.subheader("Budget Summary")
        
        # Check if both income and expenses have been added
        if not st.session_state.user_budget["income"]:
            st.warning("Please add income sources first.")
        elif not st.session_state.user_budget["expenses"]:
            st.warning("Please add expenses first.")
        else:
            # Calculate budget summary
            budget_summary = calculate_budget_summary(
                st.session_state.user_budget["income"],
                st.session_state.user_budget["expenses"]
            )
            
            # Display income vs. expenses
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "Total Income", 
                    format_currency(budget_summary["total_income"])
                )
            with col2:
                st.metric(
                    "Total Expenses", 
                    format_currency(budget_summary["total_expenses"]),
                    delta=format_currency(budget_summary["balance"]),
                    delta_color="normal" if budget_summary["balance"] >= 0 else "inverse"
                )
            
            # Display budget balance
            st.subheader("Budget Balance")
            balance = budget_summary["balance"]
            if balance >= 0:
                st.success(f"Surplus: {format_currency(balance)} (Saving rate: {budget_summary['saving_rate']:.1f}%)")
            else:
                st.error(f"Deficit: {format_currency(abs(balance))}")
            
            # Show expense breakdown by category
            st.subheader("Expense Breakdown")
            if budget_summary["expense_by_category"]:
                # Create a pie chart of expenses by category
                expense_df = pd.DataFrame([
                    {"Category": category, "Amount": amount}
                    for category, amount in budget_summary["expense_by_category"].items()
                ])
                
                fig = px.pie(
                    expense_df, 
                    values="Amount", 
                    names="Category",
                    title="Expenses by Category"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Create a bar chart comparing income to total expenses
                comparison_data = {
                    "Category": ["Income", "Expenses"],
                    "Amount": [budget_summary["total_income"], budget_summary["total_expenses"]]
                }
                comparison_df = pd.DataFrame(comparison_data)
                
                fig2 = px.bar(
                    comparison_df,
                    x="Category",
                    y="Amount",
                    title="Income vs. Expenses",
                    color="Category",
                    color_discrete_map={"Income": "#00CC96", "Expenses": "#EF553B"}
                )
                st.plotly_chart(fig2, use_container_width=True)
            
            # Get AI recommendations based on budget
            st.subheader("FinBuddy Recommendations")
            if st.button("Get Budget Recommendations"):
                with st.spinner("Analyzing your budget..."):
                    # Prepare data for the AI
                    budget_data = {
                        "income": budget_summary["total_income"],
                        "expenses": budget_summary["total_expenses"],
                        "balance": budget_summary["balance"],
                        "saving_rate": budget_summary["saving_rate"],
                        "expense_categories": budget_summary["expense_by_category"]
                    }
                    
                    prompt = f"""
                    Based on the following budget information, provide 3-5 specific recommendations 
                    to improve this person's financial situation:
                    
                    Income: ${budget_data['income']:.2f}/month
                    Expenses: ${budget_data['expenses']:.2f}/month
                    Balance: ${budget_data['balance']:.2f}/month
                    Saving rate: {budget_data['saving_rate']:.1f}%
                    
                    Expense categories:
                    {budget_data['expense_categories']}
                    
                    Provide practical, actionable advice for a student or beginner in personal finance.
                    Format each recommendation as a separate bullet point.
                    """
                    
                    # Get AI recommendations
                    recommendations = get_llm_response(prompt)
                    st.markdown(recommendations)
                    
                    # Award budget master badge if they got recommendations
                    award_badge("Budget Master", "🏆")
                    update_user_progress(0.15)
