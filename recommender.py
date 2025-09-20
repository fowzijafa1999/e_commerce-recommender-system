import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class SimpleRecommender:
    def __init__(self, products_csv="products.csv"):
        self.df = pd.read_csv(products_csv)
        self.df['text'] = self.df['name'].fillna('') + ' ' + self.df['description'].fillna('')
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['text'])

    def recommend_by_id(self, product_id, top_n=5):
        if product_id not in self.df['product_id'].values:
            return pd.DataFrame()
        idx = int(self.df.index[self.df['product_id'] == product_id][0])
        sim_scores = list(enumerate(linear_kernel(self.tfidf_matrix[idx:idx+1], self.tfidf_matrix).flatten()))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1: top_n+1]
        indices = [i[0] for i in sim_scores]
        return self.df.iloc[indices].reset_index(drop=True)
