import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random
from utils import get_llm_response, format_currency
from gamification import award_badge, update_user_progress

def display_savings_coach():
    st.title("🏦 Savings Coach")
    st.write("Set savings goals and get personalized strategies to achieve them.")
    
    # Initialize savings goals if not in session state
    if "savings_goals" not in st.session_state:
        st.session_state.savings_goals = []
    
    tab1, tab2 = st.tabs(["My Savings Goals", "Add New Goal"])
    
    # View existing savings goals
    with tab1:
        if not st.session_state.savings_goals:
            st.info("You haven't set any savings goals yet. Create one in the 'Add New Goal' tab!")
        else:
            st.subheader("Your Savings Goals")
            
            # Display all goals as cards
            for i, goal in enumerate(st.session_state.savings_goals):
                if not goal.get("deleted", False):  # Skip deleted goals
                    with st.expander(f"Goal: {goal['name']} - {format_currency(goal['target_amount'])}", expanded=True):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            # Display goal details
                            st.write(f"**Target amount:** {format_currency(goal['target_amount'])}")
                            st.write(f"**Current savings:** {format_currency(goal['current_amount'])}")
                            st.write(f"**Target date:** {goal['target_date']}")
                            
                            # Calculate and display progress
                            progress_pct = min(100, (goal['current_amount'] / goal['target_amount']) * 100)
                            st.progress(progress_pct / 100)
                            st.write(f"Progress: {progress_pct:.1f}%")
                            
                            # Time remaining calculation
                            target_date = datetime.strptime(goal['target_date'], "%Y-%m-%d")
                            days_remaining = (target_date - datetime.now()).days
                            if days_remaining > 0:
                                monthly_needed = (goal['target_amount'] - goal['current_amount']) / (days_remaining / 30)
                                st.write(f"To reach your goal, save approximately {format_currency(monthly_needed)} per month")
                            elif days_remaining <= 0 and progress_pct < 100:
                                st.error("Goal date has passed. Consider adjusting your timeline.")
                            
                            # Goal status
                            if progress_pct >= 100:
                                st.success("🎉 Goal achieved!")
                                if not goal.get("completed", False):
                                    goal["completed"] = True
                                    award_badge("Goal Achiever", "🎯")
                                    update_user_progress(0.2)
                            else:
                                goal["completed"] = False
                        
                        with col2:
                            # Add funds to the goal
                            st.write("Add funds:")
                            amount_to_add = st.number_input(
                                "Amount", 
                                min_value=0.0, 
                                step=10.0, 
                                key=f"add_amount_{i}"
                            )
                            if st.button("Add", key=f"add_btn_{i}"):
                                st.session_state.savings_goals[i]['current_amount'] += amount_to_add
                                st.success(f"Added {format_currency(amount_to_add)} to your goal!")
                                st.rerun()
                            
                            # Delete goal
                            if st.button("Delete Goal", key=f"delete_{i}"):
                                st.session_state.savings_goals[i]['deleted'] = True
                                st.success("Goal deleted!")
                                st.rerun()
                            
                            # Get strategy
                            if st.button("Get Saving Tips", key=f"tips_{i}"):
                                with st.spinner("Generating personalized tips..."):
                                    prompt = f"""
                                    Provide 3 specific, actionable tips for saving money for this goal:
                                    
                                    Goal: {goal['name']}
                                    Target amount: {format_currency(goal['target_amount'])}
                                    Current progress: {progress_pct:.1f}%
                                    Time remaining: {days_remaining} days
                                    
                                    Focus on practical methods for a student/young adult to save money.
                                    Format as bullet points.
                                    """
                                    
                                    tips = get_llm_response(prompt)
                                    st.markdown(tips)
    
    # Add new savings goal
    with tab2:
        st.subheader("Create a New Savings Goal")
        
        with st.form("new_goal_form"):
            goal_name = st.text_input("Goal Name (e.g., Emergency Fund, New Laptop)")
            goal_amount = st.number_input("Target Amount ($)", min_value=10.0, step=100.0)
            goal_date = st.date_input(
                "Target Date", 
                min_value=datetime.now().date(),
                value=(datetime.now() + timedelta(days=180)).date()
            )
            current_amount = st.number_input("Initial Savings ($)", min_value=0.0, step=10.0)
            
            submitted = st.form_submit_button("Create Goal")
            if submitted and goal_name and goal_amount > 0:
                new_goal = {
                    "name": goal_name,
                    "target_amount": goal_amount,
                    "target_date": goal_date.strftime("%Y-%m-%d"),
                    "current_amount": current_amount,
                    "start_date": datetime.now().strftime("%Y-%m-%d"),
                    "active": True,
                    "completed": False,
                    "deleted": False
                }
                
                st.session_state.savings_goals.append(new_goal)
                st.success(f"Created new savings goal: {goal_name}")
                
                # Award badge for creating first savings goal
                if len(st.session_state.savings_goals) == 1:
                    award_badge("Goal Setter", "🎯")
                    update_user_progress(0.1)
                
                st.rerun()
    
    # Show savings overview visualization if goals exist
    if st.session_state.savings_goals:
        active_goals = [g for g in st.session_state.savings_goals if not g.get("deleted", False)]
        if active_goals:
            st.subheader("Savings Overview")
            
            # Prepare data for visualization
            goal_data = []
            for goal in active_goals:
                goal_data.append({
                    "Goal": goal["name"],
                    "Current Amount": goal["current_amount"],
                    "Remaining": goal["target_amount"] - goal["current_amount"] if goal["current_amount"] < goal["target_amount"] else 0
                })
            
            goal_df = pd.DataFrame(goal_data)
            
            # Create stacked bar chart
            fig = px.bar(
                goal_df,
                x="Goal",
                y=["Current Amount", "Remaining"],
                title="Progress Towards Savings Goals",
                labels={"value": "Amount ($)", "variable": ""},
                color_discrete_map={
                    "Current Amount": "#00CC96",
                    "Remaining": "#EF553B"
                }
            )
            
            st.plotly_chart(fig, use_container_width=True)
