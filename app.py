import streamlit as st
import pandas as pd

st.set_page_config(page_title="AlphaSlabs", layout="wide")
# ✅ Centered logo using Streamlit layout (works on Cloud)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("images/logo.png", width=200)

st.markdown("<h2 style='text-align:center; color:white;'>Built for collectors. Powered by alpha.</h2>", unsafe_allow_html=True)

# Custom background
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
    </style>
""", unsafe_allow_html=True)

# ✅ Centered logo + tagline
st.markdown(
    "<div style='text-align: center;'><img src='images/logo.png' width='200'></div>",
    unsafe_allow_html=True
)
st.markdown("<h2 style='text-align:center; color:white;'>Built for collectors. Powered by alpha.</h2>", unsafe_allow_html=True)

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    search_query = st.text_input("Search", "")
with col2:
    min_price, max_price = st.slider("Price Range", 0, 500, (10, 100))
with col3:
    flip_score_min = st.slider("Flip Score Min", 0, 50, 10)

# Sample card data
data = [
    {
        "Card": "2020 Topps Chrome Luis Robert PSA 10",
        "Price": 42.50,
        "Avg Sold": 60.00,
        "Flip Score": 17.5,
        "Link": "https://www.ebay.com/itm/1234567890",
        "Image": "https://i.imgur.com/UhVb5zk.png"
    },
    {
        "Card": "2019 Prizm Ja Morant Rookie PSA 10",
        "Price": 72.00,
        "Avg Sold": 88.00,
        "Flip Score": 16.0,
        "Link": "https://www.ebay.com/itm/2345678901",
        "Image": "https://i.imgur.com/UhVb5zk.png"
    },
    {
        "Card": "2000 Pokémon Charizard Holo Base Set",
        "Price": 120.00,
        "Avg Sold": 200.00,
        "Flip Score": 25.0,
        "Link": "https://www.ebay.com/itm/1111111111",
        "Image": "https://i.imgur.com/UhVb5zk.png"
    },
    {
        "Card": "2023 UFC Chrome Paddy Pimblett Rookie",
        "Price": 35.00,
        "Avg Sold": 50.00,
        "Flip Score": 12.0,
        "Link": "https://www.ebay.com/itm/2222222222",
        "Image": "https://i.imgur.com/UhVb5zk.png"
    }
]

df = pd.DataFrame(data)

# Apply filters
df = df[(df["Price"] >= min_price) & (df["Price"] <= max_price) & (df["Flip Score"] >= flip_score_min)]
if search_query:
    df = df[df["Card"].str.contains(search_query, case=False)]

# 🧠 Auto-icon by keyword
def get_card_icon(name):
    name = name.lower()
    if any(word in name for word in ["pokemon", "charizard", "wotc"]):
        return "🔴"
    elif any(word in name for word in ["topps", "bowman", "mlb"]):
        return "⚾️"
    elif any(word in name for word in ["nfl", "select", "panini", "prizm"]):
        return "🏈"
    elif any(word in name for word in ["soccer", "futbol"]):
        return "⚽️"
    elif any(word in name for word in ["ufc", "octagon", "fight", "pimblett"]):
        return "🥊"
    else:
        return "🎴"

# Display cards in styled tabs
for _, row in df.iterrows():
    icon = get_card_icon(row['Card'])
    st.markdown(f"""
        <div class="baseball-tab">
            <img src="{row['Image']}" width="120" class="card-img">
            <div class="card-info">
                <h4>{icon} {row['Card']}</h4>
                <p class="price">💰 ${row['Price']} &nbsp; | &nbsp; Avg: ${row['Avg Sold']}</p>
                <p class="flip-score">Flip Score: {'🔥' if row['Flip Score'] > 15 else '⚠️'} {row['Flip Score']}</p>
                <a href="{row['Link']}" class="view-btn" target="_blank">View on eBay</a>
            </div>
        </div>
    """, unsafe_allow_html=True)
