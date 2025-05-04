import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class SHLRecommendationEngine:
    def __init__(self, data_path):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        with open(data_path, 'r') as f:
            self.assessments = json.load(f)
        self.assessment_texts = [a['description'] for a in self.assessments]
        self.embeddings = self.model.encode(self.assessment_texts)

    def recommend(self, query, max_duration=None, max_results=10):
        query_embedding = self.model.encode([query])[0]
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        ranked_indices = np.argsort(similarities)[::-1]

        recommendations = []
        total_duration = 0
        for idx in ranked_indices:
            assessment = self.assessments[idx]
            if max_duration and total_duration + assessment['duration'] > max_duration:
                continue
            recommendations.append({
                'name': assessment['name'],
                'url': assessment['url'],
                'remote_support': assessment['remote_support'],
                'adaptive_support': assessment['adaptive_support'],
                'duration': assessment['duration'],
                'test_type': assessment['test_type']
            })
            total_duration += assessment['duration']
            if len(recommendations) >= max_results:
                break
        return recommendations