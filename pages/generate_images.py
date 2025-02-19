import streamlit as st
import os
import glob
import shutil
import time

src_dir = "computer_vision/daily_images"
trg_dir = "computer_vision/upload_images"
DAILY_IMAGES = glob.glob(f'{src_dir}/*')
IMAGES_NAMES = [os.path.basename(file) for file in DAILY_IMAGES]

col1, col2 = st.columns(2)

def save_images(images):
    msg = st.toast('Gathering images...')
    time.sleep(1)
    msg.toast('Uploading...')
    for img in images:
        if img:
            shutil.copy2(img, trg_dir)
    time.sleep(1)
    msg.toast('Successfully uploaded!', icon="🥞")

def generate_images(prompt):
    st.toast(prompt)

# Dictionary to track selected images
selected_images = {}

# **Dynamically create a 2x2 grid**
for i, image in enumerate(DAILY_IMAGES[:4]):  # Limit to 4 images
    col = col1 if i % 2 == 0 else col2  # Assign columns dynamically
    with col:
        with st.container(border=True):
            selected_images[image] = st.checkbox(f"Image {i+1}: {IMAGES_NAMES[i]}")
            st.image(image, caption="Insert description")

prompt = st.chat_input("Is there anything particular you are looking for today sir?")
if prompt:
    generate_images("Will send the prompt to the appropriate LLM in the future.")

# **Buttons for actions**
left, right = st.columns(2)
if left.button("Save Selected Images", icon=":material/bookmark:", use_container_width=True):
    save_images([img for img, selected in selected_images.items() if selected])

if right.button("Generate", icon=":material/skip_next:", use_container_width=True):
    right.markdown("You clicked the Generate button.")
