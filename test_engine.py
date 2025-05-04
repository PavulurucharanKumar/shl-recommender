from recommendation_engine import SHLRecommendationEngine
engine = SHLRecommendationEngine('assessments.json')
query = "Hiring for a role requiring team collaboration and creative problem-solving, max 90 minutes."
recs = engine.recommend(query, max_duration=90)
print(recs)