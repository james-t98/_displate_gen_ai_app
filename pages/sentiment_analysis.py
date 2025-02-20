import streamlit as st
import pandas as pd
from nlp._preprocessing import web_scrape
from nlp._model import predict

df = web_scrape()
st.dataframe(df)  # Fix: Use 'df' instead of calling web_scrape() again

titles = df['Title'].tolist()
results = []

for title in titles:
    preds = predict(title)  # preds is a list containing a dict inside it
    if isinstance(preds, list) and len(preds) > 0 and isinstance(preds[0], dict):
        preds[0]["title"] = title  # Add title to the first dictionary in the list
        results.append(preds[0])  # Store the updated dictionary

# Convert list of dictionaries to a DataFrame
results_df = pd.DataFrame(results)

# Display the new DataFrame
st.dataframe(results_df)
