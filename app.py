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
        "image": "