import streamlit as st
import os
import glob
from gcp_imagen import generate_image

st.title("🎈 Jaime's app")

IMAGES_PATH = "daily_images"
DAILY_IMAGES = glob.glob(f'{IMAGES_PATH}/*')
IMAGES_NAMES = [os.path.basename(file) for file in DAILY_IMAGES]
image_1, image_2, image_3, image_4 = False, False, False, False
images = [image_1, image_2, image_3, image_4]

def display_generated_images():
    pass

def get_selected_images():
    for image in images:
        if image == False:
            st.write("Downloading ", image)

col1 , col2 = st.columns(2)
with col1:
    if st.button("Generate an Image"):
        display_generated_images()
with col2:
    if st.button("Download selected Images."):
        get_selected_images()

prompt = st.chat_input("Is there anything particular you are looking for today sir?")
if prompt:
    if prompt == "No":
        st.write(f"Very well then. I shall continue with my search and provide you with you desired results.")
    else:
        st.write(f"User has sent the following prompt: {prompt}")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        image_1 = st.checkbox("Image #1")
        st.image(DAILY_IMAGES[0], caption=IMAGES_NAMES[0])
    with st.container(border=True):
        image_3 = st.checkbox("Image #3")
        st.image(DAILY_IMAGES[1], caption=IMAGES_NAMES[1])

with col2:
    with st.container(border=True):
        image_2 = st.checkbox("Image #2")
        st.image(DAILY_IMAGES[2], caption=IMAGES_NAMES[2])
    with st.container(border=True):
        image_4 = st.checkbox("Image #4")
        st.image(DAILY_IMAGES[3], caption=IMAGES_NAMES[3])