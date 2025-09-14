import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load dataset
df = pd.read_csv("products.csv")
df["image"] = df["image"].str.strip()  

st.write("Sample images from CSV:")
st.write(df["image"].head())
st.image("https://via.placeholder.com/150", width=150, caption="Test Image")

# Content for recommendation (combine name + brand + description)
df["content"] = df["name"] + " " + df["brand"] + " " + df["description"]

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["content"])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Recommendation function
def recommend(product_name, num_recommendations=5):
    if product_name not in df["name"].values:
        return []
    idx = df[df["name"] == product_name].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations+1]
    product_indices = [i[0] for i in sim_scores]
    return df.iloc[product_indices]

# Streamlit UI
st.title("🛒 Product Recommender System")

# Dropdown for product selection
product_choice = st.selectbox("Select a product:", df["name"].values)

if st.button("Show Recommendations"):
    recommendations = recommend(product_choice)
    if recommendations.empty:
        st.warning("No recommendations found!")
    else:
        st.subheader("Recommended Products:")
        for _, row in recommendations.iterrows():
            st.image(row["image"], width=150)
            st.markdown(f"**{row['name']}**")
            st.write(f"Brand: {row['brand']}")
            st.write(f"Price: ₹{row['price']}")
            st.write(f"{row['description']}")
            st.markdown("---")


