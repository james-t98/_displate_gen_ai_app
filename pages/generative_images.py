import streamlit as st
import os
import glob
import shutil
import time
from PIL import Image
from io import BytesIO
from generative_ai.image_generation.model import ImageGeneration
from datetime import datetime

model = ImageGeneration()

gen_dir = "generative_ai/image_generation/generated_images"
sav_dir = "generative_ai/image_generation/saved_images"
IMAGES = glob.glob(f'{gen_dir}/*')
IMAGES_NAMES = [os.path.basename(file) for file in IMAGES]

def save_images(images):
    msg = st.toast('Gathering images...')
    time.sleep(1)
    msg.toast('Uploading...')
    for img in images:
        if img:
            shutil.copy2(img, sav_dir)
    time.sleep(1)
    msg.toast('Successfully saved!', icon="✅")

def generate_images(prompt):
    msg = st.toast('Generating image...')
    time.sleep(1)
    msg.toast('Finalizing...')
    # Generate image bytes
    image_bytes = model.generate_image(prompt).read()

    # Convert bytes to PIL Image
    image = Image.open(BytesIO(image_bytes))

    os.makedirs(gen_dir, exist_ok=True)  # Ensure directory exists
    time.sleep(1)
    msg.toast('Successfully generated.', icon="🥞")
    # Save image
    # Generate a unique filename using timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")  # Format: YYYYMMDD_HHMMSS_microseconds
    image_filename = f"generated_image_{timestamp}.png"

    image_path = os.path.join(gen_dir, image_filename)
    image.save(image_path)
    time.sleep(1)
    st.toast(f"Image saved.", icon="📸")

def delete_images(images):
    msg = st.toast('Gathering images...')
    time.sleep(1)
    msg.toast('Deleting...')
    for img in images:
        if img and os.path.exists(img):
            os.remove(img)
        else:
            msg.toast(f'The file {img} does not exist', icon="🚨")
    time.sleep(1)
    msg.toast('Successfully deleted!', icon="🗑️")

# Dictionary to track selected images
selected_images = {}

prompt = st.selectbox("Select a pre-designed prompt!",
                     (
                         "Racing motorcycle blazing through neon-lit streets at night, leaving trails of light in its wake. Wind-whipped rain streaks horizontally across the frame, creating a sense of intense velocity. The rider's leather jacket ripples violently against the air resistance, barely visible through the speed blur. Everything in the background is reduced to stretched lines of color, emphasizing the pure forward momentum.",
                         "Bullet train cutting through cherry blossom petals at dusk, creating a vortex of pink and white. The polished silver exterior reflects the setting sun in a continuous streak of fire. Station lights blend into a single continuous line as the train cleaves through space. The world outside the windows is nothing but beautiful motion blur."
                    ), 
                    key="model")

# Create dynamic columns for a 2xX grid
cols = st.columns(2)  # Create 2 columns

# Loop through images and distribute them into the 2-column layout
for i, image in enumerate(IMAGES):
    col = cols[i % 2]  # Alternate between the two columns
    with col:
        with st.container(border=True):
            selected_images[image] = st.checkbox(f"Image {i+1}: {IMAGES_NAMES[i]}")
            st.image(image, caption="Insert description")

# **Buttons for actions**
left, middle , right = st.columns(3)
if left.button("Delete", icon=":material/delete:", use_container_width=True):
    delete_images([img for img, selected in selected_images.items() if selected])

if middle.button("Save", icon=":material/bookmark:", use_container_width=True):
    save_images([img for img, selected in selected_images.items() if selected])

if right.button("Generate", icon=":material/skip_next:", use_container_width=True):
    generate_images(prompt)

st.header("Saved Images")

IMAGES = glob.glob(f'{sav_dir}/*')
IMAGES_NAMES = [os.path.basename(file) for file in IMAGES]

# Dictionary to track selected images
selected_images = {}
# Create dynamic columns for a 2xX grid
cols = st.columns(2)  # Create 2 columns

# Loop through images and distribute them into the 2-column layout
for i, image in enumerate(IMAGES):
    col = cols[i % 2]  # Alternate between the two columns
    with col:
        with st.container(border=True):
            selected_images[image] = st.checkbox(f"Saved Image {i+1}: {IMAGES_NAMES[i]}")
            st.image(image, caption="Insert description")


# **Buttons for actions**
left, right = st.columns(2)
if left.button("Delete Image", icon=":material/delete:", use_container_width=True):
    delete_images([img for img, selected in selected_images.items() if selected])

if right.button("Upload Selected Images", icon=":material/file_upload:", use_container_width=True):
    st.toast("Uploading selected images...") 
