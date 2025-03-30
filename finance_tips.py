import streamlit as st
import random
from utils import get_llm_response
from gamification import award_badge, update_user_progress

def display_finance_tips():
    st.title("💡 Daily Money Tips")
    st.write("Financial wisdom presented in a fun, GenZ-friendly format.")
    
    # Initialize tips counter in session state if not exists
    if "tips_viewed" not in st.session_state:
        st.session_state.tips_viewed = 0
    
    # Categories for financial tips
    tip_categories = [
        "Budgeting Hacks", 
        "Saving Strategies", 
        "Investing Basics", 
        "Debt Management",
        "Financial Planning", 
        "Side Hustle Ideas", 
        "Shopping Smart",
        "Credit Score Tips"
    ]
    
    # Allow user to select a category
    selected_category = st.selectbox(
        "What type of financial tips are you interested in?",
        tip_categories
    )
    
    # Daily tip section
    st.subheader("Your Daily Money Tip 💰")
    
    if st.button("Get a Fresh Tip"):
        with st.spinner("Generating your personalized tip..."):
            # Generate a tip with AI
            prompt = f"""
            Create a financial tip about {selected_category} in a GenZ-friendly style. 
            The tip should be:
            1. Practical and actionable
            2. Written in a casual, conversational tone with occasional slang
            3. Brief (2-3 sentences maximum)
            4. Presented like a social media post with an emoji
            5. Educational but not condescending
            
            Example format:
            "💸 [Brief, catchy financial tip in GenZ language]"
            
            Just provide the tip itself, no additional text.
            """
            
            tip = get_llm_response(prompt)
            
            # Display the tip in a styled container
            st.markdown(f"""
            <div class="financial-tip">
                <h3>Today's Tip</h3>
                {tip}
            </div>
            """, unsafe_allow_html=True)
            
            # Increment tips viewed counter
            st.session_state.tips_viewed += 1
            if st.session_state.tips_viewed == 1:
                award_badge("Tip Seeker", "💡")
                update_user_progress(0.05)
            elif st.session_state.tips_viewed >= 5:
                award_badge("Finance Guru", "🧠")
                update_user_progress(0.1)
    
    # Weekly challenge section
    st.subheader("Weekly Money Challenge 🏆")
    
    challenges = [
        "Track every expense for 7 days straight 📝",
        "Find 3 subscriptions you can cancel or reduce 🔍",
        "Save $5 every day this week 💰",
        "Learn one new investing term each day 📚",
        "Cook all meals at home for a week instead of eating out 🍳",
        "Set up automatic transfers to a savings account 🏦",
        "Review your budget and find one category to reduce by 10% ✂️",
        "Research one potential side hustle you could start 💼"
    ]
    
    # Select a random challenge based on the day of the week
    import datetime
    day_of_week = datetime.datetime.now().weekday()
    challenge_index = day_of_week % len(challenges)
    
    st.info(f"**This Week's Challenge:** {challenges[challenge_index]}")
    
    if st.button("Mark Challenge Complete"):
        st.success("🎉 Challenge completed! You're building great financial habits.")
        award_badge("Challenge Completer", "🏆")
        update_user_progress(0.15)
    
    # Financial wisdom collection
    st.subheader("Financial Wisdom Collection")
    
    # Categories of wisdom to display
    wisdom_categories = {
        "Budget Basics": [
            "Pay yourself first - allocate savings before spending.",
            "Follow the 50/30/20 rule: 50% needs, 30% wants, 20% savings.",
            "Review your subscriptions monthly - they add up quickly.",
            "Cash envelopes can help limit spending in problem categories.",
            "Budget for fun too - extreme restriction leads to giving up."
        ],
        "Saving Strategies": [
            "Save for emergencies first - aim for 3-6 months of expenses.",
            "Automate savings to remove the temptation to spend.",
            "Save raises and bonuses instead of increasing your lifestyle.",
            "Challenge yourself with no-spend days or weeks.",
            "Round up purchases and save the difference."
        ],
        "Investing 101": [
            "Start investing early - time is your biggest advantage.",
            "Index funds offer simple, low-cost diversification.",
            "Compound interest is powerful - even small amounts grow.",
            "Dollar-cost averaging reduces timing risk.",
            "Your asset allocation should match your time horizon."
        ]
    }
    
    # Let user select wisdom category
    wisdom_choice = st.radio("Choose a wisdom category:", list(wisdom_categories.keys()))
    
    # Display wisdoms from the selected category
    for i, wisdom in enumerate(wisdom_categories[wisdom_choice]):
        st.markdown(f"**{i+1}.** {wisdom}")
