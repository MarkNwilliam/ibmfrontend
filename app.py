import streamlit as st
import requests
import random
import re

st.title("Video Generator")

topic = st.text_input("Enter the topic:")

# Automatically generate a filename based on the topic
def sanitize_filename(topic):
    """Sanitize topic to create a valid filename."""
    topic = re.sub(r'\W+', '_', topic)  # Replace non-alphanumeric characters with underscores
    return topic[:20]  # Limit length to 20 characters

if st.button("Generate Video"):
    if not topic.strip():
        st.error("Please enter a topic!")
    else:
        output_name = f"{sanitize_filename(topic)}"  # Generate a random number

        response = requests.post(
            "http://20.9.234.187:3000/generate_video",
            json={"topic": topic, "output_name": output_name},
            headers={"Content-Type": "application/json"}
        )

        st.write("DEBUG: API Response ->", response.json())  # 🛑 Debug response

        if response.status_code == 200:
            data = response.json()
            video_url = data.get("video_url")

            if video_url:
                st.success(f"Video generated successfully: {output_name}")
                st.video(video_url)
            else:
                st.error("Error: Video URL not found.")
        else:
            st.error("Error: " + response.json().get("error", "Unknown error"))

if st.button("Check Health"):
    response = requests.get("http://20.9.234.187:5000/health")
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error("Error: " + response.json()["error"])
