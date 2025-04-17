# AlphaSlabs Streamlit MVP with Full Layout Polishing
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="AlphaSlabs", layout="wide")

# === MODERN STYLES ===
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        html, body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        }
        .navbar {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            padding: 1rem;
            background-color: #101820;
            border-bottom: 1px solid #333;
        }
        .navbar a {
            color: #f2f2f2;
            text-decoration: none;
            font-weight: 600;
            padding: 8px 14px;
            border-radius: 20px;
            transition: all 0.2s ease;
        }
        .navbar a:hover {
            background: #00ffaa30;
            color: #00ffaa;
        }
        .logo-container {
            text-align: center;
            margin: 1.5rem 0 0.5rem;
        }
        .logo-container h2 {
            color: #f0f0f0;
            font-weight: 500;
        }
        .card-container {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }
        .baseball-tab {
            display: flex;
            align-items: center;
            background-color: #14213d;
            padding: 1rem;
            border-radius: 14px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.3);
        }
        .card-img {
            margin-right: 1rem;
            border-radius: 10px;
            border: 1px solid #444;
            width: 100px;
            height: auto;
        }
        .card-info {
            color: #ffffff;
        }
        .card-info h4 {
            font-weight: 600;
            margin-bottom: 0.4rem;
        }
        .price {
            color: #ffc107;
            font-size: 1rem;
            margin-bottom: 0.2rem;
        }
        .flip-score {
            font-weight: 500;
        }
        .view-btn {
            background-color: #28a745;
            color: white;
            padding: 6px 14px;
            border: none;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 500;
            display: inline-block;
            margin-top: 0.5rem;
        }
        .view-btn:hover {
            background-color: #218838;
        }
        footer {
            text-align: center;
            color: #aaa;
            padding: 2rem 0 1rem;
            font-size: 0.8rem;
        }
    </style>
""", unsafe_allow_html=True)

# === NAVBAR ===
st.markdown("""
    <div class='navbar'>
        <a href='#'>Home</a>
        <a href='#'>My Watchlist</a>
        <a href='#'>Submit a Card</a>
        <a href='#'>Discord</a>
    </div>
""", unsafe_allow_html=True)

# === LOGO + SLOGAN ===
st.markdown("""
    <div class='logo-container'>
        <img src='https://raw.githubusercontent.com/Sharkyboy-dev/AlphaSlabs/main/images/logo.png' width='220'>
        <h2 style='color: white;'>Built for collectors. Powered by alpha.</h2>
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

selected = st.radio("Select a category:", [label for label, _ in categories], horizontal=True)

selected_file = next((file for label, file in categories if label == selected), None)

if selected_file:
    data_path = os.path.join("data", selected_file)
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)

        # Filters
        search_term = st.text_input(f"Search {selected}")
        df = df[df["Card"].str.contains(search_term, case=False)] if search_term else df

        price_range = st.slider(f"Price Range ({selected})", 0, 500, (10, 100))
        df = df[(df["Price"] >= price_range[0]) & (df["Price"] <= price_range[1])]

        min_score = st.slider(f"Flip Score Min ({selected})", 0, 100, 10)
        df["Flip Score"] = ((df["Avg Sold"] - df["Price"]) / df["Avg Sold"] * 100).round(1)
        df = df[df["Flip Score"] >= min_score]

        sort_option = st.selectbox("Sort By", ["Flip Score (High to Low)", "Flip Score (Low to High)"])
        df = df.sort_values("Flip Score", ascending=(sort_option == "Flip Score (Low to High)"))

        # Display
        st.markdown(f"""<h4 style='color:#00ffaa; margin-top:2rem;'>🔥 Best Flip Opportunities</h4>""", unsafe_allow_html=True)
        with st.container():
            for _, row in df.iterrows():
                link_label = "View on Mercari" if "mercari.com" in row["Link"] else "View on eBay"
                link_color = "#ff6f61" if "mercari.com" in row["Link"] else "#1e88e5"

                st.markdown(f"""
                    <div class='baseball-tab'>
                        <img class='card-img' src='{row["Image"]}'>
                        <div class='card-info'>
                            <h4>{row["Card"]}</h4>
                            <div class='price'>💰 ${row["Price"]} | Avg: ${row["Avg Sold"]}</div>
                            <div class='flip-score'>🔥 Flip Score: {row["Flip Score"]}%</div>
                            <a href='{row["Link"]}' class='view-btn' style='background-color:{link_color};' target='_blank'>{link_label}</a>
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
