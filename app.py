import streamlit as st

st.title("🧊 Fridge Raider v3")
st.write("Select the ingredients you have, and I'll tell you what to cook!")

# --- THE RECIPE DATABASE (20 ITEMS) ---
recipes = [
    # --- BREAKFAST ---
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
        "image": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "French Toast 🍞",
        "ingredients": {"bread", "eggs", "milk", "cinnamon", "butter"},
        "instructions": "Dip bread in egg/milk mix, fry in butter until golden brown.",
        "image": "https://images.unsplash.com/photo-1484723091739-30a097e8f929?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Oatmeal Bowl 🥣",
        "ingredients": {"oats", "milk", "honey", "banana", "cinnamon"},
        "instructions": "Cook oats in milk, top with sliced banana and honey.",
        "image": "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Fruit Smoothie 🥤",
        "ingredients": {"banana", "milk", "honey", "ice"},
        "instructions": "Blend all ingredients until smooth.",
        "image": "https://images.unsplash.com/photo-1505252585461-04db1eb84625?auto=format&fit=crop&w=400&q=80"
    },

    # --- LUNCH ---
    {
        "name": "Grilled Cheese Sandwich 🥪",
        "ingredients": {"bread", "cheese", "butter"},
        "instructions": "Butter bread, place cheese inside, grill until golden.",
        "image": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "BLT Sandwich 🥓",
        "ingredients": {"bread", "bacon", "lettuce", "tomato", "mayo"},
        "instructions": "Cook bacon, toast bread, layer ingredients with mayo.",
        "image": "https://images.unsplash.com/photo-1553909489-cd47e3faaefc?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Avocado Toast 🥑",
        "ingredients": {"bread", "avocado", "salt", "lemon", "oil"},
        "instructions": "Toast bread, smash avocado on top, season with salt and lemon.",
        "image": "https://images.unsplash.com/photo-1588137372308-15f75323a557?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Caesar Salad 🥗",
        "ingredients": {"lettuce", "croutons", "parmesan", "chicken", "dressing"},
        "instructions": "Toss lettuce with dressing, top with grilled chicken and croutons.",
        "image": "https://images.unsplash.com/photo-1550304943-4f24f54ddde9?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Caprese Salad 🇮🇹",
        "ingredients": {"tomato", "mozzarella", "basil", "oil", "balsamic"},
        "instructions": "Slice tomatoes and cheese, arrange with basil, drizzle with oil.",
        "image": "https://images.unsplash.com/photo-1529312266912-b33cf6227e24?auto=format&fit=crop&w=400&q=80"
    },

    # --- DINNER ---
    {
        "name": "Tomato Pasta 🍝",
        "ingredients": {"pasta", "tomato sauce", "garlic", "oil"},
        "instructions": "Boil pasta, sauté garlic in oil, add sauce, mix.",
        "image": "https://images.unsplash.com/photo-1626844131082-256783844137?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Chicken Stir Fry 🥡",
        "ingredients": {"chicken", "rice", "soy sauce", "vegetables", "oil"},
        "instructions": "Cook chicken, add veggies, stir in sauce, serve over rice.",
        "image": "https://images.unsplash.com/photo-1603133872878-684f10842619?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Spaghetti Carbonara 🇮🇹",
        "ingredients": {"pasta", "eggs", "cheese", "bacon", "black pepper"},
        "instructions": "Boil pasta. Fry bacon. Mix eggs and cheese. Toss hot pasta with egg mix (off heat) to create creamy sauce.",
        "image": "https://images.unsplash.com/photo-1612874742237-6526221588e3?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Simple Tacos 🌮",
        "ingredients": {"tortilla", "ground beef", "cheese", "lettuce", "salsa"},
        "instructions": "Cook meat, fill tortillas, top with cheese and salsa.",
        "image": "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Chicken Curry 🍛",
        "ingredients": {"chicken", "curry paste", "coconut milk", "rice", "onion"},
        "instructions": "Fry onion and chicken, add paste, pour in milk, simmer. Serve with rice.",
        "image": "https://images.unsplash.com/photo-1631292784640-2b24be784d5d?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Fried Rice 🍚",
        "ingredients": {"rice", "eggs", "soy sauce", "peas", "carrots", "oil"},
        "instructions": "Fry veggies, push to side, scramble eggs, add rice and sauce, mix high heat.",
        "image": "https://images.unsplash.com/photo-1603133872878-684f10842619?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Homemade Pizza 🍕",
        "ingredients": {"flour", "yeast", "tomato sauce", "cheese", "pepperoni"},
        "instructions": "Make dough, add sauce and toppings, bake at high heat (450F) for 12 mins.",
        "image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Quesadillas 🧀",
        "ingredients": {"tortilla", "cheese", "chicken", "onion", "salsa"},
        "instructions": "Place cheese and chicken on tortilla, fold, fry in pan until crispy.",
        "image": "https://images.unsplash.com/photo-1618040996337-56904b7850b9?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Mashed Potatoes & Chicken 🍗",
        "ingredients": {"potatoes", "butter", "milk", "chicken", "salt"},
        "instructions": "Boil and mash potatoes with butter/milk. Serve with roasted chicken.",
        "image": "https://images.unsplash.com/photo-1604908177453-7462950a6a3b?auto=format&fit=crop&w=400&q=80"
    },
    {
      {
        {
        "name": "Banana Bread 🍌",
        "ingredients": {"banana", "flour", "sugar", "butter", "eggs"},
        "instructions": "Mash bananas, mix with wet then dry ingredients. Bake 350F for 60 mins.",
        "image": "https://images.unsplash.com/photo-1605292356183-a77d0a9c9d1d?auto=format&fit=crop&w=400&q=80"
    
    }
]

# --- APP LOGIC ---

# 1. Setup ingredients list
all_possible_ingredients = set()
for r in recipes:
    all_possible_ingredients.update(r['ingredients'])

sorted_ingredients = sorted(list(all_possible_ingredients))

# 2. Sidebar Controls
st.sidebar.header("Your Fridge")
user_ingredients = st.sidebar.multiselect(
    "Select what you have:", 
    options=sorted_ingredients,
    default=["eggs", "cheese", "butter"]
)
user_fridge = set(user_ingredients)

# 3. Find and Display Matches
st.header("Recommended Recipes:")
col1, col2 = st.columns(2)

found_match = False

for i, recipe in enumerate(recipes):
    required_ingredients = recipe['ingredients']
    matching_items = user_fridge.intersection(required_ingredients)
    
    # Logic: Show if we have at least 1 matching ingredient
    if len(matching_items) >= 1:
        found_match = True
        
        # Display in alternating columns
        with (col1 if i % 2 == 0 else col2):
            st.image(recipe['image'], use_container_width=True)
            st.subheader(recipe['name'])
            
            missing = required_ingredients - user_fridge
            
            if not missing:
                st.success("✅ You have everything!")
                with st.expander("View Instructions"):
                    st.write(recipe['instructions'])
            else:
                match_percent = int((len(matching_items) / len(required_ingredients)) * 100)
                st.progress(match_percent, text=f"{match_percent}% Match")
                st.error(f"Missing: {', '.join(missing)}")
                
                if st.checkbox(f"Add missing items to list", key=recipe['name']):
                    st.sidebar.info(f"🛒 Buy: {', '.join(missing)}")

if not found_match:

    st.warning("No matches yet! Try selecting more ingredients.")

