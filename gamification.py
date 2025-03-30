import streamlit as st
import random
from datetime import datetime

def award_badge(badge_name, emoji):
    """Award a badge to the user if they don't already have it"""
    
    # Initialize user_badges if not exists
    if "user_badges" not in st.session_state:
        st.session_state.user_badges = []
    
    # Check if badge already exists
    badge_exists = any(badge["name"] == badge_name for badge in st.session_state.user_badges)
    
    if not badge_exists:
        # Add new badge
        new_badge = {
            "name": badge_name,
            "emoji": emoji,
            "date_earned": datetime.now().strftime("%Y-%m-%d")
        }
        st.session_state.user_badges.append(new_badge)
        
        # Show badge earned message
        st.balloons()
        st.success(f"🎉 Congratulations! You earned the {emoji} **{badge_name}** badge!")
        return True
    
    return False

def get_user_badges():
    """Get all badges earned by the user"""
    if "user_badges" not in st.session_state:
        st.session_state.user_badges = []
    
    return st.session_state.user_badges

def update_user_progress(increment):
    """Update the user's progress by the specified increment"""
    
    # Initialize user_progress if not exists
    if "user_progress" not in st.session_state:
        st.session_state.user_progress = 0.0
    
    # Increment progress and cap at 1.0
    current_progress = st.session_state.user_progress
    new_progress = min(1.0, current_progress + increment)
    st.session_state.user_progress = new_progress
    
    # Check for level up
    old_level = int(current_progress * 10)
    new_level = int(new_progress * 10)
    
    if new_level > old_level:
        st.success(f"🎉 **Level Up!** You reached Level {new_level}!")
        
        # Award special badges at certain levels
        if new_level == 5:
            award_badge("Halfway Hero", "🌟")
        elif new_level == 10:
            award_badge("Finance Master", "👑")
    
    return new_progress

def get_achievements_list():
    """Generate list of available achievements"""
    return [
        {"name": "Budget Explorer", "emoji": "🧮", "description": "Create your first budget"},
        {"name": "Income Tracker", "emoji": "💵", "description": "Add your first income source"},
        {"name": "Expense Tracker", "emoji": "📝", "description": "Add your first expense"},
        {"name": "Budget Master", "emoji": "🏆", "description": "Get budget recommendations"},
        {"name": "Goal Setter", "emoji": "🎯", "description": "Create your first savings goal"},
        {"name": "Goal Achiever", "emoji": "🎯", "description": "Complete a savings goal"},
        {"name": "Investment Student", "emoji": "📊", "description": "Complete your first investment lesson"},
        {"name": "Investment Explorer", "emoji": "🔍", "description": "Complete 3+ investment lessons"},
        {"name": "Quiz Taker", "emoji": "❓", "description": "Take your first investment quiz"},
        {"name": "Investment Guru", "emoji": "🧠", "description": "Score 80%+ on an investment quiz"},
        {"name": "Smart Shopper", "emoji": "🛒", "description": "Use the affordability calculator"},
        {"name": "Tip Seeker", "emoji": "💡", "description": "View your first financial tip"},
        {"name": "Finance Guru", "emoji": "🧠", "description": "View 5+ financial tips"},
        {"name": "Challenge Completer", "emoji": "🏆", "description": "Complete a weekly money challenge"},
        {"name": "Health Checker", "emoji": "🩺", "description": "Check your financial health score"},
        {"name": "Financial Improver", "emoji": "📈", "description": "Improve your financial health score"},
        {"name": "Halfway Hero", "emoji": "🌟", "description": "Reach level 5"},
        {"name": "Finance Master", "emoji": "👑", "description": "Reach level 10"}
    ]

def display_achievements_page():
    """Display a page showing all possible achievements and user progress"""
    st.title("🏆 Achievements")
    st.write("Track your progress and earn badges as you learn about personal finance!")
    
    all_achievements = get_achievements_list()
    user_badges = get_user_badges()
    
    # Get names of earned badges
    earned_badge_names = [badge["name"] for badge in user_badges]
    
    # Display badges in a grid
    st.subheader("Your Achievements")
    
    cols = st.columns(3)
    for i, achievement in enumerate(all_achievements):
        with cols[i % 3]:
            name = achievement["name"]
            emoji = achievement["emoji"]
            description = achievement["description"]
            
            if name in earned_badge_names:
                st.markdown(f"### {emoji} {name}")
                st.success(description)
                # Find when it was earned
                for badge in user_badges:
                    if badge["name"] == name:
                        st.caption(f"Earned on {badge['date_earned']}")
            else:
                st.markdown(f"### ❓ {name}")
                st.info(description)
                st.caption("Not yet earned")
    
    # Show progress
    st.subheader("Overall Progress")
    progress = st.session_state.get("user_progress", 0)
    st.progress(progress)
    current_level = int(progress * 10)
    next_level = current_level + 1
    st.write(f"**Current Level: {current_level}/10**")
    
    if current_level < 10:
        progress_to_next = (progress * 10) % 1 * 100
        st.write(f"Progress to Level {next_level}: {progress_to_next:.1f}%")
