import streamlit as st
import pandas as pd
from recommender import SimpleRecommender

st.set_page_config(page_title="🛍 Product Recommender", layout="wide")
st.title("🛒 Product Recommendation System")

# Load data
rec = SimpleRecommender("products.csv")
df = rec.df

# Sidebar options
st.sidebar.header("Options")
product_id = st.sidebar.selectbox(
    "Select a product",
    df['product_id'],
    format_func=lambda x: df[df['product_id'] == x]['name'].values[0]
)
top_n = st.sidebar.slider("Number of recommendations", 1, 8, 4)

# Display selected product
selected = df[df['product_id'] == product_id].iloc[0]
st.markdown(f"### 🎯 {selected['name']}")
st.image(selected['image_url'], width=250)
st.write(f"**Price:** ₹{selected['price_inr']}")
st.write(selected['description'])

# Show recommendations
if st.button("🔍 Show Recommendations"):
    recs = rec.recommend_by_id(product_id, top_n=top_n)
    st.markdown("## Recommended Products")
    cols = st.columns(2)
    for i, row in recs.iterrows():
        with cols[i % 2]:
            st.image(row['image_url'], width=180)
            st.markdown(f"**{row['name']}**")
            st.write(f"₹{row['price_inr']}")
            st.write(row['description'])
            st.markdown("---")
