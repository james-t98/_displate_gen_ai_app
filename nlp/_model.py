from transformers import pipeline

model = pipeline(model="JaimeT/finetuning-sentiment-model-3000-samples", truncation=True, max_length=512)

def predict(token):
    return model(token)