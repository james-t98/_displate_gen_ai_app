from transformers import pipeline
from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("JaimeT/text_summarizer")
summarize_model = AutoModelForSeq2SeqLM.from_pretrained("JaimeT/text_summarizer")

sentiment_model = pipeline(model="JaimeT/finetuning-sentiment-model-3000-samples", truncation=True, max_length=512)

def predict(token):
    return sentiment_model(token)

def summarize(text):
    inputs = tokenizer(text, return_tensors="pt").input_ids
    outputs = summarize_model.generate(inputs, max_new_tokens=100, do_sample=False)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)