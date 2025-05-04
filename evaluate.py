import json
from recommendation_engine import SHLRecommendationEngine

def recall_at_k(predicted, relevant, k):
    predicted_k = predicted[:k]
    relevant_set = set(relevant)
    retrieved_relevant = sum(1 for p in predicted_k if p in relevant_set)
    return retrieved_relevant / len(relevant_set) if relevant_set else 0

def ap_at_k(predicted, relevant, k):
    relevant_set = set(relevant)
    score = 0
    num_hits = 0
    for i, p in enumerate(predicted[:k], 1):
        if p in relevant_set:
            num_hits += 1
            score += num_hits / i
    return score / min(len(relevant_set), k) if relevant_set else 0

test_data = [
    {
        'query': 'I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.',
        'relevant': ['Automata - Fix (New)', 'Core Java (Entry Level) (New)', 'Java 8 (New)']
    },
    {
        'query': 'I want to hire new graduates for a sales role, max 60 minutes.',
        'relevant': ['Entry Level Sales 7.1 (International)', 'Entry Level Sales Solution']
    }
]

engine = SHLRecommendationEngine('assessments.json')
recall_scores = []
ap_scores = []

for test in test_data:
    recommendations = engine.recommend(test['query'], max_duration=40)
    predicted = [r['name'] for r in recommendations]
    recall_scores.append(recall_at_k(predicted, test['relevant'], 3))
    ap_scores.append(ap_at_k(predicted, test['relevant'], 3))

mean_recall = sum(recall_scores) / len(recall_scores)
mean_ap = sum(ap_scores) / len(ap_scores)
print(f"Mean Recall@3: {mean_recall:.4f}")
print(f"MAP@3: {mean_ap:.4f}")