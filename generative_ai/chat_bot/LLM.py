import streamlit as st
import replicate
from transformers import AutoTokenizer

class LLM():
    def __init__(self):
        pass

    def clear_chat_history(self):
        st.session_state.messages = [{"role": "assistant", "content": "Ask me anything."}]

    # @st.cache_resource(show_spinner=False)
    def get_tokenizer(self):
        """Get a tokenizer to make sure we're not sending too much text
        text to the Model. Eventually we will replace this with ArcticTokenizer
        """
        return AutoTokenizer.from_pretrained("huggyllama/llama-7b")

    def get_num_tokens(self, prompt):
        """Get the number of tokens in a given prompt"""
        tokenizer = self.get_tokenizer()
        tokens = tokenizer.tokenize(prompt)
        return len(tokens)

    # Function for generating model response
    def generate_response(self, model, temperature, top_p):
        prompt = []
        for dict_message in st.session_state.messages:
            if dict_message["role"] == "user":
                prompt.append("<|im_start|>user\n" + dict_message["content"] + "<|im_end|>")
            else:
                prompt.append("<|im_start|>assistant\n" + dict_message["content"] + "<|im_end|>")
        
        prompt.append("<|im_start|>assistant")
        prompt.append("")
        prompt_str = "\n".join(prompt)
        
        if self.get_num_tokens(prompt_str) >= 3072:
            st.error("Conversation length too long. Please keep it under 3072 tokens.")
            st.button('Clear chat history', on_click=self.clear_chat_history, key="clear_chat_history")
            st.stop()

        for event in replicate.stream(model,
                            input={"prompt": prompt_str,
                                    "prompt_template": r"{prompt}",
                                    "temperature": temperature,
                                    "top_p": top_p,
                                    }):
            yield str(event)