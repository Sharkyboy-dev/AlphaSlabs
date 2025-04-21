import os
import csv
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd


# === HTML Parser ===
def parse_mercari_html(uploaded_file):
    soup = BeautifulSoup(uploaded_file, "html.parser")
    items = soup.select("li[data-testid='ItemCell']")

    listings = []
    for item in items:
        title_tag = item.select_one("p")
        price_tag = item.select_one("div[data-testid='ItemCellPrice']")
        link_tag = item.select_one("a")

        title = title_tag.get_text(strip=True) if title_tag else "No title"
        price = price_tag.get_text(strip=True) if price_tag else "$0"
        link = f"https://www.mercari.com{link_tag['href']}" if link_tag else "No link"

        try:
            price_float = float(price.replace("$", "").replace(",", ""))
        except ValueError:
            price_float = 0.0

        listings.append({
            "Card": title,
            "Price": price_float,
            "Avg Sold": price_float,  # placeholder until eBay data
            "Flip Score": 0.0,
            "Link": link,
            "Image": "https://via.placeholder.com/100"
        })

    df = pd.DataFrame(listings)
    if not df.empty:
        df["Flip Score"] = ((df["Avg Sold"] - df["Price"]) / df["Avg Sold"] * 100).round(1)
    return df


# === Streamlit UI ===
def show_mercari_upload_ui():
    st.markdown("""
        <style>
        .upload-box {
            padding: 2rem;
            background: #111;
            border-radius: 12px;
            max-width: 600px;
            margin: auto;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
    st.header("📥 Upload Mercari HTML")
    uploaded_file = st.file_uploader("Upload saved .html page from Mercari", type=["html"])

    if uploaded_file:
        html_str = uploaded_file.read().decode("utf-8")
        df = parse_mercari_html(html_str)
        if not df.empty:
            st.success(f"✅ Parsed {len(df)} items")
            st.dataframe(df)
            csv = df.to_csv(index=False)
            st.download_button("📁 Download CSV", csv, file_name="mercari_results.csv")
        else:
            st.warning("⚠️ No card listings found in the uploaded HTML.")
    st.markdown("</div>", unsafe_allow_html=True)

