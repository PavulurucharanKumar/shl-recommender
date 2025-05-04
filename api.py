from flask import Flask, request, jsonify
from recommendation_engine import SHLRecommendationEngine
import os

app = Flask(__name__)
engine = SHLRecommendationEngine('assessments.json')

@app.route('/', methods=['GET'])
def root():
    return jsonify({"status": "API is running"})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "API is running"})

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    query = data.get('query', '')
    max_duration = data.get('max_duration', 90)
    recommendations = engine.recommend(query, max_duration)
    return jsonify(recommendations)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)