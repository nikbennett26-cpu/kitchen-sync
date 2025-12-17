import streamlit as st
import streamlit.components.v1 as components

# --- 1. Set up the Streamlit Page ---
st.set_page_config(page_title="Fridge Raider", layout="wide")

# --- 2. Define the HTML/CSS/JS Logic ---
HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* --- Global Styles --- */
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
        body { background-color: #f9fafb; color: #1f2937; line-height: 1.6; }
        
        .container { max-width: 100%; margin: 0 auto; padding: 20px; }
        
        /* --- Header & Search Section --- */
        header { text-align: center; margin-bottom: 30px; padding-top: 20px; }
        h1 { font-size: 2.5rem; color: #111; margin-bottom: 10px; }
        .subtitle { color: #6b7280; font-size: 1.1rem; margin-bottom: 25px; }

        /* The Fridge Input */
        .search-container {
            max-width: 600px;
            margin: 0 auto 30px auto;
            position: relative;
        }
        
        .search-input {
            width: 100%;
            padding: 15px 25px;
            font-size: 1.2rem;
            border: 2px solid #e5e7eb;
            border-radius: 50px;
            outline: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            text-align: center;
        }
        
        .search-input:focus {
            border-color: #e63946;
            box-shadow: 0 4px 12px rgba(230, 57, 70, 0.2);
        }

        /* --- Filter Buttons --- */
        .filters { display: flex; justify-content: center; gap: 10px; margin-bottom: 40px; flex-wrap: wrap; }
        .filter-btn {
            background-color: #e5e7eb; color: #1f2937; border: none;
            padding: 10px 20px; border-radius: 50px; cursor: pointer;
            font-weight: 600; font-size: 0.9rem; transition: all 0.2s ease;
        }
        .filter-btn:hover { background-color: #d1d5db; transform: translateY(-2px); }
        .filter-btn.active { background-color: #e63946; color: white; box-shadow: 0 4px 10px rgba(230, 57, 70, 0.3); }

        /* --- Grid & Cards --- */
        .recipe-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 30px; }
        
        .recipe-card {
            background: white; border-radius: 16px; overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            display: flex; flex-direction: column;
            animation: fadeIn 0.5s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .recipe-card:hover { transform: translateY(-5px); box-shadow: 0 12px 20px rgba(0, 0, 0, 0.1); }
        
        .card-image { width: 100%; height: 200px; object-fit: cover; }
        .card-content { padding: 20px; flex-grow: 1; display: flex; flex-direction: column; }
        .recipe-title { font-size: 1.25rem; font-weight: 700; color: #111; margin-bottom: 5px; }
        
        .ingredients-match { 
            font-size: 0.85rem; color: #e63946; font-weight: 600; margin-bottom: 10px; min-height: 20px; 
        }

        .tags-container { display: flex; gap: 8px; margin-bottom: 15px; flex-wrap: wrap; }
        .tag {
            font-size: 0.75rem; padding: 4px 10px; border-radius: 12px;
            background-color: #f3f4f6; color: #4b5563; font-weight: 600; text-transform: uppercase;
        }
        
        .description { color: #4b5563; font-size: 0.95rem; margin-bottom: 20px; flex-grow: 1; }
        .view-btn {
            padding: 10px; background-color: white; border: 2px solid #e63946;
            color: #e63946; font-weight: bold; border-radius: 8px;
            cursor: pointer; transition: all 0.2s; width: 100%; margin-top: auto;
        }
        .view-btn:hover { background-color: #e63946; color: white; }

        /* --- Empty State Message --- */
        .empty-state {
            grid-column: 1 / -1;
            text-align: center;
            padding: 50px;
            color: #9ca3af;
            font-size: 1.2rem;
            border: 2px dashed #e5e7eb;
            border-radius: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Fridge Raider</h1>
            <p class="subtitle">Tell me what's in your fridge, and I'll show you what to cook.</p>
            
            <div class="search-container">
                <input type="text" id="fridgeInput" class="search-input" placeholder="Type an ingredient (e.g. Chicken, Rice)...">
            </div>
        </header>

        <div class="filters">
            <button class="filter-btn active" data-filter="all">All</button>
            <button class="filter-btn" data-filter="Dinner">Dinner</button>
            <button class="filter-btn" data-filter="Breakfast">Breakfast</button>
            <button class="filter-btn" data-filter="Lunch">Lunch</button>
            <button class="filter-btn" data-filter="Dessert">Dessert</button>
            <button class="filter-btn" data-filter="Healthy">Healthy</button>
        </div>

        <div class="recipe-grid" id="recipeGrid">
            <div class="empty-state">
                Recipes will appear here once you start typing...
            </div>
        </div>
    </div>

    <script>
        // --- DATA: ALL 6 RECIPES ---
        const recipes = [
            // ORIGINAL 3
            { 
                id: 4, 
                title: "Golden Saffron Risotto", 
                image: "https://images.unsplash.com/photo-1595908129746-25651b384433?auto=format&fit=crop&w=800&q=80", 
                tags: ["Dinner", "Vegetarian", "Italian"], 
                ingredients: ["rice", "arborio", "saffron", "broth", "parmesan", "wine", "butter"],
                time: "40 mins", 
                description: "A luxurious, vibrant yellow Italian classic featuring premium saffron threads and parmesan." 
            },
            { 
                id: 5, 
                title: "Classic Smashburger", 
                image: "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80", 
                tags: ["Dinner", "Beef", "American"], 
                ingredients: ["beef", "ground beef", "cheese", "bun", "bread", "lettuce", "onion"],
                time: "20 mins", 
                description: "Crispy edges, juicy center, melted cheese, and toasted brioche buns." 
            },
            { 
                id: 6, 
                title: "Avocado Toast & Egg", 
                image: "https://images.unsplash.com/photo-1525351484164-8035a4206501?auto=format&fit=crop&w=800&q=80", 
                tags: ["Breakfast", "Healthy", "Vegetarian"], 
                ingredients: ["avocado", "egg", "bread", "toast", "chili", "lemon"],
                time: "15 mins", 
                description: "Creamy avocado on sourdough topped with a perfectly runny poached egg and chili flakes." 
            },
            // NEW VISUAL 3
            { 
                id: 1, 
                title: "Creamy Tuscan Chicken", 
                image: "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?auto=format&fit=crop&w=800&q=80", 
                tags: ["Dinner", "Chicken", "Creamy"], 
                ingredients: ["chicken", "spinach", "cream", "garlic", "tomato", "parmesan"],
                time: "30 mins", 
                description: "Golden chicken breasts in a rich garlic cream sauce with spinach and bursting cherry tomatoes." 
            },
            { 
                id: 2, 
                title: "Rainbow Poke Bowl", 
                image: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80", 
                tags: ["Lunch", "Healthy", "Seafood"], 
                ingredients: ["tuna", "salmon", "rice", "mango", "avocado", "cucumber", "mayo"],
                time: "20 mins", 
                description: "Fresh tuna, mango, avocado, and spicy mayo arranged in a stunning color wheel over sushi rice." 
            },
            { 
                id: 3, 
                title: "Blood Orange Galette", 
                image: "https://images.unsplash.com/photo-1614532661523-86a037b5f134?auto=format&fit=crop&w=800&q=80", 
                tags: ["Dessert", "Fruit", "Baking"], 
                ingredients: ["orange", "blood orange", "flour", "pastry", "honey", "thyme", "sugar"],
                time: "45 mins", 
                description: "A rustic, sophisticated dessert featuring caramelized blood orange slices and fresh thyme." 
            }
        ];

        const grid = document.getElementById('recipeGrid');
        const filterBtns = document.querySelectorAll('.filter-btn');
        const fridgeInput = document.getElementById('fridgeInput');

        // --- RENDER FUNCTION ---
        function displayRecipes(data) {
            // 1. If data is empty (no matches found), show message
            if (data.length === 0) {
                grid.innerHTML = '<div class="empty-state">No recipes match those ingredients yet! Try "Chicken", "Egg", or "Rice"</div>';
                return;
            }
            // 2. Otherwise, render cards
            grid.innerHTML = data.map(r => `
                <article class="recipe-card">
                    <img src="${r.image}" class="card-image">
                    <div class="card-content">
                        <h3 class="recipe-title">${r.title}</h3>
                        <div class="ingredients-match">Contains: ${r.ingredients.slice(0,3).join(', ')}</div>
                        <div class="tags-container">${r.tags.map(t => `<span class="tag">${t}</span>`).join('')}</div>
                        <p class="description">${r.description}</p>
                        <div style="margin-top: auto; display: flex; justify-content: space-between; align-items: center;">
                            <span class="time-tag">⏱ ${r.time}</span>
                            <button class="view-btn">View Recipe</button>
                        </div>
                    </div>
                </article>
            `).join('');
        }

        // --- FILTER LOGIC ---
        function filterAll() {
            const searchTerm = fridgeInput.value.toLowerCase().trim();
            const activeCategory = document.querySelector('.filter-btn.active').getAttribute('data-filter');

            // KEY CHANGE: If input is empty, clear the grid
            if (searchTerm === "") {
                grid.innerHTML = '<div class="empty-state">Recipes will appear here once you start typing...</div>';
                return;
            }

            const filtered = recipes.filter(item => {
                // 1. Check Category
                const matchesCategory = (activeCategory === 'all') || item.tags.includes(activeCategory);
                
                // 2. Check Ingredients (Search)
                const matchesSearch = item.title.toLowerCase().includes(searchTerm) ||
                                      item.ingredients.some(ing => ing.toLowerCase().includes(searchTerm));
                
                return matchesCategory && matchesSearch;
            });

            displayRecipes(filtered);
        }

        // --- EVENT LISTENERS ---
        
        // 1. Initial Load: Do NOT show recipes. Show placeholder.
        grid.innerHTML = '<div class="empty-state">Recipes will appear here once you start typing...</div>';

        // 2. Search Input Listener
        fridgeInput.addEventListener('input', filterAll);

        // 3. Button Click Listener
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                // Only trigger filter if user has already typed something
                if (fridgeInput.value.trim() !== "") {
                    filterAll();
                }
            });
        });
    </script>
</body>
</html>
"""

# --- 3. Render the HTML in Streamlit ---
components.html(HTML_CODE, height=1200, scrolling=True)
