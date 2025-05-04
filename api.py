from flask import Flask, jsonify, request
from recommendation_engine import SHLRecommendationEngine

app = Flask(__name__)
engine = SHLRecommendationEngine('assessments.json')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'API is running'}), 200

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    query = data.get('query')
    max_duration = data.get('max_duration', None)
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    recommendations = engine.recommend(query, max_duration)
    return jsonify(recommendations), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)