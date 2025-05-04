import json
with open('assessments.json', 'r') as f:
    data = json.load(f)
print(f"Loaded {len(data)} assessments")