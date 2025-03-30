import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils import calculate_budget_summary, calculate_financial_health_score, get_llm_response
from gamification import award_badge, update_user_progress

def display_financial_health_score():
    st.title("🚦 Financial Health Score")
    st.write("Get a personalized assessment of your financial situation and actionable recommendations.")
    
    # Check if user has budget data
    has_budget = False
    budget_summary = None
    
    if "user_budget" in st.session_state:
        if st.session_state.user_budget["income"] and st.session_state.user_budget["expenses"]:
            has_budget = True
            budget_summary = calculate_budget_summary(
                st.session_state.user_budget["income"],
                st.session_state.user_budget["expenses"]
            )
    
    # Check for savings goals
    has_savings_goals = False
    active_savings_goals = []
    
    if "savings_goals" in st.session_state:
        active_savings_goals = [goal for goal in st.session_state.savings_goals 
                               if not goal.get("deleted", False)]
        if active_savings_goals:
            has_savings_goals = True
    
    # Check for investment progress
    has_investment_progress = False
    investment_progress = None
    
    if "investment_progress" in st.session_state:
        if st.session_state.investment_progress["lessons_completed"] > 0:
            has_investment_progress = True
            investment_progress = st.session_state.investment_progress
    
    # Prompt user to complete prerequisites if missing data
    missing_data = []
    if not has_budget:
        missing_data.append("- Add your income and expenses in the Budget Planner")
    if not has_savings_goals:
        missing_data.append("- Set up at least one savings goal in the Savings Coach")
    if not has_investment_progress:
        missing_data.append("- Complete at least one lesson in Investment 101")
    
    if missing_data:
        st.warning("For a complete financial health assessment, please:")
        for item in missing_data:
            st.markdown(item)
        
        st.info("You can still get a basic assessment with the available information.")
    
    # Show existing score if available
    if "financial_health_score" in st.session_state and st.session_state.financial_health_score:
        old_score = st.session_state.financial_health_score.get("score", 0)
    else:
        old_score = None
    
    # Button to calculate/recalculate score
    if st.button("Calculate My Financial Health Score"):
        # Calculate financial health score
        score_result = calculate_financial_health_score(
            budget_summary, 
            active_savings_goals, 
            investment_progress
        )
        
        # Store the score in session state
        st.session_state.financial_health_score = score_result
        
        # Check if first time or improvement
        if old_score is None:
            award_badge("Health Checker", "🩺")
            update_user_progress(0.1)
        elif score_result["score"] > old_score:
            award_badge("Financial Improver", "📈")
            update_user_progress(0.15)
        
        st.rerun()
    
    # Display financial health score if available
    if "financial_health_score" in st.session_state and st.session_state.financial_health_score:
        score_result = st.session_state.financial_health_score
        score = score_result["score"]
        
        # Create score visualization
        st.subheader("Your Financial Health Score")
        
        # Create gauge chart for score
        fig = create_gauge_chart(score)
        st.plotly_chart(fig, use_container_width=True)
        
        # Score interpretation
        if score >= 80:
            st.success("🌟 Excellent! Your financial health is strong.")
        elif score >= 60:
            st.info("👍 Good job! Your financial health is on the right track.")
        elif score >= 40:
            st.warning("⚠️ Your financial health needs some attention.")
        else:
            st.error("❗ Your financial health needs significant improvement.")
        
        # Display recommendations
        st.subheader("Recommendations")
        for i, rec in enumerate(score_result["recommendations"]):
            st.markdown(f"**{i+1}.** {rec}")
        
        # Get detailed recommendations with AI
        st.subheader("Personalized Improvement Plan")
        
        if st.button("Generate Detailed Improvement Plan"):
            with st.spinner("Creating your personalized plan..."):
                # Gather all financial data
                financial_data = {
                    "score": score,
                    "has_budget": has_budget,
                    "has_savings_goals": has_savings_goals,
                    "has_investment_knowledge": has_investment_progress
                }
                
                if has_budget:
                    financial_data["income"] = budget_summary["total_income"]
                    financial_data["expenses"] = budget_summary["total_expenses"]
                    financial_data["balance"] = budget_summary["balance"]
                    financial_data["saving_rate"] = budget_summary["saving_rate"]
                
                if has_savings_goals:
                    financial_data["active_goals"] = len(active_savings_goals)
                    financial_data["completed_goals"] = sum(1 for goal in active_savings_goals if goal.get("completed", False))
                
                if has_investment_progress:
                    financial_data["investment_lessons"] = investment_progress["lessons_completed"]
                    financial_data["investment_quizzes"] = investment_progress["quizzes_taken"]
                
                # Generate comprehensive plan with AI
                prompt = f"""
                Create a detailed financial improvement plan for someone with these financial metrics:
                
                Financial Health Score: {score}/100
                
                Data points:
                {financial_data}
                
                Create a 3-step action plan with:
                1. Short-term actions (next 30 days)
                2. Medium-term goals (next 3-6 months)
                3. Long-term financial strategies (next 1-2 years)
                
                For each timeframe, provide 2-3 specific, actionable recommendations
                that will help improve their financial health score. Focus on the areas
                where they seem to be lacking based on the data.
                
                Format with clear headings and bullet points for readability.
                """
                
                improvement_plan = get_llm_response(prompt)
                st.markdown(improvement_plan)
        
        # Show breakdown of score components
        st.subheader("Score Breakdown")
        
        # Create dummy data if some components are missing
        components = []
        
        if has_budget:
            if budget_summary["balance"] > 0:
                score_percent = min(100, (budget_summary["balance"] / budget_summary["total_income"]) * 100 * 5)
                components.append({"Category": "Budget Balance", "Score": score_percent})
            else:
                components.append({"Category": "Budget Balance", "Score": 0})
        else:
            components.append({"Category": "Budget Balance", "Score": 0})
        
        if has_savings_goals:
            savings_score = min(100, len(active_savings_goals) * 25)
            components.append({"Category": "Savings Goals", "Score": savings_score})
        else:
            components.append({"Category": "Savings Goals", "Score": 0})
        
        if has_investment_progress:
            inv_score = min(100, (investment_progress["lessons_completed"] * 15 + 
                                  investment_progress["quizzes_taken"] * 10))
            components.append({"Category": "Investment Knowledge", "Score": inv_score})
        else:
            components.append({"Category": "Investment Knowledge", "Score": 0})
        
        # Add debt management as another component (placeholder score if no data)
        if has_budget:
            debt_expenses = sum(expense["amount"] for expense in st.session_state.user_budget["expenses"] 
                              if expense.get("category", "").lower() == "debt")
            if debt_expenses > 0:
                # Higher score for lower debt ratio
                debt_ratio = debt_expenses / budget_summary["total_income"]
                debt_score = max(0, 100 - (debt_ratio * 200))  # Lower is better
            else:
                debt_score = 90  # High score for no debt
        else:
            debt_score = 50  # Neutral score if no data
        
        components.append({"Category": "Debt Management", "Score": debt_score})
        
        # Create the component breakdown chart
        component_df = pd.DataFrame(components)
        fig = px.bar(
            component_df,
            x="Category",
            y="Score",
            title="Financial Health Components",
            color="Score",
            color_continuous_scale=["red", "yellow", "green"],
            range_color=[0, 100]
        )
        
        fig.update_layout(yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)
        
        # Suggest areas for improvement based on lowest components
        lowest_component = min(components, key=lambda x: x["Score"])
        
        st.subheader("Focus Area")
        st.write(f"Based on your score breakdown, you should focus on improving your **{lowest_component['Category']}**.")
        
        # Specific tips based on the lowest component
        if lowest_component["Category"] == "Budget Balance":
            st.markdown("""
            **Tips to improve your budget balance:**
            - Review your expenses to find areas to cut back
            - Look for ways to increase your income (side hustles, negotiating salary)
            - Apply the 50/30/20 rule for better expense allocation
            """)
        elif lowest_component["Category"] == "Savings Goals":
            st.markdown("""
            **Tips to improve your savings:**
            - Set up at least one emergency fund goal
            - Create specific savings goals with clear timelines
            - Automate transfers to your savings accounts
            """)
        elif lowest_component["Category"] == "Investment Knowledge":
            st.markdown("""
            **Tips to improve your investment knowledge:**
            - Complete more lessons in the Investment 101 section
            - Take quizzes to test your understanding
            - Start with learning about index funds and compound interest
            """)
        elif lowest_component["Category"] == "Debt Management":
            st.markdown("""
            **Tips to improve your debt management:**
            - Focus on paying off high-interest debt first
            - Consider consolidating debt if interest rates are high
            - Create a debt payoff plan with specific monthly targets
            """)

def create_gauge_chart(score):
    """Create a gauge chart for the financial health score"""
    
    # Define the ranges and colors
    if score >= 80:
        color = "green"
    elif score >= 60:
        color = "yellow"
    elif score >= 40:
        color = "orange"
    else:
        color = "red"
    
    # Create the gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Financial Health Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": color},
            "steps": [
                {"range": [0, 40], "color": "lightgray"},
                {"range": [40, 60], "color": "lightgray"},
                {"range": [60, 80], "color": "lightgray"},
                {"range": [80, 100], "color": "lightgray"}
            ],
            "threshold": {
                "line": {"color": "black", "width": 4},
                "thickness": 0.75,
                "value": score
            }
        }
    ))
    
    fig.update_layout(height=300)
    
    return fig
