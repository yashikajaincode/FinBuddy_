import streamlit as st
import json
import pandas as pd
import os
from datetime import datetime
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

def initialize_session_state():
    """Initialize all session state variables needed for the app"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm FinBuddy, your financial education assistant. How can I help you learn about budgeting, saving, and investing today?"}
        ]
    
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = os.environ.get("OPENAI_API_KEY", "")
    
    if "user_budget" not in st.session_state:
        st.session_state.user_budget = {
            "income": [],
            "expenses": []
        }
    
    if "savings_goals" not in st.session_state:
        st.session_state.savings_goals = []
    
    if "investment_progress" not in st.session_state:
        st.session_state.investment_progress = {
            "lessons_completed": 0,
            "quizzes_taken": 0,
            "score": 0
        }
    
    if "user_badges" not in st.session_state:
        st.session_state.user_badges = []
        
    if "user_progress" not in st.session_state:
        st.session_state.user_progress = 0.1  # Starting progress (0.0 to 1.0)
    
    if "financial_health_score" not in st.session_state:
        st.session_state.financial_health_score = None

def load_css():
    """Load custom CSS for the app (minimal, uses mostly Streamlit defaults)"""
    st.markdown("""
        <style>
        .financial-tip {
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
            background-color: #f0f7ff;
        }
        .badge-icon {
            font-size: 24px;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

def get_llm_response(prompt, system_prompt="You are FinBuddy, an AI assistant that helps users learn about personal finance, budgeting, saving, and investing. Your responses should be friendly, informative, and geared toward financial education for beginners."):
    """
    Get a response from the GPT model via LangChain or fallback to static responses
    
    Args:
        prompt (str): User prompt
        system_prompt (str): System prompt defining the AI assistant's behavior
    
    Returns:
        str: The AI response or a default response
    """
    # Dictionary of static responses based on keywords in the prompt
    static_responses = {
        "budget": "Creating a budget is the foundation of financial wellness! Start by tracking all income sources, then categorize your expenses into needs (rent, food), wants (entertainment), and savings. Aim to save at least 20% of your income using the 50/30/20 rule - 50% for needs, 30% for wants, and 20% for savings and debt repayment.",
        
        "save": "Saving money is all about small daily habits! Try the 30-day rule (wait 30 days before making non-essential purchases), automate your savings with direct deposits, and challenge yourself to no-spend days. Even saving $5 a day adds up to $1,825 in a year!",
        
        "invest": "Investing is how your money grows over time! As a beginner, consider starting with a tax-advantaged retirement account like a 401(k) or IRA. Index funds are great for beginners since they provide instant diversification with low fees. Remember, time in the market beats timing the market!",
        
        "stock": "The stock market is a place where people buy and sell ownership shares in companies. Here's what to know as a beginner:\n\n• Start with index funds that track the entire market (like S&P 500) for instant diversification\n• Only invest money you won't need for at least 5 years\n• Set up automatic contributions to benefit from dollar-cost averaging\n• Understand that market fluctuations are normal - focus on long-term trends\n• Research companies before buying individual stocks or use index funds\n• Consider using a tax-advantaged account like a Roth IRA for your investments",
        
        "stock market": "The stock market is a place where people buy and sell ownership shares in companies. Here's what to know as a beginner:\n\n• Start with index funds that track the entire market (like S&P 500) for instant diversification\n• Only invest money you won't need for at least 5 years\n• Set up automatic contributions to benefit from dollar-cost averaging\n• Understand that market fluctuations are normal - focus on long-term trends\n• Research companies before buying individual stocks or use index funds\n• Consider using a tax-advantaged account like a Roth IRA for your investments",
        
        "debt": "Managing debt strategically is crucial! Prioritize high-interest debt like credit cards first (debt avalanche method) or start with small balances for quick wins (debt snowball method). Always pay more than the minimum payment, and consider consolidating high-interest debts to a lower rate.",
        
        "credit": "Building good credit is essential! Pay bills on time (35% of your score), keep credit utilization below 30%, maintain older accounts, avoid opening too many new accounts, and diversify your credit mix. Check your credit report annually for free at AnnualCreditReport.com.",
        
        "emergency": "An emergency fund is your financial safety net! Aim to save 3-6 months of essential expenses in an easily accessible account like a high-yield savings account. Start small with $1,000, then build up gradually. This protects you from going into debt when unexpected expenses hit.",
        
        "retirement": "Retirement planning works best when you start early! If your employer offers a 401(k) match, contribute at least enough to get the full match (it's free money!). Consider opening an IRA for additional tax advantages, and increase your contributions whenever you get a raise.",
        
        "tax": "Understanding tax basics can save you money! Take advantage of tax-advantaged accounts like 401(k)s and IRAs. Track deductible expenses throughout the year, consider tax-loss harvesting for investments, and remember that tax refunds mean you've been giving the government an interest-free loan!",
        
        "house": "Buying a home requires preparation! Save for a down payment (aim for 20% to avoid PMI), check your credit score (higher scores get better rates), get pre-approved before house hunting, and remember the true cost includes maintenance, insurance, property taxes, and utilities.",
        
        "insurance": "Insurance protects your financial future! Essential types include health insurance, auto insurance, renters/homeowners insurance, and eventually life insurance if others depend on your income. Shop around annually for better rates, and choose higher deductibles to lower premiums if you have an emergency fund.",
    }
    
    # Default response if no keywords match
    default_response = "Financial literacy is key to building wealth! Start with creating a budget, build an emergency fund covering 3-6 months of expenses, pay down high-interest debt, save for retirement, and then expand to other investments. Small, consistent steps over time lead to financial freedom."
    
    # Try to use the API if available and not empty
    if st.session_state.get("openai_api_key") and st.session_state.openai_api_key.strip():
        try:
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            chat = ChatOpenAI(
                temperature=0.7,
                openai_api_key=st.session_state.openai_api_key,
                model="gpt-4o"
            )
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=prompt)
            ]
            
            response = chat(messages)
            return response.content
        except Exception as e:
            # Fall back to static responses on API error
            st.warning(f"API Error: Using static financial advice instead.")
            # Log the error details but don't show to user
            print(f"API Error details: {str(e)}")
    
    # Fallback to static responses if no API key or API error
    # Find the best matching keyword in the prompt
    lower_prompt = prompt.lower()
    for keyword, response in static_responses.items():
        if keyword in lower_prompt:
            return response
    
    # If no keyword matches, return the default response
    return default_response

def calculate_budget_summary(income, expenses):
    """Calculate budget summary statistics
    
    Args:
        income (list): List of income dictionaries with amount and name
        expenses (list): List of expense dictionaries with amount, name, and category
    
    Returns:
        dict: Summary statistics about the budget
    """
    total_income = sum(item["amount"] for item in income)
    total_expenses = sum(item["amount"] for item in expenses)
    balance = total_income - total_expenses
    
    # Group expenses by category
    expense_by_category = {}
    for expense in expenses:
        category = expense.get("category", "Other")
        if category in expense_by_category:
            expense_by_category[category] += expense["amount"]
        else:
            expense_by_category[category] = expense["amount"]
    
    # Calculate saving rate
    saving_rate = 0
    if total_income > 0:
        saving_rate = max(0, balance) / total_income * 100
    
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance,
        "expense_by_category": expense_by_category,
        "saving_rate": saving_rate
    }

def format_currency(amount):
    """Format an amount as Indian Rupees (INR)"""
    import locale
    
    # Try to set the locale to Indian English
    try:
        locale.setlocale(locale.LC_MONETARY, 'en_IN.UTF-8')
    except locale.Error:
        # Fallback if the locale is not available
        pass
    
    try:
        # Try to use locale formatting
        formatted = locale.currency(amount, grouping=True, symbol=True)
        # If locale formatting doesn't use ₹, replace the symbol
        if not formatted.startswith('₹'):
            formatted = '₹' + formatted.lstrip(locale.localeconv()['currency_symbol'])
        return formatted
    except:
        # Fallback to manual formatting with Indian number system
        if amount >= 0:
            is_negative = False
        else:
            is_negative = True
            amount = abs(amount)
            
        # Convert to string with 2 decimal places
        amount_str = f"{amount:.2f}"
        
        # Split into integer and decimal parts
        parts = amount_str.split('.')
        integer_part = parts[0]
        decimal_part = parts[1] if len(parts) > 1 else "00"
        
        # Apply Indian comma system (1,23,456.78)
        result = ""
        
        if len(integer_part) <= 3:
            result = integer_part
        else:
            # First group of 3 from the right
            result = integer_part[-3:]
            remaining = integer_part[:-3]
            
            # Rest in groups of 2
            while remaining:
                # Get at most 2 digits from the right
                group = remaining[-2:] if len(remaining) >= 2 else remaining
                result = group + "," + result
                remaining = remaining[:-len(group)]
        
        # Add decimal part
        result = f"{result}.{decimal_part}"
        
        # Add negative sign if needed
        if is_negative:
            result = "-" + result
            
        # Add Rupee symbol
        return f"₹{result}"

def calculate_financial_health_score(budget_summary, savings_goals, investment_progress):
    """
    Calculate a financial health score based on user's financial data
    
    Returns a score from 0-100 and recommendations
    """
    score = 0
    recommendations = []
    
    # Check if we have budget data
    if not budget_summary:
        return {
            "score": 0,
            "recommendations": ["Please complete your budget to get a financial health score."]
        }
    
    # Budget balance (30 points max)
    balance_ratio = budget_summary["balance"] / max(budget_summary["total_income"], 1)
    if balance_ratio >= 0.2:  # Saving at least 20% of income
        score += 30
    elif balance_ratio > 0:
        score += 15 + (balance_ratio / 0.2) * 15
    else:
        score += 0
        recommendations.append("Your expenses exceed your income. Try to reduce expenses or increase income.")
    
    # Saving goals (25 points max)
    if savings_goals:
        active_goals = sum(1 for goal in savings_goals if goal.get("active", False))
        completed_goals = sum(1 for goal in savings_goals if goal.get("completed", False))
        
        if active_goals > 0:
            score += 15
        if completed_goals > 0:
            score += 10
    else:
        recommendations.append("Set up savings goals to improve your financial health.")
    
    # Expense diversity (15 points max)
    if len(budget_summary.get("expense_by_category", {})) >= 5:
        score += 15
    else:
        score += len(budget_summary.get("expense_by_category", {})) * 3
    
    # Investment knowledge (30 points max)
    if investment_progress:
        lessons_score = min(15, investment_progress.get("lessons_completed", 0) * 5)
        quiz_score = min(15, investment_progress.get("quizzes_taken", 0) * 5)
        score += lessons_score + quiz_score
    else:
        recommendations.append("Learn about investing to boost your financial literacy.")
    
    # Round the score
    final_score = round(score)
    
    # Generate recommendations based on score
    if not recommendations:
        if final_score < 30:
            recommendations.append("Focus on building an emergency fund and tracking expenses.")
        elif final_score < 60:
            recommendations.append("Consider paying down high-interest debt and increasing your savings rate.")
        elif final_score < 90:
            recommendations.append("Look into diversifying your investments and optimizing your budget.")
        else:
            recommendations.append("Great job! Consider increasing retirement contributions or exploring advanced investment strategies.")
    
    return {
        "score": final_score,
        "recommendations": recommendations
    }
