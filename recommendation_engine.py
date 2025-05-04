from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

class SHLRecommendationEngine:
    def __init__(self, data_path):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Lighter model
        self.data = pd.read_json(data_path)
        self.embeddings = self.model.encode(self.data['description'].tolist(), show_progress_bar=False)

    def recommend(self, query, max_duration=90):
        query_embedding = self.model.encode([query], show_progress_bar=False)
        similarities = np.dot(self.embeddings, query_embedding.T).flatten()
        self.data['similarity'] = similarities
        recommendations = self.data[self.data['duration'] <= max_duration][['name', 'description', 'duration', 'similarity']]
        return recommendations.sort_values(by='similarity', ascending=False).head(5).to_dict(orient='records')