import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv("products.csv")

st.set_page_config(page_title="E-Commerce Recommender", layout="wide")

st.title("🛒 E-Commerce Recommender System")
st.write("Browse products and see recommendations!")

# Sidebar for search
search_query = st.sidebar.text_input("Search a product")

# Filter based on search
if search_query:
    filtered = df[df['product_name'].str.contains(search_query, case=False, na=False)]
else:
    filtered = df

# Show results in card layout
cols = st.columns(3)  # 3 products per row
for idx, row in filtered.iterrows():
    with cols[idx % 3]:
        st.image(row['image'], width=200)
        st.markdown(f"**{row['product_name']}**")
        st.write(f"Brand: {row['brand']}")
        st.write(f"💰 Price: ₹{row['price']}")
        if st.button("Recommend Similar", key=row['product_id']):
            st.success(f"Recommended products similar to {row['product_name']}")
