from bs4 import BeautifulSoup
import requests
import pandas as pd

# Function to validate and filter image URLs
def validate_image_url(url):
    if url.startswith("https://s3.amazonaws.com/"):
        return url  # Only return valid S3 URLs
    return "No Image"

def validate_article_url(url):
    if url.startswith("https://"):
        return url  # Only return valid S3 URLs
    return "Invalid URL"

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
            
            # Extract image link
            image_tag = article.find('div', class_='tiles-item-figure')
            image_style = image_tag['style'] if image_tag and 'style' in image_tag.attrs else ""
            image_url = "No Image"
            
            if "background-image" in image_style:
                start = image_style.find("url(") + 4
                end = image_style.find(")", start)
                image_url = image_style[start:end].strip('"')
                image_url = validate_image_url(image_url)
            
            # Store extracted data
            articles.append({
                'Date': date,
                'Title': title,
                'Link': link,
                'Image': image_url
            })
        
        # Create a DataFrame
        df = pd.DataFrame(articles)
        return df
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

def extract_text_from_page(url):
    if validate_article_url(url) == "Invalid URL":
        return "Was unable to validate URL due to constraints"

    # Send a GET request to fetch the webpage content
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract paragraphs and headings
        content = []
        for tag in soup.select(".entry-content p, .entry-content h2, .entry-content h3, .entry-content h4, .entry-content h5, .entry-content h6"):
            content.append(tag.get_text(strip=True))
        
        return content
    else:
        return ["Failed to retrieve the webpage."]