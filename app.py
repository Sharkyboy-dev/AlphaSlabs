
import streamlit as st
import pandas as pd

st.set_page_config(page_title="AlphaSlabs", layout="wide")

# Custom background style
st.markdown(
    '''
    <style>
        body {
            background: url('https://i.imgur.com/FkJEmZB.jpg') no-repeat center center fixed;
            background-size: cover;
        }
        .block-container {
            background-color: rgba(0, 0, 0, 0.85);
            padding: 2rem 2rem 2rem 2rem;
            border-radius: 10px;
        }
    </style>
    ''',
    unsafe_allow_html=True
)

# ✅ Centered logo
st.image("images/logo.png", width=200)
st.markdown("<h2 style='text-align:center; color:white;'>Built for collectors. Powered by alpha.</h2>", unsafe_allow_html=True)

# ✅ Themed PNG strip using st.image
row = st.columns(5)
row[0].image("images/pokeball.png", width=50)
row[1].image("images/football.png", width=50)
row[2].image("images/baseball_tags.png", width=50)
row[3].image("images/glove.png", width=50)
row[4].image("images/field.png", width=50)

st.markdown("---")

# Filters
col1, col2, col3, col4 = st.columns(4)
with col1:
    search_query = st.text_input("Search Keyword", "")
with col2:
    min_price, max_price = st.slider("Price Range ($)", 0, 500, (10, 100))
with col3:
    grading = st.selectbox("Grading Company", ["All", "PSA", "BGS", "SGC"])
with col4:
    flip_score = st.slider("Min Flip Score", 0, 50, 10)

# Card data
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
        "Card": "2021 Select Trevor Lawrence Silver PSA 9",
        "Price": 28.00,
        "Avg Sold": 35.00,
        "Flip Score": 7.0,
        "Link": "https://www.ebay.com/itm/3456789012",
        "Image": "https://i.imgur.com/UhVb5zk.png"
    },
]

df = pd.DataFrame(data)

filtered_df = df[
    (df["Price"] >= min_price) &
    (df["Price"] <= max_price) &
    (df["Flip Score"] >= flip_score)
]
if search_query:
    filtered_df = filtered_df[filtered_df["Card"].str.contains(search_query, case=False)]

# Display listings
for _, row in filtered_df.iterrows():
    st.markdown("---")
    cols = st.columns([1, 2])
    with cols[0]:
        st.image(row["Image"], width=160)
    with cols[1]:
        st.markdown(f"<h4 style='color:white'>{row['Card']}</h4>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#ccc;'>💰 <strong>${row['Price']}</strong> | Avg: ${row['Avg Sold']}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#ccc;'>Flip Score: {'🔥' if row['Flip Score'] > 15 else '⚠️'} {row['Flip Score']}</span>", unsafe_allow_html=True)
        st.markdown(f"[👉 View on eBay]({row['Link']})", unsafe_allow_html=True)
