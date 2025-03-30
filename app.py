import streamlit as st
import os
from finbuddy_chat import display_chat_interface
from budget_planner import display_budget_planner
from savings_coach import display_savings_coach
from investment_education import display_investment_education
from affordability_calculator import display_affordability_calculator
from finance_tips import display_finance_tips
from financial_health import display_financial_health_score
from gamification import get_user_badges, update_user_progress
from utils import initialize_session_state, load_css

def main():
    # Initialize session state variables
    initialize_session_state()
    
    # Page configuration
    st.set_page_config(
        page_title="FinBuddy - Your AI Financial Coach",
        page_icon="💰",
        layout="wide",
    )
    
    # Load custom CSS
    load_css()
    
    # Sidebar navigation
    with st.sidebar:
        st.title("FinBuddy 💰")
        st.image("assets/finbuddy_logo.svg", width=150)
        st.write("Your AI-powered financial education companion")
        
        # Navigation options
        page = st.radio(
            "Choose a Feature:",
            [
                "Chat with FinBuddy", 
                "Budget Planner", 
                "Savings Coach", 
                "Investment 101",
                "Can I Afford It?", 
                "Daily Money Tips", 
                "Financial Health Score"
            ]
        )
        
        # Display user's badges and progress
        st.divider()
        st.subheader("Your Progress")
        badges = get_user_badges()
        if badges:
            st.write("Badges earned:")
            cols = st.columns(3)
            for i, badge in enumerate(badges):
                with cols[i % 3]:
                    st.markdown(f"#### {badge['emoji']}")
                    st.caption(f"{badge['name']}")
        else:
            st.write("Complete tasks to earn badges!")
        
        # Progress bar
        progress = st.session_state.get("user_progress", 0)
        st.progress(progress)
        st.caption(f"Level: {int(progress * 10)}/10")
        
        # Show API key input field
        with st.expander("API Settings (Optional)"):
            api_key = st.text_input("OpenAI API Key (Optional)", 
                                     type="password", 
                                     value=os.environ.get("OPENAI_API_KEY", ""),
                                     help="Optional: Enter your OpenAI API key for personalized AI responses. If not provided, the app will use static responses.")
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
                st.session_state.openai_api_key = api_key
            else:
                st.info("No API key provided. Using built-in financial advice instead of AI responses.")
    
    # Main content area
    if page == "Chat with FinBuddy":
        display_chat_interface()
    elif page == "Budget Planner":
        display_budget_planner()
    elif page == "Savings Coach":
        display_savings_coach()
    elif page == "Investment 101":
        display_investment_education()
    elif page == "Can I Afford It?":
        display_affordability_calculator()
    elif page == "Daily Money Tips":
        display_finance_tips()
    elif page == "Financial Health Score":
        display_financial_health_score()
    
    # Update user progress (for demo, increment on page views)
    if st.session_state.get("page_view_count", 0) % 5 == 0:
        update_user_progress(0.1)  # Increase progress by 10%
    st.session_state.page_view_count = st.session_state.get("page_view_count", 0) + 1

if __name__ == "__main__":
    main()
