import streamlit as st
import pandas as pd
from recommender import ContentRecommender  # Use the upgraded content-based recommender

st.set_page_config(page_title="🛍 Product Recommender", layout="wide")
st.title("🛒 Simple Content-Based Product Recommender")

# -------------------- Load Data & Recommender --------------------
rec = ContentRecommender("products.csv")
df = rec.df

# -------------------- Top Filter Bar --------------------
st.markdown("### 🔍 Find Your Product")
col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    search_query = st.text_input("Search", placeholder="Type product name...")

with col2:
    categories = ["All", "Electronics", "Fashion", "Home & Kitchen", "Sports", "Beauty", "Books", "Toys"]
    category = st.selectbox("Category", categories)

with col3:
    min_price, max_price = int(df['price_inr'].min()), int(df['price_inr'].max())
    price_range = st.slider("Price (₹)", min_price, max_price, (min_price, max_price))

# -------------------- Apply Filters --------------------
filtered = df.copy()

# Search filter
if search_query:
    filtered = filtered[filtered['name'].str.contains(search_query, case=False)]

# Price filter
filtered = filtered[(filtered['price_inr'] >= price_range[0]) & (filtered['price_inr'] <= price_range[1])]

# Category filter
if category != "All":
    filtered = filtered[
        filtered['description'].str.contains(category, case=False) |
        filtered['name'].str.contains(category, case=False)
    ]

st.markdown(f"✅ {len(filtered)} products found")

# -------------------- Product Selection --------------------
if len(filtered) > 0:
    product_id = st.selectbox(
        "Choose a product",
        filtered['product_id'].tolist(),
        format_func=lambda x: filtered[filtered['product_id'] == x]['name'].values[0]
    )

    top_n = st.slider("How many recommendations?", 1, 8, 4)

    selected = df[df['product_id'] == product_id].iloc[0]
    st.markdown(f"### 🎯 {selected['name']}")
    cols = st.columns([1, 2])
    with cols[0]:
        st.image(selected['image_url'], width=240)
    with cols[1]:
        st.write(selected['description'])
        st.markdown(f"**Price:** ₹{selected['price_inr']}")

    # -------------------- Recommendations --------------------
    if st.button("Show Recommendations"):
        recs = rec.recommend_by_id(product_id, top_n=top_n)
        st.markdown("## 🤝 Recommended Products")
        cols = st.columns(2)
        for i, row in recs.iterrows():
            c = cols[i % 2]
            with c:
                st.image(row['image_url'], width=160)
                st.markdown(f"**{row['name']}**")
                st.write(f"₹{row['price_inr']}")
                st.write(row['description'])
                st.markdown("---")

