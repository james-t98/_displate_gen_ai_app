from transformers import pipeline

model = pipeline(model="JaimeT/finetuning-sentiment-model-3000-samples")

def predict(token):
    return model(token)