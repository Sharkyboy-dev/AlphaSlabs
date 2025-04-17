# AlphaSlabs Streamlit MVP with Full Layout Polishing
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="AlphaSlabs", layout="wide")

# === STYLES ===
st.markdown("""
    <style>
        body {
            background: url('https://i.imgur.com/FkJEmZB.jpg') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .navbar {
            display: flex;
            justify-content: center;
            gap: 2rem;
            padding: 10px 0;
            background-color: #001d3d;
        }
        .navbar a {
            color: white;
            text-decoration: none;
            font-weight: bold;
        }
        .logo-container {
            text-align: center;
            margin: 1rem 0 0.5rem;
        }
        .baseball-tab {
            display: flex;
            align-items: center;
            background-color: #00264d;
            padding: 1rem;
            margin-bottom: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 0 10px #000;
        }
        .card-img {
            margin-right: 1rem;
            border-radius: 8px;
        }
        .card-info {
            color: white;
        }
        .price {
            color: #ffd700;
            font-size: 1rem;
        }
        .flip-score {
            font-weight: bold;
        }
        .view-btn {
            background-color: #1e88e5;
            color: white;
            padding: 6px 12px;
            border: none;
            border-radius: 6px;
            text-decoration: none;
        }
        footer {
            text-align: center;
            color: #ccc;
            padding: 1rem 0 2rem;
            font-size: 0.85rem;
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

tab_objects = st.tabs([c[0] for c in categories])

for i, tab in enumerate(tab_objects):
    with tab:
        category_name, csv_file = categories[i]
        data_path = os.path.join("data", csv_file)

        if not os.path.exists(data_path):
            st.warning(f"❌ {csv_file} not found.")
            continue

        data = pd.read_csv(data_path)

        search_term = st.text_input(f"Search {category_name}", "", key=f"search_{i}")
        min_price, max_price = st.slider(f"Price Range ({category_name})", 0, 500, (10, 100), key=f"price_{i}")
        flip_score_min = st.slider(f"Flip Score Min ({category_name})", 0, 100, 10, key=f"score_{i}")

        def auto_tag(card_name):
            name = card_name.lower()
            if "pokemon" in name or "charizard" in name:
                return "Pokémon"
            elif "ufc" in name or "pimblett" in name:
                return "UFC"
            elif "mlb" in name or "topps" in name or "ohtani" in name:
                return "Baseball"
            elif "mahomes" in name or "panini" in name or "nfl" in name or "mac jones" in name:
                return "Football"
            elif "ja morant" in name or "prizm" in name:
                return "Basketball"
            elif "soccer" in name or "futbol" in name:
                return "Soccer"
            else:
                return "Other"

        data["Category"] = data["Card"].apply(auto_tag)
        data["Flip Score"] = ((data["Avg Sold"] - data["Price"]) / data["Price"] * 100).round(1)

        def get_icon(score):
            if score >= 100:
                return "🧨"
            elif score >= 50:
                return "🔥"
            elif score >= 25:
                return "⚠️"
            elif score >= 10:
                return "🧊"
            else:
                return "🚫"

        def get_type_emoji(name):
            name = name.lower()
            if any(word in name for word in ["pokemon", "charizard"]):
                return "🔴"
            elif any(word in name for word in ["topps", "bowman", "mlb"]):
                return "⚾️"
            elif any(word in name for word in ["nfl", "select", "panini", "prizm"]):
                return "🏈"
            elif any(word in name for word in ["soccer", "futbol"]):
                return "⚽️"
            elif any(word in name for word in ["ufc", "octagon"]):
                return "🥊"
            else:
                return "🎴"

        df = data[(data["Price"] >= min_price) & (data["Price"] <= max_price) & (data["Flip Score"] >= flip_score_min)]

        if search_term:
            df = df[df["Card"].str.contains(search_term, case=False)]

        sort_by = st.selectbox("Sort By", ["Flip Score (High to Low)", "Price (Low to High)", "Price (High to Low)"], key=f"sort_{i}")
        if sort_by == "Flip Score (High to Low)":
            df = df.sort_values(by="Flip Score", ascending=False)
        elif sort_by == "Price (Low to High)":
            df = df.sort_values(by="Price", ascending=True)
        elif sort_by == "Price (High to Low)":
            df = df.sort_values(by="Price", ascending=False)

        st.markdown("""
            <h3 style='text-align: center; color: #00ffaa;'>🔥 Best Flip Opportunities</h3>
        """, unsafe_allow_html=True)

        best_score = df["Flip Score"].max() if not df.empty else None

        for _, row in df.iterrows():
            type_icon = get_type_emoji(row['Card'])
            tier_icon = get_icon(row['Flip Score'])
            badge = "<span style='background:#ffd700;color:#000;padding:4px 8px;border-radius:6px;margin-left:10px;'>🏆 Best Flip</span>" if row["Flip Score"] == best_score and best_score is not None else ""
            st.markdown(f"""
                <div class="baseball-tab">
                    <img src="{row['Image']}" width="120" class="card-img">
                    <div class="card-info">
                        <h4>{type_icon} {row['Card']} {badge}</h4>
                        <p class="price">💰 ${row['Price']} &nbsp; | &nbsp; Avg: ${row['Avg Sold']}</p>
                        <p class="flip-score">Flip Score: {tier_icon} {row['Flip Score']}%</p>
                        <a href="{row['Link']}" class="view-btn" target="_blank">View on eBay</a>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# === FOOTER ===
st.markdown("""
    <footer>
        © 2025 AlphaSlabs · All rights reserved · Built by Sharkyboy-dev
    </footer>
""", unsafe_allow_html=True)
