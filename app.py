import streamlit as st
import random
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="My Python App",
    page_icon="🚀",
    layout="centered"
)

# --- 2. CSS INJECTION (The Mesh Gradient & Glassmorphism) ---
# We use st.markdown with unsafe_allow_html=True to inject CSS directly.
st.markdown("""
    <style>
    /* RESET & BASE */
    .stApp {
        background-color: #0f172a; /* Dark base */
    }
    
    /* THE MESH GRADIENT BACKGROUND */
    /* We attach this to the main Streamlit container */
    [data-testid="stAppViewContainer"] {
        background-color: #0f172a;
        background-image: 
            radial-gradient(at 10% 10%, #7c3aed 0px, transparent 50%),
            radial-gradient(at 90% 90%, #2563eb 0px, transparent 50%),
            radial-gradient(at 50% 50%, #db2777 0px, transparent 50%);
        background-size: 150% 150%;
        animation: gradient-animation 10s ease infinite;
    }

    @keyframes gradient-animation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* GLASSMORPHISM CARDS */
    div.css-1r6slb0, div.stButton > button {
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px;
        border: 1px solid rgba(209, 213, 219, 0.3);
        color: white !important;
    }

    /* TEXT COLORS */
    h1, h2, h3, p, span, label {
        color: white !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    
    /* INPUT FIELDS STYLING */
    input, textarea {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. APP LOGIC & FEATURES ---

# Initialize Session State for Gamification
if 'streak' not in st.session_state:
    st.session_state.streak = 3  # Fake starting streak
if 'coins' not in st.session_state:
    st.session_state.coins = 150

def claim_daily_reward():
    st.session_state.streak += 1
    st.session_state.coins += 50
    st.toast("🔥 Streak extended! +50 Coins")

# --- UI LAYOUT ---

st.title("🚀 Python Super App")
st.markdown("Welcome to your enhanced dashboard.")

# FEATURE: GAMIFICATION (Sticky Feature)
col1, col2 = st.columns(2)
with col1:
    st.metric(label="🔥 Daily Streak", value=f"{st.session_state.streak} Days")
with col2:
    st.metric(label="💰 Coins", value=st.session_state.coins, delta=50)

if st.button("Claim Daily Reward"):
    claim_daily_reward()

st.divider()

# FEATURE: TIERED ACCESS (Monetization)
st.subheader("💎 Membership Tier")
tier = st.radio("Select your plan:", ["Free", "Pro ($5/mo)", "Enterprise"], horizontal=True)

if tier == "Pro ($5/mo)":
    st.success("Pro features unlocked: Advanced Analytics enabled.")
    # Show a fake chart just for Pro users
    chart_data = [random.randint(10, 100) for _ in range(10)]
    st.line_chart(chart_data)
elif tier == "Free":
    st.info("Upgrade to Pro to see advanced analytics.")

st.divider()

# FEATURE: IN-APP FEEDBACK (Growth)
with st.expander("📢 Report a bug or suggest a feature"):
    with st.form("feedback_form"):
        text = st.text_area("What can we improve?")
        submitted = st.form_submit_button("Submit Feedback")
        if submitted:
            st.success("Thanks! We sent this directly to the dev team.")

# --- FOOTER ---
st.markdown("---")
st.caption("Built with Python & Streamlit • v2.0")
