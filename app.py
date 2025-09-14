import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv("products.csv")

# Page settings
st.set_page_config(page_title="🛒 E-Commerce Recommender", layout="wide")

st.title("🛒 E-Commerce Recommender System")
st.write("Explore products, check details, and see recommendations!")

# Sidebar filters
st.sidebar.header("🔍 Search & Filters")
search_query = st.sidebar.text_input("Search for a product")
max_price = st.sidebar.slider("Filter by price", int(df['price'].min()), int(df['price'].max()), int(df['price'].max()))
brand_filter = st.sidebar.multiselect("Filter by brand", options=df['brand'].unique())

# Apply filters
filtered = df.copy()
if search_query:
    filtered = filtered[filtered['product_name'].str.contains(search_query, case=False, na=False)]
if brand_filter:
    filtered = filtered[filtered['brand'].isin(brand_filter)]
filtered = filtered[filtered['price'] <= max_price]

# Show results
if filtered.empty:
    st.warning("No products found. Try different filters.")
else:
    cols = st.columns(3)  # 3 products per row
    for idx, row in filtered.iterrows():
        with cols[idx % 3]:
            st.image(row['image'], width=200)
            st.markdown(f"**{row['product_name']}**")
            st.write(f"Brand: `{row['brand']}`")
            st.write(f"💰 Price: ₹{row['price']}")
            if st.button(f"Recommend Similar to {row['product_id']}", key=row['product_id']):
                st.success(f"Recommended products similar to {row['product_name']} will appear here!")
