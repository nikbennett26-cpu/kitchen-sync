import streamlit as st

st.title("🧊 Fridge Raider v2")
st.write("Select the ingredients you have, and I'll tell you what to cook!")

# 1. The Database (Now with Images!)
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
        "image": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=400&q=80"# 2. Sidebar Setup
all_possible_ingredients = set()
for r in recipes:
    all_possible_ingredients.update(r['ingredients'])

sorted_ingredients = sorted(list(all_possible_ingredients))

st.sidebar.header("Your Fridge")
user_ingredients = st.sidebar.multiselect(
    "Select what you have:", 
    options=sorted_ingredients,
    default=["eggs", "cheese", "butter"]
)

user_fridge = set(user_ingredients)

# 3. Logic & Display
st.header("Recommended Recipes:")
col1, col2 = st.columns(2) # Create a 2-column layout for a nicer look

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
            
            # Missing Ingredients Logic
            missing = required_ingredients - user_fridge
            
            if not missing:
                st.success("✅ You have everything!")
                with st.expander("View Instructions"):
                    st.write(recipe['instructions'])
            else:
                # Calculate simple percentage match
                match_percent = int((len(matching_items) / len(required_ingredients)) * 100)
                st.progress(match_percent, text=f"{match_percent}% Match")
                
                st.error(f"Missing: {', '.join(missing)}")
                
                # Shopping List Feature
                if st.checkbox(f"Add missing items to list for {recipe['name']}", key=recipe['name']):
                    st.sidebar.info(f"🛒 Buy: {', '.join(missing)}")

if not found_match:
    st.warning("No matches yet! Try selecting 'eggs' or 'pasta' in the sidebar.")