from bs4 import BeautifulSoup
import requests
import mysql.connector
from mysql.connector import Error
from transformers import pipeline
import streamlit as st
from nlp._model import predict
import smtplib
from email.mime.text import MIMEText

# Example URL (replace with the actual URL you're scraping)
url = "https://www.pararius.nl/huurwoningen/rotterdam/0-1000"
columns = ['Address', 'Postcode', 'Price', 'Resource']
HOST = "localhost"
USER = "root"
PASSWORD = "nenbiz-9dapvi-putZym"
DATABASE = "streamlit"
TABLE = "Pararius"
MAILING_LIST = []

def get_description(url):
    # Send a GET request to the webpage
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return None
    
    # Parse the page content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Locate the description container
    description_div = soup.find('div', class_='listing-detail-description__content')
    if not description_div:
        print("Description section not found")
        return None
    
    # Extract text from paragraphs inside the description div
    paragraphs = description_div.find_all('p')
    description = '\n'.join(p.get_text(strip=True) for p in paragraphs)
    
    return description

def get_sentiment(token):
    preds = predict(token)  # preds is a list containing a dict
    if isinstance(preds, list) and len(preds) > 0 and isinstance(preds[0], dict):
        return preds[0]["label"]
    else:
        return "No Prediction"

def _connect_to_database():
    try:
        mydb = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        return mydb
    except Error as e:
        return None


def def_mailing_list_demo(address, postcode, price, resource):
    if len(MAILING_LIST) == 5:
        return

    MAILING_LIST.append({
        'Address': address,
        'Postcode': postcode,
        'Price': price,
        'Resource': resource,
        'Sentiment': get_sentiment(get_description(resource))
    })

def insert_pararius_record_demo(address, postcode, price, resource):
    def_mailing_list_demo(address, postcode, price, resource)

def def_mailing_list(address, postcode, price, resource):
    MAILING_LIST.append({
        'Address': address,
        'Postcode': postcode,
        'Price': price,
        'Resource': resource,
        'Sentiment': get_sentiment(get_description(resource))
    })

def insert_pararius_record(mydb, address, postcode, price, resource):
    mycursor = mydb.cursor()
    sql = f"INSERT IGNORE INTO {TABLE} (Address, Postcode, Price, Resource) VALUES (%s, %s, %s, %s)"
    val = (address, postcode, price, resource)
    mycursor.execute(sql, val)
    mydb.commit()
    def_mailing_list(address, postcode, price, resource)

def exists(mydb, postcode):
    cursor = mydb.cursor()
    sql = f"SELECT * FROM {TABLE} WHERE Postcode = '{postcode}'"
    cursor.execute(sql)

    rs = cursor.fetchall()
    return (True if rs else False)

def get_apartments_list(url):
    mydb = _connect_to_database()
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

            # Find the paragraph with class 'listing-reactions-counter__details'
            date = apartment.find("p", class_="listing-reactions-counter__details")

            # Extract text, split, and get the last two words
            if date:
                text = date.get_text(strip=True)
                words = text.split()
                extracted_text = " ".join(words[-2:])  # Get the last two words

            if mydb == None:
                insert_pararius_record_demo(address, postcode, int(price.split()[1]), resource)

            else:
                if exists(mydb, postcode):
                    continue

                insert_pararius_record(
                    mydb,
                    address,
                    postcode,
                    int(price.split()[1]),
                    resource
                )

get_apartments_list(url)

def draft_mail():
    if len(MAILING_LIST) == 0:
        return f"""
            Hi Jaime, 
            There are no new apartments that match your search criteria. 
            Possible solutions could be updating the search criteria parameters. If not, we will continue to search. 
            If new apartments are found that match your search criteria, we will update you via email.

            Kind regards,
            Future A.I. Engineer Inc.
            """

    msg = f""" 
        Hi Jaime,
        The following apartment(s) have been found on Pararius that might be of interest to you. 
        """ 
    for apartment in MAILING_LIST:
        msg += f""" 
            Address: {apartment['Address']}
            Postcode: {apartment['Postcode']}
            Price: {apartment['Price']}
            Resource: {apartment['Resource']}
            Sentiment: {apartment['Sentiment']}
        """

    msg += f"""
        Kind regards,
        Future A.I. Engineer Inc.
        """
    return msg

# Taking inputs
email_sender = st.text_input('From', value=st.secrets['EMAIL_VERIFICATION']['sender'])
email_receiver = st.text_input('To', value=st.secrets['EMAIL_VERIFICATION']['recipient'])
subject = st.text_input('Subject', value='New Apartments Found')
body = st.text_area('Body', value=draft_mail())
password = st.text_input('Password', type="password", value=st.secrets['EMAIL_VERIFICATION']['password']) 

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
        st.error(f"Error in sending e-mail : {e}")