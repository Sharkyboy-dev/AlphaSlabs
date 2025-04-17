# AlphaSlabs Streamlit MVP with Dynamic Flip Score Logic
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
    min_price, max_price = st.slider("Price Range", 0, 500, (10, 100))

center3, col_slider2, center4 = st.columns([1, 2, 1])
with col_slider2:
    flip_score_min = st.slider("Flip Score Min", 0, 100, 10)

# === SAMPLE CARD DATA ===
data = [
    {
        "Card": "2020 Topps Chrome Luis Robert PSA 10",
        "Price": 42.50,
        "Avg Sold": 60.00,
        "Link": "https://www.ebay.com/itm/1234567890",
        "Image": "https://i.imgur.com/UhVb5zk.png",
        "Category": "Baseball"
    },
    {
        "Card": "2019 Prizm Ja Morant Rookie PSA 10",
        "Price": 72.00,
        "Avg Sold": 88.00,
        "Link": "https://www.ebay.com/itm/2345678901",
        "Image": "https://i.imgur.com/UhVb5zk.png",
        "Category": "Basketball"
    },
    {
        "Card": "2000 Pokémon Charizard Holo Base Set",
        "Price": 120.00,
        "Avg Sold": 200.00,
        "Link": "https://www.ebay.com/itm/1111111111",
        "Image": "https://i.imgur.com/UhVb5zk.png",
        "Category": "Pokémon"
    },
    {
        "Card": "2023 UFC Chrome Paddy Pimblett Rookie",
        "Price": 35.00,
        "Avg Sold": 50.00,
        "Link": "https://www.ebay.com/itm/2222222222",
        "Image": "https://i.imgur.com/UhVb5zk.png",
        "Category": "UFC"
    },
    {
        "Card": "2017 Panini Select Patrick Mahomes RC",
        "Price": 80.00,
        "Avg Sold": 190.00,
        "Link": "https://www.ebay.com/itm/3333333333",
        "Image": "https://i.imgur.com/UhVb5zk.png",
        "Category": "Football"
    },
    {
        "Card": "2022 Donruss Mac Jones Downtown",
        "Price": 160.00,
        "Avg Sold": 170.00,
        "Link": "https://www.ebay.com/itm/4444444444",
        "Image": "https://i.imgur.com/UhVb5zk.png",
        "Category": "Football"
    },
    {
        "Card": "2023 Topps Now Shohei Ohtani MVP",
        "Price": 20.00,
        "Avg Sold": 22.00,
        "Link": "https://www.ebay.com/itm/5555555555",
        "Image": "https://i.imgur.com/UhVb5zk.png",
        "Category": "Baseball"
    }
]

# Calculate Flip Score (% Upside)
df = pd.DataFrame(data)
df["Flip Score"] = ((df["Avg Sold"] - df["Price"]) / df["Price"] * 100).round(1)

# Filter
df = df[(df["Price"] >= min_price) & (df["Price"] <= max_price) & (df["Flip Score"] >= flip_score_min)]

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
