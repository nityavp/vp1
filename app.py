import streamlit as st
import pandas as pd
import random
import zipfile
import os
import requests
from openai import OpenAI

# Initialize session state for posts data
if 'posts_data' not in st.session_state:
    st.session_state['posts_data'] = pd.DataFrame(columns=['Date', 'Content', 'Platform', 'Status'])

# API Key input hidden as password
api_key = st.text_input("Enter your OpenAI API Key", type="password")

# Configuration arrays for content generation
points = ["tips", "hacks", "news", "guide", "analogy", "joke", "compare", "up and downs", "funfacts"]
time_related = ["latest", "historic", "trends"]
locations = ["culture", "country", "region", "religions", "beliefs"]
hooks = [ ... ]  # Assuming your hooks list is already defined here.

# Function to generate posts using OpenAI
def generate_posts(api_key, platform, topic, style, num_posts, user_type):
    posts = []
    for _ in range(num_posts):
        chosen_points = random.choice(points) if random.random() > 0.5 else ""
        chosen_time = random.choice(time_related) if random.random() > 0.5 else ""
        chosen_location = random.choice(locations) if random.random() > 0.5 else ""
        
        custom_prompt = f"Generate a unique {platform} post about {topic} in {style} style"
        if user_type == "Personal":
            chosen_hook = random.choice(hooks)
            custom_prompt += f" with {chosen_hook}"

        try:
            client = OpenAI(api_key=api_key)
            completions = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": custom_prompt}])
            response = completions.choices[0].message.content
            posts.append(response)
        except Exception as e:
            st.error(f"Failed to generate posts: {e}")
            return []

    return posts

# UI for post generation
user_type = st.radio('Select User Type', ['Company', 'Personal'])
platform = st.selectbox('Select Social Media Platform', ['Twitter', 'LinkedIn'])
topic = st.text_input('Enter Topic')
style = st.text_input('Enter Writing Style')
num_posts = st.number_input('Number of Posts', min_value=1, max_value=20, value=1)

if st.button('Generate Posts'):
    generated_posts = generate_posts(api_key, platform, topic, style, num_posts, user_type)
    if generated_posts:
        new_rows = [{'Date': pd.Timestamp.now(), 'Content': post, 'Platform': platform, 'Status': 'Pending'} for post in generated_posts]
        st.session_state.posts_data = pd.concat([st.session_state.posts_data, pd.DataFrame(new_rows)], ignore_index=True)

# Display and edit the DataFrame containing generated posts
st.dataframe(st.session_state.posts_data, use_container_width=True)

# Image generation and ZIP file creation (assuming these functions are defined and implemented correctly)
selected_row = st.selectbox('Select a row to generate an image', range(len(st.session_state.posts_data)))
selected_style = st.text_input('Enter Image Style for Selected Row')

if st.button('Generate Image for Selected Row'):
    selected_content = st.session_state.posts_data.iloc[selected_row]['Content']
    image_url = generate_image(api_key, selected_style, selected_content)
    if image_url:
        st.image(image_url, caption='Generated Image')
        zip_path = create_zip(selected_content, image_url)
        with open(zip_path, "rb") as file:
            st.download_button('Download Content and Image in Zip', file, file_name='final_posts.zip')
