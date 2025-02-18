import streamlit as st
import os
import glob

IMAGES_PATH = "daily_images"
DAILY_IMAGES = glob.glob(f'{IMAGES_PATH}/*')
IMAGES_NAMES = [os.path.basename(file) for file in DAILY_IMAGES]
image_1 , image_2, image_3, image_4 = False, False, False, False

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        image_1 = st.checkbox("Image 1: " + IMAGES_NAMES[0])
        st.image(DAILY_IMAGES[0], caption="Insert description")
    with st.container(border=True):
        image_3 = st.checkbox("Image 3: " + IMAGES_NAMES[1])
        st.image(DAILY_IMAGES[1], caption="Insert description")

with col2:
    with st.container(border=True):
        image_2 = st.checkbox("Image 2: " + IMAGES_NAMES[2])
        st.image(DAILY_IMAGES[2], caption="Insert description")
    with st.container(border=True):
        image_4 = st.checkbox("Image 4: " + IMAGES_NAMES[3])
        st.image(DAILY_IMAGES[3], caption="Insert description")

images = [image_1 , image_2, image_3, image_4 ]

left, middle, right = st.columns(3)
if left.button("Previous", icon=":material/skip_previous:", use_container_width=True):
    left.markdown("You clicked the Previous button.")
if middle.button("Save Selected Images", icon=":material/bookmark:", use_container_width=True):
    middle.markdown("Saving images")
    for i, x in enumerate(images):
        if x: 
            middle.markdown(f"{IMAGES_NAMES[i]}")
            middle.markdown(f"{DAILY_IMAGES}")
if right.button("Generate", icon=":material/skip_next:", use_container_width=True):
    right.markdown("You clicked the Generate button.")