# AlphaSlabs Streamlit MVP with Full Layout Polishing
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="AlphaSlabs", layout="wide")

# === MODERN STYLES ===
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        html, body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(to right, #141e30, #243b55);
        }
        .navbar {
            display: flex;
            justify-content: center;
            gap: 1.8rem;
            padding: 1rem;
            background-color: #101820;
            border-bottom: 1px solid #444;
        }
        .navbar a {
            color: #eee;
            text-decoration: none;
            font-weight: 600;
            padding: 6px 14px;
            border-radius: 16px;
            transition: 0.2s ease-in-out;
        }
        .navbar a:hover {
            background: #00ffaa20;
            color: #00ffaa;
        }
        .logo-container {
            text-align: center;
            margin-top: 1.5rem;
        }
        .logo-container h2 {
            color: white;
            font-weight: 600;
        }
        .card-container {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }
        .flip-card {
            display: flex;
            align-items: center;
            background-color: #1a1a2e;
            border-radius: 16px;
            padding: 1rem;
            box-shadow: 0 3px 12px rgba(0,0,0,0.3);
        }
        .card-img {
            width: 100px;
            height: auto;
            margin-right: 1.5rem;
            border-radius: 10px;
            border: 1px solid #444;
        }
        .card-info {
            color: #f0f0f0;
        }
        .card-info h4 {
            margin: 0 0 0.4rem;
            font-size: 1.2rem;
            font-weight: 600;
        }
        .price {
            color: #ffd166;
            font-size: 1rem;
            margin-bottom: 0.2rem;
        }
        .flip-score {
            font-weight: 600;
            color: #06d6a0;
        }
        .view-btn {
            display: inline-block;
            margin-top: 0.6rem;
            background: #118ab2;
            color: white;
            padding: 6px 12px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 500;
        }
        .view-btn:hover {
            background: #0b708f;
        }
        footer {
            text-align: center;
            margin-top: 2rem;
            color: #999;
            font-size: 0.8rem;
            padding-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# === NAVBAR ===
st.markdown("""
    <div class='navbar'>
        <a href='#'>Home</a>
        <a href='#'>Watchlist</a>
        <a href='#'>Discord</a>
        <a href='#'>Submit</a>
    </div>
""", unsafe_allow_html=True)

# === HEADER ===
st.markdown("""
    <div class='logo-container'>
        <img src='https://raw.githubusercontent.com/Sharkyboy-dev/AlphaSlabs/main/images/logo.png' width='220'>
        <h2>Built for collectors. Powered by alpha.</h2>
    </div>
""", unsafe_allow_html=True)

# === CATEGORY TABS ===
categories = [
    ("Baseball", "baseball_cards.csv"),
    ("Basketball", "basketball_cards.csv"),
    ("Football", "football_cards.csv"),
    ("Pokémon", "pokemon_cards.csv"),
    ("UFC", "ufc_cards.csv"),
    ("Soccer", "soccer_cards.csv")
]

selected = st.radio("Choose Card Category", [label for label, _ in categories], horizontal=True)
selected_file = next((file for label, file in categories if label == selected), None)

# === MAIN DISPLAY ===
if selected_file:
    data_path = os.path.join("data", selected_file)
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)

        # Filters
        search_term = st.text_input(f"Search {selected}")
        if search_term:
            df = df[df["Card"].str.contains(search_term, case=False)]

        price_range = st.slider(f"Price Range ({selected})", 0, 500, (10, 100))
        df = df[(df["Price"] >= price_range[0]) & (df["Price"] <= price_range[1])]

        min_score = st.slider(f"Flip Score Min ({selected})", 0, 100, 10)
        df["Flip Score"] = ((df["Avg Sold"] - df["Price"]) / df["Avg Sold"] * 100).round(1)
        df = df[df["Flip Score"] >= min_score]

        sort_option = st.selectbox("Sort By", ["Flip Score (High to Low)", "Flip Score (Low to High)"])
        df = df.sort_values("Flip Score", ascending=(sort_option == "Flip Score (Low to High)"))

        st.markdown("<h4 style='color:#06d6a0;'>🔥 Best Flip Opportunities</h4>", unsafe_allow_html=True)

        for _, row in df.iterrows():
            st.markdown(f"""
                <div class='flip-card'>
                    <img class='card-img' src='{row["Image"]}'>
                    <div class='card-info'>
                        <h4>{row["Card"]}</h4>
                        <div class='price'>💰 ${row["Price"]} | Avg: ${row["Avg Sold"]}</div>
                        <div class='flip-score'>🔥 Flip Score: {row["Flip Score"]}%</div>
                        <a href='{row["Link"]}' class='view-btn' target='_blank'>View on eBay</a>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.error(f"data/{selected_file} not found. Please upload it to /data.")

# === FOOTER ===
st.markdown("""
    <footer>
        © 2025 AlphaSlabs · All rights reserved · Built by Sharkyboy-dev
    </footer>
""", unsafe_allow_html=True)
