import streamlit as st
import pandas as pd
import plotly.express as px
import json
from utils import get_llm_response
from gamification import award_badge, update_user_progress

def display_investment_education():
    st.title("📚 Investment 101")
    st.write("Learn about stocks, mutual funds, and cryptocurrencies through interactive lessons and quizzes!")
    
    # Initialize investment progress
    if "investment_progress" not in st.session_state:
        st.session_state.investment_progress = {
            "lessons_completed": 0,
            "quizzes_taken": 0,
            "score": 0
        }
    
    # Investment topics
    investment_topics = [
        {
            "title": "Introduction to Investing",
            "description": "Learn the basics of investing and why it's important.",
            "difficulty": "Beginner"
        },
        {
            "title": "Understanding Stocks",
            "description": "Learn how stocks work, how to read stock charts, and basic stock terminology.",
            "difficulty": "Beginner"
        },
        {
            "title": "Mutual Funds Explained",
            "description": "Understand how mutual funds work and their benefits for beginners.",
            "difficulty": "Intermediate"
        },
        {
            "title": "Introduction to Cryptocurrencies",
            "description": "Learn the basics of blockchain technology and popular cryptocurrencies.",
            "difficulty": "Intermediate"
        },
        {
            "title": "Risk and Diversification",
            "description": "Understand investment risk and how to build a diversified portfolio.",
            "difficulty": "Advanced"
        }
    ]
    
    # Create tabs for lessons and quizzes
    tab1, tab2, tab3 = st.tabs(["Lessons", "Quizzes", "Progress"])
    
    # Lessons tab
    with tab1:
        st.subheader("Investment Lessons")
        
        # Display lessons as cards
        for i, topic in enumerate(investment_topics):
            with st.expander(f"{i+1}. {topic['title']} - {topic['difficulty']}", expanded=False):
                st.write(topic["description"])
                
                if st.button("Start Lesson", key=f"lesson_{i}"):
                    st.session_state.current_lesson = i
                    
                    # Generate lesson content using LLM
                    with st.spinner("Loading lesson content..."):
                        prompt = f"""
                        Create an educational lesson on {topic['title']} for a complete beginner.
                        The lesson should be structured with:
                        1. An introduction to the concept
                        2. 3-4 key points with simple explanations
                        3. A real-world example that illustrates the concept
                        4. A conclusion summarizing what was learned
                        
                        Keep explanations simple and jargon-free. Use analogies when possible.
                        Format with markdown headings and bullet points for readability.
                        """
                        
                        lesson_content = get_llm_response(prompt)
                        
                        # Display the lesson
                        st.markdown(lesson_content)
                        
                        # Mark lesson as completed and award badge
                        st.session_state.investment_progress["lessons_completed"] += 1
                        st.success("Lesson completed! You've earned knowledge points.")
                        
                        if st.session_state.investment_progress["lessons_completed"] == 1:
                            award_badge("Investment Student", "📊")
                            update_user_progress(0.1)
                        elif st.session_state.investment_progress["lessons_completed"] >= 3:
                            award_badge("Investment Explorer", "🔍")
                            update_user_progress(0.1)
    
    # Quizzes tab
    with tab2:
        st.subheader("Test Your Knowledge")
        
        # List of quizzes available
        quizzes = [
            "Investing Basics Quiz",
            "Stock Market Quiz",
            "Mutual Funds Quiz",
            "Cryptocurrency Quiz",
            "Risk and Portfolio Quiz"
        ]
        
        selected_quiz = st.selectbox("Select a quiz to take:", quizzes)
        
        if st.button("Start Quiz"):
            # Generate quiz questions using LLM
            with st.spinner("Preparing quiz questions..."):
                prompt = f"""
                Create a 5-question multiple-choice quiz about {selected_quiz.replace('Quiz', '')}.
                Each question should have 4 options (A, B, C, D) with only one correct answer.
                
                Format your response as a JSON object with this structure:
                {{
                    "questions": [
                        {{
                            "question": "Question text here?",
                            "options": ["Option A", "Option B", "Option C", "Option D"],
                            "correct_answer": 0,
                            "explanation": "Brief explanation of the answer"
                        }},
                        ...additional questions...
                    ]
                }}
                
                Make sure the questions are appropriate for beginners learning about investment concepts.
                The correct_answer field should be the index (0-3) of the correct option.
                """
                
                # Get response and parse as JSON
                response = get_llm_response(prompt)
                
                try:
                    # Extract the JSON part from the response
                    json_str = response
                    if "```json" in response:
                        json_str = response.split("```json")[1].split("```")[0]
                    elif "```" in response:
                        json_str = response.split("```")[1].split("```")[0]
                    
                    quiz_data = json.loads(json_str)
                    
                    # Store quiz in session state
                    st.session_state.current_quiz = quiz_data
                    st.session_state.quiz_answers = [None] * len(quiz_data["questions"])
                    st.session_state.quiz_submitted = False
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"Error parsing quiz: {str(e)}")
                    st.write("Raw response:")
                    st.code(response)
        
        # Display current quiz if available
        if "current_quiz" in st.session_state and not st.session_state.get("quiz_submitted", False):
            quiz_data = st.session_state.current_quiz
            
            st.subheader(f"{selected_quiz}")
            
            # Display questions and collect answers
            for i, q in enumerate(quiz_data["questions"]):
                st.write(f"**Question {i+1}:** {q['question']}")
                
                # Radio button for answer selection
                answer = st.radio(
                    f"Select your answer for question {i+1}:",
                    q["options"],
                    key=f"q_{i}"
                )
                
                # Store the selected answer index
                selected_index = q["options"].index(answer)
                st.session_state.quiz_answers[i] = selected_index
            
            # Submit button
            if st.button("Submit Quiz"):
                # Calculate score
                correct_answers = 0
                for i, q in enumerate(quiz_data["questions"]):
                    if st.session_state.quiz_answers[i] == q["correct_answer"]:
                        correct_answers += 1
                
                score_percent = (correct_answers / len(quiz_data["questions"])) * 100
                
                # Display results
                st.session_state.quiz_results = {
                    "correct": correct_answers,
                    "total": len(quiz_data["questions"]),
                    "percentage": score_percent
                }
                
                st.session_state.quiz_submitted = True
                
                # Update investment progress
                st.session_state.investment_progress["quizzes_taken"] += 1
                st.session_state.investment_progress["score"] += score_percent / 100
                
                # Award badge for quiz completion
                if st.session_state.investment_progress["quizzes_taken"] == 1:
                    award_badge("Quiz Taker", "❓")
                    update_user_progress(0.1)
                elif score_percent >= 80:
                    award_badge("Investment Guru", "🧠")
                    update_user_progress(0.15)
                
                st.rerun()
        
        # Display quiz results if submitted
        if "quiz_results" in st.session_state and st.session_state.get("quiz_submitted", False):
            results = st.session_state.quiz_results
            quiz_data = st.session_state.current_quiz
            
            st.subheader("Quiz Results")
            
            # Display score
            if results["percentage"] >= 80:
                st.success(f"🎉 Great job! You scored {results['correct']}/{results['total']} ({results['percentage']}%)")
            elif results["percentage"] >= 60:
                st.info(f"👍 Not bad! You scored {results['correct']}/{results['total']} ({results['percentage']}%)")
            else:
                st.warning(f"📚 Keep learning! You scored {results['correct']}/{results['total']} ({results['percentage']}%)")
            
            # Display answers and explanations
            st.subheader("Review Questions:")
            for i, q in enumerate(quiz_data["questions"]):
                user_answer = st.session_state.quiz_answers[i]
                correct_answer = q["correct_answer"]
                
                st.markdown(f"**Question {i+1}:** {q['question']}")
                
                # Show options with user's answer and correct answer highlighted
                for j, option in enumerate(q["options"]):
                    if j == user_answer and j == correct_answer:
                        st.markdown(f"✅ **{option}** (Your answer, Correct)")
                    elif j == user_answer:
                        st.markdown(f"❌ **{option}** (Your answer)")
                    elif j == correct_answer:
                        st.markdown(f"✅ {option} (Correct answer)")
                    else:
                        st.markdown(f"○ {option}")
                
                # Show explanation
                st.markdown(f"**Explanation:** {q['explanation']}")
                st.divider()
            
            # Option to take another quiz
            if st.button("Take Another Quiz"):
                del st.session_state.current_quiz
                del st.session_state.quiz_answers
                del st.session_state.quiz_results
                st.session_state.quiz_submitted = False
                st.rerun()
    
    # Progress tab
    with tab3:
        st.subheader("Your Investment Learning Progress")
        
        # Display statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Lessons Completed", st.session_state.investment_progress["lessons_completed"])
        with col2:
            st.metric("Quizzes Taken", st.session_state.investment_progress["quizzes_taken"])
        with col3:
            avg_score = 0
            if st.session_state.investment_progress["quizzes_taken"] > 0:
                avg_score = (st.session_state.investment_progress["score"] / st.session_state.investment_progress["quizzes_taken"]) * 100
            st.metric("Average Quiz Score", f"{avg_score:.1f}%")
        
        # Progress bar for overall investment knowledge
        completed_items = st.session_state.investment_progress["lessons_completed"] + st.session_state.investment_progress["quizzes_taken"]
        total_possible = len(investment_topics) + len(quizzes)
        progress_pct = min(1.0, completed_items / total_possible)
        
        st.subheader("Overall Investment Knowledge")
        st.progress(progress_pct)
        st.caption(f"{int(progress_pct * 100)}% complete")
        
        # Learning recommendations
        st.subheader("Next Steps")
        if st.session_state.investment_progress["lessons_completed"] == 0:
            st.write("👉 Start with the 'Introduction to Investing' lesson to build a foundation.")
        elif st.session_state.investment_progress["quizzes_taken"] == 0:
            st.write("👉 Take your first quiz to test what you've learned!")
        elif st.session_state.investment_progress["lessons_completed"] < 3:
            st.write("👉 Continue working through the lessons to expand your knowledge.")
        else:
            st.write("👉 Great progress! Challenge yourself with the advanced topics and quizzes.")
