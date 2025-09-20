%%writefile recommender.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class ContentRecommender:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)

        # Combine name + rich description + category as text features
        self.df["text_features"] = (
            self.df["name"].fillna("") + " " + self.df["description"].fillna("")
        )

        # TF-IDF with bigrams
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2))
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["text_features"])

        # Precompute cosine similarity
        self.similarity = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def recommend_by_id(self, product_id, top_n=5):
        if product_id not in self.df["product_id"].values:
            raise ValueError("Product ID not found!")

        idx = self.df.index[self.df["product_id"] == product_id][0]
        sim_scores = list(enumerate(self.similarity[idx]))

        # Sort by similarity (high → low)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Skip itself & near duplicates (>0.95 similarity)
        recs = []
        for i, score in sim_scores[1:]:
            if score < 0.95:
                recs.append(i)
            if len(recs) >= top_n:
                break

        return self.df.iloc[recs][
            ["product_id", "name", "description", "price_inr", "image_url"]
        ].reset_index(drop=True)
