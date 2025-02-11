import streamlit as st
from gcp_imagen import generate_image

st.title("🎈 Jaime's app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

if st.button("Generate an Image"):
    st.write("Calling image generation")
    generate_image()

prompt = st.chat_input("Is there anything particular you are looking for today sir?")
if prompt:
    if prompt == "No":
        st.write(f"Very well then. I shall continue with my search and provide you with you desired results.")
    else:
        st.write(f"User has sent the following prompt: {prompt}")

col1, col2, col3 = st.columns(3)

with col1:
    st.header("Image 1")
    st.image("/workspaces/_displate_gen_ai_app/daily_images/image (5).png", caption="Sunrise by the mountains")
    st.header("Image 4")
    st.image("/workspaces/_displate_gen_ai_app/daily_images/image (5).png", caption="Sunrise by the mountains")

with col2:
    st.header("Image 2")
    st.image("/workspaces/_displate_gen_ai_app/daily_images/image (5).png", caption="Sunrise by the mountains")
    st.header("Image 5")
    st.image("/workspaces/_displate_gen_ai_app/daily_images/image (5).png", caption="Sunrise by the mountains")

with col3:
    st.header("Image 3")
    st.image("/workspaces/_displate_gen_ai_app/daily_images/image (5).png", caption="Sunrise by the mountains")
    st.header("Image 6")
    st.image("/workspaces/_displate_gen_ai_app/daily_images/image (5).png", caption="Sunrise by the mountains")