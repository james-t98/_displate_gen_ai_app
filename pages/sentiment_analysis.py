import streamlit as st
import pandas as pd
from nlp._preprocessing import web_scrape
from nlp._model import predict

df = web_scrape()

# Create empty lists to hold the predictions
pred_labels = []
pred_scores = []

for title in df['Title']:
    preds = predict(title)  # preds is a list containing a dict
    if isinstance(preds, list) and len(preds) > 0 and isinstance(preds[0], dict):
        pred_labels.append(preds[0]["label"])
        pred_scores.append(preds[0]["score"])
    else:
        pred_labels.append(None)
        pred_scores.append(None)

# Append the prediction results as new columns in the original DataFrame
df['label'] = pred_labels
df['score'] = pred_scores

st.dataframe(df)  # Display the updated DataFrame