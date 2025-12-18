import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="Fridge Raider v3 Pro", layout="wide")

# --- PROFESSIONAL CSS (MOBILE FIX: DARK MENU / WHITE TEXT) ---
st.markdown("""
<style>
    /* 1. FORCE LIGHT MODE */
    :root { color-scheme: light; }
    
    /* 2. MAIN BACKGROUND */
    .stApp { background-color: #f3f4f6 !important; }

    /* 3. TEXT COLOR */
    h1, h2, h3, h4, h5, h6, p, div, span, label, li {
        color: #1f2937 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* 4. SIDEBAR */
    section[data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e5e7eb; }
    
    /* --- 5. MOBILE DROPDOWN FIX --- */
    div[data-baseweb="popover"], div[data-baseweb="popover"] > div { background-color: #111111 !important; border: 1px solid #333333 !important; }
    ul[data-baseweb="menu"] { background-color: #111111 !important; }
    li[data-baseweb="option"] { background-color: #111111 !important; color: #ffffff !important; }
    li[data-baseweb="option"] span { color: #ffffff !important; }
    li[data-baseweb="option"]:hover, li[data-baseweb="option"][aria-selected="true"] { background-color: #2563eb !important; color: #ffffff !important; }
    div[data-baseweb="select"] > div { background-color: #ffffff !important; color: #1f2937 !important; border: 1px solid #d1d5db; }
    div[data-baseweb="select"] svg { fill: #6b7280 !important; }

    /* 6. TAB STYLING */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 10px 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e5e7eb;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563eb !important;
        color: white !important;
    }

    /* 7. HEADER */
    h1 {
        background: -webkit-linear-gradient(45deg, #2563eb, #9333ea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 3rem !important;
        padding-bottom: 10px;
    }

    /* 8. TAGS */
    .have-tag { background-color: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 15px; font-size: 0.85rem; font-weight: 600; display: inline-block; margin: 2px; border: 1px solid #86efac; }
    .missing-tag { background-color: #f3f4f6; color: #6b7280; padding: 4px 10px; border-radius: 15px; font-size: 0.85rem; display: inline-block; margin: 2px; border: 1px dashed #d1d5db; }
    
    /* SIDEBAR TAGS */
    span[data-baseweb="tag"] { background-color: #eff6ff !important; border: 1px solid #bfdbfe; }
    span[data-baseweb="tag"] span { color: #1e40af !important; }
    
    /* EXPANDER */
    .streamlit-expanderHeader { background-color: #ffffff !important; color: #1f2937 !important; border: 1px solid #e5e7eb; }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.title("Fridge Raider v3 Pro")
st.markdown("### 🍳 Your Personal AI Chef")
st.write("Stop wasting food. Select your ingredients, and let's cook something amazing.")

# --- SMART VEGAN LOGIC ---
NON_VEGAN_ITEMS = {
    "eggs", "cheese", "butter", "milk", "chicken", "beef", "bacon", "tuna", 
    "salmon", "shrimp", "honey", "cream cheese", "yogurt", "mayo", "ground beef", 
    "parmesan", "mozzarella", "feta"
}

# --- THE RECIPE DATABASE ---
recipes = [
    # --- VEGAN SPECIALS 🌱 ---
    {
        "name": "Spicy Peanut Noodles 🍜",
        "ingredients": {"pasta", "peanut butter", "soy sauce", "garlic", "chili flakes", "lime"},
        "instructions": "Boil pasta. Mix peanut butter, soy sauce, garlic, chili, lime, and a splash of pasta water. Toss.",
        "image": "https://images.unsplash.com/photo-1552611052-33e04de081de?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Lentil Soup 🥣",
        "ingredients": {"lentils", "carrots", "onion", "vegetable broth", "garlic", "spinach"},
        "instructions": "Sauté veggies. Add lentils and broth. Simmer 20 mins until soft. Stir in spinach.",
        "image": "https://images.unsplash.com/photo-1547592166-23acbe346499?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Chickpea Smash Sandwich 🥪",
        "ingredients": {"chickpeas", "avocado", "lemon", "bread", "onion", "salt"},
        "instructions": "Mash chickpeas and avocado together with lemon and onion. Spread on toasted bread.",
        "image": "https://images.unsplash.com/photo-1539252554453-1f958b22e70b?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Black Bean Tacos 🌮",
        "ingredients": {"black beans", "corn", "tortilla", "avocado", "salsa", "lime"},
        "instructions": "Warm beans and corn. Fill tortillas. Top with avocado slices, salsa, and lime juice.",
        "image": "https://images.unsplash.com/photo-1504544750208-dc0358e63f7f?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Roasted Veggie Bowl 🥗",
        "ingredients": {"sweet potato", "broccoli", "rice", "olive oil", "tahini", "lemon"},
        "instructions": "Roast veggies at 400F. Serve over rice. Drizzle with tahini mixed with lemon.",
        "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Garlic Green Beans 🥒",
        "ingredients": {"green beans", "olive oil", "garlic", "lemon", "almonds"},
        "instructions": "Blanch beans. Sauté garlic in oil. Toss beans in mix. Top with lemon/almonds.",
        "image": "https://images.unsplash.com/photo-1550951478-439401777596?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Crispy Potato Wedges 🥔",
        "ingredients": {"potatoes", "oil", "paprika", "salt", "garlic"},
        "instructions": "Cut potatoes into wedges. Toss with oil and spices. Bake 400F for 30-35 mins.",
        "image": "https://images.unsplash.com/photo-1630431341973-02e1b40a0f05?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Roasted Butternut Squash 🍠",
        "ingredients": {"butternut squash", "olive oil", "cinnamon", "maple syrup", "salt"},
        "instructions": "Cube squash. Toss with oil, cinnamon, syrup, salt. Roast 400F for 30 mins.",
        "image": "https://images.unsplash.com/photo-1576092794353-91c271811e51?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Pasta Aglio e Olio 🍝",
        "ingredients": {"pasta", "olive oil", "garlic", "chili flakes", "parsley"},
        "instructions": "Sauté garlic and chili in generous oil. Toss with cooked pasta and pasta water.",
        "image": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&fit=crop&w=600&q=80"
    },

    # --- VEGETARIAN / PANTRY STAPLES ---
    {
        "name": "Buttered Sweet Corn 🌽",
        "ingredients": {"corn", "butter", "salt", "pepper"},
        "instructions": "Boil or steam corn. Toss generously with butter, salt, and pepper.",
        "image": "https://images.unsplash.com/photo-1551754655-4d7862924585?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Garlic Sautéed Mushrooms 🍄",
        "ingredients": {"mushrooms", "butter", "garlic", "soy sauce", "parsley"},
        "instructions": "Sauté mushrooms in butter until browned. Add garlic and soy sauce. Cook 2 mins.",
        "image": "https://images.unsplash.com/photo-1520627581788-294084f74d0a?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Cheesy Rice 🍚",
        "ingredients": {"rice", "cheese", "butter", "milk", "salt"},
        "instructions": "Mix hot cooked rice with butter, milk, and cheese until melted and creamy.",
        "image": "https://images.unsplash.com/photo-1596560548464-f010549b84d7?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Roasted Brussels Sprouts 🥬",
        "ingredients": {"brussels sprouts", "olive oil", "balsamic vinegar", "honey", "salt"},
        "instructions": "Halve sprouts. Toss with oil, balsamic, honey, salt. Roast 400F for 20-25 mins until crispy.",
        "image": "https://images.unsplash.com/photo-1438217346858-d6529eda59bc?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Kale & Apple Salad 🥗",
        "ingredients": {"kale", "apple", "walnuts", "lemon", "olive oil", "parmesan"},
        "instructions": "Massage kale with oil/lemon. Toss with sliced apples, toasted walnuts, and shaved parm.",
        "image": "https://images.unsplash.com/photo-1551248429-40975aa4de74?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Cabbage Stir Fry 🥬",
        "ingredients": {"cabbage", "soy sauce", "garlic", "ginger", "sesame oil", "carrot"},
        "instructions": "Sauté garlic/ginger. Add shredded cabbage and carrot. Stir fry 5 mins. Finish with soy sauce/sesame oil.",
        "image": "https://images.unsplash.com/photo-1628833722230-10492cb91b97?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Spinach Chickpea Curry 🥘",
        "ingredients": {"spinach", "chickpeas", "coconut milk", "curry paste", "onion", "tomato"},
        "instructions": "Sauté onion. Add curry paste/tomatoes. Add chickpeas/milk. Simmer. Stir in spinach at the end.",
        "image": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Honey Glazed Carrots 🥕",
        "ingredients": {"carrots", "honey", "butter", "parsley", "salt"},
        "instructions": "Boil carrots until tender. Drain. Toss in pan with melted butter and honey. Top with parsley.",
        "image": "https://images.unsplash.com/photo-1582576163090-09d3b6f8a969?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Stuffed Mushrooms 🍄",
        "ingredients": {"mushrooms", "cream cheese", "garlic", "spinach", "breadcrumbs"},
        "instructions": "Remove stems. Mix cream cheese, garlic, chopped spinach. Fill caps. Top with breadcrumbs. Bake 375F for 20m.",
        "image": "https://images.unsplash.com/photo-1625944525533-473f1a3d54e7?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Corn & Tomato Salad 🌽",
        "ingredients": {"corn", "tomato", "onion", "basil", "olive oil", "lime"},
        "instructions": "Combine corn, diced tomato, onion, basil. Dress with olive oil and lime juice.",
        "image": "https://images.unsplash.com/photo-1530260626688-d482052d952a?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Broccoli Cheddar Soup 🥦",
        "ingredients": {"broccoli", "cheese", "milk", "broth", "onion", "flour"},
        "instructions": "Sauté onion. Add flour/milk/broth to thicken. Add broccoli, simmer until soft. Stir in cheese.",
        "image": "https://images.unsplash.com/photo-1605282823759-3e969d27a44f?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Classic Omelette 🍳",
        "ingredients": {"eggs", "cheese", "butter", "salt"},
        "instructions": "Whisk eggs, melt butter, cook until fluffy, add cheese.",
        "image": "https://images.unsplash.com/photo-1510693206972-df098062cb71?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Fluffy Pancakes 🥞",
        "ingredients": {"eggs", "milk", "flour", "butter", "sugar"},
        "instructions": "Mix dry and wet ingredients separately, combine, and fry in butter.",
        "image": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "French Toast 🍞",
        "ingredients": {"bread", "eggs", "milk", "cinnamon", "butter"},
        "instructions": "Dip bread in egg/milk mix, fry in butter until golden brown.",
        "image": "https://images.unsplash.com/photo-1484723091739-30a097e8f929?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Oatmeal Bowl 🥣",
        "ingredients": {"oats", "milk", "honey", "banana", "cinnamon"},
        "instructions": "Cook oats in milk, top with sliced banana and honey.",
        "image": "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Avocado Toast with Egg 🥑",
        "ingredients": {"bread", "avocado", "eggs", "chili flakes", "lemon"},
        "instructions": "Toast bread, smash avocado with lemon. Top with fried/poached egg and chili.",
        "image": "https://images.unsplash.com/photo-1525351484164-8035a4206501?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Veggie Breakfast Hash 🥔",
        "ingredients": {"potatoes", "bell pepper", "onion", "eggs", "oil"},
        "instructions": "Dice potatoes, peppers, and onions. Fry until soft/crispy. Crack eggs on top and steam until set.",
        "image": "https://images.unsplash.com/photo-1590554035658-4560b411d735?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Grilled Cheese Sandwich 🥪",
        "ingredients": {"bread", "cheese", "butter"},
        "instructions": "Butter bread, place cheese inside, grill until golden.",
        "image": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "BLT Sandwich 🥓",
        "ingredients": {"bread", "bacon", "lettuce", "tomato", "mayo"},
        "instructions": "Cook bacon, toast bread, layer ingredients with mayo.",
        "image": "https://images.unsplash.com/photo-1553909489-cd47e3faaefc?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Classic Tuna Salad 🐟",
        "ingredients": {"tuna", "mayo", "onion", "celery", "bread"},
        "instructions": "Mix tuna, mayo, diced onion and celery. Serve on bread or lettuce.",
        "image": "https://images.unsplash.com/photo-1550505393-885efce5988d?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Caesar Salad 🥗",
        "ingredients": {"lettuce", "croutons", "parmesan", "chicken", "dressing"},
        "instructions": "Toss lettuce with dressing, top with grilled chicken and croutons.",
        "image": "https://images.unsplash.com/photo-1550304943-4f24f54ddde9?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Greek Salad 🇬🇷",
        "ingredients": {"cucumber", "tomato", "feta", "olives", "onion", "olive oil"},
        "instructions": "Chop veggies roughly. Toss with olive oil and top with block of feta.",
        "image": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Caprese Salad 🇮🇹",
        "ingredients": {"tomato", "mozzarella", "basil", "olive oil", "balsamic vinegar"},
        "instructions": "Slice tomatoes and cheese, arrange with basil, drizzle with oil.",
        "image": "https://images.unsplash.com/photo-1529312266912-b33cf6227e24?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Hummus & Veggies 🥕",
        "ingredients": {"chickpeas", "lemon", "garlic", "olive oil", "tahini", "carrots"},
        "instructions": "Blend chickpeas, lemon, garlic, tahini and oil. Serve with carrot sticks.",
        "image": "https://images.unsplash.com/photo-1577906096429-f736f6f3a35d?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Quinoa Salad 🥣",
        "ingredients": {"quinoa", "cucumber", "tomato", "lemon", "feta", "parsley"},
        "instructions": "Cook quinoa. Mix with chopped veggies, crumbled feta, lemon juice and herbs.",
        "image": "https://images.unsplash.com/photo-1623428187969-5da2dcea5ebf?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Zucchini Fritters 🥒",
        "ingredients": {"zucchini", "flour", "eggs", "cheese", "garlic", "oil"},
        "instructions": "Grate zucchini and squeeze out water. Mix with flour, egg, cheese. Fry spoonfuls in oil until crispy.",
        "image": "https://images.unsplash.com/photo-1563229569-4252a1d7f02b?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Tomato Pasta 🍝",
        "ingredients": {"pasta", "tomato sauce", "garlic", "olive oil"},
        "instructions": "Boil pasta, sauté garlic in oil, add sauce, mix.",
        "image": "https://images.unsplash.com/photo-1626844131082-256783844137?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Pesto Pasta 🍃",
        "ingredients": {"pasta", "pesto", "parmesan", "cherry tomatoes"},
        "instructions": "Boil pasta. Save some pasta water. Toss pasta with pesto and a splash of water. Top with tomatoes.",
        "image": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Garlic Butter Shrimp 🍤",
        "ingredients": {"shrimp", "butter", "garlic", "lemon", "parsley"},
        "instructions": "Sauté garlic in butter. Add shrimp, cook 3 mins. Finish with lemon/parsley.",
        "image": "https://images.unsplash.com/photo-1559742811-822873691df8?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Chicken Stir Fry 🥡",
        "ingredients": {"chicken", "rice", "soy sauce", "vegetables", "oil"},
        "instructions": "Cook chicken, add veggies, stir in sauce, serve over rice.",
        "image": "https://images.unsplash.com/photo-1603133872878-684f10842619?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Tofu Stir Fry 🥦",
        "ingredients": {"tofu", "soy sauce", "ginger", "garlic", "broccoli", "rice"},
        "instructions": "Press tofu, cube, and fry. Remove. Fry aromatics and broccoli. Combine with sauce over rice.",
        "image": "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Beef & Broccoli 🥦",
        "ingredients": {"beef", "broccoli", "soy sauce", "garlic", "rice", "sugar"},
        "instructions": "Sear beef strips. Steam broccoli. Toss both in soy/garlic/sugar sauce. Serve over rice.",
        "image": "https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Spaghetti Carbonara 🇮🇹",
        "ingredients": {"pasta", "eggs", "cheese", "bacon", "black pepper"},
        "instructions": "Boil pasta. Fry bacon. Mix eggs and cheese. Toss hot pasta with egg mix (off heat).",
        "image": "https://images.unsplash.com/photo-1612874742237-6526221588e3?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Simple Tacos 🌮",
        "ingredients": {"tortilla", "ground beef", "cheese", "lettuce", "salsa"},
        "instructions": "Cook meat, fill tortillas, top with cheese and salsa.",
        "image": "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Black Bean Burrito 🌯",
        "ingredients": {"tortilla", "black beans", "rice", "cheese", "salsa", "corn"},
        "instructions": "Warm beans and corn. Layer rice, beans, corn, and cheese in tortilla. Roll and serve.",
        "image": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Chicken Curry 🍛",
        "ingredients": {"chicken", "curry paste", "coconut milk", "rice", "onion"},
        "instructions": "Fry onion and chicken, add paste, pour in milk, simmer. Serve with rice.",
        "image": "https://images.unsplash.com/photo-1631292784640-2b24be784d5d?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Fried Rice 🍚",
        "ingredients": {"rice", "eggs", "soy sauce", "peas", "carrots", "oil"},
        "instructions": "Fry veggies, push to side, scramble eggs, add rice and sauce, mix high heat.",
        "image": "https://images.unsplash.com/photo-1603133872878-684f10842619?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Homemade Pizza 🍕",
        "ingredients": {"flour", "yeast", "tomato sauce", "cheese", "pepperoni"},
        "instructions": "Make dough, add sauce and toppings, bake at high heat (450F) for 12 mins.",
        "image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Mac & Cheese 🧀",
        "ingredients": {"pasta", "cheese", "milk", "butter", "flour"},
        "instructions": "Make a roux with flour/butter, add milk to thicken, melt cheese in. Pour over cooked pasta.",
        "image": "https://images.unsplash.com/photo-1543339308-43e59d6b73a6?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Mushroom Risotto 🍄",
        "ingredients": {"rice", "mushrooms", "broth", "butter", "parmesan", "onion"},
        "instructions": "Sauté onions/mushrooms. Toast rice. Add broth ladle by ladle, stirring constantly.",
        "image": "https://images.unsplash.com/photo-1476124369491-e7addf5db371?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Quesadillas 🧀",
        "ingredients": {"tortilla", "cheese", "chicken", "onion", "salsa"},
        "instructions": "Place cheese and chicken on tortilla, fold, fry in pan until crispy.",
        "image": "https://images.unsplash.com/photo-1618040996337-56904b7850b9?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Mashed Potatoes & Chicken 🍗",
        "ingredients": {"potatoes", "butter", "milk", "chicken", "salt"},
        "instructions": "Boil and mash potatoes with butter/milk. Serve with roasted chicken.",
        "image": "https://images.unsplash.com/photo-1604908177453-7462950a6a3b?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Chicken Noodle Soup 🍜",
        "ingredients": {"chicken", "broth", "carrots", "celery", "pasta", "onion"},
        "instructions": "Sauté veggies. Add broth and chicken. Simmer. Add pasta near the end.",
        "image": "https://images.unsplash.com/photo-1547592166-23acbe346499?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Baked Salmon 🐟",
        "ingredients": {"salmon", "lemon", "butter", "garlic", "herbs"},
        "instructions": "Place salmon on foil. Top with butter, garlic, lemon. Bake 400F for 12-15 mins.",
        "image": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Stuffed Bell Peppers 🫑",
        "ingredients": {"bell pepper", "ground beef", "rice", "cheese", "tomato sauce"},
        "instructions": "Hollow out peppers. Fill with cooked beef/rice/sauce mix. Top with cheese. Bake 375F for 30m.",
        "image": "https://images.unsplash.com/photo-1529321044792-229d4c72803b?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Veggie Fajitas 🌮",
        "ingredients": {"bell pepper", "onion", "tortilla", "lime", "oil", "chili powder"},
        "instructions": "Slice peppers and onions. Fry in hot oil with spices. Serve in warm tortillas with lime.",
        "image": "https://images.unsplash.com/photo-1534353473418-4cfa6c56fd38?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Ratatouille 🍆",
        "ingredients": {"zucchini", "eggplant", "bell pepper", "tomato", "onion", "olive oil"},
        "instructions": "Slice all veggies into rounds. Layer in a baking dish with oil and herbs. Bake until tender.",
        "image": "https://images.unsplash.com/photo-1572453800999-e8d2d1589b7c?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Eggplant Parmesan 🍆",
        "ingredients": {"eggplant", "tomato sauce", "cheese", "flour", "oil", "parmesan"},
        "instructions": "Bread and fry eggplant slices. Layer with sauce and cheeses in dish. Bake until bubbly.",
        "image": "https://images.unsplash.com/photo-1625944122171-487627441584?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Roasted Cauliflower Tacos 🌮",
        "ingredients": {"cauliflower", "tortilla", "lime", "cabbage", "avocado", "oil"},
        "instructions": "Roast cauliflower florets with spices. Serve in tacos with cabbage slaw and avocado.",
        "image": "https://images.unsplash.com/photo-1596450523450-482025740441?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Banana Bread 🍌",
        "ingredients": {"banana", "flour", "sugar", "butter", "eggs"},
        "instructions": "Mash bananas, mix with wet then dry ingredients. Bake 350F for 60 mins.",
        "image": "https://images.unsplash.com/photo-1596229961623-455b768172c7?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Choc Chip Cookies 🍪",
        "ingredients": {"flour", "sugar", "butter", "chocolate chips", "eggs", "baking powder"},
        "instructions": "Cream butter/sugar, add eggs, mix in dry ingredients and chocolate. Bake 350F for 10m.",
        "image": "https://images.unsplash.com/photo-1499636138143-bd630f5cf386?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Chocolate Mug Cake ☕",
        "ingredients": {"flour", "sugar", "cocoa powder", "milk", "oil", "chocolate chips"},
        "instructions": "Mix all ingredients in a microwave-safe mug. Microwave for 60-90 seconds.",
        "image": "https://images.unsplash.com/photo-1586985289906-406988974504?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Guacamole & Chips 🥑",
        "ingredients": {"avocado", "onion", "tomato", "lime", "tortilla chips"},
        "instructions": "Mash avocado with lime and salt. Stir in diced onion/tomato. Serve with chips.",
        "image": "https://images.unsplash.com/photo-1600850056064-a8b380aff831?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Apple Slices & Peanut Butter 🍎",
        "ingredients": {"apple", "peanut butter"},
        "instructions": "Slice apple, dip in peanut butter. Simple and healthy.",
        "image": "https://images.unsplash.com/photo-1632161845691-32c0211329c4?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Deviled Eggs 🥚",
        "ingredients": {"eggs", "mayo", "mustard", "paprika"},
        "instructions": "Boil eggs, peel, halve. Mix yolks with mayo/mustard. Pipe back in. Dust paprika.",
        "image": "https://images.unsplash.com/photo-1590412200988-a436970781fa?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Sweet Potato Fries 🍟",
        "ingredients": {"sweet potato", "oil", "salt", "paprika", "cornstarch"},
        "instructions": "Cut potatoes into sticks. Toss with cornstarch, oil, spices. Bake 425F until crispy (25m).",
        "image": "https://images.unsplash.com/photo-1541280047394-4b533a6503c2?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Roasted Asparagus 🌿",
        "ingredients": {"asparagus", "olive oil", "lemon", "parmesan", "garlic"},
        "instructions": "Toss asparagus in oil and garlic. Roast 400F for 10-15 mins. Top with lemon/parmesan.",
        "image": "https://images.unsplash.com/photo-1516684669134-de6d7c47743b?auto=format&fit=crop&w=600&q=80"
    }
]

# --- APP LOGIC ---

all_possible_ingredients = set()
for r in recipes:
    all_possible_ingredients.update(r['ingredients'])

sorted_ingredients = sorted(list(all_possible_ingredients))

# --- SIDEBAR: Just the Fridge ---
st.sidebar.title("🥑 The Fridge")
st.sidebar.write("Check what you have:")
user_ingredients = st.sidebar.multiselect(
    "Ingredients:", 
    options=sorted_ingredients,
    default=["eggs", "cheese", "butter"]
)
user_fridge = set(user_ingredients)

# --- SIDEBAR: Global Cook Now ---
st.sidebar.markdown("---")
only_full_match = st.sidebar.checkbox("✅ Cook Now (Full Match)", value=False)

# --- MAIN PAGE TABS ---
st.write(" ")
tab1, tab2, tab3 = st.tabs(["🍽 All Recipes", "🌱 Vegan", "🥕 Simple (5-6 Ingred)"])

def render_recipes(filter_mode="all"):
    matches = []
    
    for recipe in recipes:
        required_ingredients = recipe['ingredients']
        matching_items = user_fridge.intersection(required_ingredients)
        missing_items = required_ingredients - user_fridge
        match_percent = int((len(matching_items) / len(required_ingredients)) * 100)
        
        # GLOBAL FILTER: Cook Now
        if only_full_match and match_percent < 100:
            continue
            
        # TAB SPECIFIC FILTERS
        if filter_mode == "vegan":
            if not required_ingredients.isdisjoint(NON_VEGAN_ITEMS):
                continue
        elif filter_mode == "simple":
            if not (5 <= len(required_ingredients) <= 6):
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
            with st.container():
                st.image(recipe['image'], use_container_width=True)
                st.subheader(recipe['name'])
                st.caption(f"{ing_count} Ingredients")
                
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
                st.markdown("---")

# Render content in tabs
with tab1:
    render_recipes("all")
with tab2:
    render_recipes("vegan")
with tab3:
    render_recipes("simple")
