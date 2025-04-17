# AlphaSlabs Streamlit MVP with Dynamic Flip Score Logic + AutoTag
import streamlit as st
import pandas as pd

st.set_page_config(page_title="AlphaSlabs", layout="wide")

# === STYLES ===
st.markdown("""
    <style>
        body {
            background: url('https://i.imgur.com/FkJEmZB.jpg') no-repeat center center fixed;
            background-size: cover;
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
            font-family: sans-serif;
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
        .search-row {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
        }
        .search-box, .search-select {
            padding: 10px;
            font-size: 14px;
            border-radius: 6px;
            border: none;
            outline: none;
        }
        .search-box {
            width: 300px;
        }
        .search-btn {
            background-color: #1e88e5;
            color: white;
            padding: 10px;
            font-size: 16px;
            border-radius: 6px;
            border: none;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

# === LOGO + SLOGAN ===
st.markdown("""
    <div style='text-align: center;'>
        <img src='https://raw.githubusercontent.com/Sharkyboy-dev/AlphaSlabs/main/images/logo.png' width='220'>
        <h2 style='color: white;'>Built for collectors. Powered by alpha.</h2>
    </div>
""", unsafe_allow_html=True)

# === SEARCH BAR UI ===
st.markdown("""
    <div class="search-row">
        <form action="" method="get">
            <select name="category" class="search-select">
                <option>All Categories</option>
                <option>Baseball</option>
                <option>Basketball</option>
                <option>Football</option>
                <option>UFC</option>
                <option>Pokémon</option>
                <option>Soccer</option>
            </select>
            <input name="search" class="search-box" placeholder="Search cards, players, teams, boxes, brands, sets...">
            <button class="search-btn">🔍</button>
        </form>
    </div>
""", unsafe_allow_html=True)

# === CENTERED SLIDERS ===
center1, col_slider1, center2 = st.columns([1, 2, 1])
with col_slider1:
    min_price, max_price = st.slider("Price Range", 0, 500, (10, 100), key="price_slider")

center3, col_slider2, center4 = st.columns([1, 2, 1])
with col_slider2:
    flip_score_min = st.slider("Flip Score Min", 0, 100, 10, key="score_slider")

# === SAMPLE CARD DATA ===
data = pd.read_csv("data/baseball_cards.csv")

# === AUTOTAG BY KEYWORD ===
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

# === EMOJI SCORING TIERS ===
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

# === FILTERED DATAFRAME ===
df = data[(data["Price"] >= min_price) & (data["Price"] <= max_price) & (data["Flip Score"] >= flip_score_min)]

# === DISPLAY CARDS ===
for _, row in df.iterrows():
    type_icon = get_type_emoji(row['Card'])
    tier_icon = get_icon(row['Flip Score'])
    st.markdown(f"""
        <div class="baseball-tab">
            <img src="{row['Image']}" width="120" class="card-img">
            <div class="card-info">
                <h4>{type_icon} {row['Card']}</h4>
                <p class="price">💰 ${row['Price']} &nbsp; | &nbsp; Avg: ${row['Avg Sold']}</p>
                <p class="flip-score">Flip Score: {tier_icon} {row['Flip Score']}%</p>
                <a href="{row['Link']}" class="view-btn" target="_blank">View on eBay</a>
            </div>
        </div>
    """, unsafe_allow_html=True)
