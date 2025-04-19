# AlphaSlabs Streamlit - Final Centered Filter Fix (Updated for Live Scraper Integration)
import streamlit as st
import pandas as pd
import os
import subprocess

st.set_page_config(
    page_title="AlphaSlabs",
    layout="wide",
    page_icon="📈",
    initial_sidebar_state="collapsed"
)

# === MODERN STYLES ===
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        html, body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        }
        .main-wrapper {
            max-width: 960px;
            margin: auto;
            padding: 2rem 1rem;
        }
        .filter-wrapper {
            display: flex;
            justify-content: center;
            margin-top: 2rem;
        }
        .filter-inner {
            background: #111;
            padding: 2rem;
            border-radius: 12px;
            width: 100%;
            max-width: 600px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.35);
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
            margin: 2rem 0 1rem;
        }
        .baseball-tab {
            display: flex;
            align-items: center;
            background-color: #14213d;
            padding: 1rem;
            border-radius: 14px;
            margin-bottom: 1.5rem;
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
            color: white;
            padding: 6px 14px;
            border: none;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 500;
            display: inline-block;
            margin-top: 0.5rem;
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
        <a href='#'>Watchlist</a>
        <a href='#'>Submit</a>
        <a href='#'>Discord</a>
    </div>
""", unsafe_allow_html=True)

# === WRAPPER START ===
st.markdown("<div class='main-wrapper'>", unsafe_allow_html=True)

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

# === Live Scrape Trigger ===
if st.button(f"🔄 Refresh {selected} Listings from Mercari"):
    keyword = f"{selected.lower()} cards"
    command = f"python3 mercari_scraper.py --keyword '{keyword}' --output data/{selected_file}"
    try:
        subprocess.run(command, shell=True, check=True)
        st.success(f"✅ Refreshed data for {selected}!")
    except Exception as e:
        st.error(f"❌ Failed to scrape: {e}")

if selected_file:
    path = os.path.join("data", selected_file)
    if os.path.exists(path):
        df = pd.read_csv(path)

        # === FILTER SECTION ===
        st.markdown("<div class='filter-wrapper'><div class='filter-inner'>", unsafe_allow_html=True)

        search_term = st.text_input("Search", "")
        if search_term:
            df = df[df["Card"].str.contains(search_term, case=False)]

        price_range = st.slider("Price Range", 0, 500, (10, 100))
        df = df[(df["Price"] >= price_range[0]) & (df["Price"] <= price_range[1])]

        score_min = st.slider("Flip Score Min", 0, 100, 10)
        df["Flip Score"] = ((df["Avg Sold"] - df["Price"]) / df["Avg Sold"] * 100).round(1)
        df = df[df["Flip Score"] >= score_min]

        sort_by = st.selectbox("Sort By", ["Flip Score (High to Low)", "Flip Score (Low to High)"])
        df = df.sort_values("Flip Score", ascending=(sort_by == "Flip Score (Low to High)"))

        st.markdown("</div></div>", unsafe_allow_html=True)

        # === DISPLAY CARDS ===
        st.markdown("<h4 style='color:#00ffaa; margin-top:2rem;'>🔥 Flip Opportunities</h4>", unsafe_allow_html=True)
        for _, row in df.iterrows():
            btn_label = "View on Mercari" if "mercari.com" in row["Link"] else "View on eBay"
            btn_color = "#ff6f61" if "mercari.com" in row["Link"] else "#1e88e5"

            st.markdown(f"""
                <div class='baseball-tab'>
                    <img class='card-img' src='{row["Image"]}'>
                    <div class='card-info'>
                        <h4>{row["Card"]}</h4>
                        <div class='price'>💰 ${row["Price"]} | Avg: ${row["Avg Sold"]}</div>
                        <div class='flip-score'>Score: {row["Flip Score"]}%</div>
                        <a href='{row["Link"]}' class='view-btn' style='background-color:{btn_color};' target='_blank'>{btn_label}</a>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning(f"File not found: {selected_file}")

# === WRAPPER END ===
st.markdown("</div>", unsafe_allow_html=True)

# === FOOTER ===
st.markdown("""
    <footer>
        © 2025 AlphaSlabs · All rights reserved · Built by Sharkyboy-dev
    </footer>
""", unsafe_allow_html=True)
