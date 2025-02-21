import streamlit as st
import os
from transformers import AutoTokenizer
from generative_ai.chat_bot.LLM import LLM

llm = LLM()

# App title
st.set_page_config(page_title="Streamlit Replicate Chatbot", page_icon="💬")

# Replicate Credentials
with st.sidebar:
    st.title('💬 Streamlit Replicate Chatbot')
    st.write('Create chatbots using various LLM models hosted at [Replicate](https://replicate.com/).')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
            st.warning('Please enter your Replicate API token.', icon='⚠️')
            st.markdown("**Don't have an API token?** Head over to [Replicate](https://replicate.com) to sign up for one.")
    os.environ['REPLICATE_API_TOKEN'] = replicate_api

    st.subheader("Models and parameters")
    model = st.selectbox("Select a model",("meta/meta-llama-3-70b-instruct", "mistralai/mistral-7b-instruct-v0.2", "google-deepmind/gemma-2b-it"), key="model")
    if model == "google-deepmind/gemma-2b-it":
        model = "google-deepmind/gemma-2b-it:dff94eaf770e1fc211e425a50b51baa8e4cac6c39ef074681f9e39d778773626"
    
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.7, step=0.01, help="Randomness of generated output")
    if temperature >= 1:
        st.warning('Values exceeding 1 produces more creative and random output as well as increased likelihood of hallucination.')
    if temperature < 0.1:
        st.warning('Values approaching 0 produces deterministic output. Recommended starting value is 0.7')
    
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01, help="Top p percentage of most likely tokens for output generation")

# Store LLM-generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Ask me anything."}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

st.sidebar.button('Clear chat history', on_click=llm.clear_chat_history())

# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response = llm.generate_response(model, temperature, top_p)
        full_response = st.write_stream(response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)