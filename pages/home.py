import streamlit as st

prompt = st.chat_input("Is there anything particular you are looking for today sir?")
if prompt:
    if prompt == "No":
        st.write(f"Very well then. I shall continue with my search and provide you with you desired results.")
    else:
        st.write(f"User has sent the following prompt: {prompt}")