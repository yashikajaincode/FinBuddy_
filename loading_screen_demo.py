import streamlit as st
import time
import base64
from pathlib import Path

st.set_page_config(
    page_title="FinBuddy LoadingScreen Demo",
    page_icon="💰",
    layout="wide",
)

# Custom CSS to demonstrate the LoadingScreen animations
st.markdown("""
<style>
/* Global styles for demo */
body {
    font-family: 'Inter', sans-serif;
    color: #1F2937;
    background-color: #F9FAFB;
}

/* Variables */
:root {
  --primary-color: #6366F1;
  --primary-light: #818CF8;
  --primary-dark: #4F46E5;
  
  --secondary-color: #F59E0B;
  --secondary-light: #FBBF24;
  --secondary-dark: #D97706;
  
  --success-color: #10B981;
  --success-light: #34D399;
  --success-dark: #059669;
  
  --warning-color: #F59E0B;
  --warning-light: #FBBF24;
  --warning-dark: #D97706;
  
  --danger-color: #EF4444;
  --danger-light: #F87171;
  --danger-dark: #DC2626;
}

/* Card styles */
.demo-card {
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.demo-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* Animation container */
.animation-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 200px;
    overflow: hidden;
    margin: 20px 0;
}

/* Loading Mascot Animation Styles */

/* Coin Mascot */
@keyframes bounceCoin {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}

@keyframes rotateCoin {
  0% { transform: rotateY(0); }
  100% { transform: rotateY(360deg); }
}

@keyframes scaleShadow {
  0%, 100% { transform: scaleX(1); opacity: 0.7; }
  50% { transform: scaleX(0.7); opacity: 0.4; }
}

/* Piggy Bank Mascot */
@keyframes wigglePiggy {
  0%, 100% { transform: rotate(0); }
  25% { transform: rotate(-5deg); }
  75% { transform: rotate(5deg); }
}

@keyframes blinkEyes {
  0%, 45%, 55%, 100% { transform: scaleY(1); }
  50% { transform: scaleY(0.1); }
}

@keyframes dropCoin {
  0% { top: -30px; opacity: 1; }
  60% { top: 10px; opacity: 1; }
  70% { top: 10px; opacity: 0; transform: scale(0.8); }
  100% { top: 10px; opacity: 0; }
}

/* Chart Mascot */
@keyframes pulseChart {
  0% { transform: scale(1); }
  100% { transform: scale(1.05); }
}

@keyframes barGrow {
  0% { transform: scaleY(0.7); }
  100% { transform: scaleY(1); }
}

@keyframes arrowBounce {
  0% { transform: translateX(0); }
  100% { transform: translateX(5px); }
}

/* Rocket Mascot */
@keyframes rocketMove {
  0%, 100% { transform: translateY(0) rotate(5deg); }
  50% { transform: translateY(-20px) rotate(-5deg); }
}

@keyframes flicker {
  0% { opacity: 0.7; height: 25px; }
  100% { opacity: 1; height: 30px; }
}

@keyframes particleFly {
  0% { bottom: 0; opacity: 1; }
  100% { bottom: -30px; opacity: 0; }
}

@keyframes pulseDollar {
  0% { opacity: 0.8; transform: translateX(-50%) scale(1); }
  100% { opacity: 1; transform: translateX(-50%) scale(1.1); }
}
</style>
""", unsafe_allow_html=True)

# Helper function to load HTML from file and display
def load_mascot_animation(mascot_type, theme="primary"):
    if mascot_type == "coin":
        html = f"""
        <div class="animation-container">
            <div style="animation: bounceCoin 2s infinite ease-in-out; width: 150px; height: 150px; display: flex; justify-content: center; align-items: center;">
                <div style="width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(45deg, #4F46E5, #818CF8); position: relative; display: flex; justify-content: center; align-items: center; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); animation: rotateCoin 8s infinite linear;">
                    <div style="width: 70px; height: 70px; border-radius: 50%; background-color: rgba(255, 255, 255, 0.1); display: flex; justify-content: center; align-items: center; border: 2px solid rgba(255, 255, 255, 0.3);">
                        <div style="font-size: 36px; font-weight: bold; color: white; text-shadow: 0 2px 3px rgba(0, 0, 0, 0.2);">$</div>
                    </div>
                    <div style="position: absolute; top: 10px; left: 15px; width: 20px; height: 10px; border-radius: 50%; background: rgba(255, 255, 255, 0.7); transform: rotate(-30deg);"></div>
                </div>
                <div style="position: absolute; bottom: -10px; width: 70px; height: 10px; border-radius: 50%; background-color: rgba(0, 0, 0, 0.1); animation: scaleShadow 2s infinite ease-in-out;"></div>
            </div>
        </div>
        """
    elif mascot_type == "piggy":
        html = f"""
        <div class="animation-container">
            <div style="animation: wigglePiggy 2s infinite ease-in-out; width: 150px; height: 150px; position: relative; display: flex; justify-content: center; align-items: center;">
                <div style="width: 90px; height: 70px; background-color: #F87171; border-radius: 45% 45% 50% 50%; position: relative; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);">
                    <div style="width: 20px; height: 20px; background-color: #F87171; border-radius: 50%; position: absolute; top: -10px; left: 15px; transform: rotate(-30deg);"></div>
                    <div style="width: 20px; height: 20px; background-color: #F87171; border-radius: 50%; position: absolute; top: -10px; right: 15px; transform: rotate(30deg);"></div>
                    <div style="width: 30px; height: 25px; background-color: #FECACA; border-radius: 45%; position: absolute; bottom: 5px; left: 50%; transform: translateX(-50%);">
                        <div style="width: 6px; height: 6px; background-color: #991B1B; border-radius: 50%; position: absolute; bottom: 8px; left: 8px;"></div>
                        <div style="width: 6px; height: 6px; background-color: #991B1B; border-radius: 50%; position: absolute; bottom: 8px; right: 8px;"></div>
                    </div>
                    <div style="width: 15px; height: 15px; background-color: white; border-radius: 50%; position: absolute; top: 15px; left: 20px;">
                        <div style="width: 6px; height: 6px; background-color: #1F2937; border-radius: 50%; position: absolute; top: 5px; left: 5px; animation: blinkEyes 4s infinite;"></div>
                    </div>
                    <div style="width: 15px; height: 15px; background-color: white; border-radius: 50%; position: absolute; top: 15px; right: 20px;">
                        <div style="width: 6px; height: 6px; background-color: #1F2937; border-radius: 50%; position: absolute; top: 5px; left: 5px; animation: blinkEyes 4s infinite;"></div>
                    </div>
                    <div style="width: 15px; height: 3px; background-color: #991B1B; position: absolute; top: 15px; left: 50%; transform: translateX(-50%); border-radius: 3px;"></div>
                </div>
                <div style="position: absolute; width: 15px; height: 15px; background-color: #FBBF24; border-radius: 50%; border: 1px solid #F59E0B; top: 0; left: 20px; opacity: 0; animation: dropCoin 3s infinite;"></div>
                <div style="position: absolute; width: 15px; height: 15px; background-color: #FBBF24; border-radius: 50%; border: 1px solid #F59E0B; top: 0; left: 40px; opacity: 0; animation: dropCoin 3s infinite 1s;"></div>
                <div style="position: absolute; width: 15px; height: 15px; background-color: #FBBF24; border-radius: 50%; border: 1px solid #F59E0B; top: 0; left: 60px; opacity: 0; animation: dropCoin 3s infinite 2s;"></div>
            </div>
        </div>
        """
    elif mascot_type == "chart":
        html = f"""
        <div class="animation-container">
            <div style="animation: pulseChart 2s infinite alternate; width: 150px; height: 150px; position: relative; display: flex; justify-content: center; align-items: center;">
                <div style="width: 90px; height: 70px; background-color: white; border-radius: 5px; position: relative; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1); display: flex; align-items: flex-end; justify-content: space-around; padding: 10px 10px 15px 10px; border: 1px solid #E5E7EB;">
                    <div style="width: 12px; height: 30px; background-color: #6366F1; border-radius: 3px 3px 0 0; position: relative; transform-origin: bottom; animation: barGrow 3s infinite alternate;"></div>
                    <div style="width: 12px; height: 20px; background-color: #6366F1; border-radius: 3px 3px 0 0; position: relative; transform-origin: bottom; animation: barGrow 3s infinite alternate 0.2s;"></div>
                    <div style="width: 12px; height: 40px; background-color: #6366F1; border-radius: 3px 3px 0 0; position: relative; transform-origin: bottom; animation: barGrow 3s infinite alternate 0.4s;"></div>
                    <div style="width: 12px; height: 25px; background-color: #6366F1; border-radius: 3px 3px 0 0; position: relative; transform-origin: bottom; animation: barGrow 3s infinite alternate 0.6s;"></div>
                    <div style="position: absolute; left: 10px; right: 10px; bottom: 10px; height: 2px; background-color: #E5E7EB;"></div>
                    <div style="position: absolute; width: 6px; height: 6px; background-color: #6366F1; border-radius: 50%; top: 20px; left: 20px;"></div>
                    <div style="position: absolute; width: 6px; height: 6px; background-color: #6366F1; border-radius: 50%; top: 15px; left: 35px;"></div>
                    <div style="position: absolute; width: 6px; height: 6px; background-color: #6366F1; border-radius: 50%; top: 25px; left: 50px;"></div>
                    <div style="position: absolute; width: 6px; height: 6px; background-color: #6366F1; border-radius: 50%; top: 10px; left: 65px;"></div>
                </div>
                <div style="position: absolute; right: -10px; bottom: 30px; width: 20px; height: 10px; clip-path: polygon(0 0, 100% 50%, 0 100%); background-color: #10B981; animation: arrowBounce 2s infinite alternate;"></div>
            </div>
        </div>
        """
    else:  # rocket
        html = f"""
        <div class="animation-container">
            <div style="animation: rocketMove 3s infinite ease-in-out; width: 150px; height: 150px; position: relative; display: flex; justify-content: center; align-items: center;">
                <div style="width: 40px; height: 90px; background: linear-gradient(135deg, #6366F1, #4F46E5); border-radius: 50% 50% 10% 10%; position: relative; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);">
                    <div style="width: 20px; height: 20px; background-color: rgba(255, 255, 255, 0.9); border-radius: 50%; position: absolute; top: 15px; left: 50%; transform: translateX(-50%); border: 2px solid rgba(0, 0, 0, 0.1);"></div>
                    <div style="width: 15px; height: 30px; background-color: #4F46E5; position: absolute; bottom: 20px; left: -15px; border-radius: 10px 0 0 10px;"></div>
                    <div style="width: 15px; height: 30px; background-color: #4F46E5; position: absolute; bottom: 20px; right: -15px; border-radius: 0 10px 10px 0;"></div>
                    <div style="width: 20px; height: 15px; background-color: rgba(255, 255, 255, 0.7); border-radius: 0 0 10px 10px; position: absolute; bottom: -15px; left: 50%; transform: translateX(-50%); overflow: hidden;">
                        <div style="width: 20px; height: 30px; background: linear-gradient(to bottom, #F59E0B, #EF4444); position: absolute; bottom: 0; left: 0; animation: flicker 0.3s infinite alternate; clip-path: polygon(0 0, 100% 0, 90% 30%, 100% 60%, 80% 100%, 50% 70%, 20% 100%, 0 60%, 10% 30%);"></div>
                        <div style="position: absolute; width: 5px; height: 5px; background-color: #F59E0B; border-radius: 50%; bottom: -5px; left: 2px; opacity: 0.7; animation: particleFly 1.5s infinite linear;"></div>
                        <div style="position: absolute; width: 5px; height: 5px; background-color: #F59E0B; border-radius: 50%; bottom: -5px; left: 8px; opacity: 0.7; animation: particleFly 1.5s infinite linear 0.2s;"></div>
                        <div style="position: absolute; width: 5px; height: 5px; background-color: #F59E0B; border-radius: 50%; bottom: -5px; left: 14px; opacity: 0.7; animation: particleFly 1.5s infinite linear 0.4s;"></div>
                    </div>
                </div>
                <div style="position: absolute; top: 15px; left: 50%; transform: translateX(-50%); font-size: 24px; font-weight: bold; color: white; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); animation: pulseDollar 2s infinite alternate;">$</div>
            </div>
        </div>
        """
    
    return html

# Main app
st.title("FinBuddy LoadingScreen Demonstrations")
st.markdown("These are the animated financial mascots we've created for the loading screens in the React application.")

# Mascot showcase
col1, col2 = st.columns(2)

with col1:
    st.subheader("Coin Mascot")
    st.markdown(load_mascot_animation("coin"), unsafe_allow_html=True)
    st.markdown("""
    The Coin Mascot features:
    - Bouncing animation
    - Rotating 3D effect
    - Dollar sign that pulses
    - Shadow that scales with the bounce
    """)

with col2:
    st.subheader("Piggy Bank Mascot")
    st.markdown(load_mascot_animation("piggy"), unsafe_allow_html=True)
    st.markdown("""
    The Piggy Bank Mascot features:
    - Wiggling animation
    - Blinking eyes
    - Coins dropping into the slot
    - Cute design appealing to younger users
    """)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Chart Mascot")
    st.markdown(load_mascot_animation("chart"), unsafe_allow_html=True)
    st.markdown("""
    The Chart Mascot features:
    - Growing bar chart columns
    - Trend dots
    - Pulsing animation
    - Upward arrow indicating growth
    """)

with col4:
    st.subheader("Rocket Mascot")
    st.markdown(load_mascot_animation("rocket"), unsafe_allow_html=True)
    st.markdown("""
    The Rocket Mascot features:
    - Up and down hovering animation
    - Flame effect with particles
    - Dollar sign symbolizing financial growth
    - Modern design for GenZ appeal
    """)

# Example loading screen
st.header("Full LoadingScreen Component")
st.markdown("""
This is how the LoadingScreen component looks in the React application. It includes:

- An animated financial mascot character (coin, piggy bank, chart, or rocket)
- A customizable loading message
- Animated loading dots
- A random financial tip that changes each time
- Color themes (primary, success, warning, danger)
- Minimum display time setting to prevent flickering
""")

st.markdown("""
### Code example for using the LoadingScreen:
```jsx
// Import the component
import { LoadingScreen } from './components';

// Use in your component
function MyComponent() {
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Simulate data loading
    setTimeout(() => {
      setLoading(false);
    }, 3000);
  }, []);
  
  return (
    <>
      <LoadingScreen 
        show={loading}
        message="Preparing your financial dashboard..." 
        theme="primary"
        mascotType="rocket"
        minDisplayTime={2000}
      />
      
      {!loading && (
        <div>Your component content here</div>
      )}
    </>
  );
}
```
""")

st.info("These animations add a fun, engaging element to the FinBuddy app, making the loading experience more enjoyable for GenZ users while reinforcing the financial theme of the application.")