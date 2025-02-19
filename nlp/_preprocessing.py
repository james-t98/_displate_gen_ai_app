from bs4 import BeautifulSoup
import requests
import pandas as pd

def web_scrape():
    # Example URL (replace with the actual URL you're scraping)
    url = "https://nvidianews.nvidia.com/"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, "html.parser")
        
        # List to store extracted data
        articles = []
        
        # Find all relevant divs containing articles
        for article in soup.find_all('div', class_='tiles-item-wrapper'):
            
            # Extract date
            date_tag = article.find('div', class_='tiles-item-text-date')
            date = date_tag.get_text(strip=True) if date_tag else "No Date"
            
            # Extract title
            title_tag = article.find('h3', class_='tiles-item-text-title')
            title = title_tag.get_text(strip=True) if title_tag else "No Title"
            
            # Extract link
            link_tag = title_tag.find('a') if title_tag else None
            link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else "No Link"
            
            # Store extracted data
            articles.append({
                'Date': date,
                'Title': title,
                'Link': link
            })
        
        # Create a DataFrame
        df = pd.DataFrame(articles)
        return df
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")