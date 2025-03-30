import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_llm_response, calculate_budget_summary
from gamification import award_badge, update_user_progress

def display_affordability_calculator():
    st.title("🛒 Can I Afford It?")
    st.write("Enter a potential purchase to see if it fits within your budget and get smart recommendations.")
    
    # Check if budget data exists
    has_budget = False
    budget_summary = None
    if "user_budget" in st.session_state:
        if st.session_state.user_budget["income"] and st.session_state.user_budget["expenses"]:
            has_budget = True
            budget_summary = calculate_budget_summary(
                st.session_state.user_budget["income"],
                st.session_state.user_budget["expenses"]
            )
    
    # If no budget data, prompt user to create a budget
    if not has_budget:
        st.warning("⚠️ To get accurate affordability analysis, please set up your budget in the Budget Planner first.")
        st.info("For now, we'll use a simplified analysis based only on this purchase.")
    
    # Item information form
    with st.form("affordability_form"):
        st.subheader("Purchase Information")
        
        item_name = st.text_input("What do you want to buy?")
        item_cost = st.number_input("Cost ($)", min_value=0.0, step=10.0)
        
        # Purchase type options
        purchase_type = st.radio(
            "Purchase type:",
            ["One-time purchase", "Monthly subscription/payment"]
        )
        
        # Additional context fields
        st.subheader("Additional Details (Optional)")
        
        necessity_level = st.slider(
            "How necessary is this purchase?",
            1, 10, 5,
            help="1 = Pure luxury, 10 = Absolute necessity"
        )
        
        purchase_urgency = st.radio(
            "Purchase urgency:",
            ["Can wait (not time-sensitive)", "Soon (within a few months)", "Urgent (needed immediately)"]
        )
        
        # If they have savings goals, ask if this is related
        have_savings_goal = False
        if "savings_goals" in st.session_state and st.session_state.savings_goals:
            have_savings_goal = True
            st.subheader("Savings Goals")
            
            # Get active savings goals
            active_goals = [goal for goal in st.session_state.savings_goals 
                            if not goal.get("deleted", False) and not goal.get("completed", False)]
            
            if active_goals:
                goal_names = ["Not related to any savings goal"] + [goal["name"] for goal in active_goals]
                related_goal = st.selectbox("Is this purchase related to a savings goal?", goal_names)
            else:
                st.info("You have no active savings goals.")
                related_goal = "None"
        else:
            related_goal = "None"
        
        # Submit button
        submitted = st.form_submit_button("Analyze Affordability")
        
        if submitted and item_name and item_cost > 0:
            # Show analysis
            st.subheader(f"Affordability Analysis for: {item_name}")
            
            # Prepare analysis based on available budget data
            if has_budget:
                # Calculate financial metrics
                monthly_surplus = budget_summary["balance"]
                monthly_income = budget_summary["total_income"]
                
                # Calculate different metrics based on purchase type
                if purchase_type == "One-time purchase":
                    # For one-time purchases
                    months_to_save = item_cost / monthly_surplus if monthly_surplus > 0 else float('inf')
                    percent_of_monthly_income = (item_cost / monthly_income) * 100
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Monthly Surplus", f"${monthly_surplus:.2f}")
                    with col2:
                        st.metric("Cost as % of Monthly Income", f"{percent_of_monthly_income:.1f}%")
                    
                    # Basic affordability assessment
                    if monthly_surplus <= 0:
                        st.error("⛔ You currently have no surplus in your budget to save for this purchase.")
                    elif item_cost <= monthly_surplus:
                        st.success(f"✅ You could afford this purchase from a single month's surplus!")
                    else:
                        st.info(f"ℹ️ At your current savings rate, it would take approximately {months_to_save:.1f} months to save for this purchase.")
                    
                    # Create visual comparison
                    comparison_data = {
                        "Category": ["Monthly Income", "Monthly Expenses", "Item Cost"],
                        "Amount": [monthly_income, monthly_income - monthly_surplus, item_cost]
                    }
                    
                    fig = px.bar(
                        pd.DataFrame(comparison_data),
                        x="Category",
                        y="Amount",
                        title="Purchase Cost vs. Monthly Budget",
                        color="Category",
                        color_discrete_map={
                            "Monthly Income": "#00CC96", 
                            "Monthly Expenses": "#EF553B",
                            "Item Cost": "#636EFA"
                        }
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                else:
                    # For monthly subscriptions/payments
                    new_surplus = monthly_surplus - item_cost
                    impact_percentage = (item_cost / monthly_surplus) * 100 if monthly_surplus > 0 else float('inf')
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(
                            "Current Monthly Surplus", 
                            f"${monthly_surplus:.2f}",
                            delta=f"-${item_cost:.2f}"
                        )
                    with col2:
                        st.metric(
                            "New Monthly Surplus", 
                            f"${new_surplus:.2f}",
                            delta_color="inverse" if new_surplus < 0 else "normal"
                        )
                    
                    # Basic affordability assessment for subscription
                    if new_surplus < 0:
                        st.error("⛔ This subscription would put your budget into deficit.")
                    elif impact_percentage > 50:
                        st.warning(f"⚠️ This subscription would use {impact_percentage:.1f}% of your monthly surplus.")
                    else:
                        st.success(f"✅ This subscription appears affordable, using {impact_percentage:.1f}% of your monthly surplus.")
                    
                    # Create visual for budget impact
                    current_vs_new = {
                        "Budget": ["Current Budget", "With New Subscription"],
                        "Expenses": [monthly_income - monthly_surplus, monthly_income - monthly_surplus + item_cost],
                        "Surplus": [monthly_surplus, max(0, new_surplus)]
                    }
                    
                    # Reshape data for stacked bar chart
                    plot_data = []
                    for budget in current_vs_new["Budget"]:
                        idx = current_vs_new["Budget"].index(budget)
                        plot_data.append({
                            "Budget": budget,
                            "Category": "Expenses",
                            "Amount": current_vs_new["Expenses"][idx]
                        })
                        plot_data.append({
                            "Budget": budget,
                            "Category": "Surplus",
                            "Amount": current_vs_new["Surplus"][idx]
                        })
                    
                    fig = px.bar(
                        pd.DataFrame(plot_data),
                        x="Budget",
                        y="Amount",
                        color="Category",
                        title="Budget Impact of New Subscription",
                        barmode="stack",
                        color_discrete_map={
                            "Expenses": "#EF553B",
                            "Surplus": "#00CC96"
                        }
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            else:
                # Simplified analysis without budget data
                st.info("Without your full budget information, we can only provide general guidance.")
                st.write(f"Purchase cost: ${item_cost:.2f}")
                if purchase_type == "Monthly subscription/payment":
                    st.write(f"This would cost ${item_cost * 12:.2f} per year.")
            
            # Get AI recommendations regardless of budget data
            st.subheader("FinBuddy Recommendations")
            
            with st.spinner("Analyzing your purchase..."):
                # Build prompt with available information
                prompt = f"""
                Analyze this potential purchase and provide personalized advice:

                Item: {item_name}
                Cost: ${item_cost:.2f}
                Purchase type: {purchase_type}
                Necessity level (1-10): {necessity_level} 
                Urgency: {purchase_urgency}
                Related to savings goal: {related_goal}
                
                {f'Monthly budget surplus: ${monthly_surplus:.2f}' if has_budget else 'No budget information available.'}
                
                Provide 3 specific recommendations about:
                1. Whether this purchase seems affordable based on the information
                2. Alternative approaches to making this purchase more affordable
                3. How this purchase might impact their overall financial health
                
                Format as bullet points. Be specific and practical in your advice.
                """
                
                recommendations = get_llm_response(prompt)
                st.markdown(recommendations)
            
            # Award badge for using the calculator
            award_badge("Smart Shopper", "🛒")
            update_user_progress(0.1)
