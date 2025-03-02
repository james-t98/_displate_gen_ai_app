from bs4 import BeautifulSoup
import requests
import pandas as pd
import streamlit as st
import smtplib
from email.mime.text import MIMEText

def get_apartments_list(url):
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, "html.parser")

        # List to store extracted data
        apartments = []

         # Find all relevant divs containing apartment listings
        for apartment in soup.find_all('div', class_='listing-search-item__content'):
            # Extract Address
            address_tag = apartment.find('a', class_='listing-search-item__link listing-search-item__link--title')
            address = address_tag.get_text(strip=True) if address_tag else "No Address"
            resource = "https://www.pararius.nl" + address_tag['href'] if address_tag and 'href' in address_tag.attrs else "No Link"

            # Extract Postcode & Location
            postcode_tag = apartment.find('div', class_="listing-search-item__sub-title'")
            postcode = postcode_tag.get_text(strip=True) if postcode_tag else "No Postcode"

            # Extract Price
            price_tag = apartment.find('div', class_='listing-search-item__price')
            price = price_tag.get_text(strip=True) if price_tag else "No Price"

            # Extract Apartment Features (Size, Rooms, Year Built)
            size, rooms, year_built = "No Size", "No Rooms", "No Year"
            features = apartment.find('ul', class_='illustrated-features')
            if features:
                feature_items = features.find_all('li')
                if len(feature_items) > 0:
                    size = feature_items[0].get_text(strip=True)  # Example: '50 m²'
                if len(feature_items) > 1:
                    rooms = feature_items[1].get_text(strip=True)  # Example: '2 kamers'
                if len(feature_items) > 2:
                    year_built = feature_items[2].get_text(strip=True)  # Example: '1938'

            # Extract Agent
            agent_tag = apartment.find('div', class_='listing-search-item__info')
            agent = agent_tag.get_text(strip=True) if agent_tag else "No Agent"

            # Store extracted data
            apartments.append({
                'Address': address,
                'Postcode': postcode,
                'Price': price,
                'Size': size,
                'Rooms': rooms,
                'Year Built': year_built,
                "Resource": resource,
                'Agent': agent
            })

        # Create a DataFrame
        return pd.DataFrame(apartments)

# Example URL (replace with the actual URL you're scraping)
url = "https://www.pararius.nl/huurwoningen/rotterdam/0-1100"

st.dataframe(get_apartments_list(url))

with st.form("email"):
   st.write("Email Heading and more Information to Follow!")
   option = st.selectbox('Pick an option', ['Deciding', 'Yes','No',])
   st.form_submit_button('Submit!')

st.write(option)

# Taking inputs
email_sender = st.text_input('From')
email_receiver = st.text_input('To')
subject = st.text_input('Subject')
body = st.text_area('Body')
password = st.text_input('Password', type="password") 

if st.button("Send Email"):
    try:
        msg = MIMEText(body)
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = subject

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_sender, password)
        server.sendmail(email_sender, email_receiver, msg.as_string())
        server.quit()

        st.success('Email sent successfully! 🚀')
    except Exception as e:
        st.error(f"Erreur lors de l’envoi de l’e-mail : {e}")