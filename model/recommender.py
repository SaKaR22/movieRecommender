import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import ast
import os

class MovieRecommender:
    def __init__(self):
        # Load processed data
        self.movies = pd.read_csv('data/movies_processed.csv')
        
        # Load or compute similarity matrix
        if os.path.exists('model/cosine_sim.npy'):
            self.cosine_sim = np.load('model/cosine_sim.npy')
        else:
            self._build_similarity_matrix()
        
        # Create indices mapping
        self.indices = pd.Series(self.movies.index, index=self.movies['title']).drop_duplicates()
    
    def _build_similarity_matrix(self):
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(self.movies['soup'])
        self.cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        np.save('model/cosine_sim.npy', self.cosine_sim)
    
    def get_recommendations(self, title):
        try:
            idx = self.indices[title]
        except KeyError:
            # Find similar titles
            similar_titles = self.movies[self.movies['title'].str.contains(title, case=False)]['title']
            if len(similar_titles) > 0:
                return pd.DataFrame({'title': similar_titles, 'match': 'Did you mean:'})
            return pd.DataFrame({'title': ['Movie not found'], 'match': ''})
        
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]  # Top 10
        movie_indices = [i[0] for i in sim_scores]
        
        return self.movies.iloc[movie_indices][['title', 'genres', 'director']]