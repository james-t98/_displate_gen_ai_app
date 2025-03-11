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

cols = st.columns(2)  # Create 2 columns
    
 # Loop through images and distribute them into the 2-column layout
for i, row in df.iterrows():
    col = cols[i % 2]  # Alternate between the two columns
    with col:
        with st.container(border=True, height=420):
            if row['Image'] != "No Image":
                st.image(row['Image'], use_container_width=True)
            else:
                st.text("[No Image Available]")
            st.write(f"**{row['Title']}**")
            st.write(row['Date'])
            st.write(row['label'])
            st.write(f"[Read more]({row['Link']})")