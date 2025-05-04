import streamlit as st
import requests
import pandas as pd

st.title("SHL Assessment Recommendation System")
query = st.text_area("Enter job description or query:", height=150)
max_duration = st.number_input("Max total duration (minutes)", min_value=10, max_value=180, value=90)

if st.button("Get Recommendations"):
    if not query.strip():
        st.error("Please enter a query.")
    else:
        response = requests.post('https://shl-api.onrender.com/recommend', json={'query': query, 'max_duration': max_duration})
        if response.status_code == 200:
            recommendations = response.json()
            if recommendations:
                df = pd.DataFrame(recommendations)
                st.table(df)
            else:
                st.warning("No recommendations found.")
        else:
            st.error("Error fetching recommendations.")