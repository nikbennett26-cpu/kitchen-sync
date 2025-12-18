import streamlit as st
import re

# --- PAGE CONFIG ---
st.set_page_config(page_title="Kitchen Sync", layout="wide", page_icon="🔄")

# --- THEME MANAGEMENT ---
with st.sidebar:
    st.title("🔄 Kitchen Sync")
    st.caption("Get in sync with your ingredients.")
    st.write("---")
    dark_mode = st.toggle("🌙 Dark Mode", value=False)

# --- CSS INJECTION ---
# We use one giant block to ensure variables match the selected mode

if dark_mode:
    # --- DARK MODE STYLES ---
    page_bg = "#0e1117"
    card_bg = "linear-gradient(145deg, #1e2329, #161b22)"
    text_color = "#f0f2f6"
    card_border = "1px solid rgba(255,255,255,0.08)"
    card_shadow = "5px 5px 15px #0b0d10, -5px -5px 15px #222831"
    tab_active_bg = "linear-gradient(90deg, #2563eb, #0d9488)"
    tab_text = "#9ca3af"
    tab_active_text = "#ffffff"
else:
    # --- LIGHT MODE STYLES ---
    page_bg = "#f3f4f6"
    card_bg = "linear-gradient(145deg, #ffffff, #f0f0f0)"
    text_color = "#1f2937"
    card_border = "1px solid #ffffff"
    card_shadow = "5px 5px 10px #d1d5db, -5px -5px 10px #ffffff"
    tab_active_bg = "linear-gradient(90deg, #0d9488, #2563eb)"
    tab_text = "#64748b"
    tab_active_text = "#ffffff"

st.markdown(f"""
<style>
    /* 1. APP BACKGROUND & TEXT */
    .stApp {{
        background-color: {page_bg} !important;
    }}
    h1, h2, h3, h4, h5, h6, p, div, span, label, li, textarea, .stMarkdown {{
        color: {text_color} !important;
        font-family: 'Inter', sans-serif;
    }}

    /* 2. SIDEBAR */
    section[data-testid="stSidebar"] {{
        background-color: {page_bg} !important;
        border-right: 1px solid rgba(150,150,150, 0.1);
    }}
    
    /* 3. INPUT TEXT AREA */
    .stTextArea textarea {{
        background-color: rgba(150,150,150, 0.1) !important;
        color: {text_color} !important;
        border: 1px solid rgba(150,150,150, 0.2);
        border-radius: 10px;
    }}

    /* 4. TABS (The Pill Design - NO RED LINE) */
    
    /* Hide the default highlight line */
    div[data-baseweb="tab-highlight"] {{
        display: none !important;
    }}
    div[data-baseweb="tab-border"] {{
        display: none !important;
    }}
    
    /* Style the tab buttons */
    button[data-baseweb="tab"] {{
        background-color: rgba(150,150,150, 0.1) !important;
        border-radius: 20px !important;
        margin-right: 8px !important;
        padding: 4px 16px !important;
        color: {tab_text} !important;
        border: none !important;
        font-weight: 600 !important;
    }}
    
    /* Active Tab Style */
    button[data-baseweb="tab"][aria-selected="true"] {{
        background: {tab_active_bg} !important;
        color: {tab_active_text} !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }}

    /* 5. 3D CARDS */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: {card_bg} !important;
        border: {card_border} !important;
        border-radius: 20px !important;
        padding: 20px !important;
        box-shadow: {card_shadow} !important;
        margin-bottom: 20px;
        transition: transform 0.2s ease;
    }}
    
    [data-testid="stVerticalBlockBorderWrapper"]:hover {{
        transform: translateY(-5px);
    }}
    
    /* 6. BADGES */
    .have-tag {{
        background-color: #10b981; 
        color: white !important; 
        padding: 4px 10px;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.8rem;
        display: inline-block;
        margin: 2px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }}
    
    .missing-tag {{
        background-color: rgba(150,150,150, 0.2);
        color: {text_color} !important;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        display: inline-block;
        margin: 2px;
        opacity: 0.7;
    }}
    
    .sidebar-tag {{
        background-color: #3b82f6; 
        color: white !important; 
        padding: 4px 10px;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.85rem;
        display: inline-block;
        margin: 4px 2px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }}
    
    /* 7. TITLE STYLING */
    h3 {{
        margin-top: 0 !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }}
    
    /* 8. HIDE EXPANDER BORDERS */
    .streamlit-expanderHeader {{
        background-color: transparent !important;
        border: none !important;
    }}
    [data-testid="stExpander"] {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

</style>
""", unsafe_allow_html=True)


# --- MAIN CONTENT ---
st.title("Kitchen Sync")
st.markdown("### 🍳 Everything but the... waste.")
st.write("Enter the ingredients you already have at home, and we'll find the perfect recipe for you.")

# --- LOGIC ---
NON_VEGAN_ITEMS = {
    "eggs", "cheese", "butter", "milk", "chicken", "beef", "bacon", "tuna", 
    "salmon", "shrimp", "honey", "cream cheese", "yogurt", "mayo", "ground beef", 
    "parmesan", "mozzarella", "feta"
}

# --- THE RECIPE DATABASE ---
recipes = [
    # --- 1. EMPTY FRIDGE / PANTRY STAPLES ---
    {
        "name": "Beans on Toast 🇬🇧",
        "ingredients": {"bread", "baked beans", "butter"},
        "instructions": "Toast the bread. Microwave or heat beans on stove. Butter toast heavily. Pour beans over.",
        "time": "5 mins", "one_pot": True
    },
    {
        "name": "Cheese Quesadilla 🧀",
        "ingredients": {"tortilla", "cheese", "butter"},
        "instructions": "Melt butter in pan. Add tortilla. Sprinkle cheese. Fold in half. Cook until crispy and melted.",
        "time": "5 mins", "one_pot": True
    },
    {
        "name": "Tuna Pasta 🐟",
        "ingredients": {"pasta", "tuna", "mayo", "corn", "black pepper"},
        "instructions": "Boil pasta. Drain. Mix in canned tuna, mayo, and corn while hot. Season generously.",
        "time": "12 mins", "one_pot": True
    },
    {
        "name": "Jacket Potato 🥔",
        "ingredients": {"potatoes", "butter", "cheese", "salt", "pepper"},
        "instructions": "Prick potato. Microwave 5-8 mins until soft. Cut open, fluff inside, add butter and cheese.",
        "time": "10 mins", "one_pot": True
    },
    {
        "name": "Cinnamon Sugar Toast 🍞",
        "ingredients": {"bread", "butter", "sugar", "cinnamon"},
        "instructions": "Toast bread. Butter immediately. Sprinkle heavily with sugar and cinnamon mix.",
        "time": "3 mins", "one_pot": True
    },
    {
        "name": "Peanut Butter & Banana 🍌",
        "ingredients": {"bread", "peanut butter", "banana"},
        "instructions": "Toast bread. Spread peanut butter. Top with sliced banana. Optional: Drizzle honey.",
        "time": "3 mins", "one_pot": True
    },
    {
        "name": "Buttered Sweet Corn 🌽",
        "ingredients": {"corn", "butter", "salt", "pepper"},
        "instructions": "Boil or steam corn. Toss generously with butter, salt, and pepper.",
        "time": "10 mins", "one_pot": True
    },
    {
        "name": "Cheesy Rice 🍚",
        "ingredients": {"rice", "cheese", "butter", "milk", "salt"},
        "instructions": "Mix hot cooked rice with butter, milk, and cheese until melted and creamy.",
        "time": "20 mins", "one_pot": True
    },
    {
        "name": "Egg in a Hole 🍞",
        "ingredients": {"bread", "eggs", "butter", "salt"},
        "instructions": "Cut a hole in the bread. Fry bread in butter. Crack egg into the hole. Cook until set.",
        "time": "10 mins", "one_pot": True
    },
    {
        "name": "Garlic Sautéed Mushrooms 🍄",
        "ingredients": {"mushrooms", "butter", "garlic", "soy sauce", "parsley"},
        "instructions": "Sauté mushrooms in butter until browned. Add garlic and soy sauce. Cook 2 mins.",
        "time": "12 mins", "one_pot": True
    },
    {
        "name": "Pasta Aglio e Olio 🍝",
        "ingredients": {"pasta", "olive oil", "garlic", "chili flakes", "parsley"},
        "instructions": "Sauté garlic and chili in generous oil. Toss with cooked pasta and pasta water.",
        "time": "15 mins", "one_pot": False
    },
     {
        "name": "Tomato & Onion Scramble 🍳",
        "ingredients": {"eggs", "tomato", "onion", "butter", "salt"},
        "instructions": "Sauté onion and tomato in butter. Add beaten eggs and scramble until cooked.",
        "time": "10 mins", "one_pot": True
    },

    # --- 2. VEGAN SPECIALS 🌱 ---
    {
        "name": "Spicy Peanut Noodles 🍜",
        "ingredients": {"pasta", "peanut butter", "soy sauce", "garlic", "chili flakes", "lime"},
        "instructions": "Boil pasta. Mix peanut butter, soy sauce, garlic, chili, lime, and a splash of pasta water. Toss.",
        "time": "15 mins", "one_pot": False
    },
    {
        "name": "Lentil Soup 🥣",
        "ingredients": {"lentils", "carrots", "onion", "vegetable broth", "garlic", "spinach"},
        "instructions": "Sauté veggies. Add lentils and broth. Simmer 20 mins until soft. Stir in spinach.",
        "time": "30 mins", "one_pot": True
    },
    {
        "name": "Chickpea Smash Sandwich 🥪",
        "ingredients": {"chickpeas", "avocado", "lemon", "bread", "onion", "salt"},
        "instructions": "Mash chickpeas and avocado together with lemon and onion. Spread on toasted bread.",
        "time": "10 mins", "one_pot": False
    },
    {
        "name": "Black Bean Tacos 🌮",
        "ingredients": {"black beans", "corn", "tortilla", "avocado", "salsa", "lime"},
        "instructions": "Warm beans and corn. Fill tortillas. Top with avocado slices, salsa, and lime juice.",
        "time": "15 mins", "one_pot": True
    },
    {
        "name": "Roasted Veggie Bowl 🥗",
        "ingredients": {"sweet potato", "broccoli", "rice", "olive oil", "tahini", "lemon"},
        "instructions": "Roast veggies at 400F. Serve over rice. Drizzle with tahini mixed with lemon.",
        "time": "35 mins", "one_pot": False
    },
    {
        "name": "Garlic Green Beans 🥒",
        "ingredients": {"green beans", "olive oil", "garlic", "lemon", "almonds"},
        "instructions": "Blanch beans. Sauté garlic in oil. Toss beans in mix. Top with lemon/almonds.",
        "time": "15 mins", "one_pot": True
    },
    {
        "name": "Crispy Potato Wedges 🥔",
        "ingredients": {"potatoes", "oil", "paprika", "salt", "garlic"},
        "instructions": "Cut potatoes into wedges. Toss with oil and spices. Bake 400F for 30-35 mins.",
        "time": "40 mins", "one_pot": True
    },
    {
        "name": "Roasted Butternut Squash 🍠",
        "ingredients": {"butternut squash", "olive oil", "cinnamon", "maple syrup", "salt"},
        "instructions": "Cube squash. Toss with oil, cinnamon, syrup, salt. Roast 400F for 30 mins.",
        "time": "35 mins", "one_pot": True
    },

    # --- 3. THE CLASSICS (Vegetarian & Meat) ---
    {
        "name": "Roasted Brussels Sprouts 🥬",
        "ingredients": {"brussels sprouts", "olive oil", "balsamic vinegar", "honey", "salt"},
        "instructions": "Halve sprouts. Toss with oil, balsamic, honey, salt. Roast 400F for 20-25 mins until crispy.",
        "time": "30 mins", "one_pot": True
    },
    {
        "name": "Kale & Apple Salad 🥗",
        "ingredients": {"kale", "apple", "walnuts", "lemon", "olive oil", "parmesan"},
        "instructions": "Massage kale with oil/lemon. Toss with sliced apples, toasted walnuts, and shaved parm.",
        "time": "15 mins", "one_pot": False
    },
    {
        "name": "Cabbage Stir Fry 🥬",
        "ingredients": {"cabbage", "soy sauce", "garlic", "ginger", "sesame oil", "carrot"},
        "instructions": "Sauté garlic/ginger. Add shredded cabbage and carrot. Stir fry 5 mins. Finish with soy sauce/sesame oil.",
        "time": "15 mins", "one_pot": True
    },
    {
        "name": "Spinach Chickpea Curry 🥘",
        "ingredients": {"spinach", "chickpeas", "coconut milk", "curry paste", "onion", "tomato"},
        "instructions": "Sauté onion. Add curry paste/tomatoes. Add chickpeas/milk. Simmer. Stir in spinach at the end.",
        "time": "25 mins", "one_pot": True
    },
    {
        "name": "Honey Glazed Carrots 🥕",
        "ingredients": {"carrots", "honey", "butter", "parsley", "salt"},
        "instructions": "Boil carrots until tender. Drain. Toss in pan with melted butter and honey. Top with parsley.",
        "time": "20 mins", "one_pot": True
    },
    {
        "name": "Stuffed Mushrooms 🍄",
        "ingredients": {"mushrooms", "cream cheese", "garlic", "spinach", "breadcrumbs"},
        "instructions": "Remove stems. Mix cream cheese, garlic, chopped spinach. Fill caps. Top with breadcrumbs. Bake 375F for 20m.",
        "time": "30 mins", "one_pot": True
    },
    {
        "name": "Corn & Tomato Salad 🌽",
        "ingredients": {"corn", "tomato", "onion", "basil", "olive oil", "lime"},
        "instructions": "Combine corn, diced tomato, onion, basil. Dress with olive oil and lime juice.",
        "time": "10 mins", "one_pot": False
    },
    {
        "name": "Broccoli Cheddar Soup 🥦",
        "ingredients": {"broccoli", "cheese", "milk", "broth", "onion", "flour"},
        "instructions": "Sauté onion. Add flour/milk/broth to thicken. Add broccoli, simmer until soft. Stir in cheese.",
        "time": "25 mins", "one_pot": True
    },
    {
        "name": "Classic Omelette 🍳",
        "ingredients": {"eggs", "cheese", "butter", "salt"},
        "instructions": "Whisk eggs, melt butter, cook until fluffy, add cheese.",
        "time": "10 mins", "one_pot": True
    },
    {
        "name": "Fluffy Pancakes 🥞",
        "ingredients": {"eggs", "milk", "flour", "butter", "sugar"},
        "instructions": "Mix dry and wet ingredients separately, combine, and fry in butter.",
        "time": "20 mins", "one_pot": True
    },
    {
        "name": "French Toast 🍞",
        "ingredients": {"bread", "eggs", "milk", "cinnamon", "butter"},
        "instructions": "Dip bread in egg/milk mix, fry in butter until golden brown.",
        "time": "15 mins", "one_pot": True
    },
    {
        "name": "Oatmeal Bowl 🥣",
        "ingredients": {"oats", "milk", "honey", "banana", "cinnamon"},
        "instructions": "Cook oats in milk, top with sliced banana and honey.",
        "time": "10 mins", "one_pot": True
    },
    {
        "name": "Avocado Toast with Egg 🥑",
        "ingredients": {"bread", "avocado", "eggs", "chili flakes", "lemon"},
        "instructions": "Toast bread, smash avocado with lemon. Top with fried/poached egg and chili.",
        "time": "10 mins", "one_pot": True
    },
    {
        "name": "Veggie Breakfast Hash 🥔",
        "ingredients": {"potatoes", "bell pepper", "onion", "eggs", "oil"},
        "instructions": "Dice potatoes, peppers, and onions. Fry until soft/crispy. Crack eggs on top and steam until set.",
        "time": "25 mins", "one_pot": True
    },
    {
        "name": "Grilled Cheese Sandwich 🥪",
        "ingredients": {"bread", "cheese", "butter"},
        "instructions": "Butter bread, place cheese inside, grill until golden.",
        "time": "10 mins", "one_pot": True
    },
    {
        "name": "BLT Sandwich 🥓",
        "ingredients": {"bread", "bacon", "lettuce", "tomato", "mayo"},
        "instructions": "Cook bacon, toast bread, layer ingredients with mayo.",
        "time": "15 mins", "one_pot": True
    },
    {
        "name": "Classic Tuna Salad 🐟",
        "ingredients": {"tuna", "mayo", "onion", "celery", "bread"},
        "instructions": "Mix tuna, mayo, diced onion and celery. Serve on bread or lettuce.",
        "time": "10 mins", "one_pot": False
    },
    {
        "name": "Caesar Salad 🥗",
        "ingredients": {"lettuce", "croutons", "parmesan", "chicken", "dressing"},
        "instructions": "Toss lettuce with dressing, top with grilled chicken and croutons.",
        "time": "20 mins", "one_pot": False
    },
    {
        "name": "Greek Salad 🇬🇷",
        "ingredients": {"cucumber", "tomato", "feta", "olives", "onion", "olive oil"},
        "instructions": "Chop veggies roughly. Toss with olive oil and top with block of feta.",
        "time": "15 mins", "one_pot": False
    },
    {
        "name": "Caprese Salad 🇮🇹",
        "ingredients": {"tomato", "mozzarella", "basil", "olive oil", "balsamic vinegar"},
        "instructions": "Slice tomatoes and cheese, arrange with basil, drizzle with oil.",
        "time": "10 mins", "one_pot": False
    },
    {
        "name": "Hummus & Veggies 🥕",
        "ingredients": {"chickpeas", "lemon", "garlic", "olive oil", "tahini", "carrots"},
        "instructions": "Blend chickpeas, lemon, garlic, tahini and oil. Serve with carrot sticks.",
        "time": "15 mins", "one_pot": False
    },
    {
        "name": "Quinoa Salad 🥣",
        "ingredients": {"quinoa", "cucumber", "tomato", "lemon", "feta", "parsley"},
        "instructions": "Cook quinoa. Mix with chopped veggies, crumbled feta, lemon juice and herbs.",
        "time": "20 mins", "one_pot": True
    },
    {
        "name": "Zucchini Fritters 🥒",
        "ingredients": {"zucchini", "flour", "eggs", "cheese", "garlic", "oil"},
        "instructions": "Grate zucchini and squeeze out water. Mix with flour, egg, cheese. Fry spoonfuls in oil until crispy.",
        "time": "25 mins", "one_pot": True
    },
    {
        "name": "Tomato Pasta 🍝",
        "ingredients": {"pasta", "tomato sauce", "garlic", "olive oil"},
        "instructions": "Boil pasta, sauté garlic in oil, add sauce, mix.",
        "time": "15 mins", "one_pot": False
    },
    {
        "name": "Pesto Pasta 🍃",
        "ingredients": {"pasta", "pesto", "parmesan", "cherry tomatoes"},
        "instructions": "Boil pasta. Save some pasta water. Toss pasta with pesto and a splash of water. Top with tomatoes.",
        "time": "15 mins", "one_pot": False
    },
    {
        "name": "Garlic Butter Shrimp 🍤",
        "ingredients": {"shrimp", "butter", "garlic", "lemon", "parsley"},
        "instructions": "Sauté garlic in butter. Add shrimp, cook 3 mins. Finish with lemon/parsley.",
        "time": "15 mins", "one_pot": True
    },
    {
        "name": "Chicken Stir Fry 🥡",
        "ingredients": {"chicken", "rice", "soy sauce", "vegetables", "oil"},
        "instructions": "Cook chicken, add veggies, stir in sauce, serve over rice.",
        "time": "25 mins", "one_pot": True
    },
    {
        "name": "Tofu Stir Fry 🥦",
        "ingredients": {"tofu", "soy sauce", "ginger", "garlic", "broccoli", "rice"},
        "instructions": "Press tofu, cube, and fry. Remove. Fry aromatics and broccoli. Combine with sauce over rice.",
        "time": "30 mins", "one_pot": True
    },
    {
        "name": "Beef & Broccoli 🥦",
        "ingredients": {"beef", "broccoli", "soy sauce", "garlic", "rice", "sugar"},
        "instructions": "Sear beef strips. Steam broccoli. Toss both in soy/garlic/sugar sauce. Serve over rice.",
        "time": "25 mins", "one_pot": True
    },
    {
        "name": "Spaghetti Carbonara 🇮🇹",
        "ingredients": {"pasta", "eggs", "cheese", "bacon", "black pepper"},
        "instructions": "Boil pasta. Fry bacon. Mix eggs and cheese. Toss hot pasta with egg mix (off heat).",
        "time": "20 mins", "one_pot": False
    },
    {
        "name": "Simple Tacos 🌮",
        "ingredients": {"tortilla", "ground beef", "cheese", "lettuce", "salsa"},
        "instructions": "Cook meat, fill tortillas, top with cheese and salsa.",
        "time": "20 mins", "one_pot": True
    },
    {
        "name": "Black Bean Burrito 🌯",
        "ingredients": {"tortilla", "black beans", "rice", "cheese", "salsa", "corn"},
        "instructions": "Warm beans and corn. Layer rice, beans, corn, and cheese in tortilla. Roll and serve.",
        "time": "15 mins", "one_pot": False
    },
    {
        "name": "Chicken Curry 🍛",
        "ingredients": {"chicken", "curry paste", "coconut milk", "rice", "onion"},
        "instructions": "Fry onion and chicken, add paste, pour in milk, simmer. Serve with rice.",
        "time": "30 mins", "one_pot": True
    },
    {
        "name": "Fried Rice 🍚",
        "ingredients": {"rice", "eggs", "soy sauce", "peas", "carrots", "oil"},
        "instructions": "Fry veggies, push to side, scramble eggs, add rice and sauce, mix high heat.",
        "time": "20 mins", "one_pot": True
    },
    {
        "name": "Homemade Pizza 🍕",
        "ingredients": {"flour", "yeast", "tomato sauce", "cheese", "pepperoni"},
        "instructions": "Make dough, add sauce and toppings, bake at high heat (450F) for 12 mins.",
        "time": "45 mins", "one_pot": True
    },
    {
        "name": "Mac & Cheese 🧀",
        "ingredients": {"pasta", "cheese", "milk", "butter", "flour"},
        "instructions": "Make a roux with flour/butter, add milk to thicken, melt cheese in. Pour over cooked pasta.",
        "time": "25 mins", "one_pot": True
    },
    {
        "name": "Mushroom Risotto 🍄",
        "ingredients": {"rice", "mushrooms", "broth", "butter", "parmesan", "onion"},
        "instructions": "Sauté onions/mushrooms. Toast rice. Add broth ladle by ladle, stirring constantly.",
        "time": "40 mins", "one_pot": True
    },
    {
        "name": "Quesadillas 🧀",
        "ingredients": {"tortilla", "cheese", "chicken", "onion", "salsa"},
        "instructions": "Place cheese and chicken on tortilla, fold, fry in pan until crispy.",
        "time": "15 mins", "one_pot": True
    },
    {
        "name": "Mashed Potatoes & Chicken 🍗",
        "ingredients": {"potatoes", "butter", "milk", "chicken", "salt"},
        "instructions": "Boil and mash potatoes with butter/milk. Serve with roasted chicken.",
        "time": "45 mins", "one_pot": False
    },
    {
        "name": "Chicken Noodle Soup 🍜",
        "ingredients": {"chicken", "broth", "carrots", "celery", "pasta", "onion"},
        "instructions": "Sauté veggies. Add broth and chicken. Simmer. Add pasta near the end.",
        "time": "40 mins", "one_pot": True
    },
    {
        "name": "Baked Salmon 🐟",
        "ingredients": {"salmon", "lemon", "butter", "garlic", "herbs"},
        "instructions": "Place salmon on foil. Top with butter, garlic, lemon. Bake 400F for 12-15 mins.",
        "time": "20 mins", "one_pot": True
    },
    {
        "name": "Stuffed Bell Peppers 🫑",
        "ingredients": {"bell pepper", "ground beef", "rice", "cheese", "tomato sauce"},
        "instructions": "Hollow out peppers. Fill with cooked beef/rice/sauce mix. Top with cheese. Bake 375F for 30m.",
        "time": "45 mins", "one_pot": True
    },
    {
        "name": "Veggie Fajitas 🌮",
        "ingredients": {"bell pepper", "onion", "tortilla", "lime", "oil", "chili powder"},
        "instructions": "Slice peppers and onions. Fry in hot oil with spices. Serve in warm tortillas with lime.",
        "time": "20 mins", "one_pot": True
    },
    {
        "name": "Ratatouille 🍆",
        "ingredients": {"zucchini", "eggplant", "bell pepper", "tomato", "onion", "olive oil"},
        "instructions": "Slice all veggies into rounds. Layer in a baking dish with oil and herbs. Bake until tender.",
        "time": "50 mins", "one_pot": True
    },
    {
        "name": "Eggplant Parmesan 🍆",
        "ingredients": {"eggplant", "tomato sauce", "cheese", "flour", "oil", "parmesan"},
        "instructions": "Bread and fry eggplant slices. Layer with sauce and cheeses in dish. Bake until bubbly.",
        "time": "50 mins", "one_pot": True
    },
    {
        "name": "Roasted Cauliflower Tacos 🌮",
        "ingredients": {"cauliflower", "tortilla", "lime", "cabbage", "avocado", "oil"},
        "instructions": "Roast cauliflower florets with spices. Serve in tacos with cabbage slaw and avocado.",
        "time": "30 mins", "one_pot": True
    },
    {
        "name": "Banana Bread 🍌",
        "ingredients": {"banana", "flour", "sugar", "butter", "eggs"},
        "instructions": "Mash bananas, mix with wet then dry ingredients. Bake 350F for 60 mins.",
        "time": "70 mins", "one_pot": True
    },
    {
        "name": "Choc Chip Cookies 🍪",
        "ingredients": {"flour", "sugar", "butter", "chocolate chips", "eggs", "baking powder"},
        "instructions": "Cream butter/sugar, add eggs, mix in dry ingredients and chocolate. Bake 350F for 10m.",
        "time": "20 mins", "one_pot": True
    },
    {
        "name": "Chocolate Mug Cake ☕",
        "ingredients": {"flour", "sugar", "cocoa powder", "milk", "oil", "chocolate chips"},
        "instructions": "Mix all ingredients in a microwave-safe mug. Microwave for 60-90 seconds.",
        "time": "5 mins", "one_pot": True
    },
    {
        "name": "Guacamole & Chips 🥑",
        "ingredients": {"avocado", "onion", "tomato", "lime", "tortilla chips"},
        "instructions": "Mash avocado with lime and salt. Stir in diced onion/tomato. Serve with chips.",
        "time": "10 mins", "one_pot": False
    },
    {
        "name": "Apple Slices & Peanut Butter 🍎",
        "ingredients": {"apple", "peanut butter"},
        "instructions": "Slice apple, dip in peanut butter. Simple and healthy.",
        "time": "5 mins", "one_pot": False
    },
    {
        "name": "Deviled Eggs 🥚",
        "ingredients": {"eggs", "mayo", "mustard", "paprika"},
        "instructions": "Boil eggs, peel, halve. Mix yolks with mayo/mustard. Pipe back in. Dust paprika.",
        "time": "20 mins", "one_pot": True
    },
    {
        "name": "Sweet Potato Fries 🍟",
        "ingredients": {"sweet potato", "oil", "salt", "paprika", "cornstarch"},
        "instructions": "Cut potatoes into sticks. Toss with cornstarch, oil, spices. Bake 425F until crispy (25m).",
        "time": "35 mins", "one_pot": True
    },
    {
        "name": "Roasted Asparagus 🌿",
        "ingredients": {"asparagus", "olive oil", "lemon", "parmesan", "garlic"},
        "instructions": "Toss asparagus in oil and garlic. Roast 400F for 10-15 mins. Top with lemon/parmesan.",
        "time": "20 mins", "one_pot": True
    }
]

# --- APP LOGIC ---

all_possible_ingredients = set()
for r in recipes:
    all_possible_ingredients.update(r['ingredients'])

sorted_ingredients = sorted(list(all_possible_ingredients))

# --- SIDEBAR ---
st.sidebar.write("What do you have?")
user_input_text = st.sidebar.text_area("Type items (e.g. eggs, onions, tofu):", "eggs, cheese, butter")

# PROCESS INPUT
raw_items = re.split(r'[,\n]', user_input_text)
cleaned_items = [x.strip().lower() for x in raw_items if x.strip()]

user_fridge = set()
recognized_items = []

for item in cleaned_items:
    if item in sorted_ingredients:
        user_fridge.add(item)
        recognized_items.append(item)
    else:
        for db_item in sorted_ingredients:
            if item in db_item or db_item in item: 
                if len(item) > 3 and (item in db_item or db_item in item):
                    user_fridge.add(db_item)
                    recognized_items.append(db_item)
                    break
                elif item == db_item[:-1]:
                    user_fridge.add(db_item)
                    recognized_items.append(db_item)
                    break

if recognized_items:
    st.sidebar.write("Found ingredients:")
    tags_html = "".join([f'<span class="sidebar-tag">{ing}</span>' for ing in set(recognized_items)])
    st.sidebar.markdown(tags_html, unsafe_allow_html=True)

st.sidebar.markdown("---")
only_full_match = st.sidebar.checkbox("✅ Cook Now (Full Match)", value=False)

# --- TABS ---
st.write(" ")
tab1, tab2, tab3, tab4 = st.tabs(["🍽 All Recipes", "🌱 Vegan", "🥘 One Pot", "🥕 Simple (5-6 Ingred)"])

def render_recipes(filter_mode="all"):
    matches = []
    
    for recipe in recipes:
        required_ingredients = recipe['ingredients']
        matching_items = user_fridge.intersection(required_ingredients)
        missing_items = required_ingredients - user_fridge
        match_percent = int((len(matching_items) / len(required_ingredients)) * 100)
        
        # GLOBAL FILTER
        if only_full_match and match_percent < 100:
            continue
            
        # TAB FILTERS
        if filter_mode == "vegan":
            if not required_ingredients.isdisjoint(NON_VEGAN_ITEMS):
                continue
        elif filter_mode == "simple":
            if not (5 <= len(required_ingredients) <= 6):
                continue
        elif filter_mode == "one_pot":
            if not recipe.get("one_pot", False):
                continue
        
        if len(matching_items) >= 1:
            matches.append({
                "recipe": recipe,
                "matching_items": matching_items,
                "missing_items": missing_items,
                "match_percent": match_percent
            })
            
    matches.sort(key=lambda x: x['match_percent'], reverse=True)
    
    if not matches:
        st.info("No recipes found in this category with your current ingredients!")
        return

    col1, col2 = st.columns(2)
    for i, item in enumerate(matches):
        recipe = item['recipe']
        ing_count = len(recipe['ingredients'])
        
        with (col1 if i % 2 == 0 else col2):
            with st.container(border=True):
                st.subheader(recipe['name'])
                st.caption(f"⏱️ {recipe.get('time', '--')}")
                
                if item['match_percent'] == 100:
                    st.progress(item['match_percent'], text="🔥 Perfect Match!")
                else:
                    st.progress(item['match_percent'], text=f"{item['match_percent']}% Match")
                
                st.write("**You have:**")
                have_html = "".join([f'<span class="have-tag">✔ {ing}</span>' for ing in item['matching_items']])
                st.markdown(have_html, unsafe_allow_html=True)
                
                if item['missing_items'] and not only_full_match:
                    st.write("**You need:**")
                    missing_html = "".join([f'<span class="missing-tag">{ing}</span>' for ing in item['missing_items']])
                    st.markdown(missing_html, unsafe_allow_html=True)
                
                if item['match_percent'] == 100:
                     st.success("✅ Ready to cook!")

                with st.expander("📝 View Instructions"):
                    st.write(recipe['instructions'])

# Render content
with tab1: render_recipes("all")
with tab2: render_recipes("vegan")
with tab3: render_recipes("one_pot")
with tab4: render_recipes("simple")
