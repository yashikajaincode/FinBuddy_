import streamlit as st
from utils import get_llm_response
from gamification import award_badge, update_user_progress

def display_chat_interface():
    st.title("💬 Chat with FinBuddy")
    st.write("Ask me anything about personal finance, budgeting, saving, or investing!")
    
    # Display info about static responses if no API key
    if not st.session_state.get("openai_api_key"):
        st.info("FinBuddy is currently using built-in financial advice. For personalized AI responses, add an OpenAI API key in the sidebar settings.")
        st.markdown("""
        **Try asking about these financial topics:**
        - Budgeting tips
        - How to save money
        - Investing basics
        - Managing debt
        - Building credit
        - Emergency funds
        - Retirement planning
        - Tax strategies
        - Home buying
        - Insurance needs
        """)
    
    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Accept user input
    if prompt := st.chat_input("What would you like to know about finance?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message in chat container
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Generate response
            system_prompt = """
            You are FinBuddy, an AI assistant specialized in financial education for beginners and students.
            You excel at explaining concepts like budgeting, saving, and investing in simple, engaging terms.
            Keep your responses concise but informative, and adopt a friendly, encouraging tone suitable for GenZ users.
            When appropriate, include practical examples or analogies to illustrate financial concepts.
            If asked about specific investment advice, clarify that you provide educational content only, not financial advice.
            """
            
            # Check for common financial topics to help with badge awards
            topic_keywords = {
                "budget": "budgeting",
                "save": "saving", 
                "saving": "saving",
                "invest": "investing",
                "investing": "investing",
                "stock": "investing",
                "emergency fund": "saving",
                "debt": "budgeting",
                "credit": "budgeting",
                "retirement": "investing"
            }
            
            # Check if the prompt contains financial topics
            detected_topics = []
            for keyword, topic in topic_keywords.items():
                if keyword.lower() in prompt.lower() and topic not in detected_topics:
                    detected_topics.append(topic)
            
            # Generate response
            full_response = get_llm_response(prompt, system_prompt)
            message_placeholder.markdown(full_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            # Award badges for financial topic discussions
            if detected_topics:
                for topic in detected_topics:
                    if topic == "budgeting":
                        award_badge("Budget Explorer", "🧮")
                    elif topic == "saving":
                        award_badge("Savings Guru", "💰")
                    elif topic == "investing":
                        award_badge("Investment Apprentice", "📈")
                
                # Increase user progress
                update_user_progress(0.05)  # Small increment for using the chat
