import streamlit as st
import requests
import json

st.title("SHL Assessment Recommender")
query = st.text_input("Enter job role (e.g., 'Hiring for a creative role')")
max_duration = st.slider("Max Duration (minutes)", 10, 180, 90)
if st.button("Get Recommendations"):
    try:
        response = requests.post(
            "https://shl-api-jc4u.onrender.com/recommend",
            json={"query": query, "max_duration": max_duration},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        recommendations = response.json()
        if isinstance(recommendations, list) and "error" not in recommendations[0]:
            for rec in recommendations:
                st.write(f"**{rec['name']}** (Duration: {rec['duration']} mins)")
                st.write(rec['description'])
        else:
            st.error(f"Error: {recommendations[0].get('error', 'No recommendations')}")
    except Exception as e:
        st.error(f"Failed to fetch recommendations: {str(e)}")