import streamlit as st
import os
import glob
import time

src_dir = "computer_vision/upload_images"
DAILY_IMAGES = glob.glob(f'{src_dir}/*')
IMAGES_NAMES = [os.path.basename(file) for file in DAILY_IMAGES]

col1, col2 = st.columns(2)

def image_exists(image):
    return image if image else "computer_vision/template_images/image (5).png"

def delete_images(images):
    msg = st.toast('Gathering images...')
    time.sleep(1)
    msg.toast('Deleting...')
    for img in images:
        if img and os.path.exists(img):
            os.remove(img)
        else:
            msg.toast(f'The file {img} does not exist', icon="🥞")
    time.sleep(1)
    msg.toast('Successfully deleted!', icon="🥞")

# Dictionary to track selected images
selected_images = {}

# **Dynamically create a 2x2 grid**
for i, image in enumerate(DAILY_IMAGES[:4]):  # Limit to 4 images
    col = col1 if i % 2 == 0 else col2  # Assign columns dynamically
    with col:
        with st.container(border=True):
            selected_images[image] = st.checkbox(f"Image {i+1}: {IMAGES_NAMES[i]}")
            st.image(image_exists(image), caption="Insert description")

# **Buttons for actions**
left, right = st.columns(2)
if left.button("Delete Selected Images", icon=":material/delete:", use_container_width=True):
    delete_images([img for img, selected in selected_images.items() if selected])

if right.button("Upload Selected Images", icon=":material/file_upload:", use_container_width=True):
    st.toast("Uploading selected images...")  
