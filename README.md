# SHL Assessment Recommendation System

## Overview
A web application recommending SHL assessments based on job role queries, using a Flask API and Streamlit frontend.

## Components
- **Flask API** (`api.py`): Serves `/health` and `/recommend` endpoints, using `sentence-transformers` for text similarity.
- **Streamlit App** (`app.py`): User interface to input job roles and display recommendations.
- **Recommendation Engine** (`recommendation_engine.py`): Processes queries using `all-MiniLM-L6-v2` model.
- **Data**: `assessments.json` contains assessment details.

## Deployment
- **API**: Hosted on Render (`https://shl-api-jc4u.onrender.com`)
  - Health: `GET /health`
  - Recommend: `POST /recommend` (e.g., `{"query": "Hiring for a creative role", "max_duration": 90}`)
- **Streamlit**: Hosted on Render (`https://shl-streamlit.onrender.com`)

## Setup
1. Clone: `git clone https://github.com/PavulurucharanKumar/shl-recommender.git`
2. Install: `pip install -r requirements.txt`
3. Run API: `python api.py`
4. Run Streamlit: `streamlit run app.py`

## Usage
- Enter a job role (e.g., "Hiring for a creative role") and max duration in the Streamlit app.
- View top 3 recommended assessments.

## Notes
- Free tier Render may have startup delays.
- Optimized for low memory using `all-MiniLM-L6-v2` model.

## Author
Pavuluru Charan Kumar
