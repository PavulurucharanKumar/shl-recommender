from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SHLRecommendationEngine:
    def __init__(self, data_path):
        logger.info(f"Initializing SHLRecommendationEngine with data_path: {data_path}")
        if not os.path.exists(data_path):
            logger.error(f"Data file {data_path} not found")
            raise FileNotFoundError(f"Data file {data_path} not found")
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='/tmp/model_cache')
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise
        self.data = pd.read_json(data_path)
        logger.info(f"Data loaded: {len(self.data)} records")
        try:
            self.embeddings = self.model.encode(
                self.data['description'].tolist(),
                show_progress_bar=False,
                batch_size=1,
                normalize_embeddings=True
            )
            logger.info("Embeddings computed successfully")
        except Exception as e:
            logger.error(f"Failed to compute embeddings: {str(e)}")
            raise

    def recommend(self, query, max_duration=90):
        logger.info(f"Processing recommendation for query: {query}, max_duration: {max_duration}")
        try:
            query_embedding = self.model.encode([query], show_progress_bar=False, normalize_embeddings=True)
            similarities = np.dot(self.embeddings, query_embedding.T).flatten()
            self.data['similarity'] = similarities
            recommendations = self.data[self.data['duration'] <= max_duration][['name', 'description', 'duration']]
            result = recommendations.sort_values(by='similarity', ascending=False).head(3).to_dict(orient='records')
            logger.info(f"Recommendations generated: {len(result)} items")
            return result
        except Exception as e:
            logger.error(f"Recommendation failed: {str(e)}")
            return [{"error": f"Recommendation failed: {str(e)}"}]