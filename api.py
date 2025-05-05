from flask import Flask, request, jsonify
from recommendation_engine import SHLRecommendationEngine
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
try:
    logger.info("Initializing SHLRecommendationEngine")
    engine = SHLRecommendationEngine('assessments.json')
    logger.info("SHLRecommendationEngine initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize engine: {str(e)}")
    raise

@app.route('/', methods=['GET'])
def root():
    logger.info("Received request for /")
    return jsonify({"status": "API is running"})

@app.route('/health', methods=['GET'])
def health():
    logger.info("Received request for /health")
    return jsonify({"status": "API is running"})

@app.route('/recommend', methods=['POST'])
def recommend():
    logger.info("Received request for /recommend")
    try:
        data = request.get_json()
        if not data:
            logger.error("No JSON data provided")
            return jsonify({"error": "No JSON data provided"}), 400
        query = data.get('query', '')
        max_duration = data.get('max_duration', 90)
        logger.info(f"Processing query: {query}, max_duration: {max_duration}")
        if not query:
            logger.error("Empty query provided")
            return jsonify({"error": "Query cannot be empty"}), 400
        recommendations = engine.recommend(query, max_duration)
        logger.info(f"Recommendations generated: {len(recommendations)} items")
        return jsonify(recommendations)
    except Exception as e:
        logger.error(f"Error in /recommend: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port)