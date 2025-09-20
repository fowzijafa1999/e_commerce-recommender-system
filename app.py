import streamlit as st
import pandas as pd
from recommender import ContentRecommender

st.set_page_config(page_title="🛍 Product Recommender", layout="wide")
st.title("🛒 Simple Content-Based Product Recommender")

# -------------------- Load Data --------------------
rec = ContentRecommender("products.csv")
df = rec.df

# -------------------- Sidebar Filters --------------------
st.sidebar.header("Filter Options")

# Category filter
categories = ["All"] + sorted(df['category'].unique())
selected_category = st.sidebar.selectbox("Category", categories)

# Search filter
search_query = st.sidebar.text_input("Search product", "")

# Apply filters
filtered = df.copy()
if selected_category != "All":
    filtered = filtered[filtered['category'] == selected_category]

if search_query:
    filtered = filtered[filtered['name'].str.contains(search_query, case=False, na=False)]

# -------------------- Product Selection --------------------
if len(filtered) == 0:
    st.warning("No products found with your filters/search.")
else:
    product_id = st.selectbox(
        "Choose a product",
        filtered['product_id'].tolist(),
        format_func=lambda x: filtered[filtered['product_id'] == x]['name'].values[0]
    )

    selected = df[df['product_id'] == product_id].iloc[0]

    # Display selected product
    st.markdown(f"### 🎯 {selected['name']}")
    col1, col2 = st.columns([1,2])
    with col1:
        st.image(selected['image_url'], width=250)
    with col2:
        for line in str(selected['description']).split("\n"):
            st.write(line)
        st.markdown(f"**Price:** ₹{selected['price_inr']}")
        st.markdown(f"**Category:** {selected['category']}")

    # -------------------- Recommendations --------------------
    st.markdown("---")
    st.markdown("## 🤝 Recommended Products")
    recs = rec.recommend_by_id(product_id, top_n=4)
    cols = st.columns(2)
    for i, row in recs.iterrows():
        with cols[i % 2]:
            st.image(row['image_url'], width=180)
            st.markdown(f"**{row['name']}**")
            st.write(f"₹{row['price_inr']}")
            for line in str(row['description']).split("\n"):
                st.write(line)
            st.markdown(f"**Category:** {row['category']}")
            st.markdown("---")
