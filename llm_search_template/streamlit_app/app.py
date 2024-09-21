import streamlit as st
import requests

st.title("LLM-based RAG Search")

# Input for user query
query = st.text_input("Enter your query:")

if st.button("Search"):
    if query:
        try:
            # Make a POST request to the Flask API
            flask_api_url = "http://localhost:5000/api/query"  # Replace with your Flask API URL
            response = requests.post(flask_api_url, json={"query": query})

            # Check the response status
            if response.status_code == 200:
                # Display the generated answer
                answer = response.json().get('llm_response', "No response received.")
                st.write("Answer:", answer)
            else:
                st.error(f"Error: {response.status_code}")
        
        except requests.RequestException as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.write("Please enter a valid query.")
