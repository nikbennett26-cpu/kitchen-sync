import streamlit as st
import random
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Fridge Raider Pro",
    page_icon="🧊",
    layout="wide"
)

# --- 2. THE DESIGN SYSTEM (Mesh Gradient + Glassmorphism) ---
st.markdown("""
    <style>
    /* 1. APP BACKGROUND (Animated Mesh Gradient) */
    .stApp {
        background-color: #0f172a;
        background-image: 
            radial-gradient(at 10% 10%, #4c1d95 0px, transparent 50%),
            radial-gradient(at 90% 90%, #1e40af 0px, transparent 50%),
            radial-gradient(at 50% 50%, #be185d 0px, transparent 50%);
        background-size: 150% 150%;
        animation: gradient-animation 15s ease infinite;
    }

    @keyframes gradient-animation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 2. TEXT STYLING (Make everything White/Readable) */
    h1, h2, h3, h4, h5, p, div, span, label {
        color: #ffffff !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.3);
    }
    
    /* 3. GLASSMORPHISM (Sidebar & Containers) */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.2) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Style the Expanders (Recipe details) to look like glass cards */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px;
    }
    
    /* 4. CUSTOM METRICS (Streak/Coins) */
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        color: #fbbf24 !important; /* Gold color for numbers */
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE (Gamification Features) ---
if 'streak' not in st.session_state:
    st.session_state.streak = 12
if 'points' not in st.session_state:
    st.session_state.points = 450
if 'cooked_today' not in st.session_state:
    st.session_state.cooked_today = False

def cook_recipe():
    if not st.session_state.cooked_today:
        st.session_state.points += 50
        st.session_state.streak += 1
        st.session_state.cooked_today = True
        st.toast("🍳 Yummy! +50 Cooking Points!", icon="🔥")
    else:
        st.toast("You already cooked today!", icon="✅")

# --- 4. DATA (Your Recipes) ---
recipes = [
    {
        "name": "Classic Omelette 🍳",
        "ingredients": {"eggs", "cheese", "butter", "salt"},
        "instructions": "Whisk eggs, melt butter, cook until fluffy, add cheese.",
        "image": "https://images.unsplash.com/photo-1510693206972-df098062cb71?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Fluffy Pancakes 🥞",
        "ingredients": {"eggs", "milk", "flour", "butter", "sugar"},
        "instructions": "Mix dry and wet ingredients separately, combine, and fry in butter.",
        "image": "
