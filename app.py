
import streamlit as st
import pandas as pd

st.set_page_config(page_title="AlphaSlabs", layout="wide")

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
        .centered-logo {
            display: flex;
            justify-content: center;
            margin-bottom: 1rem;
        }
        .badge-strip {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-bottom: 1rem;
        }
        .badge-strip img {
            height: 50px;
        }
    </style>
    ''',
    unsafe_allow_html=True
)

st.markdown('<div class="centered-logo"><img src="images/logo.png" width="200"></div>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center; color:white;'>Built for collectors. Powered by alpha.</h2>", unsafe_allow_html=True)

st.markdown('''
<div class="badge-strip">
    <img src="images/pokeball.png">
    <img src="images/football.png">
    <img src="images/baseball_tags.png">
    <img src="images/glove.png">
    <img src="images/field.png">
</div>
''', unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
with col1:
    search_query = st.text_input("Search Keyword", "")
with col2:
    min_price, max_price = st.slider("Price Range ($)", 0, 500, (10, 100))
with col3:
    grading = st.selectbox("Grading Company", ["All", "PSA", "BGS", "SGC"])
with col4:
    flip_score = st.slider("Min Flip Score", 0, 50, 10)

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

for _, row in filtered_df.iterrows():
    st.markdown("---")
    cols = st.columns([1, 2])
    with cols[0]:
        st.image(row["Image"], width=160)
    with cols[1]:
        st.markdown(f"<h4 style='color:white'>{row['Card']}</h4>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#ccc;'>💰 <strong>${row['Price']}</strong> | Avg: ${row['Avg Sold']}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#ccc;'>Flip Score: {'🔥' if row['Flip Score'] > 15 else '⚠️'} {row['Flip Score']}</span>", unsafe_allow_html=True)
        st.markdown(f"<a href='{row['Link']}' target='_blank'><button style='background-color:#1e88e5;color:white;padding:6px 16px;border:none;border-radius:4px;'>View on eBay</button></a>", unsafe_allow_html=True)
