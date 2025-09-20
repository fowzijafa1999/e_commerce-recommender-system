import streamlit as st
import pandas as pd
from recommender import ContentRecommender

st.set_page_config(page_title="🛍 Product Recommender", layout="wide")
st.title("🛒 Content-Based Product Recommender")

# Load recommender
rec = ContentRecommender("products.csv")
df = rec.df

# -------------------- Search --------------------
search_query = st.text_input("Search for a product", "")

# Filter by search query (case-insensitive)
if search_query:
    filtered = df[df['name'].str.contains(search_query, case=False, na=False)]
else:
    filtered = df.copy()

# -------------------- Select Product --------------------
if len(filtered) == 0:
    st.warning("No product found. Try typing something else.")
else:
    product_name = st.selectbox("Choose a product", filtered['name'].tolist())
    selected = df[df['name'] == product_name].iloc[0]

    # Display selected product
    st.markdown(f"### 🎯 {selected['name']}")
    st.image(selected['image_url'], width=250)
    for line in str(selected['description']).split("\n"):
        st.write(line)
    st.markdown(f"**Price:** ₹{selected['price_inr']}")

    # -------------------- Recommendations --------------------
    st.markdown("---")
    st.markdown("## 🤝 Recommended Products")
    recs = rec.recommend_by_id(selected['product_id'], top_n=4)
    cols = st.columns(2)
    for i, row in recs.iterrows():
        with cols[i % 2]:
            st.image(row['image_url'], width=180)
            st.markdown(f"**{row['name']}**")
            st.write(f"₹{row['price_inr']}")
            for line in str(row['description']).split("\n"):
                st.write(line)
            st.markdown("---")
