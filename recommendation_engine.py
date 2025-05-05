from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
import os

class SHLRecommendationEngine:
    def __init__(self, data_path):
        self.model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='/tmp/model_cache')
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Data file {data_path} not found")
        self.data = pd.read_json(data_path)
        self.embeddings = self.model.encode(self.data['description'].tolist(), show_progress_bar=False, batch_size=4)

    def recommend(self, query, max_duration=90):
        try:
            query_embedding = self.model.encode([query], show_progress_bar=False)
            similarities = np.dot(self.embeddings, query_embedding.T).flatten()
            self.data['similarity'] = similarities
            recommendations = self.data[self.data['duration'] <= max_duration][['name', 'description', 'duration']]
            return recommendations.sort_values(by='similarity', ascending=False).head(3).to_dict(orient='records')
        except Exception as e:
            return [{"error": f"Recommendation failed: {str(e)}"}]